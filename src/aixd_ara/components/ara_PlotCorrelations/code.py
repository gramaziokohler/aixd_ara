# flake8: noqa
from scriptcontext import sticky as st

from aixd_ara.gh_ui import plot_correlations
from aixd_ara.gh_ui_helper import component_id
from aixd_ara.gh_ui_helper import convert_str_to_bitmap
from aixd_ara.gh_ui_helper import session_id

cid = component_id(session_id(), ghenv.Component, "PlotCorrelations")


if plot:
    st[cid] = plot_correlations(session_id(), variables, "interactive")  # will launch the plotly fig in browser

if cid in st.keys():
    print(st[cid])