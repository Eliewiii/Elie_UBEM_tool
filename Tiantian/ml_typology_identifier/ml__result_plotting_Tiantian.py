import matplotlib.pyplot as plt
import pandas as pd


def box_plotting_for_each_parameter_set(parameter_set_list, noise_angle_shift_it_avg_dic, save_path, false_or_true_positive):
    bar_location = -1
    x_position_bar = []
    mark = []
    data = []
    for parameter_set in parameter_set_list:
        mark.append(parameter_set)
        data.append(noise_angle_shift_it_avg_dic[parameter_set])
        bar_location += 2
        x_position_bar.append(bar_location)
    plt.boxplot(data, labels=mark, widths=0.4)
    plt.xticks(fontsize=5)
    plt.xlabel("sets of parameter")
    plt.ylabel(false_or_true_positive + " [%]")
    plt.tight_layout()
    plt.savefig(save_path, dpi=600)  # edit
    plt.show()

def box_plotting_within_parameter_set():
    pass