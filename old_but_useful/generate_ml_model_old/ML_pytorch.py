import os
import torch
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(5776, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 5)
        self.softmax = nn.Softmax(1)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)  # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        x = self.softmax(x)
        return x


class BuildingsDataset(Dataset):
    def __init__(self, classes, class_to_label, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.len = 0
        self.idx_to_image = {}
        idx = 0
        for class_ in classes:
            files = os.listdir(root_dir + class_)
            self.len += len(files)
            for file in files:
                img_name = root_dir + class_ + '/' + file
                self.idx_to_image[idx] = [img_name, class_to_label[class_]]
                idx += 1

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        img_name, label = self.idx_to_image[idx]
        image = Image.open(img_name)

        if self.transform:
            image = self.transform(image)

        sample = {'image': image, 'label': label}
        return sample


class BuildingsDataset_single(Dataset):
    """
    Dataset to test only one file

    """

    def __init__(self, image_path, transform=None):
        self.image_path = image_path
        self.transform = transform
        self.len = 1  # just one image
        self.idx_to_image = {}
        self.idx_to_image[0] = [self.image_path, 1000]  # the class id is set to 1000 because we don't care about this
        # thsi value anyway, we don't know class it belongs to

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        img_name, label = self.idx_to_image[idx]
        image = Image.open(img_name)

        if self.transform:
            image = self.transform(image)

        sample = {'image': image, 'label': label}
        return sample


def Identify_shape_typology(image_path, transform=None):
    """
    """
    test_dataset = BuildingsDataset_single(image_path=image_path,
                                           transform=transforms.Compose(
                                               [transforms.ToTensor(), transforms.Scale((90, 90))]))

    test_loader = DataLoader(dataset=test_dataset)

    for data in test_loader:
        images = data['image']
        labels = data['label']

        outputs = model(images)


# class BuildingsDataset2(Dataset):
#     def __init__(self, classes=None, root_dir=None,full_path=None, transform=None):
#         self.root_dir = root_dir
#         self.transform = transform
#         self.len = 0
#         self.idx_to_image = {}
#
#
#     @classmethod
#     def single_image(cls):
#         """
#         For a set of images
#         """
#         None
#
#
#
#
#
#     @classmethod
#     def full_data_set(cls, classes, class_to_label, root_dir, transform=None):
#         """
#         For a set of images
#         """
#         dataset = cls(classes, root_dir, transform=None)
#         idx = 0
#         for class_ in classes:
#             files = os.listdir(root_dir + class_)
#             dataset.len += len(files)
#             for file in files:
#                 img_name = root_dir + class_ + '/' + file
#                 dataset.idx_to_image[idx] = [img_name, class_to_label[class_]]
#                 idx += 1
#         return(dataset)
#
#
#
#     def __len__(self):
#         return self.len
#
#     def __getitem__(self, idx):
#         if torch.is_tensor(idx):
#             idx = idx.tolist()
#         img_name, label = self.idx_to_image[idx]
#         image = Image.open(img_name)
#
#         if self.transform:
#             image = self.transform(image)
#
#         sample = {'image': image, 'label': label}
#         return sample


if __name__ == "__main__":
    model = Net()  # open the model before the loop of the buildings

    model.load_state_dict(torch.load('model2.pkl'))
    model.eval()

    test_path = "D:\Elie\PhD\Programming\Machine_Learning_Identifier\Test_data\double_z\sample_0.png"
    # test_path = "D:\Elie\PhD\Programming\Machine_Learning_Identifier\Test_data\h_type_1\sample_0.png"
    # test_path = "D:\Elie\PhD\Programming\Machine_Learning_Identifier\Test_data\h_type_2\sample_0.png"
    # test_path = "D:\Elie\PhD\Programming\Machine_Learning_Identifier\Test_data\\rect_crop\sample_0.png"
    # test_path = "D:\Elie\PhD\Programming\Machine_Learning_Identifier\Test_data\square\sample_0.png"

    test_dataset = BuildingsDataset_single(image_path=test_path,
                                           transform=transforms.Compose([
                                               transforms.ToTensor(), transforms.Scale((90, 90))
                                           ]))

    # test_dataset_2 = BuildingsDataset2.full_data_set(root_dir=test_path, classes=classes,class_to_label=class_to_label,
    #                                            transform=transforms.Compose([
    #                                                transforms.ToTensor(),transforms.Scale((90,90))
    #                                            ]))
    # print(test_dataset.idx_to_image[0])
    # print(test_dataset_2.idx_to_image[0])

    test_loader = DataLoader(dataset=test_dataset)
    # test_loader = DataLoader(dataset=test_dataset_2)

    # print(test_loader[0])

    total = 0
    correct = 0
    for data in test_loader:
        images = data['image']
        labels = data['label']

        outputs = model(images)
        print(outputs)

        # ## test
        # print(outputs)
        # print(labels)
        # break
        # ## test

        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)

        correct += (predicted.cpu() == labels).sum()

    print("Test Accuracy: {} %".format(100 * correct / total))
