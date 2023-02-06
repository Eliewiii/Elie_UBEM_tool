"""
Extract the GIS file and convert it into a hb model that can be read and plotted by Grasshopper.
"""

import os
import logging

from urban_canopy_ubem_tool.urban_canopy import UrbanCanopy

# Input parameter that will be given by Grasshopper (from a config file)
path_temp_file_gis_extraction = ""

# Input parameter that will be given by the user in Grasshopper
path_gis = "D:\Documents\Ale_project\Simulation\Input_Data\GIS\Example_context_filter_medium"

# Create or load the urban canopy object
# urban_canopy = UrbanCanopy()

# Add the 2D GIS to the urban canopy

# generate the hb model

# save the hb model in a hbjson file in the temp folder

# save the urban canopy object in a pickle file in the temp folder
