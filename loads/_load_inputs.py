"""
Functions to load the inputs for the program
"""
from os.path import join
from json import load

from tools._other import dict_assign_if_key_exist


def load_input_parameter(path_input_file):
    """ load the input file"""
    ## load input file
    input_file = open(path_input_file, "r")
    json_dict = load(input_file)
    input_file.close()
    ## Input file variable
    epw = dict_assign_if_key_exist(json_dict, "epw")
    gis = dict_assign_if_key_exist(json_dict, "gis")
    unit_gis = dict_assign_if_key_exist(json_dict, "unit_gis")
    target_buildings = dict_assign_if_key_exist(json_dict, "target_buildings")
    VF_criterion_shading = dict_assign_if_key_exist(json_dict, "VF_criterion_shading")
    # VF_criterion_simulated_buildings = dict_assign_if_key_exist(json_dict, "VF_criterion_simulated_buildings")
    # VF_criterion_lwr = dict_assign_if_key_exist(json_dict, "VF_criterion_lwr")
    return epw, gis, unit_gis, target_buildings, VF_criterion_shading


if __name__ == "__main__":
    epw, gis, unit_gis, target_buildings, VF_criterion_shading=load_input_parameter("D:\Elie\PhD\Simulation\Input_Data\inputs.json")
    print(epw)
