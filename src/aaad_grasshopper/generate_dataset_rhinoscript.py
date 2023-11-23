"""
Run this file in Rhino Python Editor.
The Grasshopper file must be the first active file. (Close all other Grasshopper files to avoid confusion.)
"""

import os
import pickle
import time, datetime
import random
import json
import urllib2

from aaad_grasshopper.gh_ui_helper import http_post_request, find_component_by_nickname, TYPES

try:
    import Rhino
    Grasshopper = Rhino.RhinoApp.GetPlugInObject("Grasshopper")
    import Grasshopper
except:
    #because the first try sometimes doesn't work after "Reset Script Engine"
    import clr
    clr.AddReference('Grasshopper')
    import Grasshopper

docServer = Grasshopper.GH_InstanceServer.DocumentServer
ghdoc = docServer[0] # first opened document
session_id = ghdoc.DocumentID.ToString()
print session_id


#-------------------------------------------------------------------------------
# GH interface


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

#-------------------------------------------------------------------------------
# API app


def load_dps():
    return http_post_request("getdata_design_parameters",{"session_id":session_id})


def get_pa_names():
    d = http_post_request("datablocks_dataobjects", {"session_id": session_id})
    return d['performance_attributes']


def analysis_callback(ghdoc,dp_samples, pa_names):
    
    pa_samples = []

    # pass design parameters (sample by sample) to Grasshopper model and read the performance attributes
    for sample in dp_samples:
        uid = sample['uid']
        for dp_name, dp_vals in sample.items():
            if dp_name == 'uid': continue
            component_name = "GENERATED_{}".format(dp_name)
            component = find_component_by_nickname(ghdoc, component_name)
            print component, dp_vals
            set_values(component, dp_vals)
            
        pa_dict = {k:[] for k in pa_names}
        pa_dict['uid']=uid
        for pa_name in pa_names:
            
            component_name = "REAL_{}".format(pa_name)
            component = find_component_by_nickname(ghdoc, component_name)
            pa_vals = get_values(component)
            pa_dict[pa_name]=pa_vals
        
        pa_samples.append(pa_dict)
       
    # save performance attributes to dataset
    return pa_samples

def save_pa_to_database():
    return http_post_request("import_data_from_dict",{"session_id":session_id})


#-------------------------------------------------------------------------------
# RUN

dp_samples = load_dps() 
pa_names = get_pa_names()
pa_vals = analysis_callback(ghdoc,dp_samples, pa_names)
save_pa_to_database(pa_vals)
