# flake8: noqa
from aixd_grasshopper.wrappers import WrapperShallowDataObject

if not dim or dim < 1:
    dim = 1

if domain:
    domain = (int(domain.Min), int(domain.Max))
else:
    domain = None


dobj = {"datatype": "DataInt", "name": name, "dim": dim, "domain": domain}


dataobject = WrapperShallowDataObject(dobj)
