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
## Create HB room envelop with GIS footprint
U_c.create_building_HB_room_envelop()
U_c.correct_envelop_elevation()
U_c.create_building_HB_room_bounding_box()
U_c.correct_bounding_box_elevation()

# %% Context filter algorithm

# filter context and identify the buildings to simulate
# U_c.filter_context_new(VF_criterion_shading) # previous version
U_c.filter_context_bounding_box(mvfc=0.005)

U_c.correct_context_elevation()  # todo

logging.warning("context filtered")

# %% test

# print(len(U_c.building_dict[0].context_buildings_id))

# %% Force Typology

# U_c.building_dict[0].typology = U_c.typology_dict["train_40x4_Z_A"] # apply a specific typology to a specific building
U_c.building_dict[0].typology = U_c.typology_dict["H_moe"] # apply a specific typology to a specific building
# U_c.force_default_typology()
logging.warning("typology applied")

# %% DF + HB modeling using GIS data + typology

# convert to DF stories and buildings
U_c.create_DF_building_according_to_typology()
# convert to HB model
U_c.generate_HB_model()
# U_c.convert_DF_building_to_HB_models()
U_c.HB_solve_adjacencies()

## Force rotation on building  (if necessary)

# U_c.building_dict[45].HB_model_force_rotation(80)  ################  TO MODIFY

# HB modeling using GIS data + typology


U_c.assign_conditioned_zone()
# add Ideal HVAC system
U_c.assign_ideal_hvac_system(climate_zone="A", hvac_paramater_set="team_design_builder")

# create windows
U_c.HB_building_window_generation_floor_area_ratio()

# U_c.building_dict[45].HB_model_force_rotation(80)  ################  TO MODIFY


# add shades
U_c.add_context_surfaces_to_HB_model()
# assign constructions, loads etc...
U_c.apply_buildings_characteristics()
# Add infiltration in volume per hour
U_c.add_infiltration_air_exchange(air_exchange_rate=1.)

# add blinds

# add thermal mass
U_c.add_thermal_mass_int_wall()

# log #
logging.info("Building modeled")

# Clean/create simulation folder
U_c.create_simulation_folder_buildings(path_folder_building_simulation)

# Generate json to plot context
# All the buildings that are target buildings
U_c.context_to_hbjson(path_folder_context_hbjson)
U_c.context_surfaces_to_hbjson(path_folder_building_simulation)
# U_c.GIS_context_individual_to_hbjson(path_folder_building_simulation)

# Extract simulation parameters
## Merge simulation parameters files
U_c.load_simulation_parameter(path_folder_simulation_parameter, path_simulation_parameter)
## Add design days
U_c.add_design_days_to_simulation_parameters(path_simulation_parameter, path_file_epw)

# %% Generate HB models
U_c.model_to_HBjson(path_folder_building_simulation)

# Generate local EPW
# U_c.generate_local_epw_with_uwg(path_epw="D:\Elie\PhD\Simulation\Input_Data\EPW\IS_5280_A_Haifa.epw",
#                                     path_folder_epw_uwg="D:\Elie\PhD\\test")


# Save objects   todo: put the new function that bypass the "locked class" issue
# save_object_pickle(os.path.join(path_folder_simulation, "Urban_canopy", "uc_obj_2.p"), U_c)


# %% Generate IDF and simulate the building
U_c.simulate_idf(path_folder_building_simulation, path_simulation_parameter, path_file_epw, path_energyplus_exe)
# U_c.simulate_idf(path_folder_building_simulation, path_simulation_parameter, "D:\Elie\PhD\\test\\random_neighborhood_uwg.epw", path_energyplus_exe)



# %% Extract and print results

U_c.extract_building_csv_results(path_folder_building_simulation)

# Save objects todo: update with the new function
# save_urban_canopy_object_pickle(os.path.join(path_folder_simulation, "Urban_canopy", "uc_obj.p"), U_c)

# U_c.print_detailed_results_BER(apartment_details=True)

# path for csv results
path_folder_building_results = os.path.join(path_folder_simulation, "Results")
csv_name = "Results.csv"
path_csv = os.path.join(path_folder_building_results, csv_name)
# Global results
U_c.write_global_csv_results_with_lca(path_csv)
# Individual results of buildings
U_c.write_csv_results_in_building_folder(path_folder_building_simulation)


# print(U_c.building_dict[0].HB_model.rooms[0].identifier)
# print(U_c.building_dict[0].HB_model.rooms[0].properties.energy.infiltration) #test infiltration
