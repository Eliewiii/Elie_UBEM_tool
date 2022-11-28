"""
Additional methods for the Building class.
Used for building energy rating (BER)
"""


class Mixin:

    def check_apartment_position(self):
        """ Check if the apartments are "top", "middle" or "bottom" """
        # check apartment position
        for apartment_obj in self.apartment_dict.values():
            apartment_obj.check_position(self.num_floor)



    def rate_building(self):
        """ Rate buildings according to the 5280 israeli standard  """

        # Rate each building individually
        for apartment_obj in self.apartment_dict.values():
            if apartment_obj.is_core == False:
                apartment_obj.rate_apartment(climate_zone_building=self.climate_zone)

        # Make the average of the grade of apartment according to the 5280
        for apartment_obj in self.apartment_dict.values():
            if apartment_obj.is_core == False:
                self.grade_value += apartment_obj.grade_value * apartment_obj.area / self.apartment_area

        # Give the final rating (in letter) according to the grade
        if self.grade_value < 0:
            self.rating = "F"
        elif self.grade_value < 1:
            self.rating = "E"
        elif self.grade_value < 2:
            self.rating = "D"
        elif self.grade_value < 3:
            self.rating = "C"
        elif self.grade_value < 4:
            self.rating = "B"
        elif self.grade_value < 5:
            self.rating = "A"
        else:
            self.rating = "A+"