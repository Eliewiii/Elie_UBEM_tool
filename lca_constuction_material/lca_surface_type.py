# todo """  """


class LcaSurfaceType():
    """

    """

    def __init__(self, const_set, surface_type, R, U):
        """Initialize the Urban Canopy"""

        self.R_value = R
        self.U_value = U


class LcaMatColBySurfType(LcaSurfaceType):
    """
    LCA Material Collection By Surface Type
    """

    def __init__(self, const_set, surface_type, R, U):
        # todo"""Initialize the Urban Canopy"""
        self.const_set = const_set
        self.surface_type = surface_type
        super().__init__(const_set, surface_type, R, U)

    # todo def __str__(self):
    #     """ what you see when you print the urban canopy object """
    #     return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")
    #
    # def __repr__(self):
    #     """ what you see when you type the urban canopy variable in the console """
    #     return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")


class LcaMat(LcaSurfaceType):
    """
    LCA Material
    """

    def __init__(self, R, U, real_R, real_U, name, type, life_time, climate_change):
        # todo """Initialize the Urban Canopy"""
        super().__init__(R, U)
        self.name = name
        self.real_R = real_R
        self.real_U = real_U
        self.life_time = life_time
        self.is_extrapolated = None
        self.climate_change_extrapolated = None
        self.extrapolate_values()

    # todo def __str__(self):
    #     """ what you see when you print the urban canopy object """
    #     return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")
    #
    # def __repr__(self):
    #     """ what you see when you type the urban canopy variable in the console """
    #     return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")

    def extrapolate_values(self):
        """
        Extrapolate the climate change value if the R or U value is not the same as the LcaMatColBySurfType
        it belongs to
        """
























