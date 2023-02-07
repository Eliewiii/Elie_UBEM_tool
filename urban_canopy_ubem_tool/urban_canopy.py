"""
Urban canopy class, containing and managing collections of buildings in urban areas.
"""

import os
import logging

from honeybee.model import Model

from building_ubem_tool.building import Building
from gis.extract_gis import extract_gis

class UrbanCanopy:


    def __init__(self):
        """Initialize the Urban Canopy"""
        # process the boundary and plane inputs
        self.building_dict = {}
        self.target_buildings = []
        self.building_to_simulate = []
        self.typology_dict = {}


    def __str__(self):
        """ what you see when you print the urban canopy object """
        return (f"The urban canopy is composed of {self.num_of_buildings} buildings")

    def __repr__(self):
        """ what you see when you type the urban canopy variable in the console """
        return (f"The urban canopy is composed of {self.num_of_buildings} buildings")

    def add_list_of_buildings(self, building_id_list, building_obj_list):
        """ Add a list of buildings to the urban canopy"""
        for i,building_id in enumerate(building_id_list):
            building_obj = building_obj_list[i]
            # check if the building id is already in the urban canopy
            if building_id in self.building_dict.keys():
                logging.warning(f"The building id {building_id} is already in the urban canopy, it will not"
                                f" be added again to the urban canopy")
            else:
                # add the building to the urban canopy
                self.building_dict[building_id] = building_obj




    def add_2d_gis(self, path_gis, building_id_key_gis= "idbinyan", unit = "m", additional_gis_attribute_key_dict = None):
        """ exctract the data from a shp file and create the associated buildings objects"""
        # Read GIS file
        shape_file = extract_gis(path_gis)
        ## loop to create a building_obj for each footprint in the shp file
        number_of_buildings_in_shp_file = len(shape_file['geometry']) # number of buildings in the shp file
        for building_id_shp in range(0, number_of_buildings_in_shp_file):
            # create the building object
            building_id_list, building_obj_list = Building.from_shp_file(shape_file, building_id_shp, unit, building_id_key_gis)
            # add the building to the urban canopy if it is valid
            if building_obj_list is not None:
                self.add_list_of_buildings(building_id_list, building_obj_list)

        # Collect the attributes to the buildings from the shp file
        for building in self.building_dict.values():
            building.collect_attributes_from_shp_file(shape_file, additional_gis_attribute_key_dict)


    def make_building_envelop_hb_model(self):
        """ Make the hb model for the building envelop """
        # List of the hb rooms representing the building envelops
        hb_room_envelop_list =[building.to_elevated_hb_room_envelop() for building in self.building_dict.values()]
        # Make the hb model
        return Model(identifier="urban_canopy_building_envelops",rooms=hb_room_envelop_list)



