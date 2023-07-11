"""

"""
from typology_identifier.generate_ML_data.sample_and_test_data import generate_data_base_from_sample, clean_directory
import os

from time import time
from multiprocessing import Pool

# Import the parameters
from Tiantian.ml_typology_identifier.config import *


# Initialization inputs
path_folder_shp_data = os.path.join(path_folder_model, "shp_data")
path_folder_shp_training = os.path.join(path_folder_shp_data, "training_shp")
path_folder_shp_test = os.path.join(path_folder_shp_data, "test_shp")

# Initialization outputs
#path_folder_output_data_training = ""
#path_folder_output_data_test = ""
path_folder_sub_model_list = []
for noise in nb_noised_sample:
    for angles in nb_angles_sample:
        for max_shift in nb_max_shift_sample:
            # create the file folder for the specific noise and angles
            path_folder_sub_model_list.append(os.path.join(path_folder_model, "data_noise_" + str(noise) + "_angles_" + str(angles) + "_max_shift_"+str(max_shift)))

            #path_folder_output_data_training = path_folder_shp_data = os.path.join(path_folder_model, "training_noise"+str(noise))
            #%path_folder_output_data_test = os.path.join(path_folder_model, "test_noise"+str(noise))



def generate_sample_ml(building_type, training_or_test, path_folder):
    """ generate all the sample images  """
    #logging.warning(f"Generating {training_or_test} samples for '{building_type}'")
    if training_or_test == "training":
        path_building_type_shp = os.path.join(path_folder_shp_training,
                                            building_type)  # path directory with all the samples
        ## create a folder to store the generated images
        path_output_building_type = os.path.join(path_folder,"training", building_type)
        os.mkdir(path_output_building_type)  # create the output folder

    if training_or_test == "test":
        path_building_type_shp = os.path.join(path_folder_shp_test,
                                            building_type)  # path directory with all the samples
        ## create a folder to store the generated images
        path_output_building_type = os.path.join(path_folder,"test", building_type)
        os.mkdir(path_output_building_type)  # create the output folder

    sample_list = os.listdir(path_building_type_shp)  # list of the samples in the building type folder
    # Initialize the index
    index = 0
    ## Loop on all the samples
    nb_noised= int(path_folder.split("data_noise_")[-1].split("_angles")[0])
    nb_angles = int(path_folder.split("_angles_")[-1].split("_max_shift_")[0])
    nb_max_shift = float(path_folder.split("_max_shift_")[-1].split("\\")[0])
    #nb_noised = int(path_folder[-12:-10])
    for sample in sample_list:
        for shp_file in os.listdir(os.path.join(path_building_type_shp, sample)):  # identify the .shp files
            if shp_file.endswith(".shp"):
                path_file_shp = os.path.join(path_building_type_shp, sample, shp_file)
                # return the index at the end of the generation
                index = generate_data_base_from_sample(path_file_shp, index, path_output_building_type,
                                                        nb_noised,nb_angles,nb_max_shift, is_deg)    ##max shift

if __name__ == "__main__":  # mandatory for parallel processing, what is executed by the master should be under this
    # Training set
    building_type_list = os.listdir(path_folder_shp_training)  # each folder is associated with
    # Clear folders

    # Prepare inputs parameters for paralellization
    nb_type = len(building_type_list)
    building_type_input_list = building_type_list + building_type_list  # concatenate the list with itself to have
    # for both training and test
    type_data = ["training" for i in range(nb_type)] + ["test" for i in range(nb_type)]  # input for multiprocessing
    # Number of processes to run
    nb_process = nb_type * 2
    # number of processes to run in parallel
    nb_simultaneous_process = nb_process  # eventually to optimize

    dt = time()  # timer
    # begin Pool parallel
    nb_loops = len(path_folder_sub_model_list)
    for loop,path_folder in enumerate(path_folder_sub_model_list):
        print("loop {} our of {}".format(loop,nb_loops))
        clean_directory(path_folder)
        for i in range(nb_iteration):
            path_it=os.path.join(path_folder,"it_"+str(i))
            clean_directory(path_it)
            clean_directory(os.path.join(path_it, "training"))
            clean_directory(os.path.join(path_it, "test"))

            p = Pool(nb_simultaneous_process)
            p.starmap(generate_sample_ml,
                      [(building_type_input_list[i], type_data[i], path_it) for i in range(nb_process)],
                      chunksize=1)
            p.close()
            p.join()
    # end parallel computation
    dt = time() - dt  # timer
    print(dt)


