"""
Main functions to identify the typologies of buildings based on their footprint
"""

import os
import torch

import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms
from torch.utils.data import DataLoader

from typology_identifier.generate_models._load_ml_parameters import load_ml_parameters
from typology_identifier.generate_models._ml_datasets_and_network_classes import SingleBuildingDataset, Net


# def identify_typology(footprint, year, ml_model):
#     """
#         Return the typology identifier the building belongs to according to its footprint geometry
#         and the year it was built.
#
#     Args:
#         footprint [?]: footprint of the building (shapely? Face3D?)
#         year [int]: year the building was built
#         ml_model: machine learning model to use (a priori a special class containing the model(s)
#             and the typology identifier
#
#     Returns:
#         A Face3D type rectangle representing the oriented bounding box.
#     """


def identify_shape_type(lb_face_footprint, ml_model, path_folder_image, pixel_size, labels_to_shapes_dic, min_prob=90.):
    """
        Return the typology identifier the building belongs to according to its footprint geometry
        and the year it was built.

    Args:
        footprint [lb_footprint]: footprint of the building (shapely? Face3D?)
        ml_model: machine learning model to use

    """
    # load model parameter

    # convert lb to png
    path_lb_footprint_png = lb_face_to_png_BnW(lb_face=lb_face_footprint, path_folder_image=path_folder_image)
    # creat dataloader
    image_loader = png_to_ml_dataloader(path_image=path_lb_footprint_png, pixel_size=pixel_size)
    # identify
    for image in image_loader:  # need to access this way, can only be used as iterable (but there is only one value here)
        output = ml_model(image)  # send the image to the model
        shape_probability_list = ml_output_to_probability_list(ml_output=output)

    prob_max = max(shape_probability_list)
    if prob_max > min_prob:
        shape_identified = labels_to_shapes_dic[shape_probability_list.index(prob_max)]
    else:
        shape_identified="default"

    return (shape_identified)


def identify_shape_type_from_lb_footprint(lb_face_footprint, path_model_param_json, path_folder_image):
    """
    todo
    :param lb_face_footprint:
    :param path_model_param_json:
    :param path_folder_image:
    :return:
    """

    # load model parameter
    identifier, path_training_data, path_test_data, path_model_pkl, shapes, shapes_to_labels_dic, labels_to_shapes_dic, \
    nb_shapes, pixel_size = load_ml_parameters(path_model_param_json)
    # load model
    model = load_ml_model(path_model_pkl, nb_shapes)
    # convert lb to png
    path_lb_footprint_png = lb_face_to_png_BnW(lb_face=lb_face_footprint, path_folder_image=path_folder_image)
    # creat dataloader
    image_loader = png_to_ml_dataloader(path_image=path_lb_footprint_png, pixel_size=pixel_size)
    # identify
    shape_probability_list = None  # initialize
    for image in image_loader:  # need to access this way, can only be used as iterable (but there is only one value here)
        output = model(image)  # send the image to the model
        shape_probability_list = ml_output_to_probability_list(ml_output=output)


def probability_list_to_shape_type(probability_list, labels_to_shapes_dic, minimum_proba=70):
    """ todo """


def ml_output_to_probability_list(ml_output):
    """ todo """
    probability_list = ml_output[0]  # for some reason the probability are in a list of list : [[0.1,0.2...,0.4]]
    probability_list = list(map(float, probability_list))  # convert tensor to float list
    probability_list = [proba * 100 for proba in probability_list]  # convert to probability in percent
    return probability_list


def identify_shape_type_from_png_bnw(path_image_footprint, ml_model, ml_model_param):
    """
    todo
    """
    png_to_ml_dataset(path_image, pixel_size)


def load_ml_model(path_model_pkl, nb_shapes):
    """
    todo
    """

    # Initialize the model
    model = Net(nb_classes=nb_shapes)  # open the model before the loop of the buildings
    # load the model
    model.load_state_dict(torch.load(path_model_pkl))

    return model


def lb_face_to_xy_list(lb_face):
    """ create two list, x and y, containing the list of the x and y coordinates of the vertices of the lb face """
    pt3d_list = list(lb_face.boundary)  #
    # Init
    x = []
    y = []
    for pt3d in pt3d_list:
        x.append(pt3d.x)
        y.append(pt3d.y)

    return x, y


def lb_face_to_png_BnW(lb_face, path_folder_image, building_id="single_test"):
    """ Convert LB Face3D of a building footprint into a black and white image for ML typology identification """
    # Convert LB Face3D to x and y list of coordinates
    x, y = lb_face_to_xy_list(lb_face)

    # Init path image
    image_file = "building_" + building_id + ".png"
    path_image = os.path.join(path_folder_image, image_file)

    # Generate RGB image
    plt.plot(x, y)
    plt.axis('off')
    plt.axis('equal')
    plt.savefig(path_image, bbox_inches=0, dpi=300)
    plt.clf()

    ## Convert to black and white
    img = Image.open(path_image)
    img = img.convert("L")
    img.save(path_image)

    return path_image


def png_to_ml_dataloader(path_image, pixel_size):
    """ Convert the single image to a SingleBuildingDataset """
    # Create the dataset
    dataset = SingleBuildingDataset(path_image=path_image,
                                    transform=transforms.Compose(
                                        [transforms.ToTensor(), transforms.Resize((pixel_size[0], pixel_size[1]))]))
    # Convert into loader
    image_loader = DataLoader(dataset=dataset)

    return image_loader
