"""
To generate samples and test functions
"""


class Mixin:

    @classmethod
    def generate_sample_one_building(cls, urban_canopy, in_footprint=None):
        """ """
        if in_footprint == None:
            in_footprint = [[0, 0], [10, 0], [10, 10], [0, 10]]

        building_obj = cls(urban_canopy=urban_canopy, id=0, footprint=in_footprint)

    @classmethod
    def generate_sample_buildings(cls, urban_canopy, nb_buildings=2):
        """ """
        for i in range(nb_buildings):
            in_footprint = [[i*20+0, 0], [i*20+10, 0], [i*20+10, 10], [i*20+0, 10]]
            cls(urban_canopy=urban_canopy, id=i, footprint=in_footprint)
