"""
Additional methods for the Building class.
Used for extracting results from CSV
"""
BER_reference_values = {"A": {"top": 40.6, "middle": 38.58, "bottom": 28.558},
                        "B": {"top": 46.54, "middle": 38.87, "bottom": 30.66},  # to update in the future
                        "C": {"top": 46.54, "middle": 38.87, "bottom": 30.66},  # to update in the future
                        "D": {"top": 46.54, "middle": 38.87, "bottom": 30.66}}  # to update in the future

apartment_types = ["ground", "over_open_space", "over_unheated", "under_unheated", "between_unheated", "unheated",
                   "middle", "top"]


class Mixin:

    def check_position(self, building_num_floor):
        """ Check if the apartments are "top", "middle" or "bottom" """
        if self.floor_number == 1:
            self.position = "bottom"
        elif self.floor_number == building_num_floor:
            self.position = "top"
        else:
            self.position = "middle"

    def rate_apartment(self, climate_zone_building):
        """
        Rate the apartment acording to the 5280 standard
        """
        ec_ref = BER_reference_values[climate_zone_building][self.position]  # energy consumption of the reference
        ip = (ec_ref - self.total_BER_no_light) / ec_ref * 100  # improvement percentage compare to the reference

        if ip < 0:
            self.rating = "F"
            self.grade_value = -1
        elif ip < 10:
            self.rating = "E"
            self.grade_value = 0
        elif ip < 20:
            self.rating = "D"
            self.grade_value = 1
        elif ip < 25:
            self.rating = "C"
            self.grade_value = 2
        elif ip < 30:
            self.rating = "B"
            self.grade_value = 3
        elif ip < 35:
            self.rating = "A"
            self.grade_value = 4
        else:
            self.rating = "A+"
            self.grade_value = 5


