# this code has been inspired by a forum post by "chanley" (2018.11.02) https://discourse.mcneel.com/t/can-i-instantiate-specific-component-on-the-canvas-with-a-script-python/74204/8 

import Grasshopper
import System.Drawing as sd

from aixd_grasshopper.gh_ui import get_dataobject_names_from_block
from aixd_grasshopper.gh_ui_helper import session_id

comp = ghenv.Component
ghdoc = comp.OnPingDocument()

def make_Panel(NickName, UserText, Pivot, Bounds):
    try:
        Panel = Grasshopper.Kernel.Special.GH_Panel()
        Panel.NickName = NickName
        Panel.UserText = UserText
        Panel.Properties.Colour = sd.Color.White
        #Panel.Properties.Font = sd.Font("Trebuchet MS", 10)
        Panel.Properties.Multiline = False
        Panel.Properties.DrawIndices = False
        Panel.Properties.DrawPaths = False
        ghdoc.AddObject(Panel,False,ghdoc.ObjectCount+1)
        Panel.Attributes.Pivot = Pivot
        Panel.Attributes.Bounds = Bounds
    except Exception, ex:
        ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning,str(ex))


x = ghenv.Component.Attributes.DocObject.Attributes.Bounds.Right
y = ghenv.Component.Attributes.DocObject.Attributes.Bounds.Top

w = 150
h = 150
gap = 50

errors = ""

if not datablock:
    datablock = [ "design_parameters","performance_attributes","inputML","outputML"] #all datablock names 

if get_names:
    
    for i, datablock_nickname in enumerate(datablock):
        panel_title = datablock_nickname
        response = get_dataobject_names_from_block(session_id(),datablock_nickname)
        text_items = response['names']
        if text_items:
            text_str= "\n".join(text_items)
            pt = sd.PointF(x + gap + i*gap, y + i*gap)
            rect = sd.RectangleF(0,0,w,h)
            make_Panel(panel_title, text_str, pt, rect)
        else:
            errors+=response['msg']+"\n"

if errors: ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning,str(errors))
