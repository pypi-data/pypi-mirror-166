import numpy as np

from pykkn.storage import Storage


class Parameter(Storage):
    """An object of this class represents the Parameter.

    Parameters
    ----------
    name : str
        the name of the parameter

    Examples
    --------
    para1 = Parameter('para1') \n
    para1.attrs['value'] = 1
    para1.attrs['units'] = 'cm' \n
    para1.attrs['variable'] = '-' \n
    para1.attrs['origin'] = 'this'
    """

    def __init__(self, name: str):
        super().__init__(name)

        self.is_dataset = True
        self.data = np.zeros((1, 1), dtype=np.double)

        # all information in attrs will be stored in HDF5 file as attributes
        self.attrs["kkn_CLASS"] = "PARAMETER"
        self.attrs["kkn_PARAMETER_VERSION"] = "1.0"

        self.attrs["units"] = ""  # unit of measurement
        self.attrs["variable"] = ""
        self.attrs["origin"] = ""  # origin if this is derived data
