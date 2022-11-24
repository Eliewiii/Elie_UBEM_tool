# %% Load general libraries
import os.path
import sys
import logging

from tools._folder_manipulation import create_folder_output, move_input_files_to_output_folder
from tools._save_and_load_objects import save_object_pickle

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

from library import Library

## load user defined object for the LBT, before importing the LBT (otherwise the objects will not be updated
Library.load_HBjson_sets(path_construction_and_load_library_folder=path_folder_construction_and_load_library,
                         path_LBT_user_defined=path_LBT_user_defined)
# log #
logging.info("Library imported")
#

# %% Load libraries

from urban_canopy_ubem.urban_canopy import Urban_canopy

# %% Initialize Urban Canopy object and load typologies

## Create Urban Canopy
U_c = Urban_canopy("random_neighborhood")

## Load Typologies in the Urban canopy object
U_c.load_typologies(path_folder_typology)

# %% Extract GIS

## Extract data from GIS files

## todo : extract this list from a text file
# list_constructionsets_id = []
# #const_set_list_path = "D:\\Pycharm\\Task\\Simulation\\Input_Data\\Constructions_and_Loads\\constructionsets" # Tiantian
# const_set_list_path = "D:\Elie\PhD\Simulation\Input_Data\Typology\list_constructionsets\partial_list"   # Elie
#
#
# file_list = os.listdir(const_set_list_path)
# suffix = '.txt'
# for txt_file in file_list:
#     if txt_file.endswith(suffix):
#         path_txt = os.path.join(const_set_list_path, txt_file)
#         break
# with open(path_txt, 'r') as f:
#     for line in f:
#         list_constructionsets_id.append(line.strip())
## list_constructionsets_id = ["IS_5280_ReferenceConstSet_A","FR_BER_LCA_A_R0-W1-G0","FR_BER_LCA_A_R0-W2-G0","FR_BER_LCA_A_R1-W0-G0"] # to extract from file

## inputs f
# path_folder_configuration_to_test = "D:\Elie\PhD\Simulation\Input_Data\LCA\Configuration_to_test\LCA_BER_project"  # Elie
path_folder_configuration_to_test = "D:\Elie\PhD\Simulation\Input_Data\LCA\Configuration_to_test\LCA_BER_project_test"  # Elie test
# path_folder_configuration_to_test = "D:\Pycharm\Task\Simulation\Input_Data\LCA\Configuration_to_test\LCA_BER_project_test" # Tiantian test
# path_folder_configuration_to_test = "D:\Pycharm\PyCharm 2022.2.3\Task\Simulation\Input_Data\LCA\Configuration_to_test\LCA_BER_project_test"  #Tiantian new laptop test
file_list = os.listdir(path_folder_configuration_to_test)
for in_file in file_list:
    if in_file.endswith(".csv"):
        name_csv_configuration_to_test = in_file[:-4]
        break

from lca_constuction_material.list_configuration_to_test import configuation_to_test_csv_to_json

configuration_dic = configuation_to_test_csv_to_json(path_folder_configuration_to_test,name_csv_configuration_to_test)

#list with all the name of each configuration
list_name_configuation_to_test = list(configuration_dic.keys())



U_c.vary_construction_set_from_one_building_gis(path_file_gis, unit_gis,
                                                list_variation_id=list_name_configuation_to_test)

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

# %% Context filter algorithm

# filter context and identify the buildings to simulate

# %% test

# print(len(U_c.building_dict[0].context_buildings_id))

# %% Force Typology

U_c.force_typology("train_40x4_Z_A")
# U_c.force_default_typology()

# %% Force Typology

# print(U_c.building_dict[0].num_floor)

# %% DF + HB modeling using GIS data + typology

# convert to DF stories and buildings
U_c.create_DF_building_according_to_typology()
# convert to HB model
U_c.generate_HB_model()
# U_c.convert_DF_building_to_HB_models()
U_c.HB_solve_adjacencies()

# %% DF + HB modeling using GIS data + typology

## Force rotation on building
# need to guess it and rotate it at the beginning

# U_c.building_dict[45].HB_model_force_rotation(80)  ################  TO MODIFY

# %% DF + HB modeling using GIS data + typology


U_c.assign_conditioned_zone()
# add Ideal HVAC system
U_c.assign_ideal_hvac_system(climate_zone="A", hvac_paramater_set="team_design_builder")

# create windows
U_c.HB_building_window_generation_floor_area_ratio()


# add shades
U_c.add_context_surfaces_to_HB_model()
# assign constructions, loads etc...
U_c.apply_buildings_characteristics()
# Add infiltration in volume per hour
U_c.add_infiltration_air_exchange(air_exchange_rate=1.)

# add blinds

# add thermal mass
U_c.add_thermal_mass_int_wall()

# change the constructionsets
U_c.change_hb_constr_set_according_to_variation_to_simulate(dic_configuration_to_test=configuration_dic)
# U_c.hb_change_construction_set_according_to_name(list_constructionsets_id=list_constructionsets_id)



# log #
logging.info("Building modeled")
#

# save_object_pickle(os.path.join("D:\Elie\PhD\Simulation\Input_Data\Sample_objects\Tiantian\Sample_building_LCA_project",
#                                 "Building_LCA_z_A.p"),
#                    U_c.building_dict[0])
# save_object_pickle(os.path.join("D:\Elie\PhD\Simulation\Input_Data\Sample_objects\Tiantian\Sample_building_LCA_project",
#                                 "Uc_LCA_z_A.p"),
#                    U_c)

# %% test

# print(U_c.building_dict[0].HB_model.rooms[0].properties.energy.program_type)
# print(U_c.building_dict[0].HB_model.rooms[0].properties.energy.internal_masses[0].construction)

# %% Clean/create simulation folder

U_c.create_simulation_folder_buildings(path_folder_building_simulation)

# %% Generate json to plot context
# All the buildings that are target buildings

# U_c.GIS_context_individual_to_hbjson(path_folder_building_simulation)

# %% Extract simulation parameters
## Merge simulation parameters files
U_c.load_simulation_parameter(path_folder_simulation_parameter, path_simulation_parameter)
## Add design days
U_c.add_design_days_to_simulation_parameters(path_simulation_parameter, path_file_epw)

# %% Generate HB models
U_c.model_to_HBjson(path_folder_building_simulation)

# %% Save urban_canopy object in a pickle file

# U_c.generate_local_epw_with_uwg(path_epw="D:\Elie\PhD\Simulation\Input_Data\EPW\IS_5280_A_Haifa.epw",
#                                     path_folder_epw_uwg="D:\Elie\PhD\\test")


# %% Generate IDF and simulate the building
U_c.simulate_idf(path_folder_building_simulation, path_simulation_parameter, path_file_epw, path_energyplus_exe)
# U_c.simulate_idf(path_folder_building_simulation, path_simulation_parameter, "D:\Elie\PhD\\test\\random_neighborhood_uwg.epw", path_energyplus_exe)

# %% Extract and print results

U_c.extract_building_csv_results(path_folder_building_simulation)
# U_c.print_detailed_results_BER(apartment_details=True)


## LCA
from lca_constuction_material.lca_surface_type import LcaMatColBySurfType

path_lca_database = "D:\Elie\PhD\Simulation\Input_Data\LCA\LCA_database\LCA_BER_project"  ##Elie
# path_lca_database = "D:\Pycharm\Task\Simulation\Input_Data\LCA\LCA_database\LCA_BER_project"  ##Tiantian
# path_lca_database = "D:\Pycharm\PyCharm 2022.2.3\Task\Simulation\Input_Data\LCA\LCA_database\LCA_BER_project"  ##Tiantian new

# Life time
life_time=50

lca_dict = LcaMatColBySurfType.extract_lca_database(path_folder_database=path_lca_database,life_duration=life_time)

U_c.compute_lca(dic_configuration_to_test=configuration_dic,lca_dic=lca_dict)

conversion_rate=1/0.5565
U_c.convert_carbon_footprint_kwh_per_m2_eq_compare_to_ref(conversion_rate=conversion_rate,life_time=life_time)
U_c.compute_consumption_improvement_lca()


# create a global csv file in the output folder names "results" and write into the results
path_folder_building_results = os.path.join(path_folder_simulation, "Results")
csv_name = "Results.csv"
path_csv = os.path.join(path_folder_building_results, csv_name)


U_c.write_global_csv_results_with_lca(path_csv)


# %% Generate csv results in each building object
tot_h_cop_compared_to_ref = U_c.write_csv_results_in_building_folder(path_folder_building_simulation)

###Test heating data temprary
print(tot_h_cop_compared_to_ref)
###

# generate the graph
#U_c.generate_graph_result(path_folder_building_results)
# %% test


# print(U_c.building_dict[0].HB_model.rooms[0].identifier)
# print(U_c.building_dict[0].HB_model.rooms[0].properties.energy.infiltration) #test infiltration

















