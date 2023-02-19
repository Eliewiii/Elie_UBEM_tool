"""
BuildingHBModel class, representing one building in an urban canopy that will be converted in HB models
as they will be simulated
"""

import logging

from honeybee.model import Model

from building import Building

class BuildingHBModel(Building):
    """Building class, representing one building in an urban canopy."""

    # todo :make the lb_footprint optional in the Building class
    def __init__(self, identifier, lb_footprint=None, urban_canopy=None, building_id_shp=None, **kwargs):
        # Initialize with the inherited attributes from the Building parent class
        super().__init__(identifier, lb_footprint, urban_canopy, building_id_shp)
        # get the values from the original Building object (if there is one) through **kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.hb_model_obj = None
        self.hb_model_dict = None



    @classmethod
    def from_building(cls, building_obj):
        """
        Create a BuildingHBModel object from a Building object
        :return: building_hb_model : BuildingHBModel object
        """
        # get the attributes of the building_obj (it extract all attributes, even the ones that are used
        # to create the object), but it doesn't matter, it is just a bit redundant
        kwargs = {attr: getattr(building_obj, attr) for attr in dir(building_obj) if not attr.startswith('__')}
        # create the BuildingHBModel object from the Building object
        building_hb_model = cls(building_obj.id, building_obj.lb_footprint, building_obj.urban_canopy, building_obj.shp_id, **kwargs)

        return building_hb_model

    def from_hbjson(self, path_hbjson, urban_canopy=None):
        """
        Create a BuildingHBModel object from a HBJSON file
        :return: building_hb_model : BuildingHBModel object
        """
        # Load the hb model from the hbjson file
        hb_model = Model.from_hbjson(path_hbjson)
        # get the identifier the
        identifier = hb_model.identifier
        # Try to extract certain characteristics of the model from the hb_model



def height_from_hb_model(hb_model):
    """
    Extract the height of the building from the hb model
    :param hb_model: honeybee model
    :return: height : float
    """
    # Get the height of the building from the hb model
    height =None  #todo
    return height


def elevation_from_hb_model(hb_model):
    """
    Extract the elevation of the building from the hb model
    :param hb_model:
    :return:
    """
    # todo : There is a high chance that the elevation will not be necessary,
    #  because the hb model is already at the right elevation, so wew might keep it at 0
    None


def lb_footprint_from_hb_model(hb_model):
    """
    Extract the footprint of the building from the hb model
    :param hb_model:
    :return:
    """

    None


def lb_faces_ground_bc_from_hb_model(hb_model):
    """
    Extract LB geometry faces 3D that have ground boundary condition from the HB model
    todo: not relevant if the building is on pillar...
    :param hb_model:
    :return:
    """
    # Init the list of LB geometry faces 3D that have ground boundary condition
    lb_face_ground_bc_list = []
    # Loop through the rooms of the HB model
    for room in hb_model.rooms:
        for face in room.faces:
            if face.boundary_condition.boundary_condition == "Ground":
                lb_face_ground_bc_list.append(face.geometry)

    return lb_face_ground_bc_list




def lb_face_to_shapely_polygon(lb_face):
    """
    Convert a LB geometry face 3D to a shapely polygon
    :param lb_face:
    :return:
    """













