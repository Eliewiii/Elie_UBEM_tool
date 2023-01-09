"""


"""

import torch
import pickle
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch.nn as nn
import torch.optim as optim

from _make_ml_datasets_and_network import MultipleBuildingsDataset, Net

from _load_ml_parameters import load_ml_parameters


def train_ml_model(path_model_parameters_json, num_epochs=30, batch_size=64, learning_rate=0.001):
    """

    :param path_model_parameters_json:
    :return:
    """

    path_training_data, path_test_data, shapes, shapes_to_labels_dic, \
    nb_shapes, pixel_size,path_model_pkl = load_ml_parameters(path_model_parameters_json)

    train_dataset = MultipleBuildingsDataset(root_dir=path_training_data,
                                             transform=transforms.Compose([
                                                 transforms.ToTensor(), transforms.Scale((pixel_size[0], pixel_size[1]))
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

    # todo : save model


def evaluate_ml_model(path_model_parameters_json):
    """

    :param path_model_parameters_json:
    :return:
    """

    path_training_data, path_test_data, shapes, shapes_to_labels_dic, \
    nb_shapes, pixel_size,path_model_pkl = load_ml_parameters(path_model_parameters_json)

    test_dataset = MultipleBuildingsDataset(root_dir=path_training_data,
                                            transform=transforms.Compose([
                                                transforms.ToTensor(), transforms.Scale((pixel_size[0], pixel_size[1]))
                                            ]))

    model = Net()  # open the model before the loop of the buildings

    model.load_state_dict(torch.load('model2.pkl'))
    model.eval()


if __name__ == "__main__":
    None
