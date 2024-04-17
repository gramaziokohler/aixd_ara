# flake8: noqa
import os

from scriptcontext import sticky as st

from aixd_grasshopper.gh_ui import project_setup
from aixd_grasshopper.gh_ui_helper import component_id
from aixd_grasshopper.gh_ui_helper import session_id

if project_folder and dataset_name:
    complete_path = os.path.join(project_folder, dataset_name)
    if not os.path.exists(complete_path):
        print("The path {} does not exist and will be now created.".format(complete_path))
        os.mkdir(complete_path)

    cid = component_id(ghenv.Component, "project_setup")

    if set:
        st[cid] = project_setup(session_id(), project_folder, dataset_name)

    if cid in st.keys():
        msg = st[cid]["msg"]
        path = st[cid]["path"]
