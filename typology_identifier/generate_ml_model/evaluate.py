import os
import torch
import  pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image

from ML_pytorch import Net,BuildingsDataset,BuildingsDataset_single

import time



classes = ['double_z', 'h_type_1', 'h_type_2', 'rect_crop', 'square']
class_to_label = {'double_z':0,'h_type_1':1,'h_type_2':2,'rect_crop':3,'square':4}

# class BuildingsDataset(Dataset):
#     def __init__(self, root_dir, transform=None):
#         self.root_dir = root_dir
#         self.transform = transform
#         self.len = 0
#         self.idx_to_image = {}
#         idx = 0
#         for class_ in classes:
#             files = os.listdir(root_dir + class_)
#             self.len += len(files)
#             for file in files:
#                 img_name = root_dir + class_ + '/' + file
#                 self.idx_to_image[idx] = [img_name, class_to_label[class_]]
#                 idx += 1
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
#
# class Net(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.conv1 = nn.Conv2d(1, 6, 5)
#         self.pool = nn.MaxPool2d(2, 2)
#         self.conv2 = nn.Conv2d(6, 16, 5)
#         self.fc1 = nn.Linear(5776, 120)
#         self.fc2 = nn.Linear(120, 84)
#         self.fc3 = nn.Linear(84, 5)
#         self.softmax = nn.Softmax(1)
#
#     def forward(self, x):
#         x = self.pool(F.relu(self.conv1(x)))
#         x = self.pool(F.relu(self.conv2(x)))
#         x = torch.flatten(x, 1) # flatten all dimensions except batch
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#         x = self.softmax(x)
#         return x

# train_path = "Training_data/"
#
# train_dataset = BuildingsDataset(root_dir=train_path,
#                                            transform=transforms.Compose([
#                                                transforms.ToTensor(),transforms.Scale((90,90))
#                                            ]))
#
# train_loader = DataLoader(dataset=train_dataset,shuffle=True)


model = Net()  # open the model before the loop of the buildings

model.load_state_dict(torch.load('model2.pkl'))
model.eval()

# torch.save(model, 'model1.pkl')

# test_path = "Test_data/"
test_path = "D:\Elie\PhD\Programming\Machine_Learning_Identifier\Test_data/"

test_dataset = BuildingsDataset(root_dir=test_path, classes=classes,class_to_label=class_to_label,
                                           transform=transforms.Compose([
                                               transforms.ToTensor(),transforms.Scale((90,90))
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

    # ## test
    # print(outputs)
    # print(labels)
    # break
    # ## test

    _, predicted = torch.max(outputs.data, 1)
    total += labels.size(0)

    correct += (predicted.cpu() == labels).sum()

print("Test Accuracy: {} %".format(100 * correct / total))