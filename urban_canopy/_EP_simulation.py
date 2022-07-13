"""
Additional methods for the Urban_canopy class.
Deals generate files (mostly .hbjson files) for visualization in Rhino with Grasshopper
"""
import os
import json


from honeybee_energy.simulation.output import SimulationOutput
from honeybee_energy.simulation.sizing import SizingParameter
from honeybee_energy.simulation.control import SimulationControl
from honeybee_energy.simulation.shadowcalculation import ShadowCalculation
from honeybee_energy.simulation.runperiod import RunPeriod
from honeybee_energy.simulation.parameter import SimulationParameter

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
        terrain_type = "City" #'Urban'  # By default here, but might be changed
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
