# Inputs, path to model
#path_folder_model = "D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\Tel_Aviv_MOE_test" # TO MODIFY
#path_folder_model="D:\\Pycharm\\meachnie_learning\\Neve_Avivim_test"  # Tiantian personal computer
path_folder_model="C:\\Users\\lcalab\\Documents\\Tiantian\\test_2"  # LCA lab computer


""" Parameters for image generation """
is_deg = False  # tell if the GIS are in degree or in meters, if degree it needs to be converted in meter.

nb_noised_sample = [10,20,50]
# nb_noised_sample = [(i*10-5*(i-1)) for i in range(1, 3)]  # TO MODIFY 30-40

nb_angles_sample = [36]      # TO MODIFY 35
nb_max_shift_sample = [0.5]
nb_iteration = 3

""" Parameters for training and evaluation """

# Inputs parameters training
step_num_epochs = 5  ## TO MODOIFY  ##
total_number_epoch = 50
epoch_list = [i*step_num_epochs for i in range(1,total_number_epoch//step_num_epochs+1)]

continue_training = True  ## TO MODOIFY  ## continue the training of an existing model (if it exist) or create a new one

batch_size = 8
learning_rate = 0.001
# Inputs parameters evaluation
min_percentage_list = [0.65,0.70,0.75, 0.8, 0.85]
# parameters
path_result_run_dic = {}
entire_run_num = 3
