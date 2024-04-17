"""
Run this file in Rhino Python Editor or add it to your toolbar as a button using:
    > right-click on a toolbar > New Button... > in the pop-up window, in Command section, add:
    "! _-RunPythonScript "<path>/generate_dataset_rhinoscript.py"
The Grasshopper file must be the first active file.
(Close all other Grasshopper files to avoid confusion.)
"""

import math
import os

import rhinoscriptsyntax as rs

from aixd_grasshopper.gh_ui_helper import TYPES
from aixd_grasshopper.gh_ui_helper import find_component_by_nickname
from aixd_grasshopper.gh_ui_helper import http_post_request

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


# -------------------------------------------------------------------------------
# GH interface


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


def get_values(component):
    if not component.VolatileData:
        return None
    return [x.Value for x in component.VolatileData[0]]


# -------------------------------------------------------------------------------
# API app


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
        # uid = sample['uid']
        for dp_name, dp_vals in sample.items():
            # if dp_name == 'uid': continue
            component_name = "GENERATED_{}".format(dp_name)
            component = find_component_by_nickname(ghdoc, component_name)
            set_values(component, dp_vals)

        pa_dict = {k: [] for k in pa_names}
        # pa_dict['uid']=uid
        for pa_name in pa_names:

            component_name = "REAL_{}".format(pa_name)
            component = find_component_by_nickname(ghdoc, component_name)
            pa_vals = get_values(component)
            if isinstance(pa_vals, list):
                if len(pa_vals) == 1:
                    pa_vals = pa_vals[0]  # unpack from list
            pa_dict[pa_name] = pa_vals

        pa_samples.append(pa_dict)

    # save performance attributes to dataset
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


# -------------------------------------------------------------------------------
# RUN


def run(n_batches, samples_per_batch):

    for batch in range(n_batches):
        # print("Sampling batch {}/{}...
        # (samples {}..{})".format(batch+1, n_batches, batch*samples_per_batch, (batch+1)*samples_per_batch-1))
        dp_samples = generate_dp_samples(samples_per_batch)
        pa_samples = calculate_pa_samples(ghdoc, dp_samples)
        samples = combine_dp_pa(dp_samples, pa_samples)
        add_samples_to_dataset(samples, samples_per_batch)


# -------------------------------------------------------------------------------
# INPUT INTERFACE

n_samples = rs.GetInteger("Number of samples to generate: ", number=1000, minimum=1, maximum=None)
samples_per_batch = rs.GetInteger(
    "Number of samples per batch file: ", number=n_samples / 10, minimum=1, maximum=n_samples
)

n_batches = int(math.ceil(n_samples / samples_per_batch))
n_samples_final = n_batches * samples_per_batch


pr = http_post_request("project_setup_info", {"session_id": session_id})
root = pr["root_path"]
dataset_name = pr["dataset_name"]
target_path = os.path.join(root, dataset_name)

print(
    "\t (I will generate {} samples in {} batches and save them in {})".format(n_samples_final, n_batches, target_path)
)


run(n_batches, samples_per_batch)

print("\t successfully generated all {} samples in {} batch files".format(n_samples, n_batches))
