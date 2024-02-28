from aixd_grasshopper.gh_ui import nn_summary
from aixd_grasshopper.gh_ui_helper import session_id, component_id

if not max_depth:
    max_depth = 1


if refresh:

    response = nn_summary(session_id(), max_depth)
