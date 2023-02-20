"""
Additional functions for Ladybug Face objects.
"""
import logging

from shapely.geometry import Polygon

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D

def lb_face_to_shapely_polygon(lb_face):
    """Convert a Ladybug Face to a Shapely Polygon."""
    # convert vertices into tuples
    list_tuple_vertices_2d = [(x,y) for [x,y,z] in lb_face.vertices]
    
    return Polygon(list_tuple_vertices_2d)


def shapely_polygon_to_lb_face(polygon,tolerance=0.01):
    """Convert a Ladybug Face to a Shapely Polygon."""
    # convert vertices into tuples
    point_list_outline = [list(point) for point in polygon.exterior.__geo_interface__['coordinates']]
    # convert the list of points to a list of Ladybug Point3D
    point_3d_list_outline = [Point3D(point[0], point[1], 0) for point in point_list_outline]
    # Convert the list of points to a Ladybug Face3D
    lb_footprint = Face3D(boundary=point_3d_list_outline, enforce_right_hand=True)
    # Remove collinear vertices
    lb_footprint = lb_footprint.remove_colinear_vertices(tolerance=tolerance)

    return lb_footprint


def merge_lb_face_list(lb_face_list,):
    """
    Merge LB Face3D into one.
    I cannot consider holes ! would need to adapt it eventually but it's not necessary for now
    todo: adapt if the merging create a multy-polygon
    :param lb_face_list:
    :return:
    """
    # Merge only of there is more than one face
    if len (lb_face_list) > 1:
        # convert each lb face to Polygon
        polygon_list = [lb_face_to_shapely_polygon(lb_face) for lb_face in lb_face_list]
        # Initialize merging polygon
        merged_polygon = polygon_list[0]
        # loop over each polygon
        for polygon in polygon_list[1:] :
            merged_polygon.union(polygon)  # merge the polygon with the merged polygon
        # convert the merged polygon to a LB geometry face 3D
        lb_face_merged = shapely_polygon_to_lb_face(merged_polygon)
        return lb_face_merged
    # if there is only one face, return it
    if len (lb_face_list) == 1:
        return(lb_face_list[0])
    # if there is no face, return a warning
    else:
        logging.warning("The list of faces to merge is empty")
        # raise error
        raise ValueError("The list of faces to merge is empty")




if __name__== "__main__":

    None