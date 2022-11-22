"""
Additional methods for the Urban_canopy class.
Deals with the data extraction.
"""

from building_ubem.building import Building

from math import sqrt
from copy import deepcopy

class Mixin:

    def polygon_to_building(self, footprint, shape_file, building_number_shp, unit):
        """ Convert a Polygon to a Building object """

        point_list_footprints = polygon_to_points(footprint)  # convert the POLYGON into a list of points
        # if check_point_proximity(point_list_footprints):
        id_building = self.num_of_buildings  # id of the building_zon for the urban canopy object
        # create a building_zon object (automatically added to the urban_canopy_44)
        Building.from_shp_2D(id_building, point_list_footprints, self, shape_file, building_number_shp, unit)

    def multipolygon_to_building(self, footprint, shape_file, building_number_shp, unit):
        """ Convert a MultiPolygon to a Building object """
        for polygon in footprint.geoms:
            point_list_footprints = polygon_to_points(polygon)
            # if check_point_proximity(footprint):
            id_building = self.num_of_buildings  # id of the building_zon for the urban canopy object
            # create a building_zon object (automatically added to the urban_canopy_44)
            Building.from_shp_2D(id_building, point_list_footprints, self, shape_file, building_number_shp, unit)


def polygon_to_points(polygon_obj):
    """  Transform a Polygon object to a list of points """
    ## ADD COMMENTS

    exterior_footprint = polygon_obj.exterior.__geo_interface__['coordinates']
    # eventually check that the footprint is well oriented
    interior_holes = None
    try:
        polygon_obj.interiors
    except:
        None
    else:
        interior_holes = []
        for hole in polygon_obj.interiors:
            if hole.__geo_interface__['coordinates'] != None:
                interior_holes.append(hole.__geo_interface__['coordinates'])

    return ([exterior_footprint, interior_holes])


def check_point_proximity(point_list_footprints):
    """
    + Delete the redundant points and the points that are too close to each other in the footprints
      and holes in the footprints.
    + Reduce the complexity of the shapes of buildings.
    + Prevent, à priori, some mistakes. Honeybee doesn't seem to handle when points are too close to each other,
      or at least there is a problem when such geometries are created in Python, converted in json
      and then sent to Grasshopper.
    """

    tol = 0.1  # tolerance in meter. if the distance between 2 consecutive point is lower than this value, one of the point is deleted

    ## footprint
    points = point_list_footprints[0]
    number_of_points = len(points)
    i = 0
    while i <= number_of_points - 1:  # the condition to exist the loop is not good here as the number of points is modified everytime a point is deleted
        # but we needed one, the real conditio is inside of it
        if distance(points[i], points[i + 1]) < tol:
            points.pop(i + 1)
        else:
            i += 1
        if i >= len(
                points) - 1:  # if we reach the end of the footprint, considering some points were removed, the loop ends
            break
    if distance(points[0],
                points[-1]) < tol:  # check also with the first and last points in the footprint
        points.pop(-1)

    # ## holes
    # interior_holes=[]
    # try:
    #     polygon_obj.interiors
    # except:
    #     None
    # else:
    #     for hole in polygon_obj.interiors:
    #         if hole.__geo_interface__['coordinates'] != None:
    #             interior_holes.append(hole.__geo_interface__['coordinates'])
    #             number_of_points = len(hole)
    #             i = 0
    #             while i <= number_of_points - 1:
    #                 if distance(hole[i], hole[i + 1]) < tol:
    #                     hole.pop(i + 1)
    #                 else:
    #                     i += 1
    #                 if i >= len(hole) - 1:
    #                     break
    #             if distance(hole[0], hole[-1]) < tol:
    #                 hole.pop(-1)
    if len(points)<3:
        return False
    else:
        return True

def distance(pt_1, pt_2):
    """
    :param pt_1: list for the point 1
    :param pt_2: list for the point 2
    :return: distance between the 2 points
    """

    return sqrt((pt_1[0] - pt_2[0]) ** 2 + (pt_1[1] - pt_2[1]) ** 2)


def point_tuples_to_list(point_list_footprints):
    """ Convert the points from tuples (originally in GIS file) to list for more convenience """
    point_list_footprints=deepcopy(point_list_footprints)
    ## footprints ##
    new_point_list_footprint = []
    for point in self.footprint:
        new_point_list_footprint.append(list(point))
    self.footprint = new_point_list_footprint
    ## reverse the orientation, for the normal of the surface o face down = ground floor
    self.footprint.reverse()

    ## holes ##
    new_list_hole = []
    if self.holes != []:
        for hole in self.holes:
            list_point = []
            if len(hole) == 1:
                hole = hole[0]
            for point in hole:
                list_point.append(list(point))
            list_point.reverse()
            new_list_hole.append(list_point)
        ## reverse the orientation, for the normal of the surface o face down = ground floor
        self.holes = new_list_hole

    if self.holes == [None]:
        self.holes = []