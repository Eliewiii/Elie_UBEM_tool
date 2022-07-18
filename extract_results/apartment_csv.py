BER_reference_values = {"A": {"top": 50.40, "middle": 40.08, "bottom": 34.35},
                        "B": {"top": 46.54, "middle": 38.87, "bottom": 30.66},
                        "C": {"top": 46.54, "middle": 38.87, "bottom": 30.66}, # to update in the future
                        "D": {"top": 46.54, "middle": 38.87, "bottom": 30.66}} # to update in the future

BER_ip_threshold_values = {"A": {"A": 46.54, "middle": 38.87, "bottom": 30.66},
                        "B": {"top": 46.54, "middle": 38.87, "bottom": 30.66},
                        "C": {"top": 46.54, "middle": 38.87, "bottom": 30.66}, # to update in the future
                        "D": {"top": 46.54, "middle": 38.87, "bottom": 30.66}} # to update in the future

class Apartment:

    def __init__(self, identifier, floor_number, apartment_number, building_obj):
        self.building_obj = building_obj
        ##
        self.identifier = identifier
        self.floor_number = floor_number
        self.apartment_number = apartment_number
        ##
        self.heating = {}
        self.cooling = {}
        self.lighting = {}
        self.equipment = {}
        ##
        self.total = None
        self.total_w_cop = None
        self.total_BER = None
        ## BER
        self.total_BER = None
        self.position = None
        self.is_core = self.is_core(identifier)
        self.rating = None
        self.grade_value = None
        ##
        self.area = None

    @classmethod
    def apartment_from_id(cls, identifier, building_obj):
        """
        """
        floor_number = int(identifier.split("_")[0][3:])
        apartment_number = int(identifier.split("_")[2])
        return (Apartment(identifier=identifier, floor_number=floor_number, apartment_number=apartment_number,
                          building_obj=building_obj))

    # def calculate_total_consumption(self):
    #
    #     self.heating["total"] = sum(self.heating["data"])

    def convert_to_kWh_per_sqrm(self):
        """

        """
        # conversion
        self.heating["data"] = [value / self.area / 3600 / 1000 for value in self.heating["data"]]
        self.cooling["data"] = [value / self.area / 3600 / 1000 for value in self.cooling["data"]]
        self.lighting["data"] = [value / self.area / 3600 / 1000 for value in self.lighting["data"]]
        self.equipment["data"] = [value / self.area / 3600 / 1000 for value in self.equipment["data"]]
        # compute total consumption
        self.heating["total"] = sum(self.heating["data"])
        self.cooling["total"] = sum(self.cooling["data"])
        self.lighting["total"] = sum(self.lighting["data"])
        self.equipment["total"] = sum(self.equipment["data"])
        self.total = self.heating["total"] + self.cooling["total"] + self.lighting["total"] + self.equipment["total"]
        # with COP
        cop_h = self.building_obj.cop_h
        cop_c = self.building_obj.cop_c
        self.heating["total_cop"] = sum(self.heating["data"]) / cop_h
        self.cooling["total_cop"] = sum(self.cooling["data"]) / cop_c
        self.total_w_cop = self.heating["total_cop"] + self.cooling["total_cop"] + self.lighting["total"] + \
                           self.equipment["total"]
        # BER
        self.total_BER = self.heating["total_cop"] + self.cooling["total_cop"] + self.lighting["total"]

    def rate_apartment(self,climate_zone_building):

        ec_ref = BER_reference_values[climate_zone_building][self.position]  # energy consumption of the reference
        ip = (ec_ref - self.total_BER) / ec_ref * 100  # improvement percentage compare to the reference

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

    # def rate_apartment(self,climate_zone_building):
    #
    #     ec_ref = BER_reference_values[climate_zone_building][self.position]  # energy consumption of the reference
    #     ip = (ec_ref - self.total_BER) / ec_ref * 100  # improvement percentage compare to the reference
    #
    #     if ip < 0:
    #         self.rating = "F"
    #         self.grade_value = -1
    #     elif ip < 10:
    #         self.rating = "E"
    #         self.grade_value = 0
    #     elif ip < 20:
    #         self.rating = "D"
    #         self.grade_value = 1
    #     elif ip < 25:
    #         self.rating = "C"
    #         self.grade_value = 2
    #     elif ip < 30:
    #         self.rating = "B"
    #         self.grade_value = 3
    #     elif ip < 35:
    #         self.rating = "A"
    #         self.grade_value = 4
    #     else:
    #         self.rating = "A+"
    #         self.grade_value = 5

    @staticmethod
    def is_core(apartment_identifier):
        """ check if the apartment is a core using the apartment identifier"""
        if "apartment".lower() in apartment_identifier.lower():
            return (False)
        else:
            return (True)
