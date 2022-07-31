from apartment_csv import Apartment

from honeybee.model import Model


class Building:
    """
 """

    def __init__(self, building_number_arg, simulation_name_arg, path_csv_arg, path_hbjson_arg, results_obj_arg):
        """Initialize a building"""
        self.number = building_number_arg
        self.simulation_name = simulation_name_arg
        self.path_csv = path_csv_arg
        self.results_obj = results_obj_arg
        self.path_model_json = path_hbjson_arg

        self.identifier = "Building_{}_Simulation_{}".format(str(self.number), self.simulation_name)

        self.num_floor = 0

        #
        self.dict_apartment = {}

        self.cop_c = 3.  # in the future might be extracted from somewhere
        self.cop_h = 3.  # in the future might be extracted from somewhere

        # Energy consumption
        self.total_w_cop = 0

        ## BER
        self.total_BER_no_light = 0
        self.total_BER = 0
        self.climate_zone = "A"
        self.apartment_area = 0
        self.rating = None
        self.grade_value = 0

    @classmethod
    def create_building_object_and_extract_csv(cls, results_obj, building_name, simulation_name, path_csv,
                                               path_hbjson_arg):
        """  create a building object from geometry in a shapefile """
        building_number = int(building_name.split("_")[1])  # 'Building_1'
        ## create the building object
        building_csv_obj = cls(building_number_arg=building_number, simulation_name_arg=simulation_name,
                               path_csv_arg=path_csv, results_obj_arg=results_obj, path_hbjson_arg=path_hbjson_arg)

        ## Tell the results class that there is a new building
        building_csv_obj.results_obj.list_building.append(building_csv_obj.identifier)
        building_csv_obj.results_obj.dict_building[building_csv_obj.identifier] = building_csv_obj
        ## identify apartment, create them and extract results
        building_csv_obj.identify_apartments_and_extract_results()
        building_csv_obj.convert_to_kWh_per_sqrm()
        building_csv_obj.compute_total_floor_area_apartment()
        building_csv_obj.check_apartment_position()
        building_csv_obj.rate_building()
        building_csv_obj.compute_energy_consumption()

    def identify_apartments_and_extract_results(self):

        with open(self.path_csv, 'r') as f:
            data_lines = f.readlines()  # 'lines' include every line from csv file with type 'list', the elements are 'str'
            data_table = [line.split(",") for line in data_lines]  # table with all the data
            row_0 = data_table[0]  # first row with the headings
            ## loop on every column/heading
            for i, column_heading in enumerate(row_0[1:]):  # we remove the first co
                cor_index = i + 1  # corrected index, to consider the first colum that is ignored
                apartment_id = (column_heading.split(":")[0].split(" ")[0]).lower().capitalize()  # "Flr1_apartment_0"
                # create apartment if it does not exist already
                if apartment_id not in self.dict_apartment:
                    self.dict_apartment[apartment_id] = Apartment.apartment_from_id(identifier=apartment_id,
                                                                                    building_obj=self)
                # identify the type of data in the column and then copy  the data  in the apartment_obj attribute
                if "Lights" in column_heading:
                    self.dict_apartment[apartment_id].lighting["data"] = [float(line[cor_index]) for line in data_table[
                                                                                                             1:]]  # list of the element in column i in very line of data_table, except first and last line
                elif "Equipment" in column_heading:
                    self.dict_apartment[apartment_id].equipment["data"] = [float(line[cor_index]) for line in
                                                                           data_table[1:]]
                elif "Cooling" in column_heading:
                    self.dict_apartment[apartment_id].cooling["data"] = [float(line[cor_index]) for line in
                                                                         data_table[1:]]
                elif "Heating" in column_heading:
                    self.dict_apartment[apartment_id].heating["data"] = [float(line[cor_index]) for line in
                                                                         data_table[1:]]

    def convert_to_kWh_per_sqrm(self):
        """
        convert the consumption values of each apartment in kWh/m2
        """
        # extract apartment floor area from the hbjson file, containing th model
        hb_model = Model.from_file(self.path_model_json)
        for room in hb_model.rooms:
            self.dict_apartment[room.identifier].area = room.floor_area
        # convert in kW.h/m2
        for apartment_obj in self.dict_apartment.values():
            if apartment_obj.is_core == False:
                apartment_obj.convert_to_kWh_per_sqrm()

    def check_apartment_position(self):
        """
        Find the number of floors of the building and then check if the apartment are "top", "middle" or "bottom"
        """
        # Find the number of floors of the building
        for apartment_obj in self.dict_apartment.values():
            if apartment_obj.floor_number > self.num_floor:
                self.num_floor = apartment_obj.floor_number

        # check apartmen position
        for apartment_obj in self.dict_apartment.values():
            if apartment_obj.floor_number == 1:
                apartment_obj.position = "bottom"
            elif apartment_obj.floor_number == self.num_floor:
                apartment_obj.position = "top"
            else:
                apartment_obj.position = "middle"

    def compute_total_floor_area_apartment(self):

        for apartment_obj in self.dict_apartment.values():
            if apartment_obj.is_core == False:
                self.apartment_area += apartment_obj.area

    def rate_building(self):

        for apartment_obj in self.dict_apartment.values():
            if apartment_obj.is_core == False:
                apartment_obj.rate_apartment(climate_zone_building=self.climate_zone)

        for apartment_obj in self.dict_apartment.values():
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

    def compute_energy_consumption(self):

        for apartment_obj in self.dict_apartment.values():
            if apartment_obj.is_core == False:
                self.total_w_cop += apartment_obj.total_w_cop * apartment_obj.area / self.apartment_area
                self.total_BER += apartment_obj.total_BER * apartment_obj.area / self.apartment_area
                self.total_BER_no_light += apartment_obj.total_BER_no_light * apartment_obj.area / self.apartment_area
