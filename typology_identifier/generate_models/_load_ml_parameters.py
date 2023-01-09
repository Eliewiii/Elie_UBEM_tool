"""
Load the input parameters of a machine learning model for training and testing from json
"""

import json
import os


def load_ml_parameters(path_json):
    """
        Extract the parameters of the machine learning model from json file for training and testing
        (and later to load existing model in the main program)

    :param path_json:

    :return path_training_data:
    :return path_test_data:
    :return shapes [list]:
    :return shapes_to_labels [dic]:
    :return nb_shapes [int]:
    :return pixel_size [tuple]:
     todo: path_model_pkl
    """
    parameter_dic = None  # initialization
    with open(path_json) as json_file:
        parameter_dic = json.load(json_file)  # dictionary with all the data from the json file

    identifier = parameter_dic["identifier"]

    # path to the images datasets
    path_training_data = os.path.join(parameter_dic["path_folder"], "training")
    path_test_data = os.path.join(parameter_dic["path_folder"], "test")
    path_model_pkl = os.path.join(parameter_dic["path_folder"], identifier + ".pkl")
    # List with the identifier of the shapes
    shapes = parameter_dic["shapes"]
    # Dictionary with the identifier and labels of the shapes
    shapes_to_labels_dic = {}
    for index, shape in enumerate(shapes):
        shapes_to_labels_dic[index] = shape
    # Number of shapes
    nb_shapes = len(shapes)
    # Size in pixel
    pixel_size = parameter_dic["pixel_size"]

    return path_training_data, path_test_data, shapes, shapes_to_labels_dic, nb_shapes, pixel_size,path_model_pkl


if __name__=="__main__":
    test=load_ml_parameters("D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\model_sample\model_sample.json")

