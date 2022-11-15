"""

"""

import pickle
from datetime import datetime
from os.path import join

from honeybee.model import Model
from honeybee.room import  Room

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


def save_urban_canopy_object_pickle(file_path, urban_canopy_obj):
    """ Save an object in a pickle file (mostly for debugging urban canopy and building object)"""
    for id in urban_canopy_obj.building_to_simulate:
        building_obj = urban_canopy_obj.building_dict[id]
        building_obj.HB_model_dict= Model.to_dict(building_obj.HB_model)
        building_obj.HB_model=None

        for key in building_obj.apartment_dict.keys():
            building_obj.apartment_dict[key].hb_room_dict = Room.to_dict(building_obj.apartment_dict[key].hb_room_obj)
            building_obj.apartment_dict[key].hb_room_obj=None

    with open(file_path, "wb") as pickle_file:
        pickle.dump(urban_canopy_obj,pickle_file)

    for id in urban_canopy_obj.building_to_simulate:
        building_obj = urban_canopy_obj.building_dict[id]
        building_obj.HB_model = Model.from_dict(building_obj.HB_model_dict)
        building_obj.HB_model_dict = None

        for key in building_obj.apartment_dict.keys():
            building_obj.apartment_dict[key].hb_room_obj = Room.from_dict(building_obj.apartment_dict[key].hb_room_dict)
            building_obj.apartment_dict[key].hb_room_dict=None


def load_urban_canopy_object_pickle(file_path):
    """ """

    urban_canopy_obj = None
    with open(file_path, "rb") as pickle_file:
        urban_canopy_obj = pickle.load(pickle_file)

    for id in urban_canopy_obj.building_to_simulate:
        building_obj = urban_canopy_obj.building_dict[id]
        building_obj.HB_model = Model.from_dict(building_obj.HB_model_dict)
        building_obj.HB_model_dict = None

        for key in building_obj.apartment_dict.keys():
            building_obj.apartment_dict[key].hb_room_obj = Room.from_dict(building_obj.apartment_dict[key].hb_room_dict)
            building_obj.apartment_dict[key].hb_room_dict=None

    return urban_canopy_obj




if __name__=="__main__":
    path_building_obj = "D:\Elie\PhD\Simulation\Program_output\Simulation_2222\\Urban_canopy\\uc_obj.p"
    original_building_obj = load_object_pickle(path_building_obj)
