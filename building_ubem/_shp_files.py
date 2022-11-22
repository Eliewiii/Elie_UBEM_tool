"""
Additional methods for the Building class.
Contains functions used to generate the geometry and extract the properties of the Building obj from shp files .
"""

from math import sqrt


class Mixin:

    def point_tuples_to_list(self):
        """ Convert the points from tuples (originally in GIS file) to list for more convenience """

        ## footprints ##
        new_point_list_footprint = []
        for point in self.footprint:
            new_point_list_footprint.append(list(point))
        self.footprint = new_point_list_footprint
        ## reverse the orientation, for the normal of the surface o face down = ground floor
        self.footprint.reverse()

        ## holes ##
        new_list_hole = []
        if self.holes != []:
            for hole in self.holes:
                list_point = []
                if len(hole) == 1:
                    hole = hole[0]
                for point in hole:
                    list_point.append(list(point))
                list_point.reverse()
                new_list_hole.append(list_point)
            ## reverse the orientation, for the normal of the surface o face down = ground floor
            self.holes = new_list_hole

        if self.holes == [None]:
            self.holes = []

    def scale_unit(self, unit):
        """ Apply a conversion factor if the GIS file is in degree """

        if unit == "deg":
            factor = 111139  # conversion factor, but might be a bit different, it depends on the altitude, but the
            # deformation induced would be small if it' not on a very high mountain
            for point in self.footprint:
                point[0] = point[0] * factor
                point[1] = point[1] * factor

            for hole in self.holes:
                for point in hole:
                    point[0] = point[0] * factor
                    point[1] = point[1] * factor
        elif unit == "m":
            factor = 1
        else:
            factor = 1

    def check_point_proximity(self):
        """
        + Delete the redundant points and the points that are too close to each other in the footprints
          and holes in the footprints.
        + Reduce the complexity of the shapes of buildings.
        + Prevent, à priori, some mistakes. Honeybee doesn't seem to handle when points are too close to each other,
          or at least there is a problem when such geometries are created in Python, converted in json
          and then sent to Grasshopper.
        """

        tol = 0.5  # tolerance in meter. if the distance between 2 consecutive point is lower than this value, one of the point is deleted

        ## footprint
        number_of_points = len(self.footprint)
        i = 0
        while i <= number_of_points - 1:  # the condition to exist the loop is not good here as the number of points is modified everytime a point is deleted
            # but we needed one, the real conditio is inside of it
            if distance(self.footprint[i], self.footprint[i + 1]) < tol:
                self.footprint.pop(i + 1)
            else:
                i += 1
            if i >= len(
                    self.footprint) - 1:  # if we reach the end of the footprint, considering some points were removed, the loop ends
                break
        if distance(self.footprint[0],
                    self.footprint[-1]) < tol:  # check also with the first and last points in the footprint
            self.footprint.pop(-1)

        ## holes
        if self.holes != None:
            for hole in self.holes:  # same thing as above with the holes
                number_of_points = len(hole)
                i = 0
                while i <= number_of_points - 1:
                    if distance(hole[i], hole[i + 1]) < tol:
                        hole.pop(i + 1)
                    else:
                        i += 1
                    if i >= len(hole) - 1:
                        break
                if distance(hole[0], hole[-1]) < tol:
                    hole.pop(-1)

    def affect_properties_shp(self, shp_file, building_id_shp):
        """ collect the building_zon properties from the shp file and assign them to the building_zon properties """

        ## need to move these list somewhere else, where they can be edited, but for now they stay there
        age_possibilities = ["age", "date"]
        typology_possibilities = ["typo", "typology", "type", "Typology"]
        elevation_possibilities = ["minheight"]
        height_possibilities = ["height", "Height", "govasimple"]
        number_floor_possibilities = ["number_floor", "nb_floor", "mskomot"]
        name_possibilities = ["name", "full_name_"]
        group_possibilities = ["group"]

        ## age ##
        for property_name in age_possibilities:  # loop on all the possible name
            try:  # check if the property name exist
                shp_file[property_name]
            except:  # if it doesn't, don't do anything
                None
            else:  # if it does, assign the information to the building_zon then break = get out of the loop
                self.age = int(shp_file[property_name][building_id_shp])
                break
        ## name ##
        for property_name in name_possibilities:
            try:
                shp_file[property_name]
            except:
                None
            else:
                self.name = shp_file[property_name][building_id_shp]
                break
        ## group ##
        for property_name in group_possibilities:
            try:
                shp_file[property_name]
            except:
                None
            else:
                self.group = shp_file[property_name][building_id_shp]
                break
        ## height ##
        for property_name in height_possibilities:
            try:
                shp_file[property_name]
                float(shp_file[property_name][building_id_shp])
            except:
                None
            else:
                self.height = float(shp_file[property_name][building_id_shp])
                break
        ## elevation ##
        for property_name in elevation_possibilities:
            try:
                shp_file[property_name]
                float(shp_file[property_name][building_id_shp])
            except:
                None
            else:
                self.elevation = float(shp_file[property_name][building_id_shp])
                break
        ## number of floor ##
        for property_name in number_floor_possibilities:
            try:
                shp_file[property_name]
                int(shp_file[property_name][building_id_shp])
            except:
                None
            else:
                self.num_floor = int(shp_file[property_name][building_id_shp])
                break

        ## typology ##
        for property_name in typology_possibilities:
            try:
                shp_file[property_name]
            except:
                None
            else:
                self.typo = shp_file[property_name][building_id_shp]
                break

    ## MIGHT ADD ELEVATION

    def check_property(self):
        """ check if there is enough information about the building_zon to create a model"""
        if self.height == None and (self.num_floor == None or self.num_floor < 1) :
            self.height = 9.
            self.num_floor = 3
            self.floor_height = 3.
        elif self.height == None and type(self.num_floor) == int and self.num_floor > 0:  # assume 3m floor height
            self.height = 3. * self.num_floor
            self.floor_height = 3.
        elif (self.num_floor == None or self.num_floor < 1) and (type(self.height) == int or type(self.height) == float):
            # assume approximately 3m floor height
            self.num_floor = self.height // 3.
            self.floor_height = self.height / 3.
        elif (type(self.height) == int or type(self.height) == float) and (type(
                self.num_floor) == int and self.num_floor > 0):  # both height and number of floor
            if 4. <= self.height / float(self.num_floor) <= 2.5:  # then ok
                self.floor_height = self.height / float(self.num_floor)
            else:  # prioritize the number of floor
                self.height = 3. * self.num_floor
                self.floor_height = 3.
        else:  # not the proper format
            self.height = 9.
            self.num_floor = 3
            self.floor_height = 3.


        # Todo : building_zon.check_property
        # have to define the criteria later


def distance(pt_1, pt_2):
    """
    :param pt_1: list for the point 1
    :param pt_2: list for the point 2
    :return: distance between the 2 points
    """

    return sqrt((pt_1[0] - pt_2[0]) ** 2 + (pt_1[1] - pt_2[1]) ** 2)
