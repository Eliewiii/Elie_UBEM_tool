"""


"""
import os.path

import torch
import pickle
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch.nn as nn
import torch.optim as optim

from _make_ml_datasets_and_network import MultipleBuildingsDataset, Net

from _load_ml_parameters import load_ml_parameters


def train_ml_model(path_model_parameters_json, num_epochs=30, batch_size=1, learning_rate=0.0001):
    """

    :param path_model_parameters_json:
    :param num_epochs [int]: number of loops of training ?
    :param batch_size [int]: todo ?
    :param learning_rate [float]: todo ?
    :return:
    """

    identifier,path_training_data, path_test_data,path_model_pkl, shapes, shapes_to_labels_dic, \
    nb_shapes, pixel_size = load_ml_parameters(path_model_parameters_json)

    train_dataset = MultipleBuildingsDataset(classes=shapes,
                                             class_to_label=shapes_to_labels_dic,
                                             root_dir=path_training_data,
                                             transform=transforms.Compose([
                                                 transforms.ToTensor(), transforms.Resize((pixel_size[0], pixel_size[1]))
                                             ]))

    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

    model = Net(nb_classes=nb_shapes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    model.train()
    print("Training Starts")
    for e in range(num_epochs):
        running_loss = 0
        for data in train_loader:
            images = data['image']
            labels = data['label']

            optimizer.zero_grad()

            output = model(images)
            loss = criterion(output, labels)

            loss.backward()

            optimizer.step()

            running_loss += loss.item()
        else:
            print("Epoch {} - Training loss: {}".format(e, running_loss / len(train_loader)))
    print("Training Done")

    # save model
    torch.save(model.state_dict(),path_model_pkl)


def evaluate_ml_model(path_model_parameters_json):
    """

    :param path_model_parameters_json:
    :return:
    """

    identifier,path_training_data, path_test_data,path_model_pkl, shapes, shapes_to_labels_dic, \
    nb_shapes, pixel_size = load_ml_parameters(path_model_parameters_json)


    model = Net(nb_classes=nb_shapes)  # open the model before the loop of the buildings

    model.load_state_dict(torch.load(path_model_pkl))
    model.eval()

    test_dataset = MultipleBuildingsDataset(classes=shapes,
                                             class_to_label=shapes_to_labels_dic,
                                             root_dir=path_test_data,
                                             transform=transforms.Compose([
                                                 transforms.ToTensor(), transforms.Resize((pixel_size[0], pixel_size[1]))
                                             ]))

    test_loader = DataLoader(dataset=test_dataset)

    evaluation_dictionary, label_to_shape = make_evaluation_dictionary(shapes_to_labels_dic)

    total = 0
    correct = 0
    for data in test_loader:
        images = data['image']
        labels = data['label']

        outputs = model(images)

        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)

        correct += (predicted.cpu() == labels).sum()

        #
        evaluation_dictionary[label_to_shape[int(labels[0])]]["nb_image"] = evaluation_dictionary[label_to_shape[int(labels[0])]]["nb_image"] + 1
        evaluation_dictionary[label_to_shape[int(labels[0])]]["nb_identified"] = evaluation_dictionary[label_to_shape[int(labels[0])]]["nb_identified"] + int((predicted.cpu() == labels).sum())

    print("Test Accuracy: {} %".format(100 * correct / total))

    for shape in list(evaluation_dictionary.keys()):
        evaluation_dictionary[shape]["accuracy"] = evaluation_dictionary[shape]["nb_identified"]/evaluation_dictionary[shape]["nb_image"]
    print(evaluation_dictionary)
    # todo : better printing and automatoc geberation of text file with the details



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



# Training
if __name__ == "__main__":
    path_model_parameters_json ="D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\model_sample\model_sample.json"
    train_ml_model(path_model_parameters_json, num_epochs=10, batch_size=1, learning_rate=0.0001)

# Evaluation
if __name__ == "__main__":
    path_model_parameters_json ="D:\Elie\PhD\Simulation\Input_Data\Typology\machine_learning_training\model_sample\model_sample.json"
    evaluate_ml_model(path_model_parameters_json)