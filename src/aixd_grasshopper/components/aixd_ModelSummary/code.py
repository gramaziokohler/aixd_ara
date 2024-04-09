# flake8: noqa
from scriptcontext import sticky as st

from aixd_grasshopper.gh_ui import nn_summary
from aixd_grasshopper.gh_ui_helper import component_id
from aixd_grasshopper.gh_ui_helper import session_id

cid = component_id(ghenv.Component, "model_summary")


if not max_depth:
    max_depth = 1

if get:
    st[cid] = nn_summary(session_id(), max_depth)

if cid in st.keys():
    summary = st[cid]["summary"]
