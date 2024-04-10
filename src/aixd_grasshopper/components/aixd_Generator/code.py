# flake8: noqa

# reformat request data
# original input should be a list of strings
# each string should have a form: attribute_name:value

if not n_designs or n_designs < 1:
    n_designs = 1

request_ok = True
try:
    request_dict = {}
    for rv in requested_values:
        rv = rv.strip()
        k, v = rv.split(":")
        v = float(v)
        request_dict[k] = v
    print(request_dict)
    request_ok = True

except:
    request_ok = False
    # raise ValueError("Request could not be processed")

# -------------------------------------------------------------------------------


class wrapper:
    def __init__(self, dict):
        self.dict = dict

    def __repr__(self):
        return "Generated design"


# -------------------------------------------------------------------------------


from aixd_grasshopper.gh_ui import request_designs
from aixd_grasshopper.gh_ui_helper import session_id, component_id
from scriptcontext import sticky as st

cid = component_id(session_id(), ghenv.Component, "run_generation")


if run and request_ok:
    ghenv.Component.Message = "Running"
    st[cid] = request_designs(session_id(), request_dict, n_designs)
    ghenv.Component.Message = "Finished"

if cid in st.keys():
    predictions = [wrapper(x) for x in result]
    ghenv.Component.Message = "Ready"
