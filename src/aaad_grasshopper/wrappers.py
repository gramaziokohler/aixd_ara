from compas.data import Data


class WrapperShallowDataObject(object):
    """
    Generic wrapper to store the shallow data object definitions as dictionaries.
    """

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "{}: '{}' dim={} domain={}".format(self.data["datatype"], self.data["name"], self.data["dim"], self.data["domain"])

    def __str__(self):
        return self.__repr__()

class WrapperGH(object):
    """
    Basic wrapper intended to help passing data around in Grasshopper.
    For example, it is useful when you want to pass a dictionary from one GH component to another.
    Without it, default behaviour of Grasshopper will pass only the dictionary keys as a list of strings.
    """

    def __init__(self, data):
        self.data = data


class WrapperSample(Data):
    """
    Simple wrapper class to store data of a single design sample.
    Intended to collect samples values for dataobjects.
    Each dictionary should have the following structure and contents:
    * keys : correspond to the data object names
    * values : List of values. For dataobject with dim=1, this is a 1-item list.
    """

    def __init__(self, dp={}, pa={}, dataobjects={}):
        self.design_parameters = dp
        self.performance_attributes = pa
        self.dataobjects = dataobjects  # intended for an unsorted collection of dataobjects which is neither the colleciton in dp or pa.

    def __repr__(self):
        return "Sample Wrapper dp={} pa={} other={}".format(self.design_parameters, self.performance_attributes, self.dataobjects)
