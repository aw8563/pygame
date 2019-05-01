import math
import random
import pygame
import os
import numpy as np

# gameSpeed = 100

white = (255,255,255)
black = (0,0,0)

screenWidth = 500
screenHeight = 500
grid = 10

class Tail():
	def __init__(self,x,y, turns):
		self.x = x
		self.y = y
		self.turns = turns

	def __str__(self):
		return str(self.x) + " " + str(self.y) + " | in " + str(self.turns)


class Block():
	def __init__(self, x,y, window):
		self.x = x
		self.y = y
		self.window = window

	def draw(self, colour):
		pygame.draw.rect(self.window, colour, (self.x, self.y , 10, 10), 1)
	def drawSolid(self, colour):
		pygame.draw.rect(self.window, colour, (self.x, self.y , 10, 10))
	def __str__(self):
		return str([self.x,self.y])
# main loop
class Snake():
	def __init__(self, body, window, direction = 1, gameOver = False):
		self.body = body
		self.direction = direction
		self.gameOver = gameOver
		self.tail = []
		self.window = window
		self.reward = 0

	def score(self):
		return len(self.body) - 3

	def getDirection(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.body[1].x != self.body[0].x - 10:
			self.direction = 3

		if key[pygame.K_RIGHT] and self.body[1].x != self.body[0].x + 10:
			self.direction = 1

		if key[pygame.K_UP] and self.body[1].y != self.body[0].y - 10:
			self.direction = 0

		if key[pygame.K_DOWN] and self.body[1].y != self.body[0].y + 10:
			self.direction = 2

	def getRandomDirection(self):
		direction = None
		if self.direction == 0:
			direction = random.choice([0,1,3])

		elif self.direction == 1:
			direction = random.choice([2,1,0])

		elif self.direction == 2:
			direction = random.choice([2,1,3])

		else:
			direction = random.choice([3,2,0])

		self.direction = direction

		return direction

	def move(self, food):

		tail = None
		if (self.direction == 1):
			self.body = [Block(self.body[0].x + 10, self.body[0].y, self.window)] + self.body
			if (self.body[0].x + 10 > screenWidth):
				self.gameOver = True
			self.body.pop()
			self.direction = 1


		if (self.direction == 3):
			self.body = [Block(self.body[0].x - 10, self.body[0].y, self.window)] + self.body
			if (self.body[0].x < 0):
				self.gameOver = True
			self.body.pop()
			self.direction = 3

		if (self.direction == 2):
			self.body = [Block(self.body[0].x, self.body[0].y + 10, self.window)] + self.body
			if (self.body[0].y + 10 > screenWidth):
				self.gameOver = True	
			self.body.pop()
			self.direction = 2

		if (self.direction == 0):
			self.body = [Block(self.body[0].x, self.body[0].y - 10, self.window)] + self.body
			if (self.body[0].y < 0):
				self.gameOver = True
			self.body.pop()
			self.direction = 0

		for b in self.body[1:]:
			if (self.body[0].x == b.x and self.body[0].y == b.y):
				self.gameOver = True
		
		self.reward = 1


		if self.body[0].x == food.x and self.body[0].y == food.y:
			self.reward = 100
			inSnake = True
			while (inSnake):
				inSnake = False
				food.x = (random.randint(0, (screenWidth - 10)/10))*10
				food.y = (random.randint(0, (screenHeight - 10)/10))*10
				for b in self.body:
					if (food.x == b.x and food.y == b.y):
						inSnake = True


			newTail = Tail(food.x, food.y, len(self.body))
			self.tail.append(newTail)
		# if grow > 0 and self.body[-1].x == growLocation[0][0] and self.body[-1].y == growLocation[0][1]:


	def draw(self):
		for b in self.body:
			pygame.draw.rect(self.window, (255,255,255), (b.x, b.y , 10, 10), 1)

	def grow(self):
		for t in self.tail:
			if (t.turns == 0):
				self.body.append(Block(t.x, t.y, self.window))
				self.tail = self.tail[1:]
			else:
				t.turns -= 1

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
		game.snake.body = body
		game.snake.direction = 1
		game.window.fill(white)
		game.hasFood = False


class Game():
	def __init__(self, gameSpeed):
		self.gameSpeed = gameSpeed
		os.environ['SDL_AUDIODRIVER'] = 'dummy'
		pygame.init()
		print("INITIALISE SUCCESS")


	def resetGame(self):

		self.window = pygame.display.set_mode((screenWidth, screenHeight))

		self.running = True
		self.gameOver = False
		self.red = (255,0,0)
		self.green = (0,255,0)
		self.blue = (0,0,255)
		self.black = (0,0,0)
		self.white = (255,255,255)

		self.body = [Block(100,100, self.window), Block(90,100, self.window), Block(80,100,self.window)]
		self.snake = Snake(self.body, self.window)
		self.food = Block((random.randint(0, (screenWidth - 10)/10))*10, 
						(random.randint(0, (screenWidth - 10)/10))*10, self.window)
		# self.food = Block(50,50, self.window)
	def runGame(self):
		if(self.snake.gameOver):
			# gameOverScreen(self)
			return

		self.snake.move(self.food)
		self.snake.grow()

	def draw(self):
		self.window.fill(self.black)
		myfont = pygame.font.SysFont('Comic Sans MS', 25)
		score = myfont.render('Score is ' + str(self.snake.score()), True, self.white)
		t1 = myfont.render("Q to quit", True, self.white)
		t2 = myfont.render("R to restart", True, self.white)
		self.window.blit(score,(5, 10))
		# self.window.blit(t1, (10,10))
		# self.window.blit(t2, (10,30))
		self.snake.draw()

		self.food.drawSolid(self.green)
		pygame.display.update()
		pygame.time.delay(100 - self.gameSpeed)

	def getInfo(self):

		snakeX = self.snake.body[0].x
		snakeY = self.snake.body[0].y
		foodX = self.food.x
		foodY = self.food.y

		def loop(x,y, direction):
			foodDistance = screenWidth
			wallDistance = screenHeight

			if (direction == 'left'):
				if (foodY == snakeY and foodX < snakeX):
					foodDistance = snakeX - foodX - grid
				wallDistance = snakeX
					
			elif (direction == 'right'):
				if (foodY == snakeY and foodX > snakeX):
					foodDistance = foodX - snakeX
				wallDistance = screenWidth - snakeX - grid

			elif (direction == 'up'):
				if (foodX == snakeX and foodY < snakeY):
					foodDistance = snakeY - foodY - grid
				wallDistance = snakeY

			elif (direction == 'down'):
				if (foodX == snakeX and foodY > snakeY):
					foodDistance = foodY - snakeY
				wallDistance = screenHeight - snakeY - grid
			
			return [wallDistance/10, foodDistance/10]


		# up
		if (self.snake.direction == 0):
			info = np.array([
				loop(snakeX,snakeY, 'up'),
				loop(snakeX,snakeY, 'left'),
				[0,50],
				loop(snakeX,snakeY, 'right'),
			])

		# right
		elif (self.snake.direction == 1):
			info = np.array([
				loop(snakeX,snakeY, 'right'),
				loop(snakeX,snakeY, 'up'),
				[0,50],
				loop(snakeX,snakeY, 'down'),
			])

		# down
		elif (self.snake.direction == 2):
			info = np.array([
				loop(snakeX,snakeY, 'down'),
				loop(snakeX,snakeY, 'right'),
				[0,50],
				loop(snakeX,snakeY, 'left'),
			])

		# left
		else:
			info = np.array([
				loop(snakeX,snakeY, 'left'),
				loop(snakeX,snakeY, 'down'),
				[0,50],
				loop(snakeX,snakeY, 'up'),
			])

		info.shape = (8,)

		return info
