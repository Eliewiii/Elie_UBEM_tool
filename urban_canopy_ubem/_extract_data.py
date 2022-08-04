"""
Additional methods for the Urban_canopy class.
Deals with the data extraction.
"""

from building_ubem.building import Building


class Mixin:

    def polygon_to_building(self, footprint, shape_file, building_number_shp, unit):
        """ Convert a Polygon to a Building object """
        point_list_footprints = polygon_to_points(footprint)  # convert the POLYGON into a list of points
        id_building = self.num_of_buildings  # id of the building_zon for the urban canopy object
        # create a building_zon object (automatically added to the urban_canopy_44)
        Building.from_shp_2D(id_building, point_list_footprints, self, shape_file, building_number_shp, unit)

    def multipolygon_to_building(self, footprint, shape_file, building_number_shp, unit):
        """ Convert a MultiPolygon to a Building object """
        for polygon in footprint.geoms:
            point_list_footprints = polygon_to_points(polygon)
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
