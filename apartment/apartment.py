"""
Apartment class, representing a thermal zone.
Only used (for now) for building energy rating and result extraction
"""
from apartment import _ber



apartment_types = ["ground", "over_open_space", "over_unheated", "under_unheated", "between_unheated", "unheated",
                   "middle", "top"]


class Apartment(_ber.Mixin):

    def __init__(self, identifier, hb_room_obj, floor_number, apartment_number):
        # self.building_obj = building_obj
        ##
        self.identifier = identifier
        self.hb_room_obj = hb_room_obj  # the HB_room object it belongs to
        self.hb_room_dict = None        # the HB_room dictionary (to switch between dict
                                        # and object to be able to "pickle" it)
        self.floor_number = floor_number  # the number of the floor the apartment is in
        self.apartment_number = apartment_number  # the number of apartment in the floor
        ##
        self.heating = {}  # dictionary with "data", the list of al the values (daily/monthly/yearly?)
        self.cooling = {}
        self.lighting = {}
        self.equipment = {}
        ## BER
        self.total = None               # heating, cooling, equipment and lighting
        self.total_w_cop = None         # heating, cooling, equipment and lighting considering the COP
        self.total_BER_light = None           # heating, cooling and lighting considering the COP
        self.total_BER_no_light = None  # only heating and cooling considering the COP
        self.position = None            # if top floor, middle floor or groundfloor
        self.is_core = self.is_core(identifier)
        self.rating = None              # apartment rating (A+, A, B, C ...)
        self.grade_value = None         # grade of the apartment (-1, 0, 1, 2 ...)
        ##
        self.area = None                # floor area

    @classmethod
    def apartment_from_hb_room(cls, hb_room_obj):
        """
        Create the apartment object from a hb_room obj
        """
        identifier = hb_room_obj.identifier
        floor_number = int(identifier.split("_")[0][3:])
        apartment_number = int(identifier.split("_")[2])
        return (Apartment(identifier=identifier, hb_room_obj=hb_room_obj, floor_number=floor_number,
                          apartment_number=apartment_number))


    def get_floor_area(self):
        """ get the floor area of the apartment  """
        self.area = self.hb_room_obj.floor_area

    def convert_to_kWh_per_sqrm_and_sum_consumption(self, cop_h=3.,cop_c=3.):
        """ Convert the energy consumption in KwH/m2 """
        # get floor area
        self.get_floor_area()
        # conversion from joules to kWh/m2
        self.heating["data"] = [value / self.area / 3600. / 1000. for value in self.heating["data"]]
        self.cooling["data"] = [value / self.area / 3600. / 1000. for value in self.cooling["data"]]
        self.lighting["data"] = [value / self.area / 3600. / 1000. for value in self.lighting["data"]]
        self.equipment["data"] = [value / self.area / 3600. / 1000. for value in self.equipment["data"]]
        # compute total consumption
        self.heating["total"] = sum(self.heating["data"])
        self.cooling["total"] = sum(self.cooling["data"])
        self.lighting["total"] = sum(self.lighting["data"])
        self.equipment["total"] = sum(self.equipment["data"])
        self.total = self.heating["total"] + self.cooling["total"] + self.lighting["total"] + self.equipment["total"]
        # with COP
        self.heating["total_cop"] = sum(self.heating["data"]) / cop_h
        self.cooling["total_cop"] = sum(self.cooling["data"]) / cop_c
        self.total_w_cop = self.heating["total_cop"] + self.cooling["total_cop"] + self.lighting["total"] + \
                           self.equipment["total"]
        # BER
        self.total_BER_light = self.heating["total_cop"] + self.cooling["total_cop"] + self.lighting["total"]
        self.total_BER_no_light = self.heating["total_cop"] + self.cooling["total_cop"]



    @staticmethod
    def is_core(apartment_identifier):
        """ check if the apartment is a core using the apartment identifier"""
        if "apartment".lower() in apartment_identifier.lower():
            return (False)
        else:
            return (True)
