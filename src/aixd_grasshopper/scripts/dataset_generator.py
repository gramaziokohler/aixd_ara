"""
Run this file in Rhino Python Editor or add it to your toolbar as a button using:
    > right-click on a toolbar > New Button... > in the pop-up window, in Command section, add:
    "! _-RunPythonScript "<path-to-this-file>/dataset_generator.py"
The Grasshopper file must be the first active file.
(Close all other Grasshopper files to avoid confusion.)
"""

import math
import os

import rhinoscriptsyntax as rs

from aixd_grasshopper.gh_ui_helper import TYPES
from aixd_grasshopper.gh_ui_helper import find_component_by_nickname
from aixd_grasshopper.gh_ui_helper import ghparam_get_values
from aixd_grasshopper.gh_ui_helper import ghparam_set_values
from aixd_grasshopper.gh_ui_helper import http_post_request


# --- GRASSHOPPER INTERFACE ----------------------------------------------------------------------------

try:
    import Rhino

    Grasshopper = Rhino.RhinoApp.GetPlugInObject("Grasshopper")
    import Grasshopper
except:  # noqa: E722
    # because the first try sometimes doesn't work after "Reset Script Engine"
    import clr

    clr.AddReference("Grasshopper")
    import Grasshopper

docServer = Grasshopper.GH_InstanceServer.DocumentServer
ghdoc = docServer[0]  # first opened document
session_id = ghdoc.DocumentID.ToString()


# --- APP INTERFACE ----------------------------------------------------------------------------

def generate_dp_samples(n_samples):
    return http_post_request("generate_dp_samples", {"session_id": session_id, "n_samples": n_samples})


def calculate_pa_samples(ghdoc, dp_samples):
    pa_names = get_pa_names()
    pa_samples = analysis_callback(ghdoc, dp_samples, pa_names)
    return pa_samples


def load_dps():
    return http_post_request("getdata_design_parameters", {"session_id": session_id})


def get_pa_names():
    d = http_post_request("datablocks_dataobjects", {"session_id": session_id})
    return d["performance_attributes"]


def analysis_callback(ghdoc, dp_samples, pa_names):

    pa_samples = []

    # pass design parameters (sample by sample) to Grasshopper model and read the performance attributes
    for sample in dp_samples:
        for dp_name, dp_vals in sample.items():
            component_name = "GENERATED_{}".format(dp_name)
            component = find_component_by_nickname(ghdoc, component_name)
            ghparam_set_values(component, dp_vals, expire=False)

        pa_dict = {k: [] for k in pa_names}
        for pa_name in pa_names:

            component_name = "REAL_{}".format(pa_name)
            component = find_component_by_nickname(ghdoc, component_name)
            pa_vals = ghparam_get_values(component, compute=True)
            if isinstance(pa_vals, list):
                if len(pa_vals) == 1:
                    pa_vals = pa_vals[0]  # unpack from list
            pa_dict[pa_name] = pa_vals

        pa_samples.append(pa_dict)

    return pa_samples


def add_samples_to_dataset(samples, samples_per_file=None):
    return http_post_request(
        "save_samples", {"session_id": session_id, "samples": samples, "samples_per_file": samples_per_file}
    )


def combine_dp_pa(dp_samples, pa_samples):
    z = zip(dp_samples, pa_samples)  # one list with two dicts per entry
    samples = []
    for dp, pa in z:
        d = {}
        d.update(dp)
        d.update(pa)
        samples.append(d)
    return samples


# --- MAIN ----------------------------------------------------------------------------

def run(session_id, num_samples, num_samples_per_batch):

    num_batches = int(math.ceil(num_samples / num_samples_per_batch))

    #override the number of samples to be a multiple of the number of samples per batch  
    num_samples = num_batches * num_samples_per_batch  

    pr = http_post_request("project_setup_info", {"session_id": session_id})
    project_root = pr["project_root"]
    project_name = pr["project_name"]
    target_path = os.path.join(project_root, project_name)

    print("\t ({} samples in {} batches will be generated and saved in {})".format(num_samples, num_batches, target_path))

    for _ in range(num_batches):
        dp_samples = generate_dp_samples(num_samples_per_batch)
        pa_samples = calculate_pa_samples(ghdoc, dp_samples)
        samples = combine_dp_pa(dp_samples, pa_samples)
        add_samples_to_dataset(samples, num_samples_per_batch)


    print("\t successfully generated all {} samples in {} batch files".format(num_samples, num_batches))

# --- INPUT/USER INTERFACE ----------------------------------------------------------------------------

def get_user_input():

    num_samples = rs.GetInteger("Number of samples to generate: ", number=1000, minimum=1, maximum=None)
    num_samples_per_batch = rs.GetInteger(
        "Number of samples per batch file: ", number=num_samples / 10, minimum=1, maximum=num_samples
    )
    return num_samples, num_samples_per_batch



if __name__ =="__main__":

    num_samples, num_samples_per_batch = get_user_input()
    run(session_id, num_samples, num_samples_per_batch)


