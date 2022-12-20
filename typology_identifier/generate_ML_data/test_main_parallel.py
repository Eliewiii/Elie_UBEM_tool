"""

"""
from sample_and_test_data import *
import os

import  logging
from time import time
from multiprocessing import Pool

# Inputs
path_folder_model = "D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\model_sample"
# path_folder_model = "D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\model_sample"


is_deg = True  # tell if the GIS are in degree or in meters, if degree it needs to be converted in meter.

nb_noised_sample = 10

# Initialization inputs
path_folder_shp_data = os.path.join(path_folder_model, "shp_data")
path_folder_shp_training = os.path.join(path_folder_shp_data, "training_shp")
path_folder_shp_test = os.path.join(path_folder_shp_data, "test_shp")
# Initialization outputs
path_folder_output_data_training = path_folder_shp_data = os.path.join(path_folder_model, "training")
path_folder_output_data_test = os.path.join(path_folder_model, "test")


#
# building_type_folder_path = "D://Elie//PhD//Programming//GIS//Building_type//North_Tel_Aviv//Training_data"
# # building_type_folder_path = "D://Elie//PhD//Programming//GIS//Building_type//North_Tel_Aviv//Verification"
#
# is_deg = True # if the GIS is in degree and not meters
#
# ML_path = "D://Elie//PhD//Programming//Machine_Learning_Identifier"
#
# output_folder_name = "Training_data"
# # output_folder_name = "Test_data"
#
#
# ML_output_folder_path = os.path.join(ML_path, output_folder_name)
#
#
# nb_sample_noise = 100
#


def test_par(building_type):
    logging.warning(f"Generating samples for '{building_type}'")
    path_building_type = os.path.join(path_folder_shp_training,
                                      building_type)  # path directory with all the samples
    ## create a folder to store the generated images
    path_output_building_type = os.path.join(path_folder_output_data_training, building_type)
    os.mkdir(path_output_building_type)
    ## Loop on all the samples
    index = 0
    sample_list = os.listdir(path_building_type)
    for sample in sample_list:
        for shp_file in os.listdir(os.path.join(path_building_type, sample)):
            if shp_file.endswith(".shp"):
                path_file_shp = os.path.join(path_building_type, sample, shp_file)
                index = generate_data_base_from_sample(path_file_shp, index, path_output_building_type,
                                                       nb_noised_sample, is_deg)

if __name__=="__main__":
    ## Training set
    building_type_list = os.listdir(path_folder_shp_training)  # each folder is associated with
    # Clear folders
    clean_directory(path_folder_output_data_training)
    clean_directory(path_folder_output_data_training)
    # loop on all the building types shape
    nb_process = len(building_type_list)
    # nb_it=3000
    dt=time()
    p=Pool(nb_process)
    p.map(test_par,building_type_list,chunksize=1)
    p.close()
    p.join()
    dt=time()-dt
    print(dt)
