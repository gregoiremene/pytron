#!/usr/bin/env python3

import pygame

import random

import torch
import torch.optim as optim
import torch.nn as nn

import numpy as np

from tron.game import Game, PositionPlayer

from ais.perceptron.ai import Ai, Net

# Randomly initialize a player's position on the map
def init_player_position(width, height):
    init_player_X = random.randint(0, width - 1)
    init_player_Y = random.randint(0, height - 1)
    return [init_player_X, init_player_Y]


# Simulate a game
def play(width, height):

    # Initialize players' position
    init_player_1 = init_player_position(width, height)
    init_player_2 = init_player_position(width, height)

    # Ensure the players do not start at the same position
    while init_player_1[0] == init_player_2[0] and init_player_1[1] == init_player_2[1]:
        init_player_2 = init_player_position(width, height)

    # Create a game from its size and its players
    game = Game(width, height, [
        # We create two PositionPlayer for each player of the game.
        PositionPlayer(1, Ai(), init_player_1),
        PositionPlayer(2, Ai(), init_player_2)
    ])

    # Run the game.
    game.main_loop()

    return game


# Q-learning
def main():
    # Initialize the game engine
    pygame.init()

    # Prepare the size for the game.
    width = 10
    height = 10

    ai_name = 'perceptron'

    # Hyperparameters
    gamma = 0.9  # discount factor, used to balance between immediate and future rewards
    learning_rate = 1e-3
    momentum = 0.9

    # Initialize Neural Network
    net = Net()
    torch.save(net.state_dict(), 'ais/' + ai_name + '/ai.bak')

    # Initialize Optimizer
    criterion = nn.MSELoss()
    optimizer = optim.SGD(net.parameters(), lr=learning_rate, momentum=momentum)

    games = 0  # total number of games played

    max_minibatch = 2000

    # Data structures used for learning
        states = []  # maps of the game
        actions = []  # actions taken
        rewards = []  # immediate rewards obtained

    while 1:


        # Play a game
        game = play(width, height)

        # Game duration is the length of history - 1 (the last element is the final state of the game)
        game_duration = len(game.history) - 1

        # For each player
        for p in range(1, 3):

            # For each action
            for step in range(0, game_duration):
                # Get player action at this step
                if p == 1:
                    actions[games%max_minibatch] = game.history[step].player_one_direction.value - 1
                    #actions.append(game.history[step].player_one_direction.value - 1)
                elif p == 2:
                    actions[games%max_minibatch] = game.history[step].player_two_direction.value - 1
                    #actions.append(game.history[step].player_two_direction.value - 1)

                # Get game state at this step
                states[games%max_minibatch] = game.history[step].map.state_for_player(p)
                #states.append(game.history[step].map.state_for_player(p))
                
                # Get player reward for the action taken at this step
                # cf. Slide 6 from Reinforcement Learning class: "Classical version"
                if step < game_duration - 1:
                    rewards[games%max_minibatch] = 0
                    #rewards.append(0)
                elif game.winner == p:
                    rewards[games%max_minibatch] = 1
                    #rewards.append(1)
                else:
                    rewards[games%max_minibatch] = -1
                    #rewards.append(-1)

        inputs = np.reshape(states, (len(states), 1, width + 2, height + 2))
        inputs = torch.from_numpy(inputs).float()

        # Compute predicted Q-values for each step and find the maximal predicted Q-value
        pred_q_values = net(inputs)
        max_outputs = pred_q_values.max(dim=1)[0]

        # Copy predicted Q-values into target Q_values
        target_q_values = pred_q_values.clone().detach()

        # Apply Bellman equation to determine the target Q_value for the action that was taken
        

        #utiliser sample de random ! retenir dans une liste et prendre dans la subsec
        #que les mêmes indices pour rewards, actions, et states sinon ça sera pas 
        #coordonné
        taille_subsect_minibatch = 200
        subsect_minibatch = []
        i = states.size
        if i < taille_subsect_minibatch:
            for a in range(0, len(states)):
                subsect_minibatch.append([states[a], actions[a], rewards[a]])
        else:
            # randint avec % pour en prendre 200 (besoin d'un compteur?)    
        
        #juste changer le for pour parcourir le subsec batch
        for aux in range(0, len(actions)):
            if abs(rewards[aux]) == 1:
                target_q_values[aux, actions[aux]] = rewards[aux]
            else:
                target_q_values[aux, actions[aux]] = rewards[aux] + gamma * max_outputs[aux + 1]

        # zero the parameter gradients
        net.zero_grad()

        # print(target_q_values)

        # Compute loss between predicted and "real" q values
        loss = criterion(pred_q_values, target_q_values)

        # gradient back-propagation
        loss.backward()
        optimizer.step()

        games = games + 1
        torch.save(net.state_dict(), 'ais/' + ai_name + '/ai.bak')

        print('[%5d] loss: %.3f, duration: %3.3f' % (games, loss, game_duration))


if __name__ == '__main__':
    main()
