import os
import shutil


def clean_folder(path):
    """
    Clean a folder by deleting it and recreating it
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def make_sub_folders(path_folder, list_sub_folder):
    """
    :param path_folder:
    :param list_sub_folder:

    """
    for folder in list_sub_folder:
        os.mkdir(os.path.join(path_folder, folder))


def create_folder_simulation(path_folder_simulation):
    ## Create or overwrite the output simulation folder ##
    clean_folder(path_folder_simulation)
    ## Create the main sub-folders ##
    make_sub_folders(path_folder=path_folder_simulation,
                     list_sub_folder=["Context", "Buildings", "Inputs", "Libraries", "Results","Urban_canopy"])
    ## Create Inputs sub-folders ##
    path_folder_output_inputs=os.path.join(path_folder_simulation,"Inputs")
    # todo :
    #make_sub_folders(path_folder=path_folder_simulation,
                     list_sub_folder=["Context", "Buildings", "Inputs", "Libraries", "Results", "Urban_canopy"])