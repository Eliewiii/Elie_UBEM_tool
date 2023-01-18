"""
Main functions to identify the typologies of buildings based on their footprint
"""


# def identify_typology(footprint, year, ml_model):
#     """
#         Return the typology identifier the building belongs to according to its footprint geometry
#         and the year it was built.
#
#     Args:
#         footprint [?]: footprint of the building (shapely? Face3D?)
#         year [int]: year the building was built
#         ml_model: machine learning model to use (a priori a special class containing the model(s)
#             and the typology identifier
#
#     Returns:
#         A Face3D type rectangle representing the oriented bounding box.
#     """

def identify_shapes_type(footprint, ml_model,ml_model_param):
    """ For all the shapes """
    # loop for all the shapes

    # clean temp file with the tempoary images genetrated for the identification


def identify_shape_type(footprint, ml_model,ml_model_param):
    """
        Return the typology identifier the building belongs to according to its footprint geometry
        and the year it was built.

    Args:
        footprint [lb_footprint]: footprint of the building (shapely? Face3D?)
        ml_model: machine learning model to use

    """


def load_ml_model(path_model_pkl,path_model_param_json):
    """

    """