"""
Additional methods for the Urban_canopy class.
Deals with the result extraction, here csv files
"""
from os.path import join
from building_ubem.building import Building


class Mixin:

    def set_building_path_csv_result_file(self, path_folder_building_simulation):
        """  """
        for building_id in self.building_to_simulate:
            building_obj = self.building_dict[building_id]
            path_to_csv = join(path_folder_building_simulation, building_obj.name, "EnergyPlus_simulation", "run",
                               "eplusout.csv")
            building_obj.set_path_csv_result_file(path_csv=path_to_csv)

    def extract_building_csv_results(self, path_folder_building_simulation):
        """  """

        # Set the path to the csv file of each building
        self.set_building_path_csv_result_file(path_folder_building_simulation)

        for building_id in self.building_to_simulate:
            building_obj = self.building_dict[building_id]
            building_obj.extract_results_csv()


    def write_csv_results_in_building_folder(self,path_folder_building_simulation):
        """ determine the path for the results of each building and write the results in each building file """
        # todo : loop for all the buildings, get the pass to building_??\Results and write the csv
        for building_id in self.building_to_simulate:
            print("in building")
            building_obj = self.building_dict[building_id]
            path_to_building_folder = join(path_folder_building_simulation, building_obj.name)
            path_to_result_folder = join(path_to_building_folder, "Results")
            building_obj.generate_csv_in_individual_result_folder(path_to_result_folder,building_obj)



    # def print_total_results(self):
    #
    #     for building_id in self.building_to_simulate:
    #         building_obj = self.building_dict[building_id]
    #         print(building_obj.identifier + ":")
    #         for apartment in building_obj.dict_apartment:
    #             apartment_obj = building_obj.dict_apartment[apartment]
    #             print("\t {} : {} kWh/m2".format(apartment_obj.identifier, str(apartment_obj.total)[:4]))
    #
    # def print_detailed_results(self):
    #
    #     for building_id in self.building_to_simulate:
    #         building_obj = self.building_dict[building_id]
    #         print(building_obj.identifier + ":")
    #         for apartment in building_obj.dict_apartment:
    #             apartment_obj = building_obj.dict_apartment[apartment]
    #             if apartment_obj.is_core == False:
    #                 print("\t {} : h={}, c={}, l={}, e={}, tot={} kWh/m2, {}m2".format(apartment_obj.identifier,
    #                                                                                    str(apartment_obj.heating[
    #                                                                                            "total"])[
    #                                                                                    :3],
    #                                                                                    str(apartment_obj.cooling[
    #                                                                                            "total"])[
    #                                                                                    :3],
    #                                                                                    str(apartment_obj.lighting[
    #                                                                                            "total"])[
    #                                                                                    :3],
    #                                                                                    str(apartment_obj.equipment[
    #                                                                                            "total"])[
    #                                                                                    :3],
    #                                                                                    str(apartment_obj.total)[:3],
    #                                                                                    apartment_obj.area))
    #
    # def print_detailed_results_with_COP(self):
    #
    #     for building_id in self.building_to_simulate:
    #         building_obj = self.building_dict[building_id]
    #         print(building_obj.identifier + ":")
    #         for apartment in building_obj.dict_apartment:
    #             apartment_obj = building_obj.dict_apartment[apartment]
    #             if apartment_obj.is_core == False:
    #                 print("\t {} : h_cop={}, c_cop={}, l={}, e={}, tot_cop={} kWh/m2".format(
    #                     apartment_obj.identifier,
    #                     str(apartment_obj.heating["total_cop"])[:3],
    #                     str(apartment_obj.cooling["total_cop"])[:3],
    #                     str(apartment_obj.lighting["total"])[:3],
    #                     str(apartment_obj.equipment["total"])[:3],
    #                     str(apartment_obj.total_w_cop)[:3]))

    def print_detailed_results_BER(self, apartment_details=False):

        for building_id in self.building_to_simulate:
            building_obj = self.building_dict[building_id]
            print("{} : rating={}, tot_cop={}kWh/m2,tot_ber={}kWh/m2 ".format(building_obj.name,
                                                                              building_obj.rating,
                                                                              round(building_obj.energy_consumption[
                                                                                        "total_w_cop"], 3),
                                                                              round(building_obj.energy_consumption[
                                                                                        "total_BER_no_light"], 3)))
            if apartment_details:
                for apartment_obj in building_obj.apartment_dict.values():
                    if apartment_obj.is_core == False:
                        print("\t {} : h_cop={}, c_cop={}, tot_ber_no_light={} kWh/m2, rating={} kWh/m2".format(
                            apartment_obj.identifier,
                            round(apartment_obj.heating["total_cop"], 3),
                            round(apartment_obj.cooling["total_cop"], 3),
                            round(apartment_obj.total_BER_no_light, 3),
                            apartment_obj.rating))
