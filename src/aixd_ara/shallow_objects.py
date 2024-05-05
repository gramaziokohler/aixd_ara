from typing import Dict
from typing import List

from aixd.data.data_objects import DataBool
from aixd.data.data_objects import DataCategorical
from aixd.data.data_objects import DataInt
from aixd.data.data_objects import DataReal
from aixd.data.domain import Interval
from aixd.data.domain import Options

"""
Methods to convert between shallow versions of data objects and the proper DataObject classes.

A shallow version is a dictionary of a form:
dict = {'datatype': str,
        'name': str,
        'dim' : int,
        'domain' : list of
            [True, False] (for DataBool), or
            two values (float for DataReal), or
            n values (int for DataInt or any for DataCategorical), or
            None
    }

"""


def DataInt_from_shallow(shallow_dobj):
    return DataInt(
        name=shallow_dobj["name"],
        dim=shallow_dobj["dim"],
        domain=Options(shallow_dobj["domain"]) if shallow_dobj["domain"] else None,
    )


def DataReal_from_shallow(shallow_dobj):
    return DataReal(
        name=shallow_dobj["name"],
        dim=shallow_dobj["dim"],
        domain=Interval(*shallow_dobj["domain"]) if shallow_dobj["domain"] else None,
    )


def DataCategorical_from_shallow(shallow_dobj):
    return DataCategorical(
        name=shallow_dobj["name"],
        dim=shallow_dobj["dim"],
        domain=Options(shallow_dobj["domain"]) if shallow_dobj["domain"] else None,
    )


def DataBool_from_shallow(shallow_dobj):
    return DataBool(name=shallow_dobj["name"], dim=shallow_dobj["dim"])


def dataobjects_from_shallow(shallow_dobjs: List[Dict]):  # -> List[DataObject]:
    """
    Converts a list of shallo data objects to the proper instances of respective DataObject child classes.
    """
    dobj_list = []
    for sh_dobj in shallow_dobjs:
        if sh_dobj["datatype"] == "DataBool":
            dobj_list.append(DataBool_from_shallow(sh_dobj))
        elif sh_dobj["datatype"] == "DataCategorical":
            dobj_list.append(DataCategorical_from_shallow(sh_dobj))
        elif sh_dobj["datatype"] == "DataInt":
            dobj_list.append(DataInt_from_shallow(sh_dobj))
        elif sh_dobj["datatype"] == "DataReal":
            dobj_list.append(DataReal_from_shallow(sh_dobj))
        else:
            raise ValueError(
                f"Unknow data type {sh_dobj['datatype']} in a shallow data object."
                + "Allowed values (string) are: 'DataBool', 'DataCategorical', 'DataInt', 'DataReal'."
            )

    return dobj_list
