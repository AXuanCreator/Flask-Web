import torch

from torch import nn


class RecommendNet(nn.Module):
    def __init__(self, batch_size=50):
        super(RecommendNet, self).__init__()

        # FC层
        # self.fc_borrow = nn.Linear(4,7)
        self.fc1 = nn.Linear(8 * batch_size, 1*batch_size)
        self.fc2 = nn.Linear(16*batch_size, 1*batch_size)
        # self.fc3 = nn.Linear(10, 1)

        # 激活函数
        self.relu = nn.ReLU()

    def forward(self, x):

        # FORWARD
        # x = self.relu(self.fc1(x))
        # x = self.relu(self.fc2(x))
        output = self.relu(self.fc1(x))
        # output = self.relu(self.fc4(x))

        return output.squeeze()
