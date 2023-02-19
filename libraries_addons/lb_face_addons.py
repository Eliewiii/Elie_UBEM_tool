"""
Additional functions for Ladybug Face objects.
"""
from shapely.geometry import Polygon


def lb_face_to_shapely_polygon(lb_face):
    """Convert a Ladybug Face to a Shapely Polygon."""
    # convert vertices into tuples
    list_tuple_vertices_2d = [(x,y) for [x,y,z] in lb_face.vertices]
    return Polygon(list_tuple_vertices_2d)


def shapely_polygon_to_lb_face(lb_face):
    """Convert a Ladybug Face to a Shapely Polygon."""
    # convert vertices into tuples
    list_tuple_vertices_2d = [(x,y) for [x,y,z] in lb_face.vertices]
    # convert to Polygon
    return Polygon(list_tuple_vertices_2d)

def merge_lb_face_list(lb_face_list):
    """
    Merge LB Face3D into one.
    I cannot consider holes ! would need to adapt it eventually but it's not necessary for now
    todo: adapt if the merging create a multy-polygon
    :param lb_face_list:
    :return:
    """
    # Merge only of there is more
    if len (lb_face_list) > 1:
    # convert each lb face to Polygon
    polygon_list = [lb_face_to_shapely_polygon(lb_face) for lb_face in lb_face_list]
    # Initialize merging
    merged_polygon = polygon_list[0]
    if len(polygon_list)>1:
        for polygon in polygon_list[1:] :
            merged_polygon.union(polygon)




if __name__== "__main__":

    None