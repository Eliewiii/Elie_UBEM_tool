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
    Create sub-folders in a folder
    :param path_folder:
    :param list_sub_folder:

    """
    clean_folder(path_folder)
    for folder in list_sub_folder:
        os.mkdir(os.path.join(path_folder, folder))


def move_input_files_to_output_folder(path_folder_simulation, path_EP_parameter_par=None, path_sim_input_par=None,
                                      path_epw_par=None, path_gis_par=None):
    """
    Move the input files to the output folder to have a trace of the inputs used.
    """
    if path_EP_parameter_par:  # if not None...
        for jsonfile in os.listdir(path_EP_parameter_par):
            shutil.copy(os.path.join(path_EP_parameter_par, jsonfile),
                        os.path.join(path_folder_simulation, "Inputs", "EP_parameters"))
    if path_sim_input_par:
        shutil.copy(path_sim_input_par, os.path.join(path_folder_simulation, "Inputs", "Simulation_input"))
    if path_epw_par:
        shutil.copy(path_epw_par, os.path.join(path_folder_simulation, "Inputs", "EPW"))
    if path_gis_par:
        shutil.copy(path_gis_par, os.path.join(path_folder_simulation, "Inputs", "GIS"))


def create_folder_output(path_folder_simulation):
    """
    Create the a folder for the simulation for the inputs, outputs, logs etc.

    :param path_folder_simulation:
    """
    ## Create or overwrite the output simulation folder ##
    clean_folder(path_folder_simulation)
    ## Create the main sub-folders ##
    make_sub_folders(path_folder=path_folder_simulation,
                     list_sub_folder=["Context", "Buildings", "Inputs", "Libraries", "Results", "Urban_canopy"])
    ## Create Inputs sub-folders ##
    path_folder_output_inputs = os.path.join(path_folder_simulation, "Inputs")
    make_sub_folders(path_folder=path_folder_output_inputs,
                     list_sub_folder=["EP_parameters", "EPW", "GIS", "Simulation_input"])

