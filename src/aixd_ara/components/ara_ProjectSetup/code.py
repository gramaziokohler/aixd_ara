# flake8: noqa
import os

from scriptcontext import sticky as st

from aixd_ara.gh_ui import project_setup
from aixd_ara.gh_ui_helper import clear_sticky
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import session_id

if not project_root:
    ghdoc = ghenv.Component.OnPingDocument().FilePath
    project_root = os.path.dirname(ghdoc)

if project_name:
    cid = component_id(session_id(), ghenv.Component, "ProjectSetup")

    if set:
        complete_path = os.path.join(project_root, project_name)
        if not os.path.exists(complete_path):
            print("The path {} does not exist and will be now created.".format(complete_path))
            os.mkdir(complete_path)

        clear_sticky(ghenv, st)

        st[cid] = project_setup(session_id(), project_root, project_name)

    if cid in st.keys():
        msg = st[cid]["msg"]
        path = st[cid]["path"]
