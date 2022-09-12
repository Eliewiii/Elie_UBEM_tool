# todo """  """

import os
from math import ceil


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
        # Inherit properties from the super class
        super().__init__(R, U)
        # other properties
        self.const_set = const_set
        self.surface_type = surface_type
        number = number
        self.name = const_set + "_" + surface_type + "_" + number
        self.mat_dict = []  # dictionary with all the materials
        self.compute_missing_property()
        # life duration, set by the user in the code (can change the results as materials have different life time)
        self.life_duration = None
        # Computed values from materials
        self.max_climate_change_overall = None  # maximum climate change for all the life duration for 1 square meter of surface
        self.standard_climate_change_overall = None  # standard climate change for all the life duration for 1 square meter of surface
        self.min_climate_change_overall = None  # minimum climate change for all the life duration for 1 square meter of surface

    @classmethod
    def from_csv_database(cls, path_folder_csv, file_name, const_set, surface_type):
        """ Convert a csv file,containing a collection of material into a LcaMatColBySurfType object """

        data_csv = None  # initialize the data variable
        with open(os.path.join(path_folder_csv, file_name)) as csv_file:
            data_csv = csv_file.read()

        csv_lines = data_csv.split("\n")

        # read 2nd line, where there is the default data of the material collection
        data_elements = csv_lines[1].split(",")
        r_value = float(data_elements[1])
        u_value = float(data_elements[2])
        number = file_name[:-4]  # without the .csv

        collection_obj = cls(const_set=const_set, surface_type=surface_type, R=r_value, U=u_value, number=number)

        for csv_line in csv_lines[2:]:
            if csv_line != "":
                lca_mat_obj = LcaMat.from_csv_line(csv_data_line=csv_line, R=r_value, U=u_value)
                collection_obj.mat_dict[lca_mat_obj.name] = lca_mat_obj

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

    def compute_extreme_climate_change(self, life_duration):
        """ Compute the minimum, maximum and set the standard climate change for the whole LcaMatColBySurfType """
        # set life_duration
        self.life_duration = life_duration
        # Compute the climate changes over a given period of time
        climate_change_for_all_duration_list = []  # list of climate change to get  the maximum and minimum from
        for material_obj in self.mat_dict.values(): # loop over the materials
            # number of time we need to install the material to cover all the life duration
            multiplier = ceil(life_duration / material_obj.life_time)
            if material_obj.is_standard == True:  # get the standard value
                self.standard_climate_change_overall = material_obj.climate_change_extrapolated * multiplier
            climate_change_for_all_duration_list.append(material_obj.climate_change_extrapolated * multiplier)
        self.max_climate_change_overall = max(climate_change_for_all_duration_list)
        self.min_climate_change_overall = min(climate_change_for_all_duration_list)


class LcaMat(LcaSurfaceType):
    """
    LCA Material
    """

    def __init__(self, R, U, name, type_mat, life_time, climate_change, real_R=None, real_U=None, is_standard=False):
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

    @classmethod
    def from_csv_line(cls, csv_data_line, R, U):
        """ Create an LcaMat object from a line of the csv file containing the data """

        # convert into a list of elements
        data_elements = csv_data_line.split(",")
        # check if it's the standard
        if data_elements[3] == "standard":
            is_standard = True
        else:
            is_standard = False
        # extract the rest of the values
        name = data_elements[0]
        # thermal properies
        if data_elements[1] != "":
            real_r_value = float(data_elements[1])
        elif data_elements[2] != "":
            real_u_value = float(data_elements[2])
        # other
        type_mat = data_elements[4]
        life_time = float(data_elements[5])
        climate_change = float(data_elements[6])

        return (cls(R=R, U=U, name=name, type_mat=type_mat, life_time=life_time, climate_change=climate_change,
                    real_R=real_r_value, real_U=real_u_value, is_standard=is_standard))

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
