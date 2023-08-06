from pykkn.parameter import Parameter


def build_multi_parameters(dic: dict) -> list:
    """use this function to build multi-paremeter instances with a dictionary

    Parameter
    ---------
    dic : dict
        dic is a dictionary which contains a list of parameter
        their attributes as key value pairs

    Format of dic
    ------------
    {
        "list_of_parameters":[
            {
                "name":"name_of_parameter_1",
                "value":123
            },
            {
                "name":"name_of_parameter_2",
                "value":456
            },
            {
                "name":"name_of_parameter_3",
                "value":789
            },
        ]
    }

    a more detailed description of this parameter will be in our document.

    Example use
    -----------
    ls = build_multi_parameters(dic)
    """
    assert isinstance(dic, dict), "dic should be a dictionary type"
    assert (
        "list_of_parameters" in dic.keys()
    ), "the key to contain the list should be list_of_parameters"
    assert isinstance(
        dic["list_of_parameters"], list
    ), "the value of list_of_parameters should be a list"
    assert len(dic["list_of_parameters"]) > 0, "this list should not be empty"

    lop = dic["list_of_parameters"]

    result = []
    for sub_dic in lop:
        p = Parameter(sub_dic["name"])
        p.attrs["value"] = sub_dic["value"]
        result.append(p)

    return result
