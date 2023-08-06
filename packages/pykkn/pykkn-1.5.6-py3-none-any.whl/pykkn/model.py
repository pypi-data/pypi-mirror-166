from typing import List

from pykkn.parameter import Parameter
from pykkn.storage import Storage


class Model(Storage):
    """This object is used to represent the model for data processing in the experiment

    Parameters
    ----------
    name : str
        the name of the model

    Examples
    --------
    model = Model('model1') \n
    model.add([parameter1, parameter2]) \n

    """

    def __init__(self, name: str):
        super().__init__(name)

        self.attrs["kkn_CLASS"] = "MODEL"
        self.attrs["kkn_MODEL_SUBCLASS"] = "POLY"
        self.attrs["kkn_POLY_VERSION"] = "1.0"

        self.parameters = []

    def add(self, list_obj: List[Parameter]):
        """add (multi) parameter(s) into model

        Parameters
        ----------
        list_obj : List[Parameter]
            a list of Parameter object(s)

        Raises
        ------
        AssertionError:
            raise when add method fails
        """
        assert isinstance(list_obj, list), "the input must be a list)"
        assert len(list_obj) >= 1, "the list must be not empty"
        for item in list_obj:
            if isinstance(item, Parameter):
                self.parameters.append(item)
            else:
                raise TypeError("the element in list must be a Parameter object")
