import numpy as np

from pykkn.dataset import Dataset
from pykkn.instrument import Instrument
from pykkn.model import Model
from pykkn.parameter import Parameter
from pykkn.pipeline import Pipeline
from pykkn.run import Run
from pykkn.storage import Storage


class Dataset_KeyValue(Storage):

    """Dataset_KeyValue class is used as a converter between a dictionary formated in an HDF5 storable way to a HDF file


    Parameters
    -----------
    Name : str
        Name of the whole HDF file/Run

    Path : str
        The storage path


    Examples
    --------
    DictToHDF_1 = Dataset_KeyValue("run1", 'test_key_value.h5') \n
    DictToHDF_1.nested_dict(dict)

    """

    def __init__(self, name: str, path: str = None):
        """
        Name : str
            Name of the whole HDF file/Run

        Path : str
            The storage path

        """
        super().__init__(name)

        if path is not None:
            super().set_storage_path(path)
        else:
            self.storage_path = None

        self.attrs["kkn_CLASS"] = "DATASET"
        self.attrs["kkn_DATASET_SUBCLASS"] = "KEY_VALUE"
        self.attrs["kkn_TIMESERIES_VERSION"] = "1.0"
        self.attrs["timestamp"] = "-"

    def nested_dict(
        self, Dict, _last_group=None, _key=None, _nested_group=None
    ):  # if last group was data then -> last_group=data -> data.
        """Expects a Dictionary that starts with run

        Parameter:
        1. see if dictname = parameter;
        2. if last group = parameter, go into dict and create parameter for each (e. g.: gain, offset )
        3. Go into the parameters and add the attributes

        Data is similar to parameter, just that we add data instead

        XXXXXXXXXX  data kann also have attributes  ----> How would attributes look in a JSON-> Dict?




        _Group : str
            parameter to be used by the recursive function; describes the last "wrapper class" (pipeline,instruments,model)

        _last_group : str
            parameter to be used by the recursive function

        Dict : list, tuple, dict
            nested key value pairs -->
            Dicti[key]: whole dictionary is called by the name Dicti, to get a single value Dicti[key] is called
            Dict structure => Dicti = {key : value, .. ,}
        """

        #     (self, Dict, _last_group = None, _key = None, _nested_group):: Key is the key as string/object
        for key in Dict:
            """key : value
            key = our key as a string
            Dict[key] = value of key
            """
            #### run

            if (
                isinstance(Dict[key], (list, tuple, dict))
                and _last_group == None
                and _key == None
            ):  # first dict name is the name of the run (e.g. run_01)
                key = Run(key)
                key.add([self.nested_dict(Dict[key], "run_start")])
                key.store()

            #### param
            # TODO
            if (
                isinstance(Dict[key], (list, tuple, dict))
                and key == "parameters"
                and _last_group != "pipeline"
            ):  # check if param
                return self.nested_dict(Dict[key], "parameters")

            elif (
                isinstance(Dict[key], (list, tuple, dict))
                and _last_group == "parameters"
            ):  # create param class
                key = Parameter(key)  # gain = parameter("gain")
                self.nested_dict(Dict[key], _last_group, key)
                return key  # key is the class that was created

            elif _last_group == "parameters":  # add parameter attributes
                _key.attrs[key] = Dict[key]  # gain.attrs["value"] = 10 ..

            #### dataset
            # TODO
            if (
                isinstance(Dict[key], (list, tuple, dict))
                and key == "data"
                and _last_group != "pipeline"
            ):  # check if data
                return self.nested_dict(Dict[key], "data")

            elif (
                isinstance(Dict[key], (list, tuple, dict)) and _last_group == "data"
            ):  # create data class
                key = Dataset(key)  # 1000 = dataset("1000")
                self.nested_dict(Dict, "data", _key=key)
                self.nested_dict(Dict[key], _last_group, key)
                # key.data = self.nested_dict(Dict[key], _last_group, key) --- and return Dict[key]
                return key

            elif (
                not isinstance(Dict[key], (list, tuple, dict)) and _last_group == "data"
            ):  # add the meta data
                _key.attrs[key] = Dict[key]
            # TODO
            elif (
                _last_group == "data"
            ):  # and not isinstance?                   # add data to dataset
                _key.data = Dict[key]  # Can we pass a array like this?
                # Is array list or tuple
                # is it possible to get lists or tuples as data (add them for safety?)

            #### model

            if (
                isinstance(Dict[key], (list, tuple, dict))
                and key == "model"
                and _last_group != "pipeline"
            ):  # check if model
                return self.nested_dict(Dict[key], "model")

            # inside the model dict

            elif isinstance(Dict[key], (list, tuple, dict)) and _last_group == "model":
                key = Model(key)  # create model class
                self.nested_dict(Dict, "data", _key=key)  # check for meta data
                key.add([self.nested_dict(Dict[key], _last_group="")])  # add models
                return key

            # meta data

            elif (
                not isinstance(Dict[key], (list, tuple, dict)) and _last_group == "data"
            ):  # add the meta data
                _key.attrs[key] = Dict[key]

            #### instrument
            # TODO
            if (
                isinstance(Dict[key], (list, tuple, dict))
                and key == "instrument"
                and _last_group != "pipeline"
            ):  # check if instrument
                return self.nested_dict(Dict[key], "instrument")

            # inside the instrument dict

            elif (
                isinstance(Dict[key], (list, tuple, dict))
                and _last_group == "instrument"
            ):
                key = Instrument(key)  # create instrument class
                self.nested_dict(Dict, "data", _key=key)  # check for meta data
                key.add(
                    [self.nested_dict(Dict[key], _last_group="")]
                )  # add instruments
                return key

            # meta data

            elif (
                not isinstance(Dict[key], (list, tuple, dict)) and _last_group == "data"
            ):  # add the meta data
                _key.attrs[key] = Dict[key]

            #### pipeline
            # TODO
            if (
                isinstance(Dict[key], (list, tuple, dict)) and key == "pipeline"
            ):  # check if pipeline
                return self.nested_dict(Dict[key], "pipeline", _nested_group=None)

            # inside the pipeline dict

            # check for nested groups
            elif (
                isinstance(Dict[key], (list, tuple, dict))
                and _last_group == "pipeline"
                and key != "instrument"
                and key != "data"
                and key != "model"
                and key != "parameters"
            ):
                if _nested_group == None:
                    return self.nested_dict(Dict[key], "pipeline", _nested_group=key)
                elif _nested_group != None:
                    return self.nested_dict(
                        Dict[key], "pipeline", _nested_group=_nested_group + "/" + key
                    )  # measured/capa1/raw

            # create the pipeline with nested name

            elif (
                isinstance(Dict[key], (list, tuple, dict)) and _last_group == "pipeline"
            ):
                _nested_group = Pipeline(_nested_group)  # create instrument class
                self.nested_dict(
                    Dict, "data", _key=_nested_group
                )  # check for meta data
                _nested_group.add(
                    [self.nested_dict(Dict, _last_group="")]
                )  # last group has to be != none   # add instruments
                return _nested_group

            # meta data

            elif (
                not isinstance(Dict[key], (list, tuple, dict)) and _last_group == "data"
            ):  # add the meta data
                _key.attrs[key] = Dict[key]

    # ------------------------------------------------------------------------------------------------------------------------------#

    if __name__ == "__main__":
        # TODO
        Dict = {
            "Run_01": {  # first folder is always the run folder
                "Parameter": {
                    "name": "mstm",  # meta data like this
                    "kkn_class": "PARAMETER",
                    "gain": {
                        "value": 0,
                        "unit": "-",
                    },
                    "offset": {
                        "value": 1,
                        "unit": "-",
                    },
                },
                "pipeline": {
                    "computed": {
                        "data": {
                            "attributes": [123, 456],
                            "name": "data",
                            "framerate": 1000,
                            "2000": np.ones((1, 10**4)),
                            "2100": np.ones((1, 10**4)),
                        }
                    },
                },
            },
        }
