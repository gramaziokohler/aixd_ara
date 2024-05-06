# flake8: noqa

from scriptcontext import sticky as st

from aixd_ara.gh_ui import get_dataobject_types
from aixd_ara.gh_ui import request_designs
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import instantiate_sample
from aixd_ara.gh_ui_helper import sample_summary as sample_summary_f
from aixd_ara.gh_ui_helper import session_id
from aixd_ara.gh_ui_helper import reformat_request

cid = component_id(session_id(), ghenv.Component, "run_generation")
item = component_id(session_id(), ghenv.Component, "pick_sample")

"""
requested_values: a multiline string with variable_name:values tuples.
"""

if not n_designs or n_designs < 1:
    n_designs = 1

# -------------------------------------------------------------------------------


if clear and cid in st.keys():
    del st[cid]
    st[item] = None
    ghenv.Component.Message = "no samples"

if generate and requested_values:

    variable_types = get_dataobject_types(session_id())["dataobject_types"]

    request_dict = reformat_request(requested_values, variable_types)
    st[item] = 0
    ghenv.Component.Message = "Running"
    st[cid] = request_designs(session_id(), request_dict, n_designs)
    ghenv.Component.Message = "Finished"

if pick_previous:
    st[item] -= 1
if pick_next:
    st[item] += 1

if cid in st.keys():
    samples = st[cid]["generated"]
    n = len(samples)
    i = st[item] % n

    ghenv.Component.Message = "sample {}/{}".format(i + 1, n)

    sample_dict = samples[i]
    ghdoc = ghenv.Component.OnPingDocument()
    instantiate_sample(ghdoc, sample_dict)  # sends design parameter values to the parametric model

    # --- output ---
    sample_summary = "Predicted/Generated:\n--------------------\n\n" + sample_summary_f(sample_dict)
