# flake8: noqa

from scriptcontext import sticky as st
from aixd_grasshopper.gh_ui import reset_session
from aixd_grasshopper.gh_ui_helper import session_id, clear_sticky

if reset:
    reset_session(session_id())
    clear_sticky(ghenv, st)
