# flake8: noqa
from aixd_ara.wrappers import WrapperShallowDataObject

if not dim or dim < 1:
    dim = 1

if domain:
    domain = (float(domain.Min), float(domain.Max))
else:
    domain = None


dobj = {"datatype": "DataReal", "name": name, "dim": dim, "domain": domain}


dataobject = WrapperShallowDataObject(dobj)
