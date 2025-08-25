from scriptcontext import sticky as st

from aixd_ara.gh_ui import local_sensitivity
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import session_id
from aixd_ara.gh_ui_helper import reformat_request
from aixd_ara.gh_ui import get_dataobject_types

cid = component_id(session_id(), ghenv.Component, "PlotLocalSensitivity")


if plot:
    variable_types = get_dataobject_types(session_id())["dataobject_types"]
    test_point = reformat_request(sample, variable_types)
    st[cid] = local_sensitivity(session_id(), test_point, target_name)  # will launch the plotly fig in browser

if cid in st.keys():
    print(st[cid])