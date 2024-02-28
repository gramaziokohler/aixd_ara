from aixd_grasshopper.gh_ui import create_dataset_object
from aixd_grasshopper.gh_ui_helper import session_id, component_id
from scriptcontext import sticky as st

cid = component_id(ghenv.Component, "create_dataset_object")


design_parameters = [x.data for x in design_parameters]
performance_attributes = [x.data for x in performance_attributes]


if create:
    st[cid] = create_dataset_object(session_id(), design_parameters, performance_attributes)

if cid in st.keys():
    msg = st[cid]["msg"]
