# flake8: noqa
from scriptcontext import sticky as st

from aixd_ara.gh_ui import model_input_output_dimensions
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "ModelDims")

if get:
    st[cid] = model_input_output_dimensions(session_id())

if cid in st.keys():
    summary = st[cid]["summary"]
