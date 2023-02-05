"""
Building class, representing one building in an urban canopy.
"""
import shapely

from math import sqrt

class Building:
    """Building class, representing one building in an urban canopy."""

    def __init__(self, urban_canopy, id, footprint, holes_footprint=None, name=None, group=None, age=None, typo=None,
                 height=None, num_floor=None, building_id_shp=None, elevation=0., dimension=2):
        """Initialize a building obj"""
        ## add building_zon to urban canopy dictionary
        urban_canopy.add_building(id, self)
        self.urban_canopy = urban_canopy
        # # # # # # # properties # # # # # # #
        self.id = id
        self.footprint = footprint  # will be oriented down as the ground floor "look" down
        self.holes = holes_footprint
        self.name = name
        self.group = group
        self.age = age
        self.typology = typo
        self.num_floor = None
        self.height = None
        # todo : add the elevation, especially to the buuilding envelop
        self.elevation = elevation
        self.shp_id = building_id_shp  # id in the shp file, can be useful to see which is the building_zon if a problem is spotted
        self.floor_height = None

    @classmethod
    def from_shp_file(cls, shp_file, building_id_shp, building_id_key_gis, unit):
        """
            Generate a building from a shp file.
            Can Eventually return multiple buildings if the footprint is a multipolygon.

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
                lb_footprint = polygon_to_lb_footprint(footprint, unit)

            except
                lb_footprint = polygon_to_lb_footprint(footprint, unit)

            else :
                self.polygon_to_building(footprint, shape_file, building_number_shp, unit)
        elif isinstance(footprint,
                        shapely.geometry.multipolygon.MultiPolygon):  # if the building_zon is made of multiple footprints
            self.multipolygon_to_building(footprint, shape_file, building_number_shp, unit)

        return building_id_list, building_obj_list



def polygon_to_lb_footprint(polygon, unit):
    """
    Convert a shapely polygon to a ladybug footprint.
    :param polygon: shapely polygon
    :param unit: unit of the shp file
    :return: ladybug footprint
    """
    # get the coordinates of the polygon
    coordinates = list(polygon.exterior.coords)
    # convert the coordinates to ladybug footprint
    lb_footprint = lb_polygon(coordinates, unit)
    return lb_footprint


def polygon_to_lb_footprint(polygon_obj, unit):
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
    # remove_redundant_vertices(point_list_outline)

    # Check if the polygon has holes
    try:
        polygon_obj.interiors
    except:
        interior_holes_pt_list = None
    else:
        interior_holes_pt_list = []
        for hole in polygon_obj.interiors:
            if hole.__geo_interface__['coordinates'] != None:
                list_point_hole =[]
                if len(hole) == 1:
                    hole = hole[0]
                for point in hole:
                    list_point_hole.append(list(point))
                list_point_hole.reverse()

                interior_holes_pt_list.append(list_point_hole)
        if interior_holes_pt_list == [None]:
            interior_holes_pt_list = []
        for holes in interior_holes_pt_list:
            scale_point_list_according_to_unit(holes, unit)
            # remove_redundant_vertices(holes)  #(maybe not necessary, already included in Ladybug)
    return ([exterior_footprint, interior_holes])


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
        if i >= len(point_list) - 1:  # if we reach the end of the footprint, considering some points were removed, the loop ends
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