import os

def average_result_noise_angle(path_result, path_result_run_list,entire_run_num,one_run_result_length):

    cont = []
    for path_result_run in path_result_run_list:
        path_result_csv = os.path.join(path_result_run, "adjusted_result.csv")
        with open(path_result_csv,'r') as f:
            cont.append(f.readlines())

#with open("D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_40_angles_35\\adjusted_result1.csv", 'r') as f:
    #cont1 = f.readlines()
#with open("D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_40_angles_35\\adjusted_result2.csv", 'r') as f:
    #cont2 = f.readlines()
#with open("D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_40_angles_35\\adjusted_result3.csv", 'r') as f:
    #cont3 = f.readlines()

    #Copy all the results into one csv file
    with open(os.path.join(path_result, "entire_result.csv"), 'w') as f:
        f.write("Percentages,Epochs,Shapes,true positive,false positive\n")
        for run_num in range(0,entire_run_num):
            for index in range(1, len(cont[run_num])):
                a = cont[run_num][index].split(",")
                f.write("{},{},{},{},{}".format(a[0],a[1],a[2],a[3],a[4]))

    #adjusted_result_filename = "adjusted_result"+str(simulation_time+1)
    true_positive_result = []
    false_positive_result = []
    with open(os.path.join(path_result, "average_result.csv"), 'w') as newfile:
        with open(os.path.join(path_result, "entire_result.csv"),'r') as f:
            cont_new = f.readlines()
        newfile.write("Percentages,Epochs,Shapes,true positive,false positive\n")
        for index in range(1, len(cont_new)):
            if index < one_run_result_length+1:
                a = cont_new[index].split(",")
                true_positive_result.append(float(a[3]))
                false_positive_result.append(float(a[4]))
            else:
                a = cont_new[index].split(",")
                true_positive_result[index % one_run_result_length - 1] += float(a[3])
                false_positive_result[index % one_run_result_length - 1] += float(a[4])
                if index >= (entire_run_num - 1) * one_run_result_length + 1:
                    newfile.write("{},{},{},{},{}\n".format(a[0], a[1], a[2],
                                            true_positive_result[index % one_run_result_length-1]/entire_run_num,
                                            false_positive_result[index % one_run_result_length-1]/entire_run_num))


"""""""""
        for percentage in [0.75, 0.8, 0.85]:           # three different min advantages
            for shape in ["H", "Rectangle", "Train", "Other"]:
                for nepo in [5, 10, 15, 20, 25, 30]:   # number of epochs
                    for index in range(0, len(cont1)):
                        # it is necessary to split the specific row of the content to extract the data
                        a = cont1[index].split(",")
                        b = cont2[index].split(",")
                        c = cont3[index].split(",")
                        if a[0] == str(percentage) and a[2] == shape and a[1] == str(nepo) and b[0] == str(percentage) and b[2] == shape and b[1] == str(nepo) and c[0] == str(percentage) and c[2] == shape and c[1] == str(nepo):
                            newfile.write("{},{},{},{},{}\n".format(
                                percentage,
                                nepo,
                                shape,
                                (float(a[3])+float(b[3])+float(c[3]))/3,
                                (float(a[4])+float(b[4])+float(c[4]))/3))
"""""""""""

#path_result = "D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_10_angles_10"
#path_result_run_list = ["D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_10_angles_10\\Entire_Run_1",
                        #"D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_10_angles_10\\Entire_Run_2",
                        #"D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test\\noise_10_angles_10\\Entire_Run_3"]
#entire_run_num = 3
#average_result_noise_angle(path_result, path_result_run_list,entire_run_num,18)

