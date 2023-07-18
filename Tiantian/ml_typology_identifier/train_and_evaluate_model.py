"""


"""
import os
import shutil
import json

# from typology_identifier.generate_models._train_ml_model import train_ml_model   ##to do
from Tiantian.ml_typology_identifier.generate_models._train_ml_model import train_ml_model
# from typology_identifier.generate_models._evaluate_ml_model import evaluate_ml_model  ##to do
from Tiantian.ml_typology_identifier.generate_models._evaluate_ml_model import evaluate_ml_model
from average_result import average_result_noise_angle

# Import the parameters
from Tiantian.ml_typology_identifier.config import *

path_folder_sub_model_list = []
for noise in nb_noised_sample:
    for angles in nb_angles_sample:
        for max_shift in nb_max_shift_sample:
            path_folder_sub_model_list.append(os.path.join(path_folder_model,
                                                           "data_noise_" + str(noise) + "_angles_" + str(
                                                               angles) + "_max_shift_" + str(max_shift)))
# path_model_parameters_json = os.path.join(path_folder_model, "model_param.json")

# training
if __name__ == "__main__":
    # for nb_angle in nb_angle_list:
    #   for nb_noise in nb_noise_list:
    #      for max_shift in max_shift_list:
    # The integrated simulation is repeated three times from epochs 5 to 30
    path_folder_noise_angles_list = []
    one_run_result_length = 0
    nb_loops = len(path_folder_sub_model_list)
    for loop, path_folder_sub_model in enumerate(path_folder_sub_model_list):
        print("loop {} our of {}".format(loop, nb_loops))
        path_folder_noise_angles = os.path.join(path_folder_model, path_folder_sub_model.split("data_")[1])
        path_folder_noise_angles_list.append(path_folder_noise_angles)
        os.mkdir(path_folder_noise_angles)
        for data_it in range(nb_iteration):
            path_folder_dataset_iteration = os.path.join(path_folder_noise_angles, "Iteration_" + str(data_it))
            os.mkdir(path_folder_dataset_iteration)
            path_result_run_list = []
            for simulation_time in range(0, entire_run_num):
                continue_training = False
                path_folder_noise_angles_run = os.path.join(path_folder_dataset_iteration,
                                                            "Entire_Run_" + str(simulation_time + 1))  ##todo
                path_result_run_list.append(path_folder_noise_angles_run)
                # create a dictionary to record the directory of different run folders according to key of noise/angle folder directory
                path_result_run_dic["It_" + str(data_it)] = path_result_run_list
                os.mkdir(path_folder_noise_angles_run)
                # accum_num_epochs = num_epochs
                # generate new data set with te parameters in the loop

                for i, value in enumerate(epoch_list):
                    path_folder_epochs = os.path.join(path_folder_noise_angles_run, "epochs_" + str(value))
                    os.mkdir(path_folder_epochs)
                    path_model_parameters_json = os.path.join(path_folder_epochs, "model_param.json")
                    # copy thr model_param.json into the epochs file
                    original = os.path.join(path_folder_model, "model_param.json")
                    target = path_model_parameters_json
                    shutil.copy(original, target)
                    path_it = os.path.join(path_folder_sub_model, "it_" + str(data_it))
                    train_ml_model(path_model_parameters_json, path_it, num_epochs=step_num_epochs,
                                   batch_size=batch_size,
                                   learning_rate=learning_rate, continue_training=continue_training)

                    # Evaluation
                    for min_percentage in min_percentage_list:
                        evaluate_ml_model(path_model_parameters_json, path_it, min_percentage=min_percentage,
                                          is_saved=True)
                    continue_training = True
                    # accum_num_epochs = accum_num_epochs + 5

                ## Generate csv file on the results at specific angle and noises
                with open(os.path.join(path_folder_noise_angles_run, "result.csv"), 'w') as csvfile:
                    for epo_num in epoch_list:
                        csvfile.write("Epochs,Percentages,Shapes,true positive,false positive\n")
                        epo_list = os.path.join(path_folder_noise_angles_run, "epochs_" + str(epo_num))
                        for j in min_percentage_list:
                            result_list = os.path.join(epo_list,
                                                       str(j) + ".json")  # open the json file with the specific min percentage
                            with open(result_list) as f:
                                content = json.load(f)
                                for shapes in ["H", "Rectangle", "Train"]:  # "Other" unnecessary
                                    csvfile.write("{},{},{},{},{}\n".format(
                                        epo_num,
                                        j,
                                        shapes,
                                        round(content[shapes]["true positive (accuracy) [%]"], 2),
                                        round(content[shapes]["false positive [%]"], 2)))

                ## The results csv obtained before is not easy to read, so it is necessary to adjust it##

                # Read and extract the content of the previous results csv
                with open(os.path.join(path_folder_noise_angles_run, "result.csv"), 'r') as f:
                    cont = f.readlines()
                one_run_result_length = len(cont) - 2

                # Load the content from previous csv to a new csv, which is after adjusted.
                # adjusted_result_filename = "adjusted_result"+str(simulation_time+1)
                with open(os.path.join(path_folder_noise_angles_run, "adjusted_result.csv"), 'w') as newfile:
                    newfile.write("Percentages,Epochs,Shapes,true positive,false positive\n")
                    for percentage in min_percentage_list:  # three different min advantages
                        for shape in ["H", "Rectangle", "Train"]:  # "Other" unnecessary
                            for nepo in epoch_list:  # number of epochs
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

            ## average results for iterations of training
            average_result_noise_angle(path_folder_dataset_iteration, path_result_run_list, entire_run_num,
                                       one_run_result_length)

            # shutil.rmtree()
