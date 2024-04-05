from aixd_grasshopper.gh_ui import nn_summary
from aixd_grasshopper.gh_ui_helper import session_id, component_id
from scriptcontext import sticky as st

cid = component_id(ghenv.Component, "model_summary")


if not max_depth:
    max_depth = 1

if get:
    st[cid] = nn_summary(session_id(), max_depth)

if cid in st.keys():
    summary = st[cid]["summary"]
