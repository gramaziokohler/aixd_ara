from aixd_grasshopper.gh_ui import load_model
from aixd_grasshopper.gh_ui_helper import session_id, component_id

if not checkpoint_path:
    checkpoint_path = ""
if not checkpoint_name:
    checkpoint_name = "last"

if load:
    response = load_model(session_id(), checkpoint_name, checkpoint_path)
