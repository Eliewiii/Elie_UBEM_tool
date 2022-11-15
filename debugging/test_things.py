import os

from tools._save_and_load_objects import load_urban_canopy_object_pickle

U_c_2 = load_urban_canopy_object_pickle(
    os.path.join("D:\Elie\PhD\Simulation\Program_output\Simulation_11", "Urban_canopy", "uc_obj.p"))
print(U_c_2.building_dict)