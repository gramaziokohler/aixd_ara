from aixd_grasshopper.gh_ui import model_input_output_dimensions
from aixd_grasshopper.gh_ui_helper import session_id, component_id
from scriptcontext import sticky as st
cid = component_id(ghenv.Component, "model_dims")

if get: 
    st[cid] = model_input_output_dimensions(session_id())
    
if cid in st.keys():
    if st[cid]['msg']: summary = st[cid]['msg'] #error
    else:
        summary = st[cid]['summary']