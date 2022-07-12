"""

"""

import pickle
from datetime import datetime
from os.path import join

def save_object_pickle(file_path, obj):
    """ Save an object in a pickle file (mostly for bebugging urban canopy and building object)"""
    pickle.dump(obj, open(file_path, "wb"))


def load_object_pickle(file_path):
    """ Save an object in a pickle file (mostly for bebugging urban canopy and building object)"""
    return pickle.load(open(file_path, "rb"))

def save_sample_object_pickle(file_path, obj):
    """ Save an object in a pickle file (mostly for bebugging urban canopy and building object)"""
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d_")  # get the date

    pickle.dump(obj, open(file_path+"_"+dt_string, "wb"))
