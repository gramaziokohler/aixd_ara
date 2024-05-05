# flake8: noqa
from scriptcontext import sticky as st

from aixd_ara.gh_ui import model_load
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "ModelLoad")

if not model_type:
    model_type = "CAE"
if not checkpoint_path:
    checkpoint_path = ""
if not checkpoint_name:
    checkpoint_name = "last"

if load:
    st[cid] = model_load(session_id(), model_type, checkpoint_name, checkpoint_path)

if cid in st.keys():
    msg = st[cid]["msg"]
