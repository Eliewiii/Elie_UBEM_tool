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
        # point_tuples_to_list(point_list_footprints) # todo
        if check_point_proximity(scale_unit(point_tuples_to_list(deepcopy(point_list_footprints)),unit)):
            id_building = self.num_of_buildings  # id of the building_zon for the urban canopy object
            # create a building_zon object (automatically added to the urban_canopy_44)
            Building.from_shp_2D(id_building, point_list_footprints, self, shape_file, building_number_shp, unit)

    def multipolygon_to_building(self, footprint, shape_file, building_number_shp, unit):
        """ Convert a MultiPolygon to a Building object """
        for polygon in footprint.geoms:
            point_list_footprints = polygon_to_points(polygon)
            # point_tuples_to_list(point_list_footprints)
            if check_point_proximity(scale_unit(point_tuples_to_list(deepcopy(point_list_footprints)),unit)): # todo
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

    ## holes
    if point_list_footprints[1] != None:
        for hole in point_list_footprints[1]:  # same thing as above with the holes
            number_of_points = len(hole)
            i = 0
            while i <= number_of_points - 1:
                if distance(hole[i], hole[i + 1]) < tol:
                    hole.pop(i + 1)
                else:
                    i += 1
                if i >= len(hole) - 1:
                    break
            if distance(hole[0], hole[-1]) < tol:
                hole.pop(-1)
            if len (hole)<3:
                return false

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
    ## footprints ##
    new_point_list_footprint = []
    for point in point_list_footprints[0]:
        new_point_list_footprint.append(list(point))
    point_list_footprints[0] = new_point_list_footprint
    ## reverse the orientation, for the normal of the surface o face down = ground floor
    point_list_footprints[0].reverse()

    ## holes ##
    new_list_hole = []
    if point_list_footprints[1] != []:
        for hole in point_list_footprints[1]:
            list_point = []
            if len(hole) == 1:
                hole = hole[0]
            for point in hole:
                list_point.append(list(point))
            list_point.reverse()
            new_list_hole.append(list_point)
        ## reverse the orientation, for the normal of the surface o face down = ground floor
        point_list_footprints[1] = new_list_hole

    if point_list_footprints[1] == [None]:
        point_list_footprints[1] = []
    return point_list_footprints

def scale_unit(point_list_footprints, unit):
    """ Apply a conversion factor if the GIS file is in degree """

    if unit == "deg":
        factor = 111139  # conversion factor, but might be a bit different, it depends on the altitude, but the
        # deformation induced would be small if it' not on a very high mountain
        for point in point_list_footprints[0]:
            point[0] = point[0] * factor
            point[1] = point[1] * factor

        for hole in point_list_footprints[1]:
            for point in hole:
                point[0] = point[0] * factor
                point[1] = point[1] * factor
    elif unit == "m":
        factor = 1
    else:
        factor = 1

    return point_list_footprints