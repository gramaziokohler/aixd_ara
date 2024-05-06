# flake8: noqa
from scriptcontext import sticky as st

from aixd_ara.gh_ui import plot_contours
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import convert_str_to_bitmap
from aixd_ara.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "PlotContours")


if plot:
    st[cid] = plot_contours(session_id(), variables, output_type) # if output_type interactive: will launch the plotly fig in browser

if cid in st.keys():
    print st[cid]
    #TODO: add error msg here
    if output_type == "static" and 'imgstr' in st[cid].keys():
        imgstr = st[cid]['imgstr']
        img = convert_str_to_bitmap(imgstr, scale)
