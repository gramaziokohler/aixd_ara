# flake8: noqa
from aixd_grasshopper.gh_ui import load_dataset
from aixd_grasshopper.gh_ui_helper import session_id, component_id
from scriptcontext import sticky as st

cid = component_id(ghenv.Component, "create_dataset_object")

if load:
    st[cid] = load_dataset(session_id())

if cid in st.keys():
    msg = st[cid]["msg"]
