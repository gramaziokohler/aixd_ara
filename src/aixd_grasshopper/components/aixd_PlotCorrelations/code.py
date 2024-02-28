from aixd_grasshopper.gh_ui import plot_distrib_attributes, plot_correlations
from aixd_grasshopper.gh_ui_helper import session_id, component_id, convert_str_to_bitmap
from scriptcontext import sticky as st
cid = component_id(ghenv.Component, "create_dataset_object")



if plot: 
    st[cid] = plot_correlations(session_id(), variables, output_type) # if output_type interactive: will launch the plotly fig in browser

if cid in st.keys():
    print st[cid]
    #TODO: add error msg here
    if output_type == "static" and 'imgstr' in st[cid].keys():
        imgstr = st[cid]['imgstr']
        img = convert_str_to_bitmap(imgstr, scale)