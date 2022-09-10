# todo """  """

import os


class LcaSurfaceType():
    """

    """

    def __init__(self, R=None, U=None):
        """Initialize the Urban Canopy"""

        self.R_value = R
        self.U_value = U


class LcaMatColBySurfType(LcaSurfaceType):
    """
    LCA Material Collection By Surface Type,
    """

    def __init__(self, const_set, surface_type, R, U, number):
        # todo """
        #  const_set : original construction set of the building that is modified to test alternative sets
        #
        #  """
        self.const_set = const_set
        self.surface_type = surface_type
        number = number
        self.name = const_set + "_" + surface_type + "_" + number
        self.mat_list = []
        super().__init__(const_set, surface_type, R, U)
        self.compute_missing_property()

    def compute_missing_property(self):
        """ """
        if self.R_value == None and self.U_value == None:
            raise ValueError(
                "The layer {} in the construction set {} does not have R and U".format(self.name, self.const_set))
        elif self.R_value:  # priority to R
            self.U_value = 1 / self.R_value  # in the future we'll put exceptions if it's 0
        elif self.U_value:  # priority to R
            self.R_value = 1 / self.R_value  # in the future we'll put exceptions if it's 0

    # todo def __str__(self):
    #     """ what you see when you print the urban canopy object """
    #     return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")
    #
    # def __repr__(self):
    #     """ what you see when you type the urban canopy variable in the console """
    #     return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")

    @classmethod
    def from_csv_database(cls, path_folder_csv, file_name, const_set, surface_type):
        """ Convert a csv file,containing a collection of material into a LcaMatColBySurfType object """

        data_csv = None  # initialize the data variable
        with open(os.path.join(path_folder_csv, file_name)) as csv_file:
            data_csv = csv_file.read()

        csv_lines = data_csv.split("\n")

        # read 2nd line, where there is the default data of the material collection
        element_collection = csv_lines[1].split(",")
        r_value = element_collection[1]
        u_value = element_collection[2]
        number = file_name[:-4]  # without the .csv

        collection_obj = cls(const_set=const_set, surface_type=surface_type, R=r_value, U=u_value, number=number)


        #loop for all the material


class LcaMat(LcaSurfaceType):
    """
    LCA Material
    """

    def __init__(self, R, U, name, type_mat, life_time, climate_change, real_R=None, real_U=None, is_standard=None):
        # todo """Initialize the Urban Canopy"""
        super().__init__(R, U)
        self.name = name
        self.real_R = real_R
        self.real_U = real_U
        self.type_mat = type_mat
        self.life_time = life_time
        self.climate_change = climate_change
        self.climate_change_extrapolated = None
        self.extrapolate_values()
        self.is_standard = is_standard  # if it's a material that will be very likely to be used in Israel and that will
        # be used as the middle point in the graph (eventually, not needed if bar chart

    # todo def __str__(self):
    #     """ what you see when you print the urban canopy object """
    #     return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")
    #
    # def __repr__(self):
    #     """ what you see when you type the urban canopy variable in the console """
    #     return (f"The urban canopy, named {self.name}, is composed of {self.num_of_buildings} buildings")

    def extrapolate_values(self):
        """
        Extrapolate the climate change values if the R or U value is not the same as the LcaMatColBySurfType
        it belongs to (it happens a lot to be slightly different).
        If it's the case we assume that the material is more =/less thick and that the climate change (CO2eq) is
        proportional to the thickness (not always true, but if slightly different seems to be a fair assumption
        """
        if self.real_R:
            self.climate_change_extrapolated = self.climate_change * self.R_value / self.real_R
        elif self.real_U:
            self.climate_change_extrapolated = self.climate_change * self.real_U / self.U_value