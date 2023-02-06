"""
Building class, representing one building in an urban canopy.
"""

import logging

import shapely


from math import sqrt
from ladybug_geometry.geometry3d import Point3D, Face3D


class Building:
    """Building class, representing one building in an urban canopy."""

    def __init__(self, identifier, lb_footprint, urban_canopy=None, building_id_shp=None):
        """Initialize a building obj"""
        # urban canopy and key to access to the object from building_dict
        self.urban_canopy = urban_canopy
        self.id = identifier  # id of the building in the urban canopy building_dict
        # GIS specific
        self.shp_id = building_id_shp  # id in the shp file
        # Properties
        self.name = None  # name of the building (if available in the GIS)
        self.group = None  # group/neighbourhood of the building (if available in the GIS)
        self.age = None  # year the building was built
        self.typology = None  # typology of the building
        self.height = None  # height of the building in meter
        self.num_floor = None  # number of floor of the building
        self.elevation = None  # elevation of the building in meter
        self.floor_height = None  # height of the floors in meter
        # Geometry
        self.lb_footprint = lb_footprint  # footprint of the building, including the holes in the LB geometry face format
        self.hb_room_envelope = None  # Envelop, extruded of the lb_footprint, in HB room format

    @classmethod
    def from_lb_footprint(cls, lb_footprint, identifier, urban_canopy=None, building_id_shp=None):
        """Generate a Building from a Ladybug footprint."""
        return cls(identifier, lb_footprint, urban_canopy, building_id_shp)

    @classmethod
    def from_polygon(cls, polygon, identifier, urban_canopy=None, building_id_shp=None):
        """Generate a Building from a shapely polygon."""
        lb_footprint = polygon_to_lb_footprint(polygon)
        return cls(identifier, lb_footprint, urban_canopy, building_id_shp)

    @classmethod
    def from_shp_file(cls, urban_canopy, shp_file, building_id_shp, building_id_key_gis, unit):
        """
            Generate a building from a shp file.
            Can Eventually return multiple buildings if the footprint is a multipolygon.

            :param urban_canopy:
            :param shp_file: shp file
            :param building_id_shp: id of the building in the shp file
            :param building_id_key_gis: key of the building id in the shp file
            :param unit: unit of the shp file
            :return: list of building ids and list of building objects
        """
        # Initialize the outputs
        building_id_list, building_obj_list = [], []
        # get the building id
        building_id = shp_file[building_id_key_gis][building_id_shp]
        # get the footprint of the building
        footprint = shp_file['geometry'][building_id_shp]

        # check if the building is a polygon or multiple a multipolygon
        if isinstance(footprint, shapely.geometry.polygon.Polygon):
            try:
                polygon_to_lb_footprint(footprint, unit)

            except:
                logging.warning(f"The footprint of the building id {building_id} in the GIS file could not be converted"
                                f" to a Ladybug footprint. The building will be ignored.")
            else:
                building_obj = cls.from_polygon(polygon=footprint, identifier=building_id, urban_canopy=urban_canopy,
                                                building_id_shp=building_id_shp)
                building_id_list.append(building_id)
                building_obj_list.append(building_obj)


        # if the building_zon is made of multiple footprints
        elif isinstance(footprint, shapely.geometry.multipolygon.MultiPolygon):
            for i, polygon in enumerate(footprint.geoms):
                sub_building_id = f"{building_id}_{i}"
                try:
                    polygon_to_lb_footprint(polygon, unit)
                except:
                    logging.warning(
                        f"The footprint of the building id {sub_building_id} in the GIS file could not be converted"
                        f" to a Ladybug footprint. The building will be ignored.")
                else:
                    building_obj = cls.from_polygon(polygon=footprint, identifier=sub_building_id, urban_canopy=urban_canopy,
                                                    building_id_shp=building_id_shp)
                    building_id_list.append(sub_building_id)
                    building_obj_list.append(building_obj)

        return building_id_list, building_obj_list


def polygon_to_lb_footprint(polygon_obj, unit , tolerance=0.01):
    """
        Transform a Polygon object to a Ladybug footprint.
        Args:
            polygon_obj: A Polygon object.
            unit: Unit of the shp file.
        Returns:
            lb_footprint:A Ladybug footprint.
    """

    # Convert the exterior of the polygon to a list of points
    point_list_outline = [list(point) for point in polygon_obj.exterior.__geo_interface__['coordinates']]
    # Reverse the list of points to have the right orientation (facing down)
    point_list_outline.reverse()
    # Scale the point list according to the unit of the shp file
    scale_point_list_according_to_unit(point_list_outline, unit)
    # Remove redundant vertices (maybe not necessary, already included in Ladybug)
    # remove_redundant_vertices(point_list_outline, tol=tolerance)

    # Convert the list of points to a list of Ladybug Point3D
    point_3d_list_outline = [Point3D(point[0], point[1], 0) for point in point_list_outline]

    # Convert the exterior of the polygon to a list of points
    # Check if the polygon has holes
    try:
        polygon_obj.interiors  # Check if the polygon has holes
    except:
        interior_holes_pt_list = None
    else:
        interior_holes_pt_list = []
        for hole in polygon_obj.interiors:
            if hole.__geo_interface__['coordinates'] != None:
                if len(hole) == 1:
                    hole = hole[0]
                list_point_hole = [list(point) for point in hole]
                list_point_hole.reverse()

                interior_holes_pt_list.append(list_point_hole)
        if interior_holes_pt_list == [None]:
            interior_holes_pt_list = []
        for holes in interior_holes_pt_list:
            scale_point_list_according_to_unit(holes, unit)
            # remove_redundant_vertices(holes,tol = tolerance)  #(maybe not necessary, already included in Ladybug)

        interior_holes_pt_3d_list=[]
        for hole in interior_holes_pt_list:
            interior_holes_pt_3d_list.append([Point3D(point[0], point[1], 0) for point in hole])

    # Convert the list of points to a Ladybug footprint
    lb_footprint = Face3D (boundary=point_3d_list_outline, holes=interior_holes_pt_3d_list,enforce_right_hand=True)
    # Remove collinear vertices
    lb_footprint = lb_footprint.remove_colinear_vertices(tolerance=tolerance)

    return lb_footprint


def scale_point_list_according_to_unit(point_list, unit):
    """
    Scale the point list according to the unit of the shp file.
    :param point_list: list of points, a point is a list of two coordinates
    :param unit: unit of the shp file, usually degree or meter
    """
    if unit == "deg":
        factor = 111139  # conversion factor, but might be a bit different, it depends on the altitude, but the
        # deformation induced should be small if it's not on a very high mountain
        for point in point_list:
            point[0] = point[0] * factor
            point[1] = point[1] * factor
    # a priori the only units re degrees and meters. For meter not need to scale
    else:
        None


def remove_redundant_vertices(point_list, tol=0.5):
    """
    Check if the points of the footprint are too close to each other. If yes, delete one of the points.
    :param point_list: list of points, a point is a list of two coordinates
    :param tol: tolerance in meter. if the distance between 2 consecutive point is lower than this value, one of the point is deleted
    """
    # Number of points in the point list
    number_of_points = len(point_list)
    # Initialize the index
    i = 0
    while i <= number_of_points - 1:  # go over all points
        if distance(point_list[i], point_list[i + 1]) < tol:
            point_list.pop(i + 1)
        else:
            i += 1
        if i >= len(
                point_list) - 1:  # if we reach the end of the footprint, considering some points were removed, the loop ends
            break
    if distance(point_list[0],
                point_list[-1]) < tol:  # check also with the first and last points in the footprint
        point_list.pop(-1)


def distance(pt_1, pt_2):
    """
    :param pt_1: list for the point 1
    :param pt_2: list for the point 2
    :return: distance between the 2 points
    """

    return sqrt((pt_1[0] - pt_2[0]) ** 2 + (pt_1[1] - pt_2[1]) ** 2)