"""
To generate samples and test functions
"""

from building_ubem.building import Building


class Mixin:

    @classmethod
    def generate_sample_one_building(cls, path_folder_typology):
        """ """
        u_c_obj = cls("sample_urban_canopy")
        u_c_obj.load_typologies(path_folder_typology)
        Building.generate_sample_one_building(u_c_obj)

        u_c_obj.select_target_building([0])
        ## Create Ladybug geometries with GIS footprint
        u_c_obj.create_building_LB_geometry_footprint()
        ## Create HB room envelop with GIS footprint
        u_c_obj.create_building_HB_room_envelop()
        u_c_obj.building_dict[0].typology = u_c_obj.typology_dict["BER_ref_A_south"]
        # convert to DF stories and buildings
        u_c_obj.create_DF_building_according_to_typology()
        # convert to HB model
        u_c_obj.generate_HB_model()
        # U_c.convert_DF_building_to_HB_models()
        u_c_obj.HB_solve_adjacencies()
        # %% DF + HB modeling using GIS data + typology
        u_c_obj.assign_conditioned_zone()
        # add Ideal HVAC system
        u_c_obj.assign_ideal_hvac_system(climate_zone="A", hvac_paramater_set="team_design_builder")
        # create windows
        u_c_obj.HB_building_window_generation_floor_area_ratio()
        # add shades
        u_c_obj.add_context_surfaces_to_HB_model()
        # assign constructions, loads etc...
        u_c_obj.apply_buildings_characteristics()
        # Add infiltration in volume per hour
        u_c_obj.add_infiltration_air_exchange(air_exchange_rate=1.)
        # add thermal mass
        u_c_obj.add_thermal_mass_int_wall()
        return (u_c_obj)

    @classmethod
    def generate_sample_buildings(cls, path_folder_typology, nb_buildings=None):
        """ """
        u_c_obj = cls("sample_urban_canopy")
        u_c_obj.load_typologies(path_folder_typology)
        Building.generate_sample_buildings(u_c_obj, nb_buildings)

        list_target_building = u_c_obj.building_dict
        u_c_obj.select_target_building(list_target_building)

        ## Create Ladybug geometries with GIS footprint
        u_c_obj.create_building_LB_geometry_footprint()
        ## Create HB room envelop with GIS footprint
        u_c_obj.create_building_HB_room_envelop()

        for building_id in u_c_obj.building_dict:
            u_c_obj.building_dict[building_id].typology = u_c_obj.typology_dict["BER_ref_A_south"]

        # convert to DF stories and buildings
        u_c_obj.create_DF_building_according_to_typology()
        # convert to HB model
        u_c_obj.generate_HB_model()
        # U_c.convert_DF_building_to_HB_models()
        u_c_obj.HB_solve_adjacencies()
        # %% DF + HB modeling using GIS data + typology
        u_c_obj.assign_conditioned_zone()
        # add Ideal HVAC system
        u_c_obj.assign_ideal_hvac_system(climate_zone="A", hvac_paramater_set="team_design_builder")
        # create windows
        u_c_obj.HB_building_window_generation_floor_area_ratio()
        # add shades
        u_c_obj.add_context_surfaces_to_HB_model()
        # assign constructions, loads etc...
        u_c_obj.apply_buildings_characteristics()
        # Add infiltration in volume per hour
        u_c_obj.add_infiltration_air_exchange(air_exchange_rate=1.)
        # add thermal mass
        u_c_obj.add_thermal_mass_int_wall()
        return u_c_obj
