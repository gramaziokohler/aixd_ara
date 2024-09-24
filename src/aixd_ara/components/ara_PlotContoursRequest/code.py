# flake8: noqa
from scriptcontext import sticky as st
from aixd_ara.gh_ui import plot_contours_request
from aixd_ara.gh_ui import get_dataobject_types
from aixd_ara.gh_ui_helper import session_id
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import convert_str_to_bitmap
from aixd_ara.gh_ui_helper import reformat_request


cid = component_id(session_id, ghenv.Component, "PlotContoursRequest")


if plot:
    st[cid] = plot_contours_request(session_id(), "interactive") # will launch the plotly fig in browser

if cid in st.keys():
    print st[cid]