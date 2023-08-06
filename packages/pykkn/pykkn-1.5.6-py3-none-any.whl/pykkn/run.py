from typing import List

from pykkn.parameter import Parameter
from pykkn.pipeline import Pipeline
from pykkn.storage import Storage


class Run(Storage):
    """
    This object represents the run structure

    Parameters
    ----------
    name : str
        the name of the run

    Examples
    --------
    run1 = Run('run1') \n
    run1.add([parameter1, parameter2]) \n
    run1.add([pipeline1, pipeline2]) \n

    """

    def __init__(self, name: str):
        """Initialization method of Run class

        Parameters
        ----------
        name : str
            the name of the run
        """
        super().__init__(name)

        self.attrs["kkn_CLASS"] = "MSMTRUN"
        self.attrs["kkn_MSMTRUN_VERSION"] = "1.0"

        self.parameters = []
        self.pipelines = []

    def add(self, list_obj: List[Parameter | Pipeline]):
        """add (multi) parameter(s) or pipeline(s) into run

        Parameters
        ----------
        list_obj : List[Parameter | Pipeline]
            a list of Parameter or Pipeline object(s)

        Raises
        ------
        AssertionError:
            raise when add method fails
        """

        assert isinstance(list_obj, list), "the input must be a list"
        assert len(list_obj) >= 1, "the list must be not empty"

        # add the elementin list_obj into list container
        for item in list_obj:
            if isinstance(item, Parameter):
                self.parameters.append(item)
            elif isinstance(item, Pipeline):
                self.pipelines.append(item)
            else:
                raise TypeError(
                    "the element in list_obj must be a Parameter or Pipeline object"
                )
