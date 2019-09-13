from aiGame import *

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter
import tensorflow as tf
import numpy as np


WIDTH = 500
HEIGHT = 500
LR = 1e-3

initialGames = 1000
duration = 200
minScore = 101
modelName = 'trainedModel.tflearn'



game = Game(WIDTH, HEIGHT)  
game.resetGame()

def main():
    print("STARTING TRAINING...")
    # # run series of random games
    # randomGames(10)
    # exit()

    initialData = initialPopulation(initialGames)
    model = trainModel(initialData)

    # use prexisting model
    # model = tflearn.DNN(tflearn.input_data(shape = [None, 0]))
    # model.load(modelName)

    evaluate(model, 1) # check 3 games of the ai playing

def randomGames(nGames):
    for g in range(nGames):

        game.resetGame()
        for _ in range(duration):
            game.handleAction(random.randint(0,2))
            game.runGame()
            game.refresh()

        print("GAME: " + str(g + 1) + " SCORE: " + str(game.score))

def initialPopulation(nGames, model = False):
    
    trainingData = []
    scores = []
    acceptedScores = []


    for g in range(nGames):
        gameMemory = []
        prevObservation = []

        game.resetGame()
        for _ in range(duration):

            action = random.randint(0,1)
            if len(prevObservation) > 0:
                if model:
                    action = np.argmax(model.predict(prevObservation.reshape(-1, len(prevObservation), 1))[0])


            game.handleAction(action)
            game.runGame() # observation
            

            # game.refresh()


            observation = game.getObservation()

            if len(prevObservation) > 0:
                gameMemory.append([prevObservation, action])

            prevObservation = observation

        if game.score > minScore:
            acceptedScores.append(game.score)
            for data in gameMemory:
                if data[1] == 1:
                    output = [0, 1]
                elif data[1] == 0:
                    output = [1, 0]
                trainingData.append([data[0], output])

        print("GAME: " + str(g + 1) + "/" + str(nGames), end = '\r')
        scores.append(game.score)

    trainingDataSave = np.array(trainingData)
    np.save('trainingData.npy', trainingDataSave)

    print("SIZE: " + str(len(scores)))
    return trainingData

def neuralNetworkModel(inputSize):
    # build the hidden layers
    network = input_data(shape = [None, inputSize, 1], name = 'input')

    network = fully_connected(network, 128, activation = 'relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation = 'relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation = 'relu')
    network = dropout(network, 0.8)
    # final output (left or right)
    network = fully_connected(network, 2, activation = 'softmax')
    network = regression(network, optimizer = 'adam', learning_rate = LR, name = 'targets')

    model = tflearn.DNN(network, tensorboard_dir = 'log')

    return model

def trainModel(trainingData, model = False):

    shape_second_parameter = len(trainingData[0][0]) # [0][0] = observations
    x = np.array([i[0] for i in trainingData]).reshape(-1, shape_second_parameter, 1)
    y = [i[1] for i in trainingData]


    if not model: # if we don't have a model, build one off training data
        model = neuralNetworkModel(len(x[0]))
    else:
        print("existing model")

    model.fit({'input': x}, {'targets': y}, n_epoch = 3, snapshot_step = 500, show_metric = True, run_id = 'openaistuff')
    model.save(modelName)
    return model
    
def evaluate(model, nGames):
    print("\n\n====================\nSTARTING EVALUATION\n====================\n\n\n")
    print("press enter to continue")
    input()

    scores = []
    choices = []

    gameMemory = []
    prevObservation = []
    game.resetGame()
    

    while(game.running):
        action = random.randint(0,2)
        if (len(prevObservation) > 0):
            # print(model.predict(prevObservation.reshape(-1, len(prevObservation), 1))[0])
            action = np.argmax(model.predict(prevObservation.reshape(-1, len(prevObservation), 1))[0])

        choices.append(action)
        game.handleAction(action)
        game.runGame()

        prevObservation = numpy.array(game.getObservation())
        game.refresh()


    scores.append(game.score)



    # DONE EVALUATION
    # PRINT RESULTS
    print("SCORE:", game.score//100)
    print("LEFT:", choices.count(0))
    print("RIGHT:", choices.count(1))


if __name__ == '__main__':
    print("BEGIN TRAINING") 
    main()
