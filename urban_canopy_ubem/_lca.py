"""


"""


class Mixin:

    def convert_carbon_footprint_kwh_per_m2_eq_compare_to_ref(self, conversion_rate, life_time):
        """


        """
        # Find reference building
        reference_building = None
        for id in self.building_to_simulate:
            building_obj = self.building_dict[id]
            if building_obj.is_reference:
                reference_building = building_obj
                break
        # only consider the conditioned zone floor area here, but still consider the whole building, not just the LCA of conditionned areas
        lca_max_ref = reference_building.carbon_footprint["maxi"] / reference_building.apartment_area * conversion_rate
        lca_min_ref = reference_building.carbon_footprint["mini"] / reference_building.apartment_area * conversion_rate

        # loop over the buildings
        for id in self.building_to_simulate:
            building_obj = self.building_dict[id]
            # conversion in kwh/m2/year
            building_obj.carbon_footprint_kwh_per_m2_eq_per_year["maxi"] = building_obj.carbon_footprint[
                                                                               "maxi"] / building_obj.apartment_area * conversion_rate / life_time
            building_obj.carbon_footprint_kwh_per_m2_eq_per_year["standard"] = building_obj.carbon_footprint[
                                                                                   "standard"] / building_obj.apartment_area * conversion_rate / life_time
            building_obj.carbon_footprint_kwh_per_m2_eq_per_year["mini"] = building_obj.carbon_footprint[
                                                                               "mini"] / building_obj.apartment_area * conversion_rate / life_time
            # conversion in kwh/m2 per year compared to ref
            building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["maxi"] = -(lca_min_ref - \
                                                                                  building_obj.carbon_footprint[
                                                                                      "maxi"] / building_obj.apartment_area * conversion_rate)/ life_time
            building_obj.carbon_footprint_kwh_per_m2_eq_per_year_compared_to_ref["mini"] = (lca_max_ref - \
                                                                                  building_obj.carbon_footprint[
                                                                                      "mini"] / building_obj.apartment_area * conversion_rate)/ life_time


    def compute_consumption_compared_to_ref(self):
        """

        """
        reference_building = None
        for id in self.building_to_simulate:
            building_obj = self.building_dict[id]
            if building_obj.is_reference:
                reference_building = building_obj
                break
        tot_h_cop_ref = reference_building.energy_consumption["total_h_cop"]
        tot_c_cop_ref = reference_building.energy_consumption["total_c_cop"]
        tot_ber_ref = reference_building.energy_consumption["total_BER_no_light"]

        for id in self.building_to_simulate:
            building_obj = self.building_dict[id]

            building_obj.energy_consumption["total_BER_compared_to_ref"] = tot_ber_ref - \
                                                                           building_obj.energy_consumption[
                                                                               "total_BER_no_light"]
            building_obj.energy_consumption["total_h_cop_compared_to_ref"] = tot_h_cop_ref - \
                                                                             building_obj.energy_consumption[
                                                                                 "total_h_cop"]
            building_obj.energy_consumption["total_c_cop_compared_to_ref"] = tot_c_cop_ref - \
                                                                             building_obj.energy_consumption[
                                                                                 "total_c_cop"]

    # def compute_consumption_improvement_lca(self):
    #     """
    #     Compute the overall improvement in terms of both LCA and energy consumption compared to the reference
    #     """
    #     reference_building = None
    #     for id in self.building_to_simulate:
    #         building_obj = self.building_dict[id]
    #         if building_obj.is_reference:
    #             reference_building = building_obj
    #             break
    #     tot_ber_ref = reference_building.energy_consumption["total_BER_no_light"]
    #     lca_ref_max= reference_building.carbon_footprint_kwh_per_m2_eq_per_year["maxi"]
    #     lca_ref_standard = reference_building.carbon_footprint_kwh_per_m2_eq_per_year["standard"]
    #     lca_ref_min = reference_building.carbon_footprint_kwh_per_m2_eq_per_year["mini"]
    #
    #     for id in self.building_to_simulate:
    #         building_obj = self.building_dict[id]
    #         if building_obj.is_reference==False:
    #             building_obj.improvement_lca_in_percent["maxi"]= 1-(building_obj.energy_consumption["total_BER_no_light"] + building_obj.carbon_footprint_kwh_per_m2_eq_per_year["mini"])/(tot_ber_ref+lca_ref_max)
    #             building_obj.improvement_lca_in_percent["standard"]= 1-(building_obj.energy_consumption["total_BER_no_light"] + building_obj.carbon_footprint_kwh_per_m2_eq_per_year["standard"])/(tot_ber_ref+lca_ref_standard)
    #             building_obj.improvement_lca_in_percent["mini"]= 1-(building_obj.energy_consumption["total_BER_no_light"] + building_obj.carbon_footprint_kwh_per_m2_eq_per_year["maxi"])/(tot_ber_ref+lca_ref_mini)
    #
