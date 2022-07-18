import os
from building_csv import Building


class Results:
    """
    """

    def __init__(self):
        """Initialize a building"""
        self.list_building = []
        self.dict_building = {}
        self.list_simulation = []

    def extract_csv(self, path_folder_simulations):
        ##listdir etc...
        simulation_list = os.listdir(path_folder_simulations)

        for simulation in simulation_list:
            self.list_simulation.append(simulation)
            path_folder_buildings = os.path.join(path_folder_simulations, simulation, "Buildings")

            building_list = os.listdir(path_folder_buildings)
            for building in building_list:
                path_csv_results_file = os.path.join(path_folder_buildings, building, "osw", "run", "eplusout.csv")
                path_model_hbjson = os.path.join(path_folder_buildings, building, "model_json", "in.hbjson")
                Building.create_building_object_and_extract_csv(results_obj=self, building_name=building,
                                                                simulation_name=simulation,
                                                                path_csv=path_csv_results_file,
                                                                path_hbjson_arg=path_model_hbjson)

    def print_total_results(self):

        for building in self.dict_building:
            building_obj = self.dict_building[building]
            print(building_obj.identifier + ":")
            for apartment in building_obj.dict_apartment:
                apartment_obj = building_obj.dict_apartment[apartment]
                print("\t {} : {} kWh/m2".format(apartment_obj.identifier, str(apartment_obj.total)[:4]))

    def print_detailed_results(self):

        for building in self.dict_building:
            building_obj = self.dict_building[building]
            print(building_obj.identifier + ":")
            for apartment in building_obj.dict_apartment:
                apartment_obj = building_obj.dict_apartment[apartment]
                if apartment_obj.is_core == False:
                    print("\t {} : h={}, c={}, l={}, e={}, tot={} kWh/m2, {}m2".format(apartment_obj.identifier,
                                                                                 str(apartment_obj.heating["total"])[
                                                                                 :3],
                                                                                 str(apartment_obj.cooling["total"])[
                                                                                 :3],
                                                                                 str(apartment_obj.lighting["total"])[
                                                                                 :3],
                                                                                 str(apartment_obj.equipment["total"])[
                                                                                 :3],
                                                                                 str(apartment_obj.total)[:3],apartment_obj.area ))

    def print_detailed_results_with_COP(self):

        for building in self.dict_building:
            building_obj = self.dict_building[building]
            print(building_obj.identifier + ":")
            for apartment in building_obj.dict_apartment:
                apartment_obj = building_obj.dict_apartment[apartment]
                if apartment_obj.is_core == False:
                    print("\t {} : h_cop={}, c_cop={}, l={}, e={}, tot_cop={} kWh/m2".format(
                        apartment_obj.identifier,
                        str(apartment_obj.heating["total_cop"])[:3],
                        str(apartment_obj.cooling["total_cop"])[:3],
                        str(apartment_obj.lighting["total"])[:3],
                        str(apartment_obj.equipment["total"])[:3],
                        str(apartment_obj.total_w_cop)[:3]))

    def print_detailed_results_BER(self, apartment_details=False):

        for building in self.dict_building:
            building_obj = self.dict_building[building]
            print( "{} : rating={}, tot_cop={}kWh/m2,tot_ber={}kWh/m2 ".format(building_obj.identifier,building_obj.rating,str(building_obj.total_w_cop)[:5],str(building_obj.total_BER)[:5]))
            if apartment_details :
                for apartment in building_obj.dict_apartment:
                    apartment_obj = building_obj.dict_apartment[apartment]
                    if apartment_obj.is_core == False:
                        print("\t {} : h_cop={}, c_cop={}, l={}, tot_ber={} kWh/m2, rating={} kWh/m2".format(
                            apartment_obj.identifier,
                            str(apartment_obj.heating["total_cop"])[:3],
                            str(apartment_obj.cooling["total_cop"])[:3],
                            str(apartment_obj.lighting["total"])[:3],
                            str(apartment_obj.total_BER)[:6],
                            str(apartment_obj.rating)))

