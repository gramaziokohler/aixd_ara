# flake8: noqa
from scriptcontext import sticky as st
from aixd_grasshopper.gh_ui import plot_contours_request
from aixd_grasshopper.gh_ui import get_dataobject_types
from aixd_grasshopper.gh_ui_helper import session_id
from aixd_grasshopper.gh_ui_helper import component_id
from aixd_grasshopper.gh_ui_helper import convert_str_to_bitmap
from aixd_grasshopper.gh_ui_helper import reformat_request


cid = component_id(session_id, ghenv.Component, "create_dataset_object")

n_samples = 3

if plot: 
    variable_types = get_dataobject_types(session_id())["dataobject_types"]
    request_dict = reformat_request(request, variable_types)
    print request_dict
    st[cid] = plot_contours_request(session_id(), request_dict, n_samples, output_type) # if output_type interactive: will launch the plotly fig in browser

if cid in st.keys():
    print st[cid]
    #TODO: add error msg here
    if output_type == "static" and 'imgstr' in st[cid].keys():
        imgstr = st[cid]['imgstr']
        img = convert_str_to_bitmap(imgstr, scale)