# flake8: noqa
from aixd_ara.wrappers import WrapperShallowDataObject


if not options:
    options = None
else:
    options = [str(x) for x in options]


dobj = {"datatype": "DataCategorical", "name": name, "dim": 1, "domain": options}

dataobject = WrapperShallowDataObject(dobj)
