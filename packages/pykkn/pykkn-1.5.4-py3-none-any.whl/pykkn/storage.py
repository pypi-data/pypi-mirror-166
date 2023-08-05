import base64
import json
import pickle
from pathlib import Path
from typing import Any

import h5py
import numpy as np


class Storage:
    """This class is an abstracted for all other classes, providing initialization function with a name
    and store function to generate an HDF5 file

    Parameters
    ----------
    name : str
        the name of the instant
    """

    def __init__(self, name):
        self.name = name
        self.storage_path = None
        self.is_dataset = False
        self.attrs = {}

    def set_storage_path(self, path: str):
        """set the storage path where you want to store the HDF5 file

        ATTENTION
        ---------
        please always use "/" in path string instead of "\"

        Parameters
        ----------
        path : str
            _description_
        """
        self.storage_path = Path(path)

    def is_overwritable(self):
        return self.storage_path.exists()

    def store_HDF5(self, root=None):

        # make a new HDF5 file if this is a root
        if root is None:
            root = h5py.File(self.storage_path, "w")

        # create a dataset or group according to whether this structure has data
        if self.is_dataset:

            # transfer the 'value' to data

            if self.attrs["kkn_CLASS"] == "PARAMETER":
                self.data = np.array(self.attrs["value"]).astype(np.double)
                # self.attrs.pop('value')

            # because this class has no subclass, so create it as a dataset
            # special handle for video dataset
            # it should be converted to numpy.void type, so that it can store in HDF5 file
            if (
                "kkn_DATASET_SUBCLASS" in self.attrs.keys()
                and self.attrs["kkn_DATASET_SUBCLASS"] == "VIDEO"
            ):
                s = root.create_dataset(self.name, data=np.void(self.data))
            else:
                s = root.create_dataset(self.name, data=self.data)

            if "samplerate" in self.attrs.keys():
                self.attrs["samplerate"] = float(self.attrs["samplerate"])

            # store all attributes in the groups attribute
            for name, value in self.attrs.items():
                s.attrs[name] = value
            return  # and exit the function
        else:
            # because this class has subclass, so create it as a group
            s = root.create_group(self.name)

            # iterate all keys in attrs and store their values as attributes
            for name, value in self.attrs.items():
                s.attrs[name] = value

            attrs = {
                "parameters": "self.parameters",
                "model": "self.model",
                "data": "self.data",
                "instruments": "self.instruments",
                "pipelines": "self.pipelines",
            }

            for name, attr in attrs.items():
                if hasattr(self, name):
                    s_grp = s.create_group(name)
                    for i in eval(attr):
                        i.store_HDF5(root=s_grp)

    def store_json(self, root=None):

        if root is None:
            root = {}

        root["name"] = self.name

        if self.is_dataset:

            if "value" in self.attrs.keys():
                self.data = np.array(self.attrs["value"]).tolist()
                self.attrs.pop("value")

            condition1 = (
                "kkn_DATASET_SUBCLASS" in self.attrs.keys()
                and self.attrs["kkn_DATASET_SUBCLASS"] == "IMAGE"
            )
            condition2 = (
                "kkn_DATASET_SUBCLASS" in self.attrs.keys()
                and self.attrs["kkn_DATASET_SUBCLASS"] == "VIDEO"
            )

            # encode the data attribute when this is an instance of dataset_image of dataset_video
            if condition1 or condition2:
                root["data"] = self.encode(self.data)
            else:
                if not (
                    isinstance(self.data, list)
                    or isinstance(self.data, int)
                    or isinstance(self.data, float)
                ):
                    self.data = self.data.tolist()
                root["data"] = self.data

            # decode the binary information in some attributes only for image dataset
            # If you do not do that, a TypeError will occur in json saving process
            if condition1:
                if isinstance(self.attrs["CLASS"], bytes):
                    self.attrs["CLASS"] = self.attrs["CLASS"].decode()
                if isinstance(self.attrs["IMAGE_SUBCLASS"], bytes):
                    self.attrs["IMAGE_SUBCLASS"] = self.attrs["IMAGE_SUBCLASS"].decode()

            for name, value in self.attrs.items():
                if isinstance(value, np.integer):
                    value = int(value)
                elif isinstance(value, np.floating):
                    value = float(value)
                elif isinstance(value, np.ndarray):
                    value = value.tolist()
                root[name] = value

            return root

        else:

            for name, value in self.attrs.items():
                root[name] = value

            attrs = {
                "parameters": "self.parameters",
                "model": "self.model",
                "data": "self.data",
                "instruments": "self.instruments",
                "pipelines": "self.pipelines",
            }

            for name, attr in attrs.items():
                if hasattr(self, name):
                    root[name] = []
                    for i in eval(attr):
                        root[name].append(i.store_json())
            return root

    def store(self, format=None, root=None):

        if format is None:
            if self.storage_path is None:
                # set the file saving path if it does not exist
                self.storage_path = f"{self.name}.h5"
            else:
                # replace the suffix to h5
                self.storage_path = str(self.storage_path).replace(".json", ".h5")

            self.store_HDF5()

        elif format == "json":
            if self.storage_path is None:
                # set the file saving path if it does not exist
                self.storage_path = f"{self.name}.h5"
            else:
                # replace the suffix with json
                self.storage_path = str(self.storage_path).replace(".h5", ".json")

            json_object = self.store_json()
            str_repr = json.dumps(json_object, indent=2)

            # remove unnecessary line breaks
            str_repr = str_repr.replace(",\n              ", ",")
            str_repr = str_repr.replace('","', '",\n              "')
            str_repr = str_repr.replace(",    ", ",\n                  ")

            # save the dict data in a file
            with open(self.storage_path, "w") as f:
                f.write(str_repr)

    def __str__(self):
        """rewrite the built-in method to modify the behaviors of print() for this instance
        to make the print result more readable

        before: \n
        >>>print(run1) \n
        <run.Run object at 0x0000022AA45715A0>

        after: \n
        >>>print(run1) \n
        'run1'

        here, the string 'run1' is the name of this instance
        """
        return self.name

    def __repr__(self):
        """rewrite the built-in method to modify the behaviors of print() for a list of instances
        to make the print result more readable

        before: \n
        >>>print(run1.pipelines) \n
        [<pipeline.Pipeline object at 0x0000022AA45715A0>, <pipeline.Pipeline object at 0x0000022AA4gd1s0>]

        after: \n
        >>>print(run1.pipelines) \n
        ['pipe1', 'pipe2']

        here, the strings 'pipe1' and 'pipe2' are the names of this instance
        """
        return self.name

    def show(self):
        """use the method to show the detailed information about this instance, for example all attributes and names.
        It should return a string like this:

        Examples
        --------
        >> msmtrun.show()

        #### pipelines ####

        ['aa', 'bb', 'cc']

        #### parameters ####

        ['dd', 'ee', 'ff']

        #### attributes ####

        'author' : 'who'    \n
        'author' : 'derGeraet'  \n
        'pmanager' : 'tcorneli' \n
        'targettmp' : 70    \n
        'targetrps' : 2     \n
        'oil' : 'PA06'  \n

        """
        s = ""
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                s = s + f"\n#### {key} ####\n" + f"{value}\n"
            elif isinstance(value, dict):
                for key_2, value_2 in self.attrs.items():
                    s = f"{key_2} : {value_2}\n" + s
            else:
                s = f"{key} : {value}\n" + s
        s = "\n#### attributes ####\n" + s
        print(s)

    def add_attrs_dict(self, dict):
        """Add a flat Dictionary of key values as a set of attributes.

        Parameters:
        -----------
        dict : str
            The Dictionary consists of Key Value pairs, with the keys being the names of the attribute
            and the value being the value assigned to the attribute
        """
        for key, value in dict.items():
            self.attrs[key] = value

    def encode(self, object: Any) -> str:
        """encode anything as a string
        Parameters:
        ----------
        object: Any
            an object which can be an instance of any class
        Returns:
        --------
        object_string: str
            an encoded string, maybe very long if the original object is large
        """
        object_binary = pickle.dumps(object)
        object_encoded = base64.b64encode(object_binary)
        object_string = object_encoded.decode()

        return object_string

    def decode(self, object_string: str) -> object:
        """decode a string as its original form
        Parameters:
        -----------
        object_string: str
            an encoded string
        Returns:
        --------
        object: object
            this is a instance of its original class, you can check its type with type()
        """
        object_encoded = object_string.encode()
        object_binary = base64.b64decode(object_encoded)
        object = pickle.loads(object_binary)

        return object
