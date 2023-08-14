import torch
import torch.nn as nn


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(225, 100)
        self.fc2 = nn.Linear(100, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 32)
        self.fc5 = nn.Linear(32, 1)

    def forward(self, x):
        x1 = torch.relu(self.fc1(x))
        x2 = torch.relu(self.fc2(x1))
        x3 = torch.relu(self.fc3(x2))
        x4 = torch.relu(self.fc4(x3))
        x5 = self.fc5(x4)
        #print("x1:",x1,"x2:",x2,"x3:",x3,"x4:",x4)
        return x5


# Create the neural network
My_nn = NeuralNetwork()


def use_nn_forward(data, loss):
    data = torch.tensor(data, dtype=torch.float, requires_grad=True)

    if loss != -1:
        print("loss: ", loss)
        loss_tensor = torch.tensor(loss, dtype=torch.float)
        loss_tensor.requires_grad_(True)
        loss_tensor.backward()
    return My_nn(data).item() * 1000



