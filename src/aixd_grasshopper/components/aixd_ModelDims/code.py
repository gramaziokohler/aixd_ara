# flake8: noqa
from scriptcontext import sticky as st

from aixd_grasshopper.gh_ui import model_input_output_dimensions
from aixd_grasshopper.gh_ui_helper import component_id
from aixd_grasshopper.gh_ui_helper import session_id

cid = component_id(ghenv.Component, "model_dims")

if get:
    st[cid] = model_input_output_dimensions(session_id())

if cid in st.keys():
    summary = st[cid]["summary"]
