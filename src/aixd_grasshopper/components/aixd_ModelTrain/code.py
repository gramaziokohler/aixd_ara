# flake8: noqa

from scriptcontext import sticky as st

from aixd_grasshopper.gh_ui import model_train
from aixd_grasshopper.gh_ui import project_setup_info
from aixd_grasshopper.gh_ui_helper import component_id
from aixd_grasshopper.gh_ui_helper import session_id

cid = component_id(ghenv.Component, "model_train")


if not epochs or epochs < 1:
    epochs = 1

if wb:
    import webbrowser

    projectname = project_setup_info(session_id())["dataset_name"]  # project name == dataset name

    if run:
        url = "https://wandb.ai/{}/{}".format(wb, projectname)
        webbrowser.open(url)
        # TODO: check login and add interface to login if needed


if run:
    st[cid] = model_train(session_id(), epochs, wb)


if cid in st.keys():
    best_ckpt = st[cid]["best_ckpt"]
    path = st[cid]["path"]
    ghenv.Component.Message = st[cid]["msg"]
else:
    ghenv.Component.Message = ""

# TODO:
# * return path or name of best checkpoint
# * make non-GUI-blocking
# * display progress
