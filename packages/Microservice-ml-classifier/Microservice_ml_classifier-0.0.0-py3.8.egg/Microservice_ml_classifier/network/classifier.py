import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.sequential1 = nn.Sequential(nn.Conv2d(3, 6, 5),
                                         nn.ReLU(),
                                         nn.Dropout(0.2),
                                         nn.MaxPool2d(2, 2))
        self.sequential2 = nn.Sequential(nn.Conv2d(6, 16, 5),
                                         nn.ReLU(),
                                         nn.Dropout(0.2),
                                         nn.MaxPool2d(2, 2))
        self.sequential3 = nn.Sequential(nn.Linear(16 * 5 * 5, 120),
                                         nn.ReLU(),
                                         nn.Dropout(0.2))
        self.sequential4 = nn.Sequential(nn.Linear(120, 84),
                                         nn.ReLU(),
                                         nn.Dropout(0.2))
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.sequential1(x)
        x = self.sequential2(x)
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = self.sequential3(x)
        x = self.sequential4(x)
        x = self.fc3(x)
        return x