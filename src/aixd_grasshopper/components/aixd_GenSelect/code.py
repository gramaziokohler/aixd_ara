#TODO: outsource the value setting methods
#TODO: turn orange if index out of range



from ghpythonlib.treehelpers import list_to_tree
#from aixd_grasshopper.rhino_inside import find_component_by_nickname
import Grasshopper

dp_pred = predictions[select].dict['design_parameters']
pa_pred = predictions[select].dict['performance_attributes']

generated_sample = predictions[select]
print(dp_pred)
print(pa_pred)
print ghdoc.Objects.Count

def find_component_by_nickname(ghdoc, component_nickname):
    found = []
    #all_objects = ghdoc.Objects
    all_objects = ghenv.Component.OnPingDocument().Objects
    for obj in all_objects:
        
        if obj.Attributes.PathName == component_nickname:
            #if obj.NickName == component_nickname:
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
    if not isinstance(vals, list): vals = [vals]
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
    "Text": Grasshopper.Kernel.Types.GH_String
    }


for dp_name, dp_vals in dp_pred.items():
    #print dp_name, dp_vals
    component_name = "GENERATED_{}".format(dp_name)
    component = find_component_by_nickname(ghdoc, component_name)
    print("{}: {}".format(component_name,dp_vals))
    
    if not dp_vals:
        print("empty values for {}".format(comp))
    else:
        set_values(component, dp_vals)
        
    

    txt="Generated & Predicted\n"
    txt+="---------------------\n\n"
    txt+="Design Parameters:\n\n"
    for name,values in dp_pred.items():
        txt+="{}:  {}\n".format(name,values)
    txt+="\n"
    txt+="Performance Attributes:\n\n"
    for name,values in pa_pred.items():
        txt+="{}:  {}\n".format(name,values)
    
    sample_summary = txt