"""

"""
from honeybee.facetype import Wall, RoofCeiling
from honeybee.boundarycondition import Outdoors


class Mixin:

    def compute_lca(self, dic_configuration_to_test, lca_dic):
        """
        Compute the LCA of the building using the configuration file and the LCA database
        """

        # loop over the configuration id to find the proper one
        for configuration_id in dic_configuration_to_test.keys():
            # do the modification if the configuration correspond to the simulated building
            if configuration_id in self.name:
                for room in self.HB_model.rooms:
                    list_old_construction_sets = list(
                        dic_configuration_to_test[configuration_id]["construction_sets"].values)

                # check every room in the building
                for room in self.HB_model.rooms:
                    # loop over the construction sets
                    for initial_constr_set_id in dic_configuration_to_test[configuration_id][
                        "construction_sets"].keys():
                        # check what's the contruction set that was replaced
                        if room.properties.energy.construction_set.identifier == \
                                dic_configuration_to_test[configuration_id][
                                    "construction_sets"][initial_constr_set_id]["new_constr_set"]:
                            # loop over the surface type to replace
                            for surface_type in \
                                    dic_configuration_to_test[configuration_id]["construction_sets"][
                                        initial_constr_set_id][
                                        "surface_types"].values():
                                # compute the area for this surface type
                                area = 0.
                                for surface in room.faces:
                                    if surface_type == "roof" and isinstance(surface.type, Wall) and isinstance(
                                            surface.boundary_condition, Outdoors):
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
                                    initial_constr_set_id]["surface_types"][surface_type].values():
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
                                    self.carbon_footprint["standard"] = self.carbon_footprint["maxi"] + area * \
                                                                        lca_dic[initial_constr_set_id][surface_type][
                                                                            layer][
                                                                            alternative_number].standard_climate_change_overall
                                    print(surface_type,lca_dic[initial_constr_set_id][surface_type][
                                                                            layer][
                                                                            alternative_number].standard_climate_change_overall)

                            break
                break
