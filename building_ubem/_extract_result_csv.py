"""
Additional methods for the Building class.
Used for extracting results from CSV
"""

from apartment.apartment import Apartment

from honeybee.model import Model


class Mixin:
    """
    """

    def set_path_csv_result_file(self, path_csv):
        """ Set the path to the result file of the building, so that it can extract it itself """
        self.path_csv = path_csv

    def extract_results_csv(self):
        """   """
        self.generate_apartment_obj()
        self.extract_consumption_csv()
        self.convert_unit_apartment_to_kWh_per_sqrm()
        self.compute_total_floor_area_apartment()
        self.check_apartment_position()
        self.rate_building()
        self.compute_energy_consumption()


    def generate_apartment_obj(self):
        """ Generate apartment objects that will be used for the result extraction and the Building Energy Rating """
        for room_obj in self.HB_model.rooms:
            apartment_obj = Apartment.apartment_from_hb_room(hb_room_obj=room_obj, building_obj=self)
            self.apartment_dict[apartment_obj.identifier] = apartment_obj



    def extract_consumption_csv(self):
        """ """
        with open(self.path_csv, 'r') as f:
            data_lines = f.readlines()  # 'lines' include every line from csv file with type 'list', the elements are 'str'
            data_table = [line.split(",") for line in data_lines]  # table with all the data
            row_0 = data_table[0]  # first row with the headings
            ## loop on every column/heading
            for i, column_heading in enumerate(row_0[1:]):  # we remove the first column that cointains only the name of each line
                cor_index = i + 1  # corrected index, to consider the first colum that is ignored
                #  from FLR1_APARTMENT_0 IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Supply Air Total Heating Energy [J](Monthly) to "Flr1_apartment_0"
                apartment_id = (column_heading.split(":")[0].split(" ")[0]).lower().capitalize()
                # identify the type of data in the column and then copy  the data  in the apartment_obj attribute
                if "Lights" in column_heading:
                    self.apartment_dict[apartment_id].lighting["data"] = [float(line[cor_index]) for line in data_table[
                                                                                                             1:]]  # list of the element in column i in very line of data_table, except first and last line
                elif "Equipment" in column_heading:
                    self.apartment_dict[apartment_id].equipment["data"] = [float(line[cor_index]) for line in
                                                                           data_table[1:]]
                elif "Cooling" in column_heading:
                    self.apartment_dict[apartment_id].cooling["data"] = [float(line[cor_index]) for line in
                                                                         data_table[1:]]
                elif "Heating" in column_heading:
                    self.apartment_dict[apartment_id].heating["data"] = [float(line[cor_index]) for line in
                                                                         data_table[1:]]

    def convert_unit_apartment_to_kWh_per_sqrm(self):
        """
        convert the consumption values of each apartment in kWh/m2
        """
        # convert in kW.h/m2
        for apartment_obj in self.apartment_dict.values():
            if apartment_obj.is_core == False:
                apartment_obj.convert_to_kWh_per_sqrm_and_sum_consumption()

    def check_apartment_position(self):
        """
        Check if the apartment are "top", "middle" or "bottom"
        """
        # check apartment position
        for apartment_obj in self.apartment_dict.values():
            if apartment_obj.floor_number == 1:
                apartment_obj.position = "bottom"
            elif apartment_obj.floor_number == self.num_floor:
                apartment_obj.position = "top"
            else:
                apartment_obj.position = "middle"

    def compute_total_floor_area_apartment(self):

        for apartment_obj in self.apartment_dict.values():
            if apartment_obj.is_core == False:
                self.apartment_area += apartment_obj.area

    def compute_energy_consumption(self):

        for apartment_obj in self.apartment_dict.values():
            if apartment_obj.is_core == False:
                self.energy_consumption["total_w_cop"] += apartment_obj.total_w_cop * apartment_obj.area / self.apartment_area
                self.energy_consumption["total_BER"] += apartment_obj.total_BER * apartment_obj.area / self.apartment_area
                self.energy_consumption["total_BER_no_light"] += apartment_obj.total_BER_no_light * apartment_obj.area / self.apartment_area

    def rate_building(self):

        for apartment_obj in self.apartment_dict.values():
            if apartment_obj.is_core == False:
                apartment_obj.rate_apartment(climate_zone_building=self.climate_zone)

        for apartment_obj in self.apartment_dict.values():
            if apartment_obj.is_core == False:
                self.grade_value += apartment_obj.grade_value * apartment_obj.area / self.apartment_area

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

    def generate_csv_in_individual_result_folder(self,path_to_result_folder):
        """ """


