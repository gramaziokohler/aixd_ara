from aixd_grasshopper.gh_ui import run_training
from aixd_grasshopper.gh_ui_helper import session_id, component_id
from scriptcontext import sticky as st
cid = component_id(ghenv.Component, "create_dataset_object")



#---data clean-up-------------------------------------------------------------

if not epochs or epochs <1: epochs = 1

default_settings = {
    "inputML": "design_parameters", 
    "outputML": "performance_attributes",
    "latent_dim": 30,
    "hidden_layers":[512, 256, 128, 64],
    "batch_size":64
    }


if settings: settings = settings.dict #extract from wrapper
else: settings = {}

for k in default_settings.keys():
    if (k not in settings) or (k in settings and settings[k]==None) or (k in settings and settings[k]==[]):
        settings[k]=default_settings[k]
        print k, default_settings[k]


#---comm------------------------------------------------------------------------

if run: 
    st[cid] = run_training(session_id(), settings, epochs)


if cid in st.keys():
    best_ckpt = st[cid]['best_ckpt']
    path = st[cid]['path']
    ghenv.Component.Message = st[cid]['msg']
else:
    ghenv.Component.Message = ""

# TODO: 
# * return path or name of best checkpoint
# * make non-GUI-blocking
# * display progress 