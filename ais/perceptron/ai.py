from tron.player import Player, Direction
from tron.game import Tile

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

import os

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1, 1)
        self.fc1 = nn.Linear(64*144, 400)
        self.fc2 = nn.Linear(400, 50)
        self.fc3 = nn.Linear(50, 4)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1, 64*144)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


class Ai(Player):
    """
    This class implements an AI based on the perceptron defined in class Net
    """
    def __init__(self):
        super(Ai, self).__init__()
        self.net = Net()
        # Load network weights if they have been initialized already
        exists = os.path.isfile(self.find_file('ai.bak'))
        if exists:
            self.net.load_state_dict(torch.load(self.find_file('ai.bak')))

    def action(self, map, id):

        game_map = map.state_for_player(id)

        input = np.reshape(game_map, (1, 1, game_map.shape[0], game_map.shape[1]))
        input = torch.from_numpy(input).float()
        output = self.net(input)

        _, predicted = torch.max(output.data, 1)
        predicted = predicted.numpy()
        next_action = predicted[0] + 1

        if next_action == 1:
            next_direction = Direction.UP
        if next_action == 2:
            next_direction = Direction.RIGHT
        if next_action == 3:
            next_direction = Direction.DOWN
        if next_action == 4:
            next_direction = Direction.LEFT

        return next_direction
