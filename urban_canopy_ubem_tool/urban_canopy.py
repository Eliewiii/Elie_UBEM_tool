"""
Urban canopy class, containing and managing collections of buildings in urban areas.
"""

import os
import logging
import pickle

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

    @classmethod
    def from_pkl(cls, path_pkl):
        """ Load the urban canopy from a pickle file """
        with open(path_pkl, 'rb') as f:
            urban_canopy = pickle.load(f)
        return urban_canopy

    def add_list_of_buildings(self, building_id_list, building_obj_list):
        """ Add a list of buildings to the urban canopy"""
        for i, building_id in enumerate(building_id_list):
            building_obj = building_obj_list[i]
            # check if the building id is already in the urban canopy
            if building_id in self.building_dict.keys():
                logging.warning(f"The building id {building_id} is already in the urban canopy, it will not"
                                f" be added again to the urban canopy")
            else:
                # add the building to the urban canopy
                self.building_dict[building_id] = building_obj

    def add_2d_gis(self, path_gis, building_id_key_gis="idbinyan", unit="m", additional_gis_attribute_key_dict=None):
        """ Extract the data from a shp file and create the associated buildings objects"""
        # Read GIS file
        shape_file = extract_gis(path_gis)
        # Check if the building_id_key_gis is an attribute in the shape file
        try:
            shape_file[building_id_key_gis]
        except KeyError:
            logging.error(
                f"The key {building_id_key_gis} is not an attribute of the shape file, the id will be generated automatically")
            raise
            # if the key is not valid, set it to None, and the building will automatically be assigned an id
            building_id_key_gis = None

        ## loop to create a building_obj for each footprint in the shp file
        number_of_buildings_in_shp_file = len(shape_file['geometry'])  # number of buildings in the shp file
        for building_id_shp in range(0, number_of_buildings_in_shp_file):
            # create the building object
            building_id_list, building_obj_list = Building.from_shp_file(self, shape_file, building_id_shp,
                                                                         building_id_key_gis,unit)
            # add the building to the urban canopy if it is valid
            if building_obj_list is not None:
                self.add_list_of_buildings(building_id_list, building_obj_list)

        # Collect the attributes to the buildings from the shp file
        for building in self.building_dict.values():
            building.collect_attributes_from_shp_file(shape_file, additional_gis_attribute_key_dict)

    def make_building_envelop_hb_model(self, path_folder=None):
        """ Make the hb model for the building envelop and save it to hbjson file if the path is provided """
        # List of the hb rooms representing the building envelops
        hb_room_envelop_list = [building.to_elevated_hb_room_envelop() for building in self.building_dict.values()]
        # additional cleaning of the colinear vertices, might not be necessary
        for room in hb_room_envelop_list:
            room.remove_colinear_vertices_envelope(tolerance=0.01, delete_degenerate=True)
        # Make the hb model
        hb_model = Model(identifier="urban_canopy_building_envelops", rooms=hb_room_envelop_list,tolerance=0.01)
        hb_dict =hb_model.to_dict()
        if path_folder is not None:
            hb_model.to_hbjson(name="buildings_envelops", folder=path_folder)
        return hb_dict,hb_model

    def to_pkl(self, path_folder):
        """ Save the urban canopy to a pickle file """
        with open(os.path.join(path_folder, "urban_canopy.pkl"), 'wb') as f:
            pickle.dump(self, f)
