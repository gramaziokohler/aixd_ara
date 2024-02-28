from aixd_grasshopper.gh_ui import get_one_sample
from aixd_grasshopper.gh_ui_helper import session_id, component_id
import Grasshopper


if not item:
    item = -1

if get:
    sample = get_one_sample(session_id(), item)


# TODO - clean up:


# -------------------------------------------------------------------------------
def find_component_by_nickname(ghdoc, component_nickname):
    found = []
    # all_objects = ghdoc.Objects
    all_objects = ghenv.Component.OnPingDocument().Objects
    for obj in all_objects:

        if obj.Attributes.PathName == component_nickname:
            # if obj.NickName == component_nickname:
            found.append(obj)

    if not found:
        print("No ghcomponent found with a nickname {}.".format(component_nickname))
        return
    if len(found) > 1:
        print("{len(found)} ghcomponents found with the nickname {} - will return None.".format(component_nickname))
        return
    return found[0]


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
    if not isinstance(vals, list):
        vals = [vals]
    for v in vals:
        component.PersistentData.Append(ghtype(v))
    component.ExpireSolution(True)


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


# -------------------------------------------------------------------------------


if sample:

    for dp_name, dp_vals in sample["design_parameters"].items():
        # print dp_name, dp_vals
        component_name = "GENERATED_{}".format(dp_name)
        component = find_component_by_nickname(ghdoc, component_name)
        print("{}: {}".format(component_name, dp_vals))

        if not dp_vals:
            print("empty values for {}".format(comp))
        else:
            set_values(component, dp_vals)


# -------------------------------------------------------------------------------
if sample:
    txt = ""
    txt += "Design Parameters:\n\n"
    for name, values in sample["design_parameters"].items():
        txt += "{}:  {}\n".format(name, values)
    txt += "\n"
    txt += "Performance Attributes:\n\n"
    for name, values in sample["performance_attributes"].items():
        txt += "{}:  {}\n".format(name, values)

    sample = txt

    trigger = False

# sample = None
