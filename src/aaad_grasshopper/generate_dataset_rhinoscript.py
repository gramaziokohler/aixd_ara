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
import math

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


#-------------------------------------------------------------------------------
# GH interface


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


def get_values(component):
    if not component.VolatileData:
        return None
    return [x.Value for x in component.VolatileData[0]]

#-------------------------------------------------------------------------------
# API app

def generate_dp_samples(n_samples):
    return http_post_request("generate_dp_samples", {"session_id": session_id, "n_samples":n_samples})
    

def calculate_pa_samples(ghdoc, dp_samples):
    pa_names = get_pa_names()
    
    pa_samples = analysis_callback(ghdoc, dp_samples, pa_names)
    
    return pa_samples
    

def load_dps():
    return http_post_request("getdata_design_parameters",{"session_id":session_id})


def get_pa_names():
    d = http_post_request("datablocks_dataobjects", {"session_id": session_id})
    return d['performance_attributes']


def analysis_callback(ghdoc, dp_samples, pa_names):
    
    pa_samples = []

    # pass design parameters (sample by sample) to Grasshopper model and read the performance attributes
    for sample in dp_samples:
        #uid = sample['uid']
        for dp_name, dp_vals in sample.items():
            #if dp_name == 'uid': continue
            component_name = "GENERATED_{}".format(dp_name)
            component = find_component_by_nickname(ghdoc, component_name)
            set_values(component, dp_vals)
            
        pa_dict = {k:[] for k in pa_names}
        #pa_dict['uid']=uid
        for pa_name in pa_names:
            
            component_name = "REAL_{}".format(pa_name)
            component = find_component_by_nickname(ghdoc, component_name)
            pa_vals = get_values(component)
            if isinstance(pa_vals, list):
                if len(pa_vals)==1:
                    pa_vals = pa_vals[0] #unpack from list
            pa_dict[pa_name]=pa_vals

        pa_samples.append(pa_dict)
       
    # save performance attributes to dataset
    return pa_samples

def add_samples_to_dataset(samples, samples_per_file=None):
    return http_post_request("save_samples",{"session_id":session_id, "samples":samples, "samples_per_file":samples_per_file})

def combine_dp_pa(dp_samples, pa_samples):
    z = zip(dp_samples, pa_samples) # one list with two dicts per entry
    samples = []
    for dp,pa in z:
        d = {}
        d.update(dp)
        d.update(pa)
        samples.append(d)
    return samples


#-------------------------------------------------------------------------------
# RUN

#dp_samples = load_dps() 
#pa_names = get_pa_names()
#pa_vals = analysis_callback(ghdoc,dp_samples, pa_names)
#save_pa_to_database(pa_vals)


n_samples = 1000     
samples_per_batch = 100
n_batches = int(math.ceil(n_samples / samples_per_batch))

for batch in range(n_batches):
    dp_samples = generate_dp_samples(samples_per_batch)
    pa_samples = calculate_pa_samples(ghdoc, dp_samples)
    samples = combine_dp_pa(dp_samples, pa_samples)
    add_samples_to_dataset(samples, samples_per_batch)