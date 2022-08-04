"""
Functions to generate modified EPW files (for EnergyPlus) considering the microclimate
"""

import dragonfly.model

from dragonfly_uwg.simulation.parameter import UWGSimulationParameter
from dragonfly_uwg.run import run_uwg


class Mixin:

    def generate_local_epw_with_uwg(self, path_epw, path_folder_epw_uwg):
        """ """
        self.prepare_df_obj_for_uwg()
        self.add_uwg_properties_to_df_model_uwg()
        self.add_uwg_simulation_parameters()
        ## run UWG

        run_uwg(self.df_model_uwg, path_epw, self.parameter_uwg, path_folder_epw_uwg, silent=False)

    def prepare_df_obj_for_uwg(self):
        """ """
        self.hb_models_to_df_buildings()
        self.df_buildings_uwg_to_df_model()

    def hb_models_to_df_buildings(self):
        """ """
        for building_id in self.building_to_simulate:
            building_obj = self.building_dict[building_id]
            building_obj.hb_model_to_df_building()
            building_obj.apply_uwg_properties_to_df_building()

    def df_buildings_uwg_to_df_model(self):
        """ """
        df_building_uwg_list = []
        for building_id in self.building_to_simulate:
            building_obj = self.building_dict[building_id]
            df_building_uwg_list.append(building_obj.df_building_uwg)


        self.df_model_uwg = dragonfly.model.Model(identifier=f"{self.name}_uwg", buildings=df_building_uwg_list,
                                                  context_shades=None)  # context shade could be added from non-simulated buildings
        # the non simulated buildings could even be considered as DF buildings, need to test

    def add_uwg_properties_to_df_model_uwg(self):
        """ Assign the Terrain, Traffic, Tree Cover and Grass Cover of the area """
        None  # for now nothing to add here
        self.parameter_uwg = UWGSimulationParameter()

    def add_uwg_simulation_parameters(self):
        """ add parameters regarding the weather station and the urban boundary condition """
        None  # for now nothing to add here, too advanced
