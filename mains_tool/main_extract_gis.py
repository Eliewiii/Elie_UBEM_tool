"""
Extract the GIS file and convert it into a hb model that can be read and plotted by Grasshopper.
"""

import os
import logging

from urban_canopy_ubem_tool.urban_canopy import UrbanCanopy

# Input parameter that will be given by Grasshopper (from a config file)
path_folder_gis_extraction = ""

# Input parameter that will be given by the user in Grasshopper
path_gis = "D:\Documents\Ale_project\Simulation\Input_Data\GIS\Example_context_filter_medium"

# Create or load the urban canopy object
path_urban_canopy_pkl = os.path.join(path_folder_gis_extraction, "urban_canopy.pkl")
if os.path.isfile(path_urban_canopy_pkl):
    urban_canopy = UrbanCanopy.load_pkl(path_urban_canopy_pkl)
    logging.info(f"An urban canopy already exist in the simulation folder, the input GIS will be added to it")
else:
    urban_canopy = UrbanCanopy()
    logging.info(f"New urban canopy object was created")


# Add the 2D GIS to the urban canopy
urban_canopy.add_2d_gis(path_gis, building_id_key_gis="idbinyan", unit="m", additional_gis_attribute_key_dict=None)
logging.info(f"A new urban canopy object was created")
# generate the hb model that contains all the building envelopes to plot in Grasshopper
urban_canopy.make_building_envelop_hb_model(path_folder=path_folder_gis_extraction)
logging.info(f"HB model for the building envelop created successfully")
# save the urban canopy object in a pickle file in the temp folder
urban_canopy.to_pkl(path_folder=path_folder_gis_extraction)
logging.info(f"Urban canopy object saved successfully")