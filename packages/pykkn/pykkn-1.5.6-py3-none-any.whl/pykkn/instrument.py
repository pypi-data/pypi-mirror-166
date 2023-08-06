from typing import List

from pykkn.model import Model
from pykkn.storage import Storage


class Instrument(Storage):
    """This class represents Datasets that are mapped from other datasets using a given model

    This can be used to convert the input of a sensor to its actual physical data using the given model,
    for example polynomials or lookup tables.

    Parameters
    ----------
    name : str
        the name of the instrument

    Examples
    --------
    instrument = Instrument('instrument1') \n
    instrument.add([model1, model2]) \n
    """

    def __init__(self, name: str):
        super().__init__(name)

        self.attrs["kkn_CLASS"] = "INSTRUMENT"
        self.attrs["kkn_INSTRUMENT_VERSION"] = "1.0"

        self.model = []

    def add(self, list_obj: List[Model]):
        """add (multi) model(s) into instrument

        Parameters
        ----------
        list_obj : List[Model]
            a list of Model object(s)

        Raises
        ------
        AssertionError:
            raise when adding method fails
        """
        assert isinstance(
            list_obj, list
        ), "the input must be a list containing Model object(s)"
        assert len(list_obj) >= 1, "the list must be not empty"
        for item in list_obj:
            if isinstance(item, Model):
                self.model.append(item)
            else:
                raise TypeError("the element in list must be a Model object")
