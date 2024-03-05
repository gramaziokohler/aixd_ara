from aixd_grasshopper.gh_ui import model_train
from aixd_grasshopper.gh_ui_helper import session_id, component_id
from scriptcontext import sticky as st

cid = component_id(ghenv.Component, "model_train")


if not epochs or epochs < 1:
    epochs = 1
if not wb:
    wb = False

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
