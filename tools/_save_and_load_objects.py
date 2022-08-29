"""

"""

import pickle
from datetime import datetime
from os.path import join

def save_object_pickle(file_path, obj):
    """ Save an object in a pickle file (mostly for bebugging urban canopy and building object)"""
    with open(file_path, "wb") as pickle_file:
        pickle.dump(obj,pickle_file)


def load_object_pickle(file_path):
    """ Save an object in a pickle file (mostly for bebugging urban canopy and building object)"""
    obj=None
    with open(file_path, "rb") as pickle_file:
        obj=pickle.load(pickle_file)
    return obj

def save_sample_object_pickle(file_path, obj):
    """ Save an object in a pickle file (mostly for bebugging urban canopy and building object)"""
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_")  # get the date

    with open(file_path+"_"+dt_string, "wb") as pickle_file:
        pickle.dump(obj,pickle_file)

if __name__=="__main__":
    path_building_obj = "D:\Elie\PhD\Simulation\Program_output\Simulation_2222\\Urban_canopy\\uc_obj.p"
    original_building_obj = load_object_pickle(path_building_obj)
