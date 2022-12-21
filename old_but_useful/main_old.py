"""
Main file.
import the geometry from a shape file (.shp), read it (and create a geometry for Ladybug/Honeybee)
"""
import os
import json
from getpass import getuser

####  Get user  ####

elie='elie-medioni'
path_folder_elie="D://Elie//PhD//Simulation"
path_LBT_elie = "C://Users//elie-medioni//ladybug_tools//resources//standards//honeybee_standards"

abraham=''
path_folder_abraham=None
path_LBT_abraham = None

user = getuser()

####  Manual Inputs  ####

epw = "ISR_Tel_Aviv_1999.epw"
gis = "Tel_Aviv_center"
unit_gis = "m"
target_buildings = [1]

####  Inputs  ####
if user==elie:
    path_LBT_user_defined = path_LBT_elie
    path_folder = path_folder_elie
elif user==abraham:
    path_LBT_user_defined = path_LBT_abraham
    path_folder = path_folder_abraham
else:
    print("The user is not defined")


path_folder_typology = os.path.join(path_folder,"Input_Data","Typologies")
path_folder_construction_and_load_library = os.path.join(path_folder,"Input_Data","Constructions_and_Loads")
## GIS
path_file_gis = os.path.join(path_folder,"Input_Data","GIS",gis)
## EPW
path_file_epw = os.path.join(path_folder,"Input_Data","EPW",epw)
## Simulation parameters
path_folder_simulation_parameter = os.path.join(path_folder,"Input_Data","Simulation_parameters","test")
path_simulation_parameter = os.path.join(path_folder_simulation_parameter,"simulation_parameter.json")
## Simulation
path_folder_simulation = os.path.join(path_folder,"Simulation")
path_folder_context_hbjson = os.path.join(path_folder_simulation,"Context")
path_folder_building_simulation = os.path.join(path_folder_simulation,"Simulation","Buildings")





# # # # # # # # # # # # # # # #           Load Typology             # # # # # # # # # # # # # # # # # # # # #


from typology.typology import Typology

## load typology HB constructions etc... , critical to be before importing honeybee-energy

Typology.load_typologies_HBjson_sets(path_construction_and_load_library_folder=path_folder_construction_and_load_library,
                                     path_LBT_user_defined                    =path_LBT_user_defined)

from urban_canopy_44 import Urban_canopy

from honeybee.model import Model
from honeybee.room import Room

from honeybee_energy import run

import honeybee_energy
import honeybee


# # # # # # # # # # # # # # # #           Initialization             # # # # # # # # # # # # # # # # # # # # #


### read a txt file with the information (for instance whose computer is used)

### extract which buildings to simulate
# target_buildings = [3+i for i in range(32-3)]
# target_buildings = [27,31,51,55,101,106]
# target_buildings = [27,31,33,37,50,75,101]


### extract simulation parameters

# GIS files



# Constructions
# forced_construction = '2013::ClimateZone6::SteelFramed'
forced_construction = '2004::ClimateZone1::SteelFramed_2'
forced_construction = honeybee_energy.lib.constructionsets.construction_set_by_identifier(forced_construction)


forced_program_apartments = "2013::HighriseApartment::Apartment"
forced_program_apartments = honeybee_energy.lib.programtypes.program_type_by_identifier(forced_program_apartments)

forced_program_cores = '2013::HighriseApartment::Corridor'
forced_program_cores = honeybee_energy.lib.programtypes.program_type_by_identifier(forced_program_cores)


# windows =honeybee_energy.lib.constructions.window_construction_by_identifier("zob")
# print(windows)
# print(honeybee_energy.lib.materials.window_material_by_identifier("ShadeMaterial_2715f3de"))


####  Extract the geometry  ####

## Create Urban Canopy
U_c = Urban_canopy("random_neighborhood")

## Load Typologies in the Urban canopy object
U_c.load_typologies(path_folder_typology)

## Extract data from GIS files

# U_c.extract_gis_2D(local_path+"GIS_files//New_Avraham_2//test.shp","m")
# U_c.extract_gis_2D("D://Elie//PhD//Programming//GIS//Tel_Aviv_Lev_Hiar//","deg")
# U_c.extract_gis_2D(local_path+"GIS_files//Israel2//buildings.shp","deg")
# U_c.extract_gis_2D(local_path+"GIS_files//Technion_Shai_Typo_2//Technion_Shai_Typo.shp","m")

U_c.extract_gis_2D(path_file_gis,"m")
print("GIS extracted")


## Define buildings to smulate
U_c.select_target_building(target_buildings)

## Create Ladybug geometries with GIS footprint
U_c.create_building_LB_geometry_footprint()
## Create HB room envellop with GIS footprint
U_c.create_building_HB_room_envelop()

####  Identify the building_zon to simulate and the context  ####

# identify the context of the target buildings with the filter context algorithm

# add the context buildings that are not target buildings to the simulation

# identify the context buildings of the simulated non-target buildings
# (separate between LWR and just EP context)


####  Load constructions etc...  ####



### force building_zon typology (until it's guessed automatically ###

U_c.building_dict[0].typology=U_c.typology_dict["train_40x4"]
U_c.building_dict[1].typology=U_c.typology_dict["train_40x4"]


# # # # # # # # # # # # # # # #           Context extraction             # # # # # # # # # # # # # # # # # # # # #

## Context to hbjson ##
path_folder_context_hbjson = os.path.join(path_folder,"Simulation//Context")
U_c.context_to_hbjson(path_folder_context_hbjson)



U_c.filter_context(0.1)



U_c.create_simulation_folder(path_folder_simulation)
U_c.context_surfaces_to_hbjson(path_folder_simulation)
U_c.GIS_context_individual_to_hbjson(path_folder_simulation)



####  Identify typology  ####

# U_c.force_typology("forced_test_1")

####  Create DF and HB model  ####



# convert to DF stories and buildings
U_c.create_DF_building_according_to_typology()



# convert to HB model
U_c.convert_DF_building_to_HB_models()
U_c.HB_solve_adjacencies()

## Force rotation on building_zon  # just for a better plot here

# U_c.building_dict[1].HB_model_force_rotation(10)

# U_c.building_dict[37].HB_model_force_rotation(-25)
# U_c.building_dict[27].HB_model_force_rotation(-25)
# U_c.building_dict[75].HB_model_force_rotation(155)
# U_c.building_dict[31].HB_model_force_rotation(155)
# U_c.building_dict[33].HB_model_force_rotation(155)
# U_c.building_dict[50].HB_model_force_rotation(155)
# U_c.building_dict[101].HB_model_force_rotation(155)


# create windows
U_c.assign_conditioned_zone()
U_c.HB_building_window_generation_floor_area_ratio()

# add shades
U_c.add_context_surfaces_to_HB_model()
# assign constructions, loads etc...
U_c.apply_buildings_characteristics()

# assign simulation parameters


print("Building modeled")

####  Context refinement  ####

#  refine the context surfaces with the second pass of the filter context algorithm
#  on the honeybee surfaces !

# assign the context surfaces with their material or reflectance
# (except for context surfaces that are not form simulated building_zon, opt for a standard reflectance)

####  Compute view factors  ####

# compute the important view factors

#### Export model ####
# path=folder_path_elie+"Building_modeling"
#
# U_c.building_dict[0].HB_model.to_hbjson("one_building",path)
#
#
# zob=Model.from_hbjson(path_folder_elie+"Building_modeling//one_building.hbjson")



#### Extract simulation parameters ####

U_c.simulation_parameters_from_json(path_folder_simulation_parameter)

HB_simulation_parameter_dic=honeybee_energy.simulation.parameter.SimulationParameter.to_dict(U_c.simulation_parameters)
# print(dic)

## Write full simulation parameter file
with open(path_simulation_parameter,"w") as json_file :
    json.dump(HB_simulation_parameter_dic,json_file)

## Convert simulation parameters to IDF ##




U_c.generate_IDF_from_HB_model(path_folder_building_simulation,path_simulation_parameter)





#### Useful checks ####


# check construction
# print(U_c.building_dict[0].HB_model.rooms[0].faces[0].properties.energy.construction)


# print(U_c.building_dict[3].HB_model.rooms[0].properties.energy.is_conditioned)

# print(U_c.building_dict[0].HB_model.rooms[-1].faces[-1].can_be_ground)

# orient = honeybee.orientation.angles_from_num_orient()
# print(orient)
# print(honeybee.orientation.face_orient_index(U_c.building_dict[0].HB_model.rooms[0].faces[1],orient))
# print(U_c.building_dict[0].HB_model.rooms[0].faces[1].normal)
#

# print(U_c.building_dict[0].HB_model.rooms[0].properties.energy.program_type)


# print(U_c.building_dict[0].HB_model.rooms[4].properties.energy.is_conditioned)


# print(test.rooms[1].faces[1].vertices)

# print(len(U_c.building_dict[34].footprint))
# # print(U_c.building_dict[0].footprint)
# print(U_c.building_dict[34].footprint)
# print(U_c.building_dict[0].height)
#
# print(U_c)


# ##  Create file with the footprint point in it
#
# with open("..\list_points_footprint.txt","w") as file_txt:
#
#     for i in range(U_c.num_of_buildings-1) :
#         file_txt.write(';'.join(str(point) for point in U_c.building_dict[i].footprint ))
#         file_txt.write("\n")
#
#     file_txt.write(';'.join(str(point) for point in U_c.building_dict[U_c.num_of_buildings-1].footprint))
#



##

# U_c.generate_IDF_str_simulation_parameter()
#
# U_c.generate_IDF_from_HB_model(path_folder_idf)