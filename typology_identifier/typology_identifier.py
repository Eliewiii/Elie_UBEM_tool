"""
Main functions to identify the typologies of buildings based on their footprint
"""


def identify_typology(footprint, year, ml_model):
    """
        Return the typology identifier the building belongs to according to its footprint geometry
        and the year it was built.

    Args:
        footprint [?]: footprint of the building (shapely? Face3D?)
        year [int]: year the building was built
        ml_model: machine learning model to use (a priori a special class containing the model(s)
            and the typology identifier

    Returns:
        A Face3D type rectangle representing the oriented bounding box.
    """
