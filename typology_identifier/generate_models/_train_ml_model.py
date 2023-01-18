"""


"""
import os

import torch
import pickle
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch.nn as nn
import torch.optim as optim

from _make_ml_datasets_and_network import MultipleBuildingsDataset, Net

from _load_ml_parameters import load_ml_parameters


def train_ml_model(path_folder_model,path_model_parameters_json, num_epochs=30, batch_size=1, learning_rate=0.0001):
    """
    Train the machine learning algorithm
    :param path_model_parameters_json:
    :param num_epochs [int]: number of loops of training ?
    :param batch_size [int]: todo ?
    :param learning_rate [float]: todo ?
    """
    # Load model parameter
    identifier,path_training_data, path_test_data,path_model_pkl, shapes, shapes_to_labels_dic, \
    nb_shapes, pixel_size = load_ml_parameters(path_model_parameters_json)

    # Make the data set from the training images
    train_dataset = MultipleBuildingsDataset(classes=shapes,
                                             class_to_label=shapes_to_labels_dic,
                                             root_dir=path_training_data,
                                             transform=transforms.Compose([
                                                 transforms.ToTensor(), transforms.Resize((pixel_size[0], pixel_size[1]))
                                             ]))

    # Load the dataset according to the batch size and shuffle the images
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

    # Make the model
    model = Net(nb_classes=nb_shapes)
    criterion = nn.CrossEntropyLoss() # training criteria
    optimizer = optim.Adam(model.parameters(), lr=learning_rate) # choose optimizer

    # start the training of the model
    model.train()
    print("Training Starts")
    for e in range(num_epochs): # loop over the epochs
        running_loss = 0  # initialize loss
        for data in train_loader:
            images = data['image']  # load image
            labels = data['label']  # load the label of the image

            optimizer.zero_grad()

            output = model(images)  # pass the image through the model
            loss = criterion(output, labels)  # compute the loss

            loss.backward()

            optimizer.step()

            running_loss += loss.item()  # sums the loss
        else:
            print("Epoch {} - Training loss: {}".format(e, running_loss / len(train_loader)))
    print("Training Done")

    # save model
    torch.save(model.state_dict(),path_model_pkl)

    # Write the training parameters in a txt file
    with open(os.path.join(path_folder_model,"model_training_param.txt"),"w") as training_par_file :
        training_par_file.write(f"number of epochs = {num_epochs}, batch_size = {batch_size}, learning_rate = {learning_rate} ")


# Training
if __name__ == "__main__":
    path_folder_model ="D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\Tel_Aviv_MOE"
    path_model_parameters_json = os.path.join(path_folder_model,"model_param.json")
    train_ml_model(path_folder_model,path_model_parameters_json, num_epochs=3, batch_size=1, learning_rate=0.0001)

