"""
Generate the paths necessary to collect the data and write the output
"""

import os
import json

from getpass import getuser
from datetime import datetime
from loads._load_inputs import load_input_parameter


####  Get user  ####
# # Elie
elie = 'elie-medioni'
# path_folder_elie="D://Elie//PhD//Simulation"
path_folder_elie = "D://Elie//PhD//Simulation"
# path_LBT_elie = "C://Users//elie-medioni//ladybug_tools//resources//standards//honeybee_standards"
path_LBT_elie = "C://Users//elie-medioni//AppData//Roaming//ladybug_tools//standards"
# # Abraham
abraham = ''
path_folder_abraham = None
path_LBT_abraham = None
# # Tiantian
tiantian = 'elie-medioni'
# path_folder_elie="D://Elie//PhD//Simulation"
path_folder_tiantian = "D://Elie//PhD//Simulation"
# path_LBT_elie = "C://Users//elie-medioni//ladybug_tools//resources//standards//honeybee_standards"
path_LBT_tiantian = "C://Users//elie-medioni//AppData//Roaming//ladybug_tools//standards"


user = getuser()

if user == elie:
    path_LBT_user_defined = path_LBT_elie
    path_folder = path_folder_elie
elif user == abraham:
    path_LBT_user_defined = path_LBT_abraham
    path_folder = path_folder_abraham
else:
    print("The user is not defined")

#### Extract Input file ####
## Path of the input file
path_input_file = os.path.join(path_folder, "Input_Data", "inputs.json")
epw, gis, unit_gis, target_buildings, VF_criterion_shading = load_input_parameter(path_input_file)

#### Prepare paths ####
path_folder_typology = os.path.join(path_folder, "Input_Data", "Typology", "Typologies")
path_folder_construction_and_load_library = os.path.join(path_folder, "Input_Data", "Constructions_and_Loads")
## GIS
path_file_gis = os.path.join(path_folder, "Input_Data", "GIS", gis)
## EPW
path_file_epw = os.path.join(path_folder, "Input_Data", "EPW", epw)
## Simulation parameters
path_folder_simulation_parameter = os.path.join(path_folder, "Input_Data", "Simulation_parameters", "annual_results")
path_simulation_parameter = os.path.join(path_folder_simulation_parameter, "simulation_parameter.json")
## folder outputs
path_folder_output = os.path.join(path_folder, "Program_output", )
## EnergyPlus
path_energyplus_exe = "C:\EnergyPlusV22-1-0\energyplus.exe"

## name of the simulation
now = datetime.now()
dt_string = now.strftime("%Y_%m_%d_%Hh_%Mm_%Ss")  # get the date and time to get an unique identifier

simulation_name = ""
manual_input = input("Type an additional string for the name of the simulation: ")
if manual_input != "":
    simulation_id = "Simulation_" + simulation_name + manual_input
    if simulation_id in os.listdir(path_folder_output):
        simulation_id = "Simulation_" + simulation_name + "_" + manual_input + "_" + dt_string
else:
    simulation_id = "Simulation_" + simulation_name + "_" + manual_input + "_" + dt_string

## Path simulation folders
path_folder_simulation = os.path.join(path_folder_output, simulation_id)
path_folder_context_hbjson = os.path.join(path_folder_simulation, "Context")
path_folder_building_simulation = os.path.join(path_folder_simulation, "Buildings")
path_logger = os.path.join(path_folder_simulation, "debug.log")
