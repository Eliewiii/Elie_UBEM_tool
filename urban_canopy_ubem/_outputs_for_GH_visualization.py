"""
Additional methods for the Urban_canopy class.
Deals generate files (mostly .hbjson files) for visualization in Rhino with Grasshopper
"""

import os

from honeybee.model import Model
from ladybug_geometry.geometry3d.pointvector import Vector3D


class Mixin:

    def create_building_HB_room_envelop(self):
        """ create a honeybee room with extruded footprints of buildings, mostly for plotting purposes """
        for i, id in enumerate(self.building_dict):
            self.building_dict[id].LB_footprint_to_HB_room_envelop()

    def create_building_HB_room_bounding_box(self):
        """ create a honeybee room with extruded footprints of buildings, mostly for plotting purposes """
        for i, id in enumerate(self.building_dict):
            self.building_dict[id].generate_oriented_bounding_box()

    def correct_envelop_elevation(self):
        """ correct the elevation of the building envelop (not to put it at z=0) """
        for i, id in enumerate(self.building_dict):
            self.building_dict[id].correct_envelop_elevation()

    def correct_bounding_box_elevation(self):
        """ correct the elevation of the building envelop (not to put it at z=0) """
        for i, id in enumerate(self.building_dict):
            self.building_dict[id].correct_bounding_box_elevation()

    def context_to_hbjson(self, path_folder_context_hbjson):
        """
        Generate a hbjson file to plot the context in Rhinoceros
        The hbjson is a HB model.
        Each room of the model represent one building_zon.
        Rooms are generated with the building_zon envelop = LB polyface3D
        """

        room_list = []  # list of the rooms

        for id in range(self.num_of_buildings):
            # plot only the buildings that are not simulated/modeled = the rest of the GIS for now
            if id not in self.building_to_simulate:
                room_list.append(self.building_dict[id].HB_room_envelop)

        model = Model(identifier="context", rooms=room_list)

        # generate model
        model.to_hbjson(name="context", folder=path_folder_context_hbjson)

    def context_surfaces_to_hbjson(self, path_folder_simulation):
        """
        Write the context surfaces of each building_zon in a hbjson file in the building_zon directory
        """
        for building_id in self.building_to_simulate:
            path_dir_building_context = os.path.join(path_folder_simulation, self.building_dict[building_id].name,
                                                     "Context_surfaces_json")
            self.building_dict[building_id].context_surfaces_to_hbjson(path_dir_building_context)

    def GIS_context_individual_to_hbjson(self, path_folder_simulation):
        """
        Write the context surfaces of each building_zon in a hbjson file in the building_zon directory
        """
        for building_id in self.building_to_simulate:
            path_dir_building_context = os.path.join(path_folder_simulation, self.building_dict[building_id].name,
                                                     "GIS_context_json")
            self.building_dict[building_id].GIS_context_to_hbjson(path_dir_building_context)
