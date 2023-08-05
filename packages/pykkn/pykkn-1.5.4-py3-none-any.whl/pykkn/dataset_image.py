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
    dataset1.data = "/test/test_rig_1.jpg"
    """

    def __init__(self, name: str):
        super().__init__(name)

        self.is_dataset = True
        self._data = None

        self.attrs["kkn_CLASS"] = "DATASET"
        self.attrs["kkn_DATASET_SUBCLASS"] = "IMAGE"
        self.attrs["kkn_DATASET_VERSION"] = "1.0"
        self.attrs["timestamp"] = "-"

        """ The following attributes ensure that an image is correctly displayed in HDF5 view. \n
        To enable HDFview to correctly display images, the string attributes must have a finite length to be correctly interpreted.\n
        Further notice: These attributes does not need to to be changed \n

        Attribute name = 'CLASS'             (Required),     Attribute value = 'IMAGE' (Fixed)
            Explanation: This attribute identifies this data set as intended to be interpreted as an image that conforms to the specifications on this page. \n
        Attribute name = 'IMAGE_VERSION'     (recommended),  Attribute value = '1.2' (Fixed)
            Explanation: This attribute identifies the version number of this specification to which it conforms.  The current version number is "1.2". \n
        Attribute name = 'IMAGESUBCLASS'     (Required),     Attribute value = 'IMAGE_TRUECOLOR' (Changeble, but highly recommended)
            Explanation: The value of this attribute indicates the type of palette that should be used with the image. Other Attr values = "IMAGE_GRAYSCALE" or "IMAGE_BITMAP" or "IMAGE_INDEXED" \n
        Attribute name = 'IMAGE_MINMAXRANGE' (recommended)   Attribute value = [0, 255] (Changeable, recommended)
            Explanation: This attribute is an array of two numbers, of the same HDF5 datatype as the data. The first element is the minimum value of the data, and the second is the maximum. This is used for images with IMAGE_SUBCLASS="IMAGE_GRAYSCALE", "IMAGE_BITMAP" or "IMAGE_INDEXED".
        Attribute name = 'INTERLACE_MODE'    (Optional),     Attribute value = 'INTERLACE_PIXEL' (Default value)
            Explanation: For images with more than one component for each pixel, this optional attribute specifies the layout of the data. Other Attribute value = "INTERLACE_PLANE"
        """
        self.attrs["CLASS"] = np.string_("IMAGE")
        # self.attrs['IMAGE_MINMAXRANGE'] = np.array([0, 255]) # Better solution: [self.data.min(), self.data.max()], but it doenst work yet!
        self.attrs["IMAGE_SUBCLASS"] = np.string_("IMAGE_TRUECOLOR")
        # self.attrs['IMAGE_VERSION'] = np.string_('1.2')
        # self.attrs['INTERLACE_MODE'] = np.string_('INTERLACE_PIXEL')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, path_image: str):
        """the setter function to store a image file and some information in an HDF5 file

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
