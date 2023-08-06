import numpy as np

from pykkn.storage import Storage


class Dataset(Storage):
    """An object of this class represents the dataset.

    At present, there is no requirement for the type of data, it is simply stored in the dataset.data attribute
    and further processing will be performed according to the different data types read in.

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
    dataset.set_storage_path('test/test_ut_ds.h5') \n
    dataset.store() \n

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


if __name__ == "__main__":
    d = Dataset("abc")
    d.data = 1
    d.set_storage_path("tests/test_results/path_test.h5")
    d.store(format="json")
