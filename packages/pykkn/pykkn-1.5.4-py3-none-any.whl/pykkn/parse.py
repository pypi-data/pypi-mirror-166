from pathlib import Path
from typing import List

import h5py
from PIL import Image

from pykkn.dataset import Dataset
from pykkn.dataset_image import Dataset_Image
from pykkn.dataset_video import Dataset_Video
from pykkn.instrument import Instrument
from pykkn.model import Model
from pykkn.parameter import Parameter
from pykkn.pipeline import Pipeline
from pykkn.run import Run


def dataset_data_parse(obj: object, h5: h5py.File) -> object:
    """data parser for dataset class

    Parameters
    ----------
    obj : object
        pykkn component class object without data
    h5 : h5py.File
        HDF5 file structure or sub structure

    Returns
    -------
    object
        pykkn component class object with data
    """
    obj.data = h5[()]
    return obj


def image_data_parse(obj: object, h5: h5py.File) -> object:
    """data parser for dataset_image class

    Parameters
    ----------
    obj : object
        pykkn component class object without data
    h5 : h5py.File
        HDF5 file structure or sub-structure

    Returns
    -------
    object
        pykkn component class object with data
    """
    # read data and convert it from numpy array to pillow image
    image = Image.fromarray(h5[()])
    # create and save this image file to temp folder
    temp_path = Path(".temp")
    if not temp_path.exists():
        temp_path.mkdir()
    image.save(temp_path / "temp.png")
    # assign this image object to pykkn object
    obj._data = Image.open(temp_path / "temp.png")
    return obj


def video_data_parse(obj: object, h5: h5py.File) -> object:
    """data parser for dataset_video class

    Parameters
    ----------
    obj : object
        pykkn component class object without data
    h5 : h5py.File
        HDF5 file structure or sub-structure

    Returns
    -------
    object
        pykkn component class object with data
    """
    # read binary data and store in form of mp4 file
    temp_path = Path(".temp")
    if not temp_path.exists():
        temp_path.mkdir()
    with open(temp_path / "temp.mp4", "wb") as f:
        f.write(h5[()])
    with open(temp_path / "temp.mp4", "rb") as f:
        obj._data = f.read()
    return obj


def create_instance(root: h5py.File, key: str) -> object:
    """create the corresponding object and assign attribute

    Parameters
    ----------
    root : h5py.File
        HDF5 file structure or sub-structure
    key : str
        name of this object

    Returns
    -------
    object
        pykkn components object

    Raises
    ------
    TypeError
        raised when given a wrong dataset class
    TypeError
        raised when given a wrong component class
    """
    # create object according to its kkn_CLASS
    if root[key].attrs["kkn_CLASS"] == "MSMTRUN":
        obj = Run(key)
    elif root[key].attrs["kkn_CLASS"] == "PIPELINE":
        obj = Pipeline(key)
    elif root[key].attrs["kkn_CLASS"] == "INSTRUMENT":
        obj = Instrument(key)
    elif root[key].attrs["kkn_CLASS"] == "MODEL":
        obj = Model(key)
    elif root[key].attrs["kkn_CLASS"] == "PARAMETER":
        obj = Parameter(key)
    elif root[key].attrs["kkn_CLASS"] == "DATASET":
        if root[key].attrs["kkn_DATASET_SUBCLASS"] == "TIMESERIES":
            obj = Dataset(key)
            obj = dataset_data_parse(obj, root[key])
        elif root[key].attrs["kkn_DATASET_SUBCLASS"] == "IMAGE":
            obj = Dataset_Image(key)
            obj = image_data_parse(obj, root[key])
        elif root[key].attrs["kkn_DATASET_SUBCLASS"] == "VIDEO":
            obj = Dataset_Video(key)
            obj = video_data_parse(obj, root[key])
        else:
            raise TypeError(
                f"Error Dataset Type: {root[key].attrs['kkn_DATASET_SUBCLASS']}"
            )
    else:
        raise TypeError(f"Error Class Type: {root[key].attrs['kkn_CLASS']}")
    # assign attributes to this object
    for k, v in root[key].attrs.items():
        obj.attrs[k] = v

    return obj


def recursive_create_instance(file: h5py.File) -> List[object]:
    """recursively create object and assign attributes

    Parameters
    ----------
    file : h5py.File
        HDF5 file structure or sub-structure

    Returns
    -------
    List[object]
        a list of pykkn component objects
    """
    results = []
    for key in list(file.keys()):
        # create a component object and assign its attributes
        obj = create_instance(file, key)
        # if this object has not sub-structure
        if obj.attrs["kkn_CLASS"] not in ["PARAMETER", "DATASET"]:
            for subgroup_name in list(file[key].keys()):
                if subgroup_name != "pipelines":
                    obj.add(recursive_create_instance(file[key][subgroup_name]))
                else:
                    # here is the special situation for pipeline object because of its name xx/xx/xx
                    # TODO here still some space to improve
                    for a in list(file[key][subgroup_name].keys()):
                        aa = file[key][subgroup_name][a]
                        for b in list(aa.keys()):
                            bb = aa[b]
                            for c in list(bb.keys()):
                                pipe_obj = create_instance(
                                    file[key][subgroup_name], f"{a}/{b}/{c}"
                                )
                                for sub_subgroup_name in list(
                                    file[key][subgroup_name][f"{a}/{b}/{c}"]
                                ):
                                    pipe_obj.add(
                                        recursive_create_instance(
                                            file[key][subgroup_name][f"{a}/{b}/{c}"][
                                                sub_subgroup_name
                                            ]
                                        )
                                    )
                                obj.add([pipe_obj])
        results.append(obj)

    return results


def pykkn_parse(path: str) -> object:
    """read a HDF5 file and convert it to pykkn data management structure

    Parameters
    ----------
    path : str
        path of HDF5 file

    Returns
    -------
    object
        one of the component types, the type of return depends on the structure of json structure
    """
    # open an HDF5 file
    file = h5py.File(path)

    # create a list of objects which convert from top structure
    obj = recursive_create_instance(file)

    # get the first object
    root = obj[0]

    # give user a message and print the root name
    print(f"parsing finished, the root's name is {root}")

    return root
