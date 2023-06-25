import os.path

import torch
import pickle
import json
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch.nn as nn
import torch.optim as optim

from _ml_datasets_and_network_classes import SingleBuildingDataset, Net

from _load_ml_parameters import load_ml_parameters


def evaluate_ml_model(path_model_parameters_json):
    """

    :param path_model_parameters_json:
    :return:
    """
    # Load model parameter
    identifier, path_training_data, path_test_data, path_model_pkl, shapes, shapes_to_labels_dic, labels_to_shapes_dic,  \
    nb_shapes, pixel_size = load_ml_parameters(path_model_parameters_json)

    # Initialize the model
    model = Net(nb_classes=nb_shapes)  # open the model before the loop of the buildings
    # load the model
    model.load_state_dict(torch.load(path_model_pkl))
    # start evaluation
    # Make the data set from the training images
    path_image= "D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\Tel_Aviv_MOE\\test\Train\\sample_0.png"
    test_dataset = SingleBuildingDataset(path_image=path_image,
                                             transform=transforms.Compose([
                                                 transforms.ToTensor(), transforms.Resize((pixel_size[0], pixel_size[1]))
                                             ]))
    # Load the dataset according to the batch size and shuffle the images
    test_loader = DataLoader(dataset=test_dataset)

    for image in test_loader:
        outputs = model(image)
        outputs = outputs[0]
        outputs = list(map(float,outputs))






def make_evaluation_dictionary(shapes_to_labels_dic):
    """

    :param shapes_to_labels_dic:
    :return evaluation_dictionary:
    :return label_to_shape:
    """
    label_to_shape={}
    for (shape,label) in list(shapes_to_labels_dic.items()):
        label_to_shape[label]=shape

    evaluation_dictionary = {}
    for shape in list(shapes_to_labels_dic.keys()):
        evaluation_dictionary[shape]={"nb_image": 0, "nb_identified":0, "accuracy":None}


    return evaluation_dictionary, label_to_shape



# Evaluation zob


if __name__ == "__main__":
    path_folder_model ="D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\Tel_Aviv_MOE"
    path_model_parameters_json = os.path.join(path_folder_model,"model_param.json")
    evaluate_ml_model(path_model_parameters_json)