"""
Functions to generate modified EPW files (for EnergyPlus) considering the microclimate
"""

import dragonfly.building
import dragonfly.model
import honeybee


class Mixin:

    def hb_model_to_df_building(self):
        """ """
        self.df_building_uwg = dragonfly.building.Building.from_honeybee(self.HB_model)

    def apply_uwg_properties_to_df_building(self):
        """  """

        self.df_building_uwg.properties.uwg.program = self.uwg_program
        self.df_building_uwg.properties.uwg.vintage = self.vintage
        self.df_building_uwg.properties.uwg.fract_heat_to_canyon = self.fract_heat_to_canyon
        self.df_building_uwg.properties.uwg.shgc = self.shgc
        self.df_building_uwg.properties.uwg.wall_albedo = self.wall_albedo
        self.df_building_uwg.properties.uwg.roof_albedo = self.roof_albedo
        self.df_building_uwg.properties.uwg.roof_veg_fraction = self.roof_veg_fraction


