# %% Load general libraries
import copy
import os.path
import sys
import logging
import copy

from tools._folder_manipulation import create_folder_output, move_input_files_to_output_folder
from tools._save_and_load_objects import save_urban_canopy_object_pickle,load_object_pickle

# %% Load inputs

from loads._paths import path_folder_typology, path_folder_construction_and_load_library, path_file_gis, path_file_epw, \
    path_folder_simulation_parameter, path_simulation_parameter, path_energyplus_exe, \
    path_folder_simulation, path_folder_context_hbjson, path_folder_building_simulation, path_logger, \
    path_LBT_user_defined, path_input_file
from loads._paths import unit_gis, target_buildings

# create the simulation folder and move the inputs to the output folder
create_folder_output(path_folder_simulation=path_folder_simulation)
move_input_files_to_output_folder(path_folder_simulation, path_EP_parameter_par=path_folder_simulation_parameter,
                                  path_sim_input_par=path_input_file,
                                  path_epw_par=None, path_gis_par=None)
# logging.basicConfig(filename=path_logger, format='%(asctime)s %(levelname)s %(message)s', filemode='w')
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[logging.FileHandler(path_logger), logging.StreamHandler(sys.stdout)])
# log #
logging.info("Input data extracted and simulation folder created")
#

# %% test

# print(path_folder_building_simulation)

# %% Load Typology

from library.library import Library

## load user defined object for the LBT, before importing the LBT (otherwise the objects will not be updated
Library.load_HBjson_sets(path_construction_and_load_library_folder=path_folder_construction_and_load_library,
                         path_LBT_user_defined=path_LBT_user_defined)
# log #
logging.info("Library imported")
#

# %% Load libraries

from urban_canopy_ubem.urban_canopy import Urban_canopy

# %% Initialize Urban Canopy object and load typology

## Create Urban Canopy
U_c = Urban_canopy("random_neighborhood")

## Load Typologies in the Urban canopy object
U_c.load_typologies(path_folder_typology)

# %% Extract GIS

## Extract data from GIS files
U_c.extract_gis_2D(path_file_gis, unit_gis)

# log #
logging.info("GIS extracted")
#


# %% Identify target buildings

## Define buildings to simulate
U_c.select_target_building(target_buildings)

# %% Generate building envelop

## Create Ladybug geometries with GIS footprint
U_c.create_building_LB_geometry_footprint()
U_c.create_building_HB_room_envelop()
##

path_folder_model = "D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\Tel_Aviv_MOE"
path_model_param_json = os.path.join(path_folder_model, "model_param.json")

path_temp_image_folder="D:\Elie\PhD\Simulation\Input_Data\Typology\\temp_identification"
U_c.identify_shapes_type_building_to_simulate(path_model_param_json, path_temp_image_folder, min_prob=98.)

from honeybee.model import Model

room_list_H = []
room_list_train = []
room_list_rectangle = []
room_list_default = []

for building_id in list(U_c.building_dict.keys()):
    building_obj= U_c.building_dict[building_id]
    print(building_obj.typology)
    room = building_obj.HB_room_envelop
    try:
        room.to_dict()
    except:
        print(f"building {building_id}'s geometry not ok, it is removed from the simulation")
    else:
        if building_obj.typology.identifier == "H":
            room_list_H.append(room)
        elif building_obj.typology.identifier == "Train":
            room_list_train.append(room)
        elif building_obj.typology.identifier == "Rectangle":
            room_list_rectangle.append(room)
        if building_obj.typology.identifier == "default":
            room_list_default.append(room)

path_folder_identified_shapes = "D:\Elie\PhD\Simulation\Input_Data\Typology\\identified_typo_json"

model_H = Model("h",rooms=room_list_H)
model_train = Model("train",rooms=room_list_train)
model_rectangle = Model("rectangle",rooms=room_list_rectangle)
model_default = Model("default",rooms=room_list_default)

model_H.to_hbjson(name="H", folder=path_folder_identified_shapes)
model_train.to_hbjson(name="train", folder=path_folder_identified_shapes)
model_rectangle.to_hbjson(name="rectangle", folder=path_folder_identified_shapes)
model_default.to_hbjson(name="default", folder=path_folder_identified_shapes)



