"""


"""
import os
import shutil
import json

import Tiantian.ml_typology_identifier.main_generate_dataset_ml_parallel
from typology_identifier.generate_models._train_ml_model import train_ml_model
from typology_identifier.generate_models._evaluate_ml_model import evaluate_ml_model
from main_generate_dataset_ml_parallel import path_folder_noise_angles

#os.mkdir(path_folder_noise_angles)

# Inputs parameters training
num_epochs = 5  ## TO MODOIFY  ##
continue_training = False  ## TO MODOIFY  ## continue the training of an existing model (if it exist) or create a new one

batch_size = 8
learning_rate = 0.001
# Inputs parameters evaluation
min_percentage_list = [0.75, 0.8, 0.85]
# Path to model
# path_folder_model = "D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\Tel_Aviv_MOE_test" # to modify
path_folder_model = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test"

#path_model_parameters_json = os.path.join(path_folder_model, "model_param.json")

# training
for simulation_time in range(0, 3):
    continue_training = False
    path_folder_noise_angles = path_folder_noise_angles + "_" + str(simulation_time+1)
    os.mkdir(path_folder_noise_angles)
    accum_num_epochs = num_epochs
    for i in range(0, 6):
        path_folder_epochs = os.path.join(path_folder_noise_angles, "epochs_"+str(accum_num_epochs))
        os.mkdir(path_folder_epochs)
        path_model_parameters_json = os.path.join(path_folder_epochs, "model_param.json")
        # copy thr model_param.json into the epochs file
        original = os.path.join(path_folder_model, "model_param.json")
        target = path_model_parameters_json
        shutil.copy(original, target)
        train_ml_model(path_model_parameters_json, num_epochs=num_epochs, batch_size=batch_size,
                       learning_rate=learning_rate,continue_training=continue_training)

        # Evaluation
        for min_percentage in min_percentage_list:
            evaluate_ml_model(path_model_parameters_json, min_percentage=min_percentage, is_saved=True)
        continue_training = True
        accum_num_epochs = accum_num_epochs + 5

    ## Generate csv file on the results at specific angle and noises
    with open(os.path.join(path_folder_noise_angles, "result.csv"), 'w') as csvfile:
        csvfile.write("Epochs,Percentages,Shapes,true positive,false positive\n")
        for epo_num in [5, 10, 15, 20, 25, 30]:
            epo_list = os.path.join(path_folder_noise_angles, "epochs_"+str(epo_num))
            for j in min_percentage_list:
                result_list = os.path.join(epo_list, str(j) + ".json")  # open the json file with the specific min percentage
                with open(result_list) as f:
                    content = json.load(f)
                    for shapes in ["H", "Rectangle", "Train", "Other"]:
                        csvfile.write("{},{},{},{},{}\n".format(
                            epo_num,
                            j,
                            shapes,
                            round(content[shapes]["true positive (accuracy) [%]"], 2),
                            round(content[shapes]["false positive [%]"], 2)))

    ## The results csv obtained before is not easy to read, so it is necessary to adjust it##

    # Read and extract the content of the previous results csv
    with open(os.path.join(path_folder_noise_angles, "result.csv"), 'r') as f:
        cont = f.readlines()

    #Load the content from previous csv to a new csv, which is after adjusted.
    #adjusted_result_filename = "adjusted_result"+str(simulation_time+1)
    with open(os.path.join(path_folder_noise_angles, "adjusted_result.csv"), 'w') as newfile:
        newfile.write("Percentages,Epochs,Shapes,true positive,false positive\n")
        for percentage in [0.75, 0.8, 0.85]:           # three different min advantages
            for shape in ["H", "Rectangle", "Train", "Other"]:
                for nepo in [5, 10, 15, 20, 25, 30]:   # number of epochs
                    for index in range(0, len(cont)):
                        # it is necessary to split the specific row of the content to extract the data
                        a = cont[index].split(",")
                        if a[1] == str(percentage) and a[2] == shape and a[0] == str(nepo):
                            newfile.write("{},{},{},{},{}\n".format(
                                percentage,
                                nepo,
                                shape,
                                float(a[3]),
                                float(a[4])))

    #shutil.rmtree()



