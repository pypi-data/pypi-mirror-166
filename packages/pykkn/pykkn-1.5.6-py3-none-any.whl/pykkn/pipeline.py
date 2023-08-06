from typing import List

from pykkn.dataset import Dataset
from pykkn.instrument import Instrument
from pykkn.storage import Storage
from pykkn.dataset_image import Dataset_Image
from pykkn.dataset_video import Dataset_Video



class Pipeline(Storage):
    """This object represents a pipeline

    This name of pipeline should contain the following information: \n
    <measured/derived>/<capa>/<raw/scaled>

    Parameters
    ----------
    name : str
        the name of the pipeline

    Examples
    --------
    pipeline1 = Pipeline('measured/capa1/raw') \n
    pipeline1.attrs['variable'] = 'voltage' \n
    pipeline1.attrs['units'] = 'volts' \n
    pipeline1.attrs['origin'] = 'this' \n

    pipeline.add([dataset1, dataset2]) \n
    pipeline.add([instrument1, insturment2]) \n
    """

    def __init__(self, name: str):
        super().__init__(name)

        self.attrs["kkn_CLASS"] = "PIPELINE"
        self.attrs["kkn_PIPELINE_VERSION"] = "1.0"

        self.instruments = []

        self.data = []  # the dataset in this pipeline

        self.attrs["variable"] = "-"
        self.attrs["units"] = "-"  # unit of measurement
        self.attrs["origin"] = "-"  # origin if this is derived data

    def add(self, list_obj: List[Instrument | Dataset]):
        """add (multi) dataset(s) and instrument(s) into model

        Parameters
        ----------
        list_obj : List[Instrument  |  Dataset]
            a list of Instrument or Dataset object(s)

        Raises
        ------
        TypeError
            raised when the element of list_obj is not the type of Instrument or Dataset
        AssertionError
            raised when list_obj is not a list or it is empty
        """

        # Before extend the list of attributes, must be sure that there is actually a non-empty list
        assert isinstance(
            list_obj, list
        ), "the input must be a list containing Instrument or Dataset object(s)"
        assert len(list_obj) >= 1, "the list must be not empty"

        # Assign it to different properties based on the type of elements in the list
        for item in list_obj:
            if isinstance(item, Instrument):
                self.instruments.append(item)
            elif isinstance(item, Dataset) or isinstance(item, Dataset_Image) or isinstance(item, Dataset_Video):
                self.data.append(item)
            else:
                raise TypeError(
                    "input must be a list of Instrument or Dataset object(s)"
                )
