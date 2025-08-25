from scriptcontext import sticky as st

from aixd_ara.gh_ui import global_sensitivity
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "PlotGlobalSensitivity")

if set_name is None: set_name = "val" # 'train','val' or 'test' 

if plot:
    st[cid] = global_sensitivity(session_id(),  target_name, set_name, n_samples)  # will launch the plotly fig in browser

if cid in st.keys():
    print(st[cid])