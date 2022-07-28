"""
Additional methods for the Urban_canopy class.
Deals generate files (mostly .hbjson files) for visualization in Rhino with Grasshopper
"""
import os
import json
import logging

from honeybee_energy.hvac.idealair import IdealAirSystem
from honeybee_energy.simulation.output import SimulationOutput
from honeybee_energy.simulation.sizing import SizingParameter
from honeybee_energy.simulation.control import SimulationControl
from honeybee_energy.simulation.shadowcalculation import ShadowCalculation
from honeybee_energy.simulation.runperiod import RunPeriod
from honeybee_energy.simulation.parameter import SimulationParameter
from honeybee_energy.altnumber import autosize
from honeybee.altnumber import no_limit
from honeybee_energy.lib.schedules import schedule_by_identifier

from honeybee.model import Model
from ladybug.epw import EPW


class Mixin:

    def add_design_days_to_simulation_parameters(self, path_simulation_parameter, path_file_epw, terrain_type_in="City",
                                                 timestep_in=6):
        """ Add the design days, necessary for EnergyPlus to simulate, to the simulation parameters """
        # sim_parameter_obj = None
        with open(path_simulation_parameter, 'r') as f:
            json_dic = json.load(f)
            sim_parameter_obj = SimulationParameter.from_dict(json_dic)
        epw_obj = EPW(path_file_epw)
        des_days = [epw_obj.approximate_design_day('WinterDesignDay'),
                    epw_obj.approximate_design_day('SummerDesignDay')]
        sim_parameter_obj.sizing_parameter.design_days = des_days

        sim_parameter_obj.terrain_type = terrain_type_in
        sim_parameter_obj.timestep = timestep_in
        # replace the simulatio_paramter.json by the updated one
        sim_parameter_dic = SimulationParameter.to_dict(sim_parameter_obj)
        with open(path_simulation_parameter, "w") as json_file:
            json.dump(sim_parameter_dic, json_file)

    def simulation_parameters_from_json(self, simulation_parameter_folder):
        """ Concatenate the individual simulation parameter files to a global one """
        output = None
        run_period = None
        simulation_control = None
        shadow_calculation = None
        sizing_parameter = None
        # default
        timestep = 6  # By default here, but might be changed
        north_angle = 0
        terrain_type = "City"  # 'Urban'  # By default here, but might be changed
        # Extract the parameters from json files
        with open(os.path.join(simulation_parameter_folder, "SimulationOutput.json"), 'r') as f:
            json_dict = json.load(f)
            output = SimulationOutput.from_dict(json_dict)
        with open(os.path.join(simulation_parameter_folder, "RunPeriod.json"), 'r') as f:
            json_dict = json.load(f)
            run_period = RunPeriod.from_dict(json_dict)
        with open(os.path.join(simulation_parameter_folder, "SimulationControl.json"), 'r') as f:
            json_dict = json.load(f)
            simulation_control = SimulationControl.from_dict(json_dict)
        with open(os.path.join(simulation_parameter_folder, "ShadowCalculation.json"), 'r') as f:
            json_dict = json.load(f)
            shadow_calculation = ShadowCalculation.from_dict(json_dict)
        with open(os.path.join(simulation_parameter_folder, "SizingParameter.json"), 'r') as f:
            json_dict = json.load(f)
            sizing_parameter = SizingParameter.from_dict(json_dict)

        self.simulation_parameters = SimulationParameter(output=output, run_period=run_period, timestep=timestep,
                                                         simulation_control=simulation_control,
                                                         shadow_calculation=shadow_calculation,
                                                         sizing_parameter=sizing_parameter,
                                                         north_angle=north_angle, terrain_type=terrain_type)

    def load_simulation_parameter(self, path_folder_simulation_parameter, path_simulation_parameter):
        """ convert properly the simulation parameters for HB """
        self.simulation_parameters_from_json(path_folder_simulation_parameter)
        HB_simulation_parameter_dic = SimulationParameter.to_dict(self.simulation_parameters)
        with open(path_simulation_parameter, "w") as json_file:
            json.dump(HB_simulation_parameter_dic, json_file)

    def configure_ideal_hvac_system(self, climate_zone="A", hvac_paramater_set="default"):
        """ """
        if climate_zone not in ["A", "B", "C", "D"]:
            logging.warning("The climate zone input to configure the HVAC system cooling and heating period "
                            "is invalid, it will be set as 'A'.")
            climate_zone = "A"
        # Select the heating and cooling schedules
        if climate_zone == "A" or climate_zone == "B":
            schedule_cooling = schedule_by_identifier("Is_5280_CoolingSch_A_B")
            schedule_heating = schedule_by_identifier("Is_5280_HeatingSch_A_B")
        elif climate_zone == "C":
            schedule_cooling = schedule_by_identifier("Is_5280_CoolingSch_C")
            schedule_heating = schedule_by_identifier("Is_5280_HeatingSch_C")
        else:
            schedule_cooling = schedule_by_identifier("Is_5280_CoolingSch_D")
            schedule_heating = schedule_by_identifier("Is_5280_HeatingSch_D")
        # Generate the ideal hvac_system
        if hvac_paramater_set == "default":
            ideal_air_system_obj = IdealAirSystem("ideal_air_system_UBEM", economizer_type='DifferentialDryBulb',
                                                  demand_controlled_ventilation=False,
                                                  sensible_heat_recovery=0, latent_heat_recovery=0,
                                                  heating_air_temperature=50, cooling_air_temperature=13,
                                                  heating_limit=autosize, cooling_limit=autosize,
                                                  heating_availability=schedule_heating,
                                                  cooling_availability=schedule_cooling)
        elif hvac_paramater_set == "team_design_builder":
            ideal_air_system_obj = IdealAirSystem("ideal_air_system_UBEM", economizer_type='NoEconomizer',
                                                  demand_controlled_ventilation=False,
                                                  sensible_heat_recovery=0, latent_heat_recovery=0,
                                                  heating_air_temperature=35, cooling_air_temperature=12,
                                                  heating_limit=autosize, cooling_limit=autosize,
                                                  heating_availability=schedule_heating,
                                                  cooling_availability=schedule_cooling)
        else:  # our ideal
            ideal_air_system_obj = IdealAirSystem("ideal_air_system_UBEM", economizer_type='NoEconomizer',
                                                  demand_controlled_ventilation=False,
                                                  sensible_heat_recovery=0, latent_heat_recovery=0,
                                                  heating_air_temperature=50, cooling_air_temperature=13,
                                                  heating_limit=no_limit, cooling_limit=no_limit,
                                                  heating_availability=schedule_heating,
                                                  cooling_availability=schedule_cooling)

        self.hvac_system = ideal_air_system_obj

    ### Not sure this function in useful
    # def simulation_parameters_for_idf(self, idf):
    #     """
    #     Extract simulation parameter from an idf file
    #     """
    #     idf_string = None  # idf in a single string to crete Simulationparameter object with HB_energy
    #     with open(idf, "r") as idf_file:
    #         idf_string = idf_file.read()  # convert idf file in string
    #     simulation_parameter = parameter.SimulationParameter.from_idf(
    #         idf_string)  # create the Simulationparameter object
    #     return (simulation_parameter)


if __name__ == '__main__':
    a = Mixin()
    a.configure_ideal_hvac_system(hvac_paramater_set="default")
    print(a.hvac_system.cooling_air_temperature)
