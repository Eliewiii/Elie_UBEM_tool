"""
Extract the GIS file and convert it into a hb model that can be read and plotted by Grasshopper.
"""

import os
import sys
import logging
import argparse
import json

# sys.path.append('D://Elie//PhD//Programming//Elie_UBEM_tool')
sys.path.append('D://Documents//PhD')


from urban_canopy_ubem_tool.urban_canopy import UrbanCanopy

# default paths if no input is given

# WORK
# default_path_gis = "D:\Elie\PhD\Simulation\Input_Data\GIS\gis_typo_id_extra_small"
# default_path_gis = "D:\Elie\PhD\Simulation\\Input_Data\GIS\Example_context_filter_medium"
# default_folder_gis_extraction = "D:\Elie\PhD\Simulation\sim_new_tool\gis_extraction"


# HOME
# default_path_gis="D:\Documents\Phd_23_02_12\Simulation\Input_Data\GIS\gis_typo_id_extra_small"
default_path_gis="D:\Documents\Phd_23_02_12\Simulation\Input_Data\GIS\gis_typo_id_small"
default_folder_gis_extraction = "D:\Documents\Phd_23_02_12\Simulation\sim_new_tool\gis_extraction"

default_unit = "m"


default_additional_gis_attribute_key_dict = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gis", help="path to gis file", nargs='?', default=default_path_gis)
    parser.add_argument("-f", "--folder", help="path to the simulation folder", nargs='?', default=default_folder_gis_extraction)
    parser.add_argument("-u", "--unit", help="value of arg3", nargs='?', default=default_unit)
    parser.add_argument("-d", "--dic", help="path to the additional key dictionary", nargs='?', default=default_additional_gis_attribute_key_dict)
    parser.add_argument("-m", "--mov", help="Boolean telling if building should be moved to the origin", nargs='?', default=False)

    args = parser.parse_args()

    # Input parameter that will be given by Grasshopper
    path_gis = args.gis
    unit = args.unit
    path_folder_gis_extraction = args.folder
    path_additional_gis_attribute_key_dict = args.dic
    move_buildings_to_origin = bool(args.mov)
    move_buildings_to_origin = True

    # Create or load the urban canopy object
    path_urban_canopy_pkl = os.path.join(path_folder_gis_extraction, "urban_canopy.pkl")
    if os.path.isfile(path_urban_canopy_pkl):
        urban_canopy = UrbanCanopy.from_pkl(path_urban_canopy_pkl)
        logging.info(f"An urban canopy already exist in the simulation folder, the input GIS will be added to it")
    else:
        urban_canopy = UrbanCanopy()
        logging.info(f"New urban canopy object was created")

    # Get the building_id_key_gis if it is given in the additional_gis_attribute_key_dict
    building_id_key_gis = "idbinyan" # default value
    additional_gis_attribute_key_dict = None
    # check if given in the additional_gis_attribute_key_dict
    if default_additional_gis_attribute_key_dict and os.path.isfile(path_additional_gis_attribute_key_dict):
        with open(path_additional_gis_attribute_key_dict, "r") as f:
            additional_gis_attribute_key_dict = json.load(f)
            if "building_id_key_gis" in additional_gis_attribute_key_dict:
                building_id_key_gis = additional_gis_attribute_key_dict["building_id_key_gis"]



    # Add the 2D GIS to the urban canopy
    urban_canopy.add_2d_gis(path_gis, building_id_key_gis, unit, additional_gis_attribute_key_dict)
    logging.info(f"Builing geometries extracted from the GIS file successfully")
    # Move the buildings to the origin if asked
    if move_buildings_to_origin:
        urban_canopy.move_buildings_to_origin()
    # generate the hb model that contains all the building envelopes to plot in Grasshopper
    urban_canopy.make_building_envelop_hb_model(path_folder=path_folder_gis_extraction)
    logging.info(f"HB model for the building envelop created successfully")
    # save the urban canopy object in a pickle file in the temp folder
    urban_canopy.to_pkl(path_folder=path_folder_gis_extraction)
    logging.info(f"Urban canopy object saved successfully")