import json

from pykkn.dataset import Dataset
from pykkn.dataset_image import Dataset_Image
from pykkn.dataset_video import Dataset_Video
from pykkn.instrument import Instrument
from pykkn.model import Model
from pykkn.parameter import Parameter
from pykkn.pipeline import Pipeline
from pykkn.run import Run


def create_instance(dic: dict) -> object:
    """create the corresponding object

    Parameters
    ----------
    dic : dict
        json structure or sub-structure

    Returns
    -------
    object
        one of the component types, the type of return depends on the structure of json structure

    Raises
    ------
    TypeError
        raised when given a wrong dataset class
    TypeError
        raised when given a wrong component class
    """

    # create component object according to its kkn_CLASS attribute
    if dic["kkn_CLASS"] == "MSMTRUN":
        obj = Run(dic["name"])
    elif dic["kkn_CLASS"] == "PIPELINE":
        obj = Pipeline(dic["name"])
    elif dic["kkn_CLASS"] == "INSTRUMENT":
        obj = Instrument(dic["name"])
    elif dic["kkn_CLASS"] == "MODEL":
        obj = Model(dic["name"])
    elif dic["kkn_CLASS"] == "PARAMETER":
        obj = Parameter(dic["name"])
    elif dic["kkn_CLASS"] == "DATASET":
        if dic["kkn_DATASET_SUBCLASS"] == "TIMESERIES":
            obj = Dataset(dic["name"])
        elif dic["kkn_DATASET_SUBCLASS"] == "IMAGE":
            obj = Dataset_Image(dic["name"])
        elif dic["kkn_DATASET_SUBCLASS"] == "VIDEO":
            obj = Dataset_Video(dic["name"])
        else:
            raise TypeError(f"Error Dataset Type: {dic['kkn_DATASET_SUBCLASS']}")
    else:
        raise TypeError(f"Error Class Type: {dic['kkn_CLASS']}")

    return obj


def recursive_create_instance(file: dict) -> object:
    """Recursively read json structure, create the corresponding object and assign the original property value to it

    Parameters
    ----------
    file : dict
        json structure or sub-structure

    Returns
    -------
    object
        one of the component types, the type of return depends on the structure of json file
    """
    # create object
    obj = create_instance(file)

    # iter all key-value pairs in this dictionary structure
    for key, value in file.items():
        if not isinstance(value, list):
            obj.attrs[key] = value
        else:
            # special case for dataset and parameter class
            if (
                key == "data"
                and file["kkn_CLASS"] in ["DATASET", "PARAMETER"]
                or key == "shape"
                and file["kkn_CLASS"] == "DATASET"
            ):
                obj.attrs[key] = value
            else:
                # here means there is a sub-structure in this file
                for element in file[key]:
                    obj.add([recursive_create_instance(element)])

    return obj


def pykkn_parse(path):
    """read a json file and convert it to the pykkn data management structure

    Parameters
    ----------
    path : str
        path of the object json file

    Returns
    -------
    object
        one of the component types, the type of return depends on the structure of json file
    """
    # open and read a json file
    with open(path, "r") as f:
        dic = json.load(f)

    # create object
    obj = recursive_create_instance(dic)

    return obj
