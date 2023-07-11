import os
import pandas as pd
from main_generate_dataset_ml_parallel import nb_noised_sample, nb_angles_sample, nb_max_shift_sample, nb_iteration
from ml__result_plotting_Tiantian import box_plotting_for_each_parameter_set
from train_and_evaluate_model import entire_run_num

path_folder_model = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test"

"""

Plotting the false and true positive result at each set of parameters

"""
parameter_set_list = []
noise_angle_shift_it_avg_dic = {}
for noise in nb_noised_sample:
    for angles in nb_angles_sample:
        for max_shift in nb_max_shift_sample:
            parameter_set = "noise = "+str(noise)+"\n"+"angles = "+str(angles)+"\n"+"max shift = "+str(max_shift)
            parameter_set_list.append(parameter_set)
            path_folder_noise_angles = os.path.join(path_folder_model,"noise_" + str(noise) + "_angles_" + str(angles) + "_max_shift_" + str(max_shift))
            iteration_result_list = []
            for iteration in range(0,nb_iteration):
                path_average_result = os.path.join(path_folder_noise_angles,"Iteration_"+str(iteration),"average_result.csv")
                # H result at 0.75, edit
                iteration_result = pd.read_csv(path_average_result)
                H_false = iteration_result.iloc[1]["false positive"]
                iteration_result_list.append(H_false)
            noise_angle_shift_it_avg_dic[parameter_set] = iteration_result_list
# edit the saving path and determine false or true positive
save_path = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\Result\\Plotting_set_of_parameter\\H_false_0.75.png"
false_or_true_positive = "False positive"
box_plotting_for_each_parameter_set(parameter_set_list, noise_angle_shift_it_avg_dic, save_path, false_or_true_positive)

"""

Plotting the false and true positive result within one set of parameters

"""
mark = []
for noise in nb_noised_sample:
    for angles in nb_angles_sample:
        for max_shift in nb_max_shift_sample:
            for iteration in range(nb_iteration):
                path_iteration = os.path.join(path_folder_model,
                                              "noise_" + str(noise) + "_angles_" + str(angles) + "_max_shift_" + str(max_shift),
                                              "Iteration_" + str(iteration))
                mark.append("Iteration "+str(nb_iteration+1))
                for nb_simulation in range(entire_run_num):
                    simulation_result = pd.read_csv(os.path.join(path_iteration,"Entire_run_"+str(entire_run_num+1)))
                    
