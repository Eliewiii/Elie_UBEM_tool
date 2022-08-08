"""
Additional methods for the Building class.
Contains the setter for Building object attribute.
They verify if the attributes are valid, which mean the proper type, acceptable, and consistent
(with the other attributes) values.
"""

import logging


class Mixin:

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name == None:
            self.__name = "Building_" + str(self.id)
        else:
            None  # for now, will add the real name of the building_zon when we define properly how to treat it

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if age == None:
            self.__age = None
        else:
            try:
                int(age)
            except:
                logging.warning("Building {}: the format of the age is wrong".format(self.id))
            else:
                self.__age = float(age)

    @property
    def shp_id(self):
        return self.__shp_id

    @shp_id.setter
    def shp_id(self, shp_id):
        if shp_id == None:
            self.__shp_id = self.id
        else:
            try:
                int(shp_id)
            except:
                logging.warning("Building {}: the format of the building_id_shp is wrong".format(self.id))
            else:
                self.__shp_id = shp_id

    # @property
    # def use(self):
    #     return self.__use
    # @use.setter
    # def use(self, use):
    #     if use==None:
    #         self.__use = None
    #     else:
    #         try:
    #             int(use)
    #         except:
    #             print("the format of the use is wrong")
    #         else:
    #             self.__use = float(use)

    # @property
    # def height(self):
    #     return self.__height
    #
    # @height.setter
    # def height(self, height):
    #     try:
    #         float(height)
    #     except:
    #         logging.warning("Building {}: the format of the height is wrong".format(self.id))
    #     else:
    #
    #         self.__height = float(height)

    # @property
    # def num_floor(self):
    #     return self.__num_floor
    #
    # @num_floor.setter
    # def num_floor(self, num_floor):
    #     if num_floor == None:
    #         self.__num_floor = 3  # by default 3 floors
    #     else:
    #         None
    #         try:
    #             float(num_floor)
    #         except:
    #             logging.warning("Building {}: the format of the number of floor is wrong".format(self.id))
    #         else:
    #             self.__num_floor = int(num_floor)

    # @property
    # def floor_height(self):
    #     return self.__floor_height
    #
    # @floor_height.setter
    # def floor_height(self, floor_height):
    #     if floor_height == None:
    #         self.__floor_height = self.height / self.num_floor
    #     else:
    #         try:
    #             float(floor_height)
    #         except:
    #             logging.warning("Building {}: the format of the number of floor height is wrong".format(self.id))
    #             self.__floor_height = self.height / self.num_floor
    #         else:
    #             if 6 > floor_height > 2.2:
    #                 self.__floor_height = float(floor_height)
    #             else:
    #                 self.__floor_height = self.height / self.num_floor

    @property
    def is_target(self):
        return self.__is_target

    @is_target.setter
    def is_target(self, is_target):
        if is_target == False:
            self.__is_target = False
        elif is_target == True:
            self.__is_target = True
            self.is_simulated = True  # if it's a target building_zon we simulate it...
            if self.id not in self.urban_canopy.target_buildings:
                self.urban_canopy.target_buildings.append(self.id)
        else:
            None

    @property
    def is_simulated(self):
        return self.__is_simulated

    @is_simulated.setter
    def is_simulated(self, is_simulated):
        if is_simulated == False:
            self.__is_simulated = False
        elif is_simulated == True:
            self.__is_simulated = True
            if self.id not in self.urban_canopy.building_to_simulate:
                self.urban_canopy.building_to_simulate.append(self.id)
        else:
            None

    @property
    def int_mass_ratio(self):
        return self.__int_mass_ratio

    @int_mass_ratio.setter
    def int_mass_ratio(self, int_mass_ratio):
        if int_mass_ratio == None:
            self.__int_mass_ratio = 1.5  # by default 1.5, value of the Israeli standard 5282
        else:
            try:
                float(int_mass_ratio)
            except:
                logging.warning("Building {}: the format of the internal mass ratio is wrong".format(self.id))
            else:
                if 0 < self.__int_mass_ratio < 5:
                    self.__int_mass_ratio = float(int_mass_ratio)
                else:
                    logging.warning(
                        "Building {}: the value of the internal mass ratio is not good, it was replaced by 1.5".format(
                            self.id))
                    self.__int_mass_ratio = 1.5

                    # @property
                # def is_simulated(self):
                #     return self.__is_simulated
                # @is_simulated.setter
                # def is_simulated(self, is_simulated):
                #     if is_simulated==None:
                #         self.__is_simulated="Building_"+str(self.id)
                #     else:
                #         None

    @property
    def cop_h(self):
        return self.__cop_h

    @cop_h.setter
    def cop_h(self, cop_h):
        if cop_h == None:
            self.__cop_h = 3.  # by default 3
        else:
            try:
                float(cop_h)
            except:
                logging.warning("Building {}: the format of the COP is wrong".format(self.id))
            else:
                self.__cop_h = float(cop_h)

    @property
    def cop_c(self):
        return self.__cop_c

    @cop_c.setter
    def cop_c(self, cop_c):
        if cop_c == None:
            self.__cop_c = 3.  # by default 3
        else:
            try:
                float(cop_c)
            except:
                logging.warning("Building {}: the format of the COP is wrong".format(self.id))
            else:
                self.__cop_c = float(cop_c)
