# flake8: noqa
from aixd_ara.wrappers import WrapperShallowDataObject

if not dim or dim < 1:
    dim = 1


dobj = {"datatype": "DataBool", "name": name, "dim": dim}


dataobject = WrapperShallowDataObject(dobj)
