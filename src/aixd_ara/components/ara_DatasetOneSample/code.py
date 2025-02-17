# flake8: noqa
from scriptcontext import sticky as st

from aixd_ara.gh_ui import get_one_sample
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import instantiate_sample, sample_summary
from aixd_ara.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "DatasetOneSample")


if item is None:
    item = -1

if get:
    st[cid] = get_one_sample(session_id(), item)

ghdoc = ghenv.Component.OnPingDocument()


if cid in st.keys():
    sample = st[cid]
    instantiate_sample(ghdoc, sample)

    sample_summary = sample_summary(sample)
