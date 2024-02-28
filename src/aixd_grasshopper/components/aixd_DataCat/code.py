from aixd_grasshopper.wrappers import WrapperShallowDataObject

if not dim or dim < 1:
    dim = 1

if not options:
    options = None


dobj = {"datatype": "DataCategorical", "name": name, "dim": dim, "domain": options}

dataobject = WrapperShallowDataObject(dobj)
