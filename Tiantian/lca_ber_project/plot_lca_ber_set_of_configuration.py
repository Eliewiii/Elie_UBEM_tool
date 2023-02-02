 # %% Load general libraries
import os.path
import sys
import logging

from tools._folder_manipulation import create_folder_output, move_input_files_to_output_folder
from tools._save_and_load_objects import load_urban_canopy_object_pickle

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


# path= "D:\Elie\PhD\Simulation\Input_Data\Sample_objects\Tiantian\\urban_canopy.pkl"  #Elie
path = "D:\Pycharm\PyCharm 2022.2.3\Task\Simulation\Input_Data\Sample_objects\Tiantian\\urban_canopy.pkl"  #Tiantian

U_c=load_urban_canopy_object_pickle(path)

# Create the sub folders in the simulation folder
U_c.create_simulation_folder_buildings(path_folder_building_simulation)

path_folder_building_results = os.path.join(path_folder_simulation, "Results")

# generate the graph
U_c.generate_graph_result(path_folder_building_results)
# %% test
