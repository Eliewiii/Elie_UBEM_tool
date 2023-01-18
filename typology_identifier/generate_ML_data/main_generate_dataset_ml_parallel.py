"""

"""
from sample_and_test_data import *
import os

import logging
from time import time
from multiprocessing import Pool

# Inputs
# path_folder_model = "D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\model_sample"
path_folder_model = "D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\Tel_Aviv_MOE" # another model potentially

is_deg = False  # tell if the GIS are in degree or in meters, if degree it needs to be converted in meter.

nb_noised_sample = 60

# Initialization inputs
path_folder_shp_data = os.path.join(path_folder_model, "shp_data")
path_folder_shp_training = os.path.join(path_folder_shp_data, "training_shp")
path_folder_shp_test = os.path.join(path_folder_shp_data, "test_shp")
# Initialization outputs
path_folder_output_data_training = path_folder_shp_data = os.path.join(path_folder_model, "training")
path_folder_output_data_test = os.path.join(path_folder_model, "test")


def generate_sample_ml(building_type, training_or_test):
    """ generate all the sample images  """
    logging.warning(f"Generating {training_or_test} samples for '{building_type}'")
    if training_or_test == "training":
        path_building_type_shp = os.path.join(path_folder_shp_training,
                                              building_type)  # path directory with all the samples
        ## create a folder to store the generated images
        path_output_building_type = os.path.join(path_folder_output_data_training, building_type)
        os.mkdir(path_output_building_type)  # create the output folder

    if training_or_test == "test":
        path_building_type_shp = os.path.join(path_folder_shp_test,
                                              building_type)  # path directory with all the samples
        ## create a folder to store the generated images
        path_output_building_type = os.path.join(path_folder_output_data_test, building_type)
        os.mkdir(path_output_building_type)  # create the output folder

    sample_list = os.listdir(path_building_type_shp)  # list of the samples in the building type folder
    # Initialize the index
    index = 0
    ## Loop on all the samples
    for sample in sample_list:
        for shp_file in os.listdir(os.path.join(path_building_type_shp, sample)):  # identify the .shp files
            if shp_file.endswith(".shp"):
                path_file_shp = os.path.join(path_building_type_shp, sample, shp_file)
                # return the index at the end of the generation
                index = generate_data_base_from_sample(path_file_shp, index, path_output_building_type,
                                                       nb_noised_sample, is_deg)

if __name__ == "__main__":  # mandatory for parallel processing, what is executed by the master should be under this
    # Training set
    building_type_list = os.listdir(path_folder_shp_training)  # each folder is associated with
    # Clear folders
    clean_directory(path_folder_output_data_training)
    clean_directory(path_folder_output_data_test)
    # Prepare inputs parameters for paralellization
    nb_type = len(building_type_list)
    building_type_input_list = building_type_list + building_type_list  # concatenate the list with itself to have
                                                                        # for both training and test
    type_data = ["training" for i in range(nb_type)] + ["test" for i in range(nb_type)]  # input for multiprocessing
    # Number of processes to run
    nb_process = nb_type * 2
    # number of processes to run in parallel
    nb_simultaneous_process = nb_process # eventually to optimize

    dt = time()  # timer
    # begin Pool parallel
    p = Pool(nb_simultaneous_process)
    p.starmap(generate_sample_ml, [(building_type_input_list[i],type_data[i]) for i in range(nb_process)], chunksize=1)
    p.close()
    p.join()
    # end parallel computation
    dt = time() - dt  # timer
    print(dt)


