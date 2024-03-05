from aixd_grasshopper.gh_ui import model_load
from aixd_grasshopper.gh_ui_helper import session_id, component_id
from scriptcontext import sticky as st

cid = component_id(ghenv.Component, "model_load")

if not checkpoint_path:
    checkpoint_path = ""
if not checkpoint_name:
    checkpoint_name = "last"

if load:
    st[cid] = model_load(session_id(), checkpoint_name, checkpoint_path)

if cid in st.keys():
    msg = st[cid]["msg"]
