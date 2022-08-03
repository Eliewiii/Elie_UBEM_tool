"""
Functions to generate modified EPW files (for EnergyPlus) considering the microclimate
"""

import dragonfly.building
import honeybee


class Mixin:
    def hb_model_to_df_building(self):
        """ """
        self.df_model = dragonfly.building.Building.from_honeybee(self.HB_model)

    def apply_uwg_properties_to_df_building(self):
        """  """

        self.df_model.properties.uwg.program = self.uwg_program
        self.df_model.properties.uwg.vintage = self.vintage
        self.df_model.properties.uwg.fract_heat_to_canyon = self.fract_heat_to_canyon
        self.df_model.properties.uwg.shgc = self.shgc
        self.df_model.properties.uwg.wall_albedo = self.wall_albedo
        self.df_model.properties.uwg.roof_albedo = self.roof_albedo
        self.df_model.properties.uwg.roof_veg_fraction = self.roof_veg_fraction
