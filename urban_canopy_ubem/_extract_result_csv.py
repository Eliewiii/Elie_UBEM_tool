"""
Additional methods for the Urban_canopy class.
Deals with the result extraction, here csv files
"""
from os.path import join
from building_ubem.building import Building
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

    def write_global_csv_results(self, file_path):
        """ Write a global csv result file in the Simulation/Result folder for all the simulations """
        with open(file_path, 'w') as csvfile:
            csvfile.write(
                "Building,Heating (COP) [kWh/m2],Colling (COP) [kWh/m2],Total (COP) [kWh/m2],Total BER [kWh/m2],Rating\n")
            for building_id in self.building_to_simulate:
                building_obj = self.building_dict[building_id]
                csvfile.write("{},{},{},{},{},{}\n".format(
                    building_obj.name,
                    round(building_obj.energy_consumption["total_h_cop"], 2),
                    round(building_obj.energy_consumption["total_c_cop"], 2),
                    round(building_obj.energy_consumption["total_w_cop"], 2),
                    round(building_obj.energy_consumption["total_BER_no_light"], 2),
                    building_obj.rating))

    def write_global_csv_results_with_lca(self, file_path):
        """ Write a global csv result file in the Simulation/Result folder for all the simulations """
        with open(file_path, 'w') as csvfile:
            csvfile.write(
                "Building,Heating (COP) [kWh/m2],Cooling (COP) [kWh/m2],Total (COP) [kWh/m2],Total BER [kWh/m2],Rating,Climate Change min [kWh/m2/year eq],Climate Change standard [kWh/m2/year eq],Climate Change max [kWh/m2/year eq]\n")
            for building_id in self.building_to_simulate:
                building_obj = self.building_dict[building_id]
                csvfile.write("{},{},{},{},{},{},{},{},{}\n".format(
                    building_obj.name,
                    round(building_obj.energy_consumption["total_h_cop"], 2),
                    round(building_obj.energy_consumption["total_c_cop"], 2),
                    round(building_obj.energy_consumption["total_w_cop"], 2),
                    round(building_obj.energy_consumption["total_BER_no_light"], 2),
                    building_obj.rating,
                    round(building_obj.carbon_footprint_kwh_per_m2_eq_per_year["mini"], 4),
                    round(building_obj.carbon_footprint_kwh_per_m2_eq_per_year["standard"], 4),
                    round(building_obj.carbon_footprint_kwh_per_m2_eq_per_year["maxi"], 4)))

    def write_csv_results_in_building_folder(self, path_folder_building_simulation):
        """ determine the path for the results of each building and write the results in each building file """
        # todo : loop for all the buildings, get the pass to building_??\Results and write the csv
        ###heat_bar = []
        for building_id in self.building_to_simulate:
            building_obj = self.building_dict[building_id]

            ### to test the data in temporary
            ###heat_bar.append(building_obj.energy_consumption["total_h_cop_compared_to_ref"])

            path_to_building_folder = join(path_folder_building_simulation, building_obj.name)
            path_to_result_folder = join(path_to_building_folder, "Results")
            building_obj.generate_csv_in_individual_result_folder(path_to_result_folder)

        ## in temprary only for test
        ###return heat_bar

    def generate_graph_result(self, path_folder_building_results):
        """

        """
        fig, ax = plt.subplots()
        width = 0.2
        bar_location = 0
        model = []           # A list in the form of ["Building_1", "Building_2",...]
        x_position_bar = []  # A list used to record the location of the center of bar for each building in the graph

        for building_id in self.building_to_simulate:
            building_obj = self.building_dict[building_id]
            model.append(building_obj.name[-8:])
            bar_location += 1
            x_position_bar.append(bar_location)
            heating_bar = ax.bar(bar_location - width, building_obj.energy_consumption["total_h_cop_compared_to_ref"],
                                 width, color="red", label="heating", zorder=10)
            cooling_bar = ax.bar(bar_location - width, building_obj.energy_consumption["total_c_cop_compared_to_ref"],
                                 width, color="blue",
                                 bottom=building_obj.energy_consumption["total_h_cop_compared_to_ref"],
                                 label="cooling", zorder=10)
            #carbon_ftp_bar = ax.bar(bar_location,
                                    #building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["mini"] -
                                    #building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["maxi"],
                                    #width, color="green",
                                    #bottom=building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["maxi"],
                                    #label="carbon footprint", zorder=10)
            carbon_ftp_bar = ax.bar(bar_location,
                                    -building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["mini"]+
                                    building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["maxi"],
                                    width, color="green",
                                    bottom=building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["mini"],
                                    label="carbon footprint", zorder=10)

            #tot_impact_bar = ax.bar(bar_location + width,
                                    #building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["mini"] -
                                    #building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["maxi"],
                                    #width, color="orange",
                                    #bottom=building_obj.energy_consumption["total_BER_compared_to_ref"] +
                                    #building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["maxi"],
                                    #label="total environmental impact", zorder=10)
            tot_impact_bar = ax.bar(bar_location + width,
                                    -building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["mini"] +
                                    building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["maxi"],
                                    width, color="orange",
                                    bottom=building_obj.energy_consumption["total_BER_compared_to_ref"] +
                                           building_obj.carbon_footprint_kwh_per_m2_eq_per_year_improvement_compared_to_ref["mini"],
                                    label="total environmental impact", zorder=10)
            if bar_location == 1:
                ax.legend()
        ax.set_xticks(x_position_bar, labels=model)
        # ax.set_xticks(x_position_bar)

        ax.set_ylabel("Environmental impact in KWh/m2 compared to reference")
        plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
        fig.tight_layout()
        plt.savefig(join(path_folder_building_results, "graph.png"))
        plt.show()



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
