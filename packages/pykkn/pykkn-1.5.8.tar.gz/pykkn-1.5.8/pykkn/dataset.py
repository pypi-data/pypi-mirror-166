import numpy as np

from pykkn.storage import Storage


class Dataset(Storage):
    """An object of this class represents the dataset.

    Parameters
    ----------
    name : str
        the name of the dataset

    Examples
    ---------
    dataset = Dataset('dataset1') \n
    dataset.data = np.double(1) \n
    dataset.attrs['samplerate'] = 1000 \n
    dataset.attrs['timestamp'] = '2022-06-12 10:39:11' \n
    """

    def __init__(self, name: str):
        super().__init__(name)

        self.is_dataset = True
        self.data = np.double(1)

        self.attrs["kkn_CLASS"] = "DATASET"
        self.attrs["kkn_DATASET_SUBCLASS"] = "TIMESERIES"
        self.attrs["kkn_TIMESERIES_VERSION"] = "1.0"

        # the format of time stamp should be "YYYY-MM-DD HH:mm:ss"
        self.attrs["timestamp"] = "-"
        self.attrs["samplerate"] = np.double(1)
