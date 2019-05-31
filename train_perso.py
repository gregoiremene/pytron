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
    learning_rate = 4e-3
    momentum = 0.9

    # Initialize Neural Network
    net = Net()
    torch.save(net.state_dict(), 'ais/' + ai_name + '/ai.bak')

    # Initialize Optimizer
    criterion = nn.MSELoss()
    optimizer = optim.SGD(net.parameters(), lr=learning_rate, momentum=momentum)

    games = 0  # total number of games played
    moyenne_duration = 0
    moyenne_loss = 0

    max_minibatch = 10000

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
                    if len(actions) < max_minibatch:
                        actions.append(game.history[step].player_one_direction.value - 1)
                    else:
                        actions[games%max_minibatch] = game.history[step].player_one_direction.value - 1
                    #actions.append(game.history[step].player_one_direction.value - 1)
                elif p == 2:
                    if len(actions) < max_minibatch:
                        actions.append(game.history[step].player_two_direction.value - 1)
                    else:
                        actions[games%max_minibatch] = game.history[step].player_two_direction.value - 1
                    #actions.append(game.history[step].player_two_direction.value - 1)

                # Get game state at this step
                if len(states) < max_minibatch:
                    states.append(game.history[step].map.state_for_player(p))
                else:
                    states[games%max_minibatch] = game.history[step].map.state_for_player(p)
                #states.append(game.history[step].map.state_for_player(p))
                
                # Get player reward for the action taken at this step
                # cf. Slide 6 from Reinforcement Learning class: "Classical version"
                if step < game_duration - 1:
                    if len(rewards) < max_minibatch:
                        rewards.append(0)
                    else:
                        rewards[games%max_minibatch] = 0
                    #rewards.append(0)
                elif game.winner == p:
                    if len(rewards) < max_minibatch:
                        rewards.append(1)
                    else:
                        rewards[games%max_minibatch] = 1
                    #rewards.append(1)
                else:
                    if len(rewards) < max_minibatch:
                        rewards.append(-1)
                    else:
                        rewards[games%max_minibatch] = -1
                    #rewards.append(-1)

        #utiliser sample de random ! retenir dans une liste et prendre dans la subsec
        #que les mêmes indices pour rewards, actions, et states sinon ça sera pas 
        #coordonné
        
        taille_subsect_minibatch = 500
        liste_indice = range(taille_subsect_minibatch)
        subsect_minibatch = []
        i = len(states)
        if i < taille_subsect_minibatch:
            for a in range(0, len(states)):
                subsect_minibatch.append([states[a], actions[a], rewards[a]])
        else:
            liste_alea_indice = random.sample(liste_indice, taille_subsect_minibatch)
            for a in range(0, len(liste_alea_indice)):
                subsect_minibatch.append([states[liste_alea_indice[a]], actions[liste_alea_indice[a]], rewards[liste_alea_indice[a]]])
        
        #print('taille states : [%5d], taille subsecminibatch : [%5d]' % (len(states), len(subsect_minibatch)))
        #construction des états pour le inputs
        states_inputs = []
        for c in range(0,len(subsect_minibatch)):
            states_inputs.append(subsect_minibatch[c][0])
        inputs = np.reshape(states_inputs, (len(subsect_minibatch), 1, width + 2, height + 2))
        inputs = torch.from_numpy(inputs).float()

        # Compute predicted Q-values for each step and find the maximal predicted Q-value
        pred_q_values = net(inputs)
        max_outputs = pred_q_values.max(dim=1)[0]

        # Copy predicted Q-values into target Q_values
        target_q_values = pred_q_values.clone().detach()

        # Apply Bellman equation to determine the target Q_value for the action that was taken

        #juste changer le for pour parcourir le subsec batch
        for aux in range(0, len(subsect_minibatch) - 1):
            if abs(subsect_minibatch[aux][2]) == 1:
                target_q_values[aux, subsect_minibatch[aux][1]] = subsect_minibatch[aux][2]
            else:
                #print('actions[aux] : %3.3f, aux : %5d' % (actions[aux], aux))
                rew = subsect_minibatch[aux][2]
                maxx = max_outputs[aux + 1]
                #target_q_values[aux, subsect_minibatch[aux][1]] = subsect_minibatch[aux][2] + gamma * max_outputs[aux + 1]
                target_q_values[aux, subsect_minibatch[aux][1]] = rew + gamma * maxx

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

        nombre_echant = 1000
        if (games == 1):
            moyenne_duration = game_duration
            moyenne_loss = loss
            #print('[%5d] average loss: %.3f, average duration: %3.3f' % (games, moyenne_loss, moyenne_duration))
        elif (games%nombre_echant == 0):
            print('[%5d] average loss: %.3f, average duration: %3.3f' % (games, moyenne_loss/nombre_echant, moyenne_duration//nombre_echant))
            moyenne_duration = 0
            moyenne_loss = 0
        else:
            moyenne_duration = moyenne_duration + game_duration
            moyenne_loss = moyenne_loss + loss


if __name__ == '__main__':
    main()
