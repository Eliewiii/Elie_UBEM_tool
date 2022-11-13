"""
Additional methods for the Urban_canopy class.
Generate the geomatry and the LB/DF/HB objects of teh buildings
"""


class Mixin:

    def create_building_LB_geometry_footprint(self):
        """
        goes from list of points to Ladybug footprints for all the building_zon in the GIS, not only th simulated one
        """
        for i, id in enumerate(self.building_dict):
            self.building_dict[id].footprint_to_LB_face()

    # # # # # # # # # # # # # # # #       Dragonfly   # # # # # # # # # # # # # # # # # # # # #

    # def create_DF_building(self):
    #     """ goes from list of points to Ladybug geometry objects """
    #     for id in self.building_to_simulate:
    #         self.building_dict[id].LB_face_to_DF_building()

    def Apply_floor_layout(self):
        """ apply the layout of a given typology without adaption to the building_zon specificities """
        for id in self.building_to_simulate:
            self.building_dict[id].extract_face_typo()

    def LB_layout_to_DF_story(self):
        """ goes from layout in Ladybug 3Dface format to DF stories for all the buildings """
        for id in self.building_to_simulate:
            self.building_dict[id].LB_layout_to_DF_story()

    def DF_story_to_DF_building(self):
        """ goes from DF stories to DF Buildings for all the buildings """
        for id in self.building_to_simulate:
            self.building_dict[id].DF_story_to_DF_building()

    # # # # # # # # # # # # # # # #  Dragonfly without typology   # # # # # # # # # # # # # # # # # # # # #





    # # # # # # # # # # # # # # # #   Dragonfly to Honeybee   # # # # # # # # # # # # # # # # # # # # #

    def DF_to_HB(self):
        """ goes from list of points to Ladybug geometry objects """
        for id in self.building_to_simulate:
            self.building_dict[id].DF_building_to_HB_model()

    # # # # # # # # # # # # # # # #       Honeybee   # # # # # # # # # # # # # # # # # # # # #

    def HB_solve_adjacencies(self):
        """ Solve the adjacencies for all the buildings """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_solve_adjacencies()
            # self.building_dict[id].HB_model.to_hbjson("test", "D://Elie//PhD//Programming//")

    def HB_building_window_generation_floor_area_ratio(self):
        """ Generate windows on buildings according to a floor area % ratio on façade per direction  """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_building_window_generation_floor_area_ratio()

    def add_thermal_mass_int_wall(self):
        """ Add thermal mass to buildings """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_add_thermalmass_int_wall()

    def assign_conditioned_zone(self):
        """
        Assign an ideal hvac system for every apartment types rooms, turning them into conditioned zones for all buildings.
        """
        for id in self.building_to_simulate:
            self.building_dict[id].HB_assign_conditioned_zone()

    def assign_ideal_hvac_system(self, climate_zone=None, hvac_paramater_set=None):
        """
        Assign an ideal hvac system for every apartment types rooms, turning them into conditioned zones for all buildings.
        """
        ideal_air_system_obj=self.configure_ideal_hvac_system(climate_zone, hvac_paramater_set)
        for id in self.building_to_simulate:
            self.building_dict[id].HB_assign_ideal_hvac_system(ideal_air_system_obj)

    def add_infiltration_air_exchange(self, air_exchange_rate):
        """
        Add air infiltration exchange with a rate in volume per hour, Always_on schedule by default
        :param air_exchange_rate: float : air flow exchange rate with the exterior due to infiltration [vol/h]
        :return:
        """
        for id in self.building_to_simulate:
            self.building_dict[id].add_infiltration_air_exchange(air_exchange_rate)
