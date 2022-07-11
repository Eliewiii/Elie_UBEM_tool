"""
Additional methods for the Building class.

"""


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
                print("the format of the age is wrong")
            else:
                self.__age = float(age)

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

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        if height == None:
            self.__height = 9.0  # by default 3 floors of 3 meters
        else:
            try:
                float(height)
            except:
                print("the format of height is wrong")
            else:
                self.__height = float(height)

    @property
    def num_floor(self):
        return self.__num_floor

    @num_floor.setter
    def num_floor(self, num_floor):
        if num_floor == None:
            self.__num_floor = self.height // 3.  # by default 3 meters
        else:
            None
            try:
                float(num_floor)
            except:
                print("the format of the number of floor is wrong")
            else:
                self.__num_floor = int(num_floor)

    @property
    def floor_height(self):
        return self.__floor_height

    @floor_height.setter
    def floor_height(self, floor_height):
        if floor_height == None:
            self.__floor_height = self.height / self.num_floor
        else:
            try:
                float(floor_height)
            except:
                print("the format of the floor height is wrong")
                self.__floor_height = self.height / self.num_floor
            else:
                if floor_height > 0:
                    self.__floor_height = float(floor_height)
                else:
                    self.__floor_height = self.height / self.num_floor

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
                print("the format of height is wrong")
            else:
                self.__int_mass_ratio = float(int_mass_ratio)

    # @property
    # def is_simulated(self):
    #     return self.__is_simulated
    # @is_simulated.setter
    # def is_simulated(self, is_simulated):
    #     if is_simulated==None:
    #         self.__is_simulated="Building_"+str(self.id)
    #     else:
    #         None
