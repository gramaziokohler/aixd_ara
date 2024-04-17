import json


import Grasshopper
import urllib2
from System import Convert
from System import Guid
from System.Drawing import Bitmap
from System.Drawing import Size
from System.IO import MemoryStream

from aixd_grasshopper.constants import DEFAULT_PORT

TYPES = {
    "Arc": Grasshopper.Kernel.Types.GH_Arc,
    "Boolean": Grasshopper.Kernel.Types.GH_Boolean,
    "Box": Grasshopper.Kernel.Types.GH_Box,
    "Brep": Grasshopper.Kernel.Types.GH_Brep,
    "Circle": Grasshopper.Kernel.Types.GH_Circle,
    "ComplexNumber": Grasshopper.Kernel.Types.GH_ComplexNumber,
    "Curve": Grasshopper.Kernel.Types.GH_Curve,
    "Guid": Grasshopper.Kernel.Types.GH_Guid,
    "Integer": Grasshopper.Kernel.Types.GH_Integer,
    "Interval": Grasshopper.Kernel.Types.GH_Interval,
    "Interval2D": Grasshopper.Kernel.Types.GH_Interval2D,
    "Line": Grasshopper.Kernel.Types.GH_Line,
    "Mesh": Grasshopper.Kernel.Types.GH_Mesh,
    "Number": Grasshopper.Kernel.Types.GH_Number,
    "Plane": Grasshopper.Kernel.Types.GH_Plane,
    "Point": Grasshopper.Kernel.Types.GH_Point,
    "Rectangle": Grasshopper.Kernel.Types.GH_Rectangle,
    "String": Grasshopper.Kernel.Types.GH_String,
    "SubD": Grasshopper.Kernel.Types.GH_SubD,
    "Surface": Grasshopper.Kernel.Types.GH_Surface,
    "Vector": Grasshopper.Kernel.Types.GH_Vector,
    "Text": Grasshopper.Kernel.Types.GH_String,
}


def http_post_request(action, data):
    """
    action: string corresponding to the http header
    data: dictionary of json-serializable data
    """
    headers = {
        "Content-Type": "application/octet-stream",
        "Accept": "application/octet-stream",
    }
    data = json.dumps(data)
    url = "http://127.0.0.1:{}/{}".format(DEFAULT_PORT, action)
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request).read()
    response = json.loads(response)

    return response


def session_id():
    doc_key = Grasshopper.Instances.ActiveCanvas.Document.DocumentID.ToString()
    return doc_key


def component_id(session_id, component, name):
    return "{}_{}_{}".format(session_id, component.InstanceGuid, name)


def clear_sticky(ghenv, st):
    """
    Removes all items from the sticky dictionary use by Grasshopper components in the given document.
    Resets all components that used the sticky to hold data.

    Parameters
    ----------
    ghenv: Grasshopper environment object `GhPython.Component.PythonEnvironment`
    st: sticky dictionary
    """

    ghdoc = ghenv.Component.OnPingDocument()
    ghdoc_id = ghdoc.DocumentID.ToString()

    keys = st.keys()

    # The keys we are looking for are strings of the form "{session_id}_{guid_str}_{ghcomponent_nickname}".
    # There might be other keys in the sticky dictionary, so we need to filter them out.
    for key in keys:

        session_id = None
        guid_str = None
        try:
            session_id = key.split("_")[0]
            guid_str = key.split("_")[1]
        except Exception:
            pass

        if not session_id or not guid_str:
            continue

        # The retrieved session_id and guid_str may either come from a different Grasshopper document,
        # or from some other process and be incorrect/meaningless.
        # In these cases, the following code will do nothing anyway.
        if session_id == ghdoc_id:
            reset_component(ghdoc, guid_str)
            st.pop(key)


def reset_component(ghdoc, guid_str):
    """
    adapted from:
    https://github.com/compas-dev/compas/blob/ea4b5b5191a350d24cbb479c6770daa68dbe53fd/src/compas_ghpython/timer.py#L8
    """

    guid = Guid(guid_str)
    ghcomp = ghdoc.FindComponent(guid)

    def callback(ghdoc):
        if ghdoc.SolutionState != Grasshopper.Kernel.GH_ProcessStep.Process:
            ghcomp.ExpireSolution(False)

    if not ghcomp:
        return
    delay = 1  # [ms]
    ghdoc.ScheduleSolution(delay, Grasshopper.Kernel.GH_Document.GH_ScheduleDelegate(callback))


def find_component_by_nickname(ghdoc, component_nickname):
    found = []
    all_objects = ghdoc.Objects
    # all_objects = ghenv.Component.OnPingDocument().Objects
    for obj in all_objects:
        if obj.Attributes.PathName == component_nickname:
            # if obj.NickName == component_nickname:
            found.append(obj)

    if not found:
        print("No ghcomponent found with a nickname {}.".format(component_nickname))
        return
    if len(found) > 1:
        print("{} ghcomponents found with the nickname {} - will return None.".format(len(found), component_nickname))
        return
    return found[0]


# set & get values methods (rhinopythonscript style)


def set_value(component, val):
    component.Script_ClearPersistentData()
    component.AddPersistentData(val)
    component.ExpireSolution(True)


def set_values(component, vals):
    """
    Data type of vals must match the type of the component.
    See TYPES list.
    """
    ghtype = TYPES[component.TypeName]

    component.Script_ClearPersistentData()
    for v in vals:
        component.PersistentData.Append(ghtype(v))
    component.ExpireSolution(True)


def get_values(component):
    if not component.VolatileData:
        return None
    return [x.Value for x in component.VolatileData[0]]


def convert_str_to_bitmap(base64_imgstr, scale=1.0):
    """Get image from string and rescale."""

    b64_bytearray = Convert.FromBase64String(base64_imgstr)
    stream = MemoryStream(b64_bytearray)
    bitmap = Bitmap(stream)

    if not scale:
        scale = 1.0
    size = Size(bitmap.Width * scale, bitmap.Height * scale)
    bitmap = Bitmap(bitmap, size)
    return bitmap
