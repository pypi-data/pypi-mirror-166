from pathlib import Path

import numpy as np
from PIL import Image

from pykkn.storage import Storage


class Dataset_Image(Storage):
    """An object of this class represents one image
    (Multiple images have not been considered or investigated yet). \n
    The user only needs to provide the path of the image
    this class will read it using the pillow lib

    Parameters
    ----------
    name : str
        the name of the dataset

    Examples
    ---------
    ataset1 = Dataset_Image('image_dataset_1') \n
    dataset1.data = "test_rig_1.jpg"
    """

    def __init__(self, name: str):
        super().__init__(name)

        self.is_dataset = True
        self._data = None

        self.attrs["kkn_CLASS"] = "DATASET"
        self.attrs["kkn_DATASET_SUBCLASS"] = "IMAGE"
        self.attrs["kkn_DATASET_VERSION"] = "1.0"
        self.attrs["timestamp"] = "-"

        self.attrs["CLASS"] = np.string_("IMAGE")
        # self.attrs['IMAGE_MINMAXRANGE'] = np.array([0, 255])
        self.attrs["IMAGE_SUBCLASS"] = np.string_("IMAGE_TRUECOLOR")
        # self.attrs['IMAGE_VERSION'] = np.string_('1.2')
        # self.attrs['INTERLACE_MODE'] = np.string_('INTERLACE_PIXEL')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, path_image: str):
        """the setter function to store a image file and some information

        Parameters
        ----------
        path_image : str
            the path to the video file.
        """

        path = Path(path_image)

        self._data = Image.open(path)

        self.attrs["file_name"] = path.name
        self.attrs["file_format"] = self._data.format
        self.attrs["image_mode"] = self._data.mode

        data_np = np.array(self._data)
        self.attrs["shape"] = data_np.shape
        self.attrs["image_width"] = data_np.shape[1]
        self.attrs["image_height"] = data_np.shape[0]
        self.attrs["num_channels"] = data_np.shape[2]
        self.attrs["data_type"] = f"{data_np.dtype}"

        del data_np

    def output_file(self):
        """this function is designed to export image"""
        self._data.save(self.attrs["file_name"])
