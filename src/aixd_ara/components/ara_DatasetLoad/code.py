# flake8: noqa
from scriptcontext import sticky as st

from aixd_ara.gh_ui import load_dataset
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "DatasetLoad")

if load:
    st[cid] = load_dataset(session_id())

if cid in st.keys():
    msg = st[cid]["msg"]
