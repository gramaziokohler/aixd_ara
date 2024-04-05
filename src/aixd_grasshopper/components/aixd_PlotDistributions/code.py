from scriptcontext import sticky as st

from aixd_grasshopper.gh_ui import plot_distrib_attributes
from aixd_grasshopper.gh_ui_helper import component_id
from aixd_grasshopper.gh_ui_helper import convert_str_to_bitmap
from aixd_grasshopper.gh_ui_helper import session_id

cid = component_id(ghenv.Component, "create_dataset_object")


if plot:
    st[cid] = plot_distrib_attributes(session_id(), variables, output_type) # if output_type interactive: will launch the plotly fig in browser

if cid in st.keys():
    print st[cid]
    #TODO: add error msg here
    if output_type == "static" and 'imgstr' in st[cid].keys():
        imgstr = st[cid]['imgstr']
        img = convert_str_to_bitmap(imgstr, scale)
