import matplotlib.pyplot as plt
import pandas as pd
from average_result import average_result_noise_angle
from train_and_evaluate_model import path_result_run_dic,path_folder_sub_model_list,entire_run_num

import os

# Variables initialization

#noise_angles_result_path = "D:\\Pycharm\\meachnie_learning\\without_Other_test\\noise_40_angles_35\\adjusted_result.csv"


def plotting_method_1(noise_angles_result_path):
    total_result = pd.read_csv(noise_angles_result_path)
    epochs = [5,10,15,20,25,30]
    percentage = ["75%","80%","85%"]
    round_num = 0
    plot_index = 0    # The index of plotting, there are six plotting in all. Three percentages with "true positive" and "false positive" result

    for i in [0,18,36]:     # i calls for the beginning line of the test results in another min percentage
        round_num += 1
        for label_index in [1,2]:
            plot_index += 1
            if label_index % 2 == 0:
                result_label = "true positive"
            else:
                result_label = "false positive"
            H_data = total_result.iloc[i:(i + 6)]
            Rec_data = total_result.iloc[(i + 6):(i + 12)]
            Train_data = total_result.iloc[(i + 12):(i + 18)]
            H_result = H_data[result_label]
            Rec_result = Rec_data[result_label]
            Train_result = Train_data[result_label]
            plt.subplot(3, 2, plot_index)
            plt.plot(epochs, H_result, 's-', color='r', label="H")
            plt.plot(epochs, Rec_result, 'o-', color='g', label="Rectangle")
            plt.plot(epochs, Train_result, 'x-', color='y', label="Train")
            plt.xlabel("Epochs")
            plt.ylabel(result_label + " [%]")
            plt.legend(loc="best")
            plt.title("Min_percentage="+percentage[round_num-1])

    plt.suptitle("ML test result in noise_40_angles_35")
    plt.savefig("D:\\Pycharm\\meachnie_learning\\without_Other_test\\noise_40_angles_35\\graph.png")
    plt.show()

def plotting_method_2(noise30_angles_result_path,noise35_angles_result_path,noise40_angles_result_path):
    epochs = [5, 10, 15, 20, 25, 30]
    color_name = ["red","green","yellow"]
    percentage = ""
    round_num = 0

    plt.figure(figsize=(15, 10))
    for i in [0, 24, 48]:  # i calls for the beginning line of the test results in another min percentage
    #for i in [0, 18, 36]:
        if i == 0:
            colors = 'r'
            percentage = "_percentage75%"
        elif i == 24:
        #elif i == 18:
            colors = 'g'
            percentage = "_percentage80%"
        else:
            colors = 'y'
            percentage = "_percentage85%"
        round_num += 1
        for noise in [30,35,40]:
            total_result = 0
            labels = ""
            linestyles = ''
            if noise == 30:
                total_result = pd.read_csv(noise30_angles_result_path)
                labels = "noise 30"+percentage
                linestyles = 'dotted'
            if noise == 35:
                total_result = pd.read_csv(noise35_angles_result_path)
                labels = "noise 35"+percentage
                linestyles = 'dashed'
            if noise == 40:
                total_result = pd.read_csv(noise40_angles_result_path)
                labels = "noise 40"+percentage
                linestyles = 'solid'
            H_data = total_result.iloc[i:(i + 6)]
            #H_result = H_data["true positive"]
            H_result = H_data["false positive"]
            plt.subplot(1, 3, 1)
            plt.plot(epochs, H_result, linestyle=linestyles, color=colors, label=labels)
            plt.xlabel("Epochs")
            #plt.ylabel("True positive [%]")
            plt.ylabel("False positive [%]")
            plt.legend(loc="best")
            plt.title("H")

            Rec_data = total_result.iloc[(i + 6):(i + 12)]
            #Rec_result = Rec_data["true positive"]
            Rec_result = Rec_data["false positive"]
            plt.subplot(1, 3, 2)
            plt.plot(epochs, Rec_result, linestyle=linestyles, color=colors, label=labels)
            plt.xlabel("Epochs")
            #plt.ylabel("True positive [%]")
            plt.ylabel("False positive [%]")
            plt.legend(loc="best")
            plt.title("Rectangle")

            Train_data = total_result.iloc[(i + 12):(i + 18)]
            #Train_result = Train_data["true positive"]
            Train_result = Train_data["false positive"]
            plt.subplot(1, 3, 3)
            plt.plot(epochs, Train_result, linestyle=linestyles, color=colors, label=labels)
            plt.xlabel("Epochs")
            #plt.ylabel("True positive [%]")
            plt.ylabel("False positive [%]")
            plt.legend(loc="best")
            plt.title("Train")

    plt.savefig("D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\false positive.png")
    #plt.savefig("D:\\Pycharm\\Test2\\Without_other\\true positive.png")
    plt.show()

def box_plotting(result1_path,result2_path,result3_path):
    #data1 = [list(range(-5, 11)), list(range(-5, 6))]
    total_result1 = pd.read_csv(result1_path)
    total_result2 = pd.read_csv(result2_path)
    total_result3 = pd.read_csv(result3_path)
    mark = ["0.75 min percentage", "0.8 min percentage", "0.85 min percentage"]
    x_position_bar = []
    epochs = ["5", "10", "15", "20", "25", "30"]

    colors = ["red", "green", "yellow"]
    i = 0   #edit
    ## try apply the loop for each shape
    bar_location = -1
    #if i == 0:
        #shape = "H_multiple_result.png"
    #elif i == 6:
        #shape = "Rec_multiple_result.png"
    #else:
        #shape = "Train_multiple_result.png"
    for a in range(i,i+6):
        data = [[total_result1.iloc[a]["true positive"],total_result2.iloc[a]["true positive"],total_result3.iloc[a]["true positive"]],
                [total_result1.iloc[a+24]["true positive"], total_result2.iloc[a+24]["true positive"],total_result3.iloc[a+24]["true positive"]],
                [total_result1.iloc[a+48]["true positive"], total_result2.iloc[a+48]["true positive"],total_result3.iloc[a+48]["true positive"]]]
        bar_location += 2
        x_position_bar.append(bar_location)
        plt1 = plt.boxplot(data, patch_artist=True, labels=mark, positions=(bar_location-0.6, bar_location, bar_location+0.6),
                        widths=0.4)
        for patch, color in zip(plt1['boxes'], colors):
            patch.set_facecolor(color)

        # adding text inside the plot
        #plt.text(bar_location + 0.15, 6.3, 'A', fontsize=10)

        if bar_location == 1:
            plt.legend(plt1['boxes'], mark)

    plt.xticks(x_position_bar, labels=epochs)
    plt.xlabel("epochs")
    plt.ylabel("True positive [%]")
    plt.savefig("D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_40_angles_35\\H_multiple_simu_result.png") #edit
    plt.show()


### calculate the average of results ####


for path_result in path_folder_sub_model_list:
    average_result_noise_angle(path_result, path_result_run_dic[path_result],entire_run_num,18)



noise30_angles_result_path = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_30_angles_35\\adjusted_result.csv"
noise35_angles_result_path = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_35_angles_35\\adjusted_result.csv"
noise40_angles_result_path = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_40_angles_35\\adjusted_result.csv"
#noise30_angles_result_path = "D:\\Pycharm\\meachnie_learning\\without_Other_test\\noise_30_angles_35\\adjusted_result.csv"
#noise35_angles_result_path = "D:\\Pycharm\\meachnie_learning\\without_Other_test\\noise_35_angles_35\\adjusted_result.csv"
#noise40_angles_result_path = "D:\\Pycharm\\meachnie_learning\\without_Other_test\\noise_40_angles_35\\adjusted_result.csv"
plotting_method_2(noise30_angles_result_path,noise35_angles_result_path,noise40_angles_result_path)


#result1_path = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_40_angles_35\\adjusted_result1.csv"
#result2_path = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_40_angles_35\\adjusted_result2.csv"
#result3_path = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_40_angles_35\\adjusted_result3.csv"
#box_plotting(result1_path,result2_path,result3_path)


