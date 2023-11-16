class WrapperShallowDataObject(object):
    """
    Generic wrapper to store the shallow data object definitions as dictionaries.
    """

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "{}: '{}' dim={} domain={}".format(self.data["datatype"], self.data["name"], self.data["dim"], self.data["domain"])


class WrapperGH(object):
    """
    Basic wrapper intended to help passing data around in Grasshopper.
    For example, it is useful when you want to pass a dictionary from one GH component to another.
    Without it, default behaviour of Grasshopper will pass only the dictionary keys as a list of strings.
    """

    def __init__(self, data):
        self.data = data


class WrapperSample(object):
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
        pass
