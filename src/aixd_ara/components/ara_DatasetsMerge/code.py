# flake8: noqa
from scriptcontext import sticky as st
from Grasshopper.Kernel.GH_RuntimeMessageLevel import Error, Warning

from aixd_ara.gh_ui import merge_datasets
from aixd_ara.gh_ui_helper import clear_sticky
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import session_id

if samples_per_file is None: samples_per_file = 1000
assert samples_per_file>0, "samples_per_file must be a positive integer, got {}".format(samples_per_file)

if root_folder:
    cid = component_id(session_id(), ghenv.Component, "ProjectSetup")
    
    if merge:
        st[cid] = merge_datasets(session_id(), root_folder, new_dataset_name,samples_per_file)
    
    if cid in st.keys():
        status = st[cid]["status"]
        msg = st[cid]["msg"]
        # if status=="error":
        #     ghenv.Component.AddRuntimeMessage(Error, msg)
        # elif status=="warning":
        #     ghenv.Component.AddRuntimeMessage(Warning, msg)