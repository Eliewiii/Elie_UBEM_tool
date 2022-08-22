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
os.environ["CUDA_VISIBLE_DEVICES"] = ""

train_path = "../../../Machine_Learning_Identifier/Training_data/"

classes = ['double_z', 'h_type_1', 'h_type_2', 'rect_crop', 'square']
class_to_label = {'double_z':0,'h_type_1':1,'h_type_2':2,'rect_crop':3,'square':4}


class BuildingsDataset(Dataset):
    def __init__(self, root_dir, transform=None):
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


num_epochs = 30
batch_size =64
learning_rate = 0.001

train_dataset = BuildingsDataset(root_dir=train_path,
                                           transform=transforms.Compose([
                                               transforms.ToTensor(),transforms.Scale((90,90))
                                           ]))

train_loader = DataLoader(dataset=train_dataset,batch_size=batch_size,shuffle=True)



class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(5776, 120) #16*19*19
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 5)
        self.softmax = nn.Softmax(1)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        x = self.softmax(x)
        return x

# device = torch.device('cuda')
def to_gpu(x):
    return x
# def to_gpu(x):
#     return  x

model = Net()
model = to_gpu(model)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

model.train()
print("Training Starts")
for e in range(num_epochs):
    running_loss = 0
    for data in train_loader:
        images = to_gpu(data['image'])
        labels = to_gpu(data['label'])
        # images = data['image'].to(device)
        # labels = data['label'].to(device)

        optimizer.zero_grad()

        output = model(images)
        loss = criterion(output, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()
    else:
        print("Epoch {} - Training loss: {}".format(e, running_loss / len(train_loader)))
print("Training Done")

torch.save(model.state_dict(), '../../../Machine_Learning_Identifier/model1.pkl')