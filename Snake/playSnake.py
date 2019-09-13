from snake import Game as game
from snake import Block as block
import pygame
from pygame.locals import *



LR = 1e-3
goal_steps = 300
score_requirement = 100
initial_games = 500
g = game(100)

black = (0,0,0)
white = (255,255,255)

def gameOverScreen(game):
    game.window.fill(black)
    game.snake.draw()

    myfont = pygame.font.SysFont('Comic Sans MS', 25)

    gameOverFont = pygame.font.SysFont('Comic Sans MS', 50)
    gameOverText = gameOverFont.render('GAME OVER!', True, white)
    scoreText = myfont.render("Your score is " + str(game.snake.score()), True, white)
    t1 = myfont.render("Q to quit", True, white)
    t2 = myfont.render("R to restart", True, white)

    game.window.blit(gameOverText,(130, 150))
    game.window.blit(scoreText, (170,250))
    game.window.blit(t1, (195,300))
    game.window.blit(t2, (185,320))

    pygame.display.update()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():

        if (event.type == pygame.QUIT or key[pygame.K_q]):
            pygame.quit()
            exit()
    if key[pygame.K_r]:
        game.snake.gameOver = False
        game.snake.body = [block(100,100, game.window), block(90,100, game.window), block(80,100,game.window)]
        game.snake.direction = 1
        game.window.fill(white)
        game.hasFood = False


def generate_population(model):
    # [OBS, MOVES]
    global score_requirement
 
    training_data = []
    # all scores:
    scores = []
    # just the scores that met our threshold:
    accepted_scores = []
    # iterate through however many games we want:
    print('Score Requirement:', score_requirement)
    for _ in range(initial_games):
        print('Simulation ', _, " out of ", str(initial_games), '\r', end="")
        # reset env to play again
        g.resetGame()
        score = 0
        # moves specifically from this environment:
        game_memory = []
        # previous observation that we saw
        prev_observation = []
        # for each frame in 200
        for _ in range(goal_steps):
            # choose random action (0 or 1)
            if len(prev_observation) == 0:
                action = g.snake.getRandomDirection()
            else:
                if not model:
                    action = g.snake.getRandomDirection()
                else:
                    prediction = model.predict(prev_observation.reshape(-1, len(prev_observation), 1))
                    g.snake.direction = np.argmax(prediction[0])
 
            # do it!
            # observation, reward, done, info = env.step(action)
            g.runGame()

            observation = g.getInfo()
            reward = g.snake.reward


            # notice that the observation is returned FROM the action
            # so we'll store the previous observation here, pairing
            # the prev observation to the action we'll take.
            if len(prev_observation) > 0:
                game_memory.append([prev_observation, g.snake.direction])
            prev_observation = observation
            score += reward
            if g.snake.gameOver: break
 
        # IF our score is higher than our threshold, we'd like to save
        # every move we made
        # NOTE the reinforcement methodology here.
        # all we're doing is reinforcing the score, we're not trying
        # to influence the machine in any way as to HOW that score is
        # reached.
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                # convert to one-hot (this is the output layer for our neural network)
 
                action_sample = [0, 0, 0, 0]
                action_sample[data[1]] = 1
                output = action_sample
                # saving our training data
                training_data.append([data[0], output])
 
        # save overall scores
        scores.append(score)
    # some stats here, to further illustrate the neural network magic!
    print('Average accepted score:', mean(accepted_scores))
    print('Score Requirement:', score_requirement)
    print('Median score for accepted scores:', median(accepted_scores))
    print(Counter(accepted_scores))
    score_requirement = mean(accepted_scores)
    
    # just in case you wanted to reference later
    training_data_save = np.array([training_data, score_requirement])
    np.save('saved.npy', training_data_save)
 
    return training_data



def create_dummy_model(training_data):
    shape_second_parameter = len(training_data[0][0])
    x = np.array([i[0] for i in training_data])
    X = x.reshape(-1, shape_second_parameter, 1)
    y = [i[1] for i in training_data]
    model = create_neural_network_model(input_size=len(X[0]), output_size=len(y[0]))
    return model
 
def create_neural_network_model(input_size, output_size):
    network = input_data(shape=[None, input_size, 1], name='input')
    
    network = tflearn.fully_connected(network, 32)
    network = tflearn.fully_connected(network, 64)
    network = tflearn.fully_connected(network, 128)
    network = tflearn.fully_connected(network, 64)
    network = tflearn.fully_connected(network, 32)


    network = fully_connected(network, output_size, activation='softmax')
    network = regression(network, name='targets')
    model = tflearn.DNN(network, tensorboard_dir='tflearn_logs')
 
    return model

def train_model(training_data, model=False):
    shape_second_parameter = len(training_data[0][0])
    x = np.array([i[0] for i in training_data])
    X = x.reshape(-1, shape_second_parameter, 1)
    y = [i[1] for i in training_data]
 
    model.fit({'input': X}, {'targets': y}, n_epoch=3, batch_size=16, show_metric=True)
    model.save('miniskake_trained.tflearn')
 
    return model
def randomGames(num):
    for n in range(num):
        g = game(100)
        g.resetGame()
        lost =  g.snake.gameOver
        while(not lost):

            lost = g.snake.gameOver
            g.runGame()
            g.snake.getRandomDirection()
            # g.snake.getDirection()


            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
                    break
            if key[pygame.K_q]:
                running = False
            if key[pygame.K_r]:
                g.resetGame()


def evaluate(model):
    # now it's time to evaluate the trained model
    scores = []
    choices = []
    g = game(20)
    for each_game in range(20):
        score = 0
        game_memory = []
        prev_obs = []
        g.resetGame()
        for _ in range(goal_steps): 
            if len(prev_obs) == 0:
                action = g.snake.getRandomDirection()
                print("RANDOM")
            else:
                prediction = model.predict(prev_obs.reshape(-1, len(prev_obs), 1))
                g.snake.direction = np.argmax(prediction[0])
                print("DECISION")
 
            choices.append(g.snake.direction)  
            g.runGame()    
            g.draw()      
            new_observation = g.getInfo()
            prev_obs = new_observation

            reward = g.snake.reward
            game_memory.append([new_observation, g.snake.direction])
            score += reward
            if g.snake.gameOver: break
 
        scores.append(score)
    print('Average Score is')
    print('Average Score:', sum(scores) / len(scores))
    print('choice 1:{}  choice 0:{}'.format(choices.count(1) / len(choices), choices.count(0) / len(choices)))
    print('Score Requirement:', score_requirement)


if __name__ == "__main__":

    print("ALL IMPORTS DONE")
    print("Press 1 to play")
    print("Press 2 to train AI")
    print("Press 3 for random")

    mode = int(input())
    if (mode == 1 or mode == 3):
        g = game(50)
        g.resetGame()
        while not g.snake.gameOver:
            if (mode == 1):
                g.snake.getDirection()
            if (mode == 3):
                g.snake.getRandomDirection()
            g.snake.move(g.food)
            g.draw()
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    exit()
            if key[pygame.K_q]:
                pygame.quit()
                exit()
            if key[pygame.K_r]:
                g.resetGame()

            if g.snake.gameOver:
                while(g.snake.gameOver):
                    gameOverScreen(g)
        pygame.quit()

    elif mode == 2:
        import tflearn
        from tflearn.layers.core import input_data, dropout, fully_connected
        from tflearn.layers.estimator import regression
        from statistics import median, mean
        from collections import Counter
        import tensorflow as tf
        import numpy as np

        print("START TRAINING....")
        training_data = generate_population(None)
        model = create_dummy_model(training_data)
        model = train_model(training_data, model)
        evaluate(model)
        generation = 1
        while True:
            generation += 1 
            print('Generation: ', generation)
            # training_data = initial_population(model)
            training_data = np.append(training_data, generate_population(None), axis=0)
            print('generation: ', generation, ' initial population: ', len(training_data))
            if len(training_data) == 0:
                break
            model = train_model(training_data, model)
            evaluate(model)


