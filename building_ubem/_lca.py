"""

"""
from honeybee.facetype import Wall, RoofCeiling
from honeybee.boundarycondition import Outdoors, Ground
from os.path import join
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Mixin:

    def compute_lca(self, dic_configuration_to_test, lca_dic):
        """
        Compute the LCA of the building using the configuration file and the LCA database
        """

        # loop over the configuration id to find the proper one
        for configuration_id in dic_configuration_to_test.keys():
            # do the modification if the configuration correspond to the simulated building
            if configuration_id in self.name:
                # check every room in the building
                for room in self.HB_model.rooms:
                    # loop over the construction sets
                    for initial_constr_set_id in dic_configuration_to_test[configuration_id][
                        "construction_sets"].keys():
                        # check what's the contruction set that was replaced
                        if room.properties.energy.construction_set.identifier == \
                                dic_configuration_to_test[configuration_id][
                                    "construction_sets"][initial_constr_set_id]["new_const_set"]:
                            # loop over the surface type to replace
                            for surface_type in \
                                    dic_configuration_to_test[configuration_id]["construction_sets"][
                                        initial_constr_set_id][
                                        "surface_types"].keys():
                                # compute the area for this surface type
                                area = 0.
                                for surface in room.faces:
                                    if surface_type == "roof" and isinstance(surface.type, RoofCeiling) and isinstance(
                                            surface.boundary_condition, Outdoors) :
                                        area += surface.area - surface.aperture_area
                                    elif surface_type == "ext_wall" and isinstance(surface.type, Wall) and isinstance(
                                            surface.boundary_condition,
                                            Outdoors):
                                        area += surface.area - surface.aperture_area

                                    elif surface_type == "windows" and isinstance(surface.type, Wall) and isinstance(
                                            surface.boundary_condition,
                                            Outdoors):
                                        area += surface.aperture_area
                                # loop over the layers
                                for layer in dic_configuration_to_test[configuration_id]["construction_sets"][
                                    initial_constr_set_id]["surface_types"][surface_type].keys():
                                    # get the number of the alternative
                                    alternative_number = \
                                        dic_configuration_to_test[configuration_id]["construction_sets"][
                                            initial_constr_set_id]["surface_types"][surface_type][layer]

                                    self.carbon_footprint["mini"] = self.carbon_footprint["mini"] + area * \
                                                                    lca_dic[initial_constr_set_id][surface_type][layer][
                                                                        alternative_number].min_climate_change_overall
                                    self.carbon_footprint["maxi"] = self.carbon_footprint["maxi"] + area * \
                                                                    lca_dic[initial_constr_set_id][surface_type][layer][
                                                                        alternative_number].max_climate_change_overall
                                    self.carbon_footprint["standard"] = self.carbon_footprint["standard"] + area * \
                                                                        lca_dic[initial_constr_set_id][surface_type][
                                                                            layer][
                                                                            alternative_number].standard_climate_change_overall
                                    # print(room.identifier,surface_type,lca_dic[initial_constr_set_id][surface_type][
                                    #                                         layer][
                                    #                                         alternative_number].standard_climate_change_overall,area)

                            break
                break

    def convert_carbon_footprint_kwh_per_m2_eq_compare_to_ref(self,conversion_rate):
        """


        """
        reference_building = None


    # def generate_graph_result(self, path_folder_building_simulation):
    #     """
    #
    #     """
    #     fig, ax = plt.subplots()
    #     width = 0.3
    #     bar_location = -0.1
    #     model = []           # A list in the form of ["Building_1", "Building_2",...]
    #     x_position_bar = []  # A list used to record the location of the center of bar for each building in the graph
    #
    #     for building_id in self.building_to_simulate:
    #         building_obj = self.building_dict[building_id]
    #         model.append(building_obj.name)
    #         bar_location += 1.1
    #         x_position_bar.append(bar_location)
    #         heating_bar = ax.bar(bar_location - width, building_obj.energy_consumption["tot_h_cop_compared_to_ref"],
    #                              width, color="red", label="heating", zorder=10)
    #         cooling_bar = ax.bar(bar_location - width, building_obj.energy_consumption["tot_c_cop_compared_to_ref"],
    #                              width, color="blue",
    #                              bottom=building_obj.energy_consumption["tot_h_cop_compared_to_ref"],
    #                              label="cooling", zorder=10)
    #         carbon_ftp_bar = ax.bar(bar_location,
    #                                 building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["mini"] -
    #                                 building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["maxi"],
    #                                 width, color="green",
    #                                 bottom=building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["maxi"],
    #                                 label="carbon footprint", zorder=10)
    #         tot_impact_bar = ax.bar(bar_location + width,
    #                                 building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["mini"] -
    #                                 building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["maxi"],
    #                                 width, color="green",
    #                                 bottom=building_obj.energy_consumption["tot_BER_compared_to_ref"],
    #                                 label="total environmental impact", zorder=10)
    #         if bar_location == 1:
    #             ax.legend()
    #     ax.set_xticks(x_position_bar, labels=model)
    #     ax.set_ylabel("Environmental impact in KWh/m2 compared to reference")
    #
    #     fig.tight_layout()
    #     plt.savefig(join(path_folder_building_results, "graph.png"))
    #     plt.show()

