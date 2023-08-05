"""
Part of ezsaver package
https://github.com/EricThomson/ezsaver
"""

import pathlib
from pathlib import Path
import joblib
from varname import argname

def get_var_names(*variables):
    """
    return variable names
    """
    var_names = []
    for var_ind in range(len(variables)):
        var_name = argname(f"variables[{var_ind}]")
        var_names.append(var_name)
    return var_names

def save(filepath, *variables_to_save):
    """
    enter filepath, variables to save (as many as you want),
    and it will save them to the file as a binary pickle.

    Currently only works with full filepath, as it checks to see if parent directory exists. Should change this probably.
    """
    # If filepath is not pathlib, create pathlib
    if not isinstance(filepath, pathlib.PurePath):
        filepath = Path(filepath)
        #raise TypeError(f"filepath must be pathlib object not {type(filepath)}")

    # check to see if directory exists. If not, throw error.
    if not filepath.parent.exists():
        raise FileNotFoundError(f"Parent directory doesn't exist: {filepath.parent}")

    # Create dict containing same variable names as strings
    data_dict = {}
    var_names = []
    var_vals = []
    for var_ind, var_val in enumerate(variables_to_save):
        var_name = argname(f"variables_to_save[{var_ind}]")
        data_dict[var_name] = var_val

    # save dict
    with open(filepath, 'wb') as f:
        joblib.dump(data_dict, f)

    return filepath


def load(filepath):
    """
    simple interface to load file saved using ez_save function.
    Technically, it will load any binary file given in filepath using joblib.

    would probably be good to check to see if it is ez_save format :/
    """
    # load the file in filepath
    with open(filepath, 'rb') as f:
        data_dict = joblib.load(f)

    return data_dict


if __name__ == '__main__':
    """
    test var names
    """
    print("\nezsaver: testing get_var_names()...")
    var1 = 'hi'
    var2 = 2
    var_names = get_var_names(var1, var2)
    print(f"Var names for var1, var2: {var_names}")

    """
    test save
    """
    print("\nezsaver: testing save()...")
    import numpy as np
    data1 = 2
    data2 = np.random.random(size=(2,3))
    print("Data being saved:")
    print(f"data1: {data1}")
    print(f"data2:\n{data2}")
    fpath = fpath = r'../workspace/test.pkl'
    saved_path = save(fpath, data1, data2)
    print(f"Save path:\n:{saved_path}")

    """
    test load
    """
    print("\nezsaver: testing load()...")
    load(fpath)
    dict_loaded = load(fpath)
    data1_loaded = dict_loaded['data1']
    data2_loaded = dict_loaded['data2']
    print(f"Data loaded:\n{data1_loaded}\n{data2_loaded}")


    print("\nDone testing ezsave")
