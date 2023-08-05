from pathlib import Path

import cv2

from pykkn.storage import Storage


class Dataset_Video(Storage):
    """An object of this class represents the video dataset.

    Parameters
    ----------
    name : str
        the name of the dataset

    Examples
    --------
    dataset1 = Dataset_Video('video_dataset_1') \n
    ataset1.data = r"C:/Users/Administrator/Videos/Captures/test_meeting_recording.mp4"   \n
    dataset1.data = "C:/Users/Administrator/Videos/Captures/test_meeting_recording.mp4"    \n
    dataset1.attrs['timestamp'] = '2022-06-13 11:22:11' \n

    dataset1.set_storage_path('test/test_ut_video.h5')  \n

    dataset1.store()    \n
    """

    def __init__(self, name: str):
        super().__init__(name)

        self.is_dataset = True

        self._data = None

        self.attrs["kkn_CLASS"] = "DATASET"
        self.attrs["kkn_DATASET_SUBCLASS"] = "VIDEO"
        self.attrs["kkn_TIMESERIES_VERSION"] = "1.0"
        self.attrs["timestamp"] = "-"

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, path_video: str):
        """the setter function to store a video file and some information in an HDF5 file

        Parameters
        ----------
        path_video : str
            the path to the video file.
        """
        path = Path(path_video)

        # convert the video into binary format and store
        with open(path, "rb") as f:
            self._data = f.read()

        # store the name and suffix of the video file, to convert this binary format into original format
        self.attrs["file_name"] = path.name
        self.attrs["file_suffix"] = path.suffix.split(".")[-1]

        # in order to read some attributes about this video, open it with opencv
        cap = cv2.VideoCapture(str(path))

        self.attrs["video_fps"] = int(cap.get(cv2.CAP_PROP_FPS))
        self.attrs["video_num_frames"] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.attrs["video_width"] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.attrs["video_height"] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.attrs[
            "video_length"
        ] = f"{int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) // int(cap.get(cv2.CAP_PROP_FPS))}s"

        # delete the useless variable to save memory
        del cap

    def output_file(self, path_output):
        """this function is designed to convert the binary format data into the original format

        Parameters
        ----------
        path_output : str
            the path of output
        """
        with open(self.attrs["file_name"], "rb") as f:
            f.write(self.data)

    def convert_pics(self, path_output):
        """this function is to convert the video file into frame segmentations

        Parameters
        ----------
        path_output : str
            the path of output
        """
        pass
