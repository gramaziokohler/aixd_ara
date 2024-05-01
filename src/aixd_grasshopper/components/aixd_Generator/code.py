# flake8: noqa

from scriptcontext import sticky as st

from aixd_grasshopper.gh_ui import get_dataobject_types
from aixd_grasshopper.gh_ui import request_designs
from aixd_grasshopper.gh_ui_helper import component_id
from aixd_grasshopper.gh_ui_helper import instantiate_sample
from aixd_grasshopper.gh_ui_helper import sample_summary
from aixd_grasshopper.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "run_generation")
item = component_id(session_id(), ghenv.Component, "pick_sample")

"""
requested_values: a multiline string with variable_name:values tuples. 

"""

if not n_designs or n_designs < 1:
    n_designs = 1


def recast_type(value, typename):
    if typename == "real":
        return float(value)
    if typename == "integer":
        return int(value)
    if typename == "categorical":
        return str(value)
    if typename == "bool":
        return bool(value)


class wrapper:
    def __init__(self, dict):
        self.dict = dict

    def __repr__(self):
        return "Generated design"


def reformat_request(request_string):
    types = get_dataobject_types(session_id())["dataobject_types"]
    request_dict = {}

    for rv in request_string:
        rv = rv.strip()

        # split into name:value(s)
        k, v = rv.split(":")

        if k not in types.keys():
            raise ValueError(
                "'{0}' is not a valid variable name. There is not variable with this name in the dataset.".format(k)
            )

        # check if a list or a single value
        if v[0] == "[" and v[-1] == "]":
            v = v[1:-1]
            v = v.split(",")
            v = [recast_type(vi, types[k]) for vi in v]
        else:
            v = recast_type(v, types[k])
        request_dict[k] = v
    return request_dict


# -------------------------------------------------------------------------------


if clear and cid in st.keys():
    del st[cid]
    st[item] = None
    ghenv.Component.Message = "no samples"

if generate and requested_values:

    request_dict = reformat_request(requested_values)
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
    instantiate_sample(ghdoc, sample_dict) # sends design parameter values to the parametric model

    # --- output ---
    sample_txt = sample_summary(sample_dict)
    sample = wrapper(samples[i])
