import pygame, random, time, sys
import math, numpy, copy, pyautogui
import pkg_resources.py2_warn
import matplotlib.pyplot as plot
import pygame.locals as keys
from pygame.locals import *
from Tetra_Pieces import *
'''
Importing my piece module
A matrix is a board used in Tetris
Using Colors instead of Colours
Keep with the PEP 8 Line Length! 79 Characters are the max!
'''
# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (240,115,73)
BLUE = (0,0,255)
YELLOW = (212,154,42)
TEALGRAY = (85,115,137)
RED = (255,0,0)

BACKGROUND = BLACK
MATRIXCL = RED # CL = Colours
TEXTCL = WHITE
CL = (RED, BLUE, YELLOW, ORANGE)

# Game Properties
SCREENWIDTH = 800
SCREENHEIGHT = 600
MATRIXSIZE = 20
MATRIXWIDTH = 10
MATRIXHEIGHT = 20
XBORDER = int((SCREENWIDTH - MATRIXWIDTH * MATRIXSIZE) / 2)
YBORDER = SCREENHEIGHT - (MATRIXHEIGHT * MATRIXSIZE) - 5
FPS = 60

# Piece Properties
display_PIECE = Pieces_Array()

PIECES = {'S': display_PIECE.piece_S(),
		  'Z': display_PIECE.piece_Z(),
		  'J': display_PIECE.piece_J(),
		  'L': display_PIECE.piece_L(),
		  'I': display_PIECE.piece_I(),
		  'O': display_PIECE.piece_O(),
		  'T': display_PIECE.piece_T()}

PIECEWIDTH = 5
PIECEHEIGHT = 5

# AI Properties
pyautogui.PAUSE = 0.03
pyautogui.FAILSAFE = True
MAXGAMES = 75

# Plot Properties
scoreArray = []
weight0Array = []
weight1Array = []
weight2Array = []
weight3Array = []
gameIndexArray = []

# Init Properties
BLANK = '0'
global CLOCK
CLOCK = pygame.time.Clock()

def evaluatedifficulty_fallrate(score):
	difficulty = int(score / 10) + 1
	fallRate = 0.07 * math.exp(
		(1 - difficulty) / 3)
	return difficulty, fallRate



class Inputs():

	def __init__(self):
		pass

	def checkForExit(self):
		for event in pygame.event.get(QUIT):
			pygame.quit()
			quit()
			sys.exit()
		for event in pygame.event.get(KEYUP):
			if event.key == K_ESCAPE:
				pygame.quit()
				quit()
				sys.exit()
			pygame.event.post(event)


	def checkForKeyInput(self):
		self.checkForExit()

		for event in pygame.event.get([KEYDOWN, KEYUP]):
			if event.type == KEYDOWN:
				continue
			return event.key
		return None
		

	def movement(self, matrix):
		for event in pygame.event.get():
			if event.type == KEYUP:
				if (event.key == K_p):
					self.SCREEN.fill(BACKGROUND)
					self.presentText("Pause")
					self.SCREEN.fill(BACKGROUND)
					self.FallReset = time.time()
					self.MoveDownReset = time.time()
					self.MoveSidewaysReset = time.time()
				elif (event.key == K_LEFT or event.key == K_a):
					self.Left = False
				elif (event.key == K_RIGHT or event.key == K_d):
					self.Right = False
				elif (event.key == K_DOWN or event.key == K_s):
					self.Down = False

			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a) and (
					self.validPiecePlacement(
						matrix, self.pieceDrop, adj_X = -1)):
					self.pieceDrop['x'] -= 1
					self.left = True
					self.Right = False
					self.MoveSidewaysReset = time.time()

				elif (event.key == K_RIGHT or event.key == K_d) and (
					self.validPiecePlacement(
						matrix, self.pieceDrop, adj_X = 1)):
					self.pieceDrop['x'] += 1
					self.Right = True
					self.Left = False
					self.MoveSidewaysReset = time.time()

				elif (event.key == K_UP or event.key == K_w):
					self.pieceDrop['rotation'] = (
						self.pieceDrop['rotation'] + 1) % len(
						PIECES[self.pieceDrop['shape']])

					if not self.validPiecePlacement(matrix, self.pieceDrop):
						self.pieceDrop['rotation'] = (
							self.pieceDrop['rotation'] - 1) % len(
							PIECES[self.pieceDrop['shape']])

				elif (event.key == K_q):
					self.pieceDrop['rotation'] = (
						self.pieceDrop['rotation'] - 1) % len(
						PIECES[self.pieceDrop['shape']])

					if not self.validPiecePlacement(
						matrix, self.pieceDrop):
						self.pieceDrop['rotation'] = (
							self.pieceDrop['rotation'] + 1) % len(
							PIECES[self.pieceDrop['shape']])

				elif (event.key == K_DOWN or event.key == K_s):
					self.Down = True
					if self.validPiecePlacement(
						matrix, self.pieceDrop, adj_Y = 1):
						self.pieceDrop['y'] += 1
					self.MoveDownReset = time.time()

				elif (event.key == K_SPACE):
					self.Down = False
					self.Right = False
					self.Left = False
					for i in range(1, MATRIXHEIGHT):
						if not self.validPiecePlacement(
							matrix, self.pieceDrop, adj_Y = i):
							break
					self.pieceDrop['y'] += i - 1

		if (self.Left or self.Right) and (
			time.time() - self.MoveSidewaysReset > self.SidewaysRate):

			if self.Left and self.validPiecePlacement(
				matrix, self.pieceDrop, adj_X = -1):
				self.pieceDrop['x'] -= 1

			elif self.Right and self.validPiecePlacement(
				matrix, self.pieceDrop, adj_X = 1):
				self.pieceDrop['x'] += 1
			self.MoveSidewaysReset = time.time()

		if self.Down and (
			time.time() - self.MoveDownReset > self.DownRate) and (
			self.validPiecePlacement(matrix, self.pieceDrop, adj_Y = 1)):
			self.pieceDrop['y'] += 1
			self.MoveDownReset = time.time()

		if time.time() - self.FallReset > self.fallRate:

			if not self.validPiecePlacement(matrix, self.pieceDrop, adj_Y = 1):
				self.addToMatrix(matrix, self.pieceDrop)
				lines, matrix = self.removeCompletedLines(matrix)
				self.score += lines * lines
				self.difficulty, self.fallRate = evaluatedifficulty_fallrate(self.score)
				self.pieceDrop = None
			else:
				self.pieceDrop['y'] += 1
				self.FallReset = time.time()


class Display(Inputs):
	def __init__(self, SCREENWIDTH, SCREENHEIGHT):
		self.SCREEN = pygame.display.set_mode((
			SCREENWIDTH, SCREENHEIGHT))
		self.BIGFONT = pygame.font.Font('fonts/Tetris.ttf', 175)
		self.SMALLFONT = pygame.font.Font('fonts/Minecraft.ttf', 18)
		ICON = pygame.image.load('images/TetraAI_Icon.png')
		pygame.display.set_icon(ICON)
		pygame.display.set_caption('TetraAI')

	
	def clearscreen(self):
		self.SCREEN.fill(BACKGROUND)
		pygame.display.update()

	def maketext(self, text, font, color):
		scr = font.render(text, True, color)
		return scr, scr.get_rect()

	def presentText(self, text):
		# Display Large text with color and center it
		titleSCR, titleREND = self.maketext(text, 
			                                self.BIGFONT, 
			                                RED)
		titleREND.center = (int(SCREENWIDTH / 2),
							int(SCREENHEIGHT / 2) - 3)
		self.SCREEN.blit(titleSCR, titleREND)

		pressKeySCR, pressKeyREND = self.maketext('Press wait!',
		 									  	   self.SMALLFONT,
		 									  	   BLUE)

		pressKeyREND.center = (int(SCREENWIDTH / 2),
							   int(SCREENHEIGHT / 2) + 100)
		self.SCREEN.blit(pressKeySCR, pressKeyREND)

		pygame.display.update()
		CLOCK.tick()
		time.sleep(0.5)              


	def quit(self):
		return super().checkForExit()

	def drawStatus(self):
		scoreSCR = self.SMALLFONT.render(
			f"Score: {self.score} ", True, TEXTCL)
		scoreREND = scoreSCR.get_rect()
		scoreREND.topleft = (SCREENWIDTH - 150, 20)
		self.SCREEN.blit(scoreSCR, scoreREND)

		diffiSCR = self.SMALLFONT.render(
			f"Level: {self.difficulty}", True, TEXTCL)
		diffiREND = diffiSCR.get_rect()
		diffiREND.topleft = (SCREENWIDTH - 150, 50)
		self.SCREEN.blit(diffiSCR, diffiREND)

		moveSCR = self.SMALLFONT.render(
			f"Current Move: {self.currentMove}", True, TEXTCL)
		moveREND = moveSCR.get_rect()
		moveREND.topleft = (SCREENWIDTH - 275, 200)
		self.SCREEN.blit(moveSCR, moveREND)

		completeSCR = self.SMALLFONT.render(
			f"Games Completed: {self.gamesCompleted}", True, TEXTCL)
		completeREND = completeSCR.get_rect()
		completeREND.topleft = (SCREENWIDTH - 275, 230)
		self.SCREEN.blit(completeSCR, completeREND)


class Matrix(Display):
	def __init__(self):
		super().__init__(SCREENWIDTH, SCREENHEIGHT)

	def createMatrix(self):
		# Create the matrix data structure
		matrix = []
		for i in range(MATRIXWIDTH):
			matrix.append([BLANK] * MATRIXHEIGHT)
		return matrix

	def matrixToScreen(self, box_x, box_y):
		# Convert xy coords for matrix to a certain coordinate on screen
		return (XBORDER + (box_x * MATRIXSIZE)), (
			YBORDER + (box_y * MATRIXSIZE))



	def newOutline(self, box_x, box_y, color, pixel_x = None, pixel_y = None):
		"""
		Draw a box outline for each tetromino one by one onto the matrix
		at the coords I specify however there is cords for
		pixel_x and pixel_y which are coords for "Next" piece
		"""
		if color == BLANK:
			return
		if pixel_x == None and pixel_y == None:
			pixel_x, pixel_y = self.matrixToScreen(box_x, box_y)
		pygame.draw.rect(self.SCREEN, CL[color], 
						(pixel_x + 1, pixel_y + 1, MATRIXSIZE - 1,
						 MATRIXSIZE - 1))

	def displayMatrix(self, matrix):
		# Drawing the border for the Matrix
		pygame.draw.rect(self.SCREEN, MATRIXCL, 
						(XBORDER - 3, YBORDER - 7, 
						(MATRIXSIZE * MATRIXWIDTH) + 8, 
						(MATRIXSIZE * MATRIXHEIGHT) + 8), 5)

		# Make the background for the matrix
		pygame.draw.rect(self.SCREEN, BACKGROUND, 
						(XBORDER, YBORDER, 
					     MATRIXSIZE * MATRIXWIDTH,
						 MATRIXSIZE * MATRIXHEIGHT))

		for x in range(MATRIXWIDTH):
			for y in range(MATRIXHEIGHT):
				self.newOutline(x, y, matrix[x][y])

class AI(Matrix):
	def __init__(self):
		super().__init__()



	def getParams(self, matrix):
		heights = [0] * MATRIXWIDTH
		diffs = [0] * (MATRIXWIDTH - 1)
		holes = 0
		diffSum = 0


		for i in range(0, MATRIXWIDTH):
			for j in range(0, MATRIXHEIGHT):
				if int(matrix[i][j]) > 0:  
					heights[i] = MATRIXHEIGHT - j
					break

		for i in range(0, len(diffs)):
			diffs[i] = heights[i + 1] - heights[i]

		maxHeight = max(heights)

		for i in range(0, MATRIXWIDTH):
			occupied = 0
			for j in range(0, MATRIXHEIGHT):
				if int(matrix[i][j]) > 0:
					occupied = 1
				if int(matrix[i][j]) == 0 and occupied == 1:
					holes += 1

		heightSum = sum(heights)
		for i in diffs:
			diffSum += abs(i)
		return heightSum, diffSum, maxHeight, holes


	def predictedScore(self, testMatrix, weights):
		heightSum, diffSum, maxHeight, holes = self.getParams(testMatrix)
		A = weights[0]
		B = weights[1]
		C = weights[2]
		D = weights[3]
		testScore = float(A * heightSum + B * diffSum + C * maxHeight + D * holes)
		return testScore


	def emulateMatrix(self, testMatrix, testPiece, move):
		rotation = move[0]
		sideways = move[1]
		testLinesRemoved = 0
		referenceHeight = self.getParams(testMatrix)[0]
		if testPiece is None:
			return None

		for i in range(0, rotation):
			testPiece['rotation'] = (
				testPiece['rotation'] + 1) % len(
				PIECES[testPiece['shape']])

		if not self.validPiecePlacement(
			testMatrix, testPiece, adj_X= sideways, adj_Y=0):
			return None

		testPiece['x'] += sideways
		for i in range(0, MATRIXHEIGHT):
			if self.validPiecePlacement(
				testMatrix, testPiece, adj_X=0, adj_Y=1):
				testPiece['y'] = i

		if self.validPiecePlacement(
			testMatrix, testPiece, adj_X=0, adj_Y=0):
			self.addToMatrix(testMatrix, testPiece)
			testLinesRemoved, testMatrix = self.removeCompletedLines(
													testMatrix)

		heightSum, diffSum, maxHeight, holes = self.getParams(testMatrix)
		reward = 5 * (testLinesRemoved * testLinesRemoved) - (
			heightSum - referenceHeight)
		return testMatrix, reward


	def findBestMove(self, matrix, piece, weights, learning):
		moveList = []
		scoreList = []
		for rotation in range(0, len(PIECES[piece['shape']])):
			for sideways in range(-5 ,6):
				move = [rotation, sideways]
				testMatrix = copy.deepcopy(matrix)
				testPiece = copy.deepcopy(piece)
				testMatrix = self.emulateMatrix(testMatrix, testPiece, move)
				if testMatrix is not None:
					moveList.append(move)
					testScore = self.predictedScore(testMatrix[0], weights)
					scoreList.append(testScore)
		bestScore = max(scoreList)
		bestMove = moveList[scoreList.index(bestScore)]

		if random.random() < learning:
			move = moveList[random.randint(0, len(moveList) - 1)]
		else:
			move = bestMove
		return move


	def makeMove(self, move):
		rotation = move[0]
		sideways = move[1]
		if rotation != 0:
			pyautogui.press('up')
			rotation -= 1
		else:
			if sideways == 0:
				pyautogui.press('space')
			if sideways < 0:
				pyautogui.press('left')
				sideways += 1
			if sideways > 0:
				pyautogui.press('right')
				sideways -= 1

		return [rotation, sideways]

	def gradientDescent(self, matrix, piece, weights, learning):
		move = self.findBestMove(matrix, piece, weights, learning)
		oldParams = self.getParams(matrix)
		testMatrix = copy.deepcopy(matrix)
		testPiece = copy.deepcopy(piece)
		testMatrix = self.emulateMatrix(testMatrix, testPiece, move)
		if testMatrix is not None:
			newParams = self.getParams(testMatrix[0])
			reward = testMatrix[1]
		for i in range(0, len(weights)):
			weights[i] = weights[i] + self.alpha * weights[i] * (
				reward - oldParams[i] + self.phi * newParams[i])
		regularizer = abs(sum(weights))
		for i in range(0, len(weights)):
			weights[i] = 100 * weights[i] / regularizer
			#1e4 = 10000
			weights[i] = math.floor(1e4 * weights[i]) / 1e4
		return move, weights





class Pieces(AI):
	def __init__(self):
		super().__init__()
	
	def makePieces(self):
		shape = random.choice(list(PIECES.keys()))
		newPiece = {'shape': shape,
					'rotation': random.randint(0, 
						len(PIECES[shape]) - 1),
					'x': int(MATRIXWIDTH / 2) - 
						 int(PIECEWIDTH / 2),
					'y': -2,
					'color': random.randint(0,
							 len(CL) -1)}
		return newPiece

	def drawPiece(self, piece, pixel_x = None, pixel_y = None):
		shapeDrawen = PIECES[piece['shape']][piece['rotation']]
		if pixel_x is None and pixel_y is None:
			pixel_x, pixel_y = super().matrixToScreen(piece['x'], piece['y'])

		for x in range(PIECEWIDTH):
			for y in range(PIECEHEIGHT):
				if shapeDrawen[y][x] != BLANK:
					super().newOutline(
						    None, None,
						    piece['color'],
						    pixel_x + (x * MATRIXSIZE),
						    pixel_y + (y * MATRIXSIZE))

	def drawNewPiece(self, piece):
		nextSCR = self.SMALLFONT.render("Next: ", True, TEXTCL)
		nextREND = nextSCR.get_rect()
		nextREND.topleft = (SCREENWIDTH - 120, 80)
		self.SCREEN.blit(nextSCR, nextREND)

		self.drawPiece(piece, pixel_x = SCREENWIDTH - 120, pixel_y = 100)
		

	def addToMatrix(self, matrix, piece):
		# Place Tetrominos on matrix
		for x in range(PIECEWIDTH):
			for y in range(PIECEHEIGHT):
				if PIECES[piece['shape']][
				piece['rotation']][y][x] != BLANK and (
					x + piece['x'] < 10 and y + piece['y'] < 20):
					matrix[x + piece['x']][y + piece['y']] = piece['color']

	def onMatrix(self, x, y):
		return x >= 0 and x < MATRIXWIDTH and y < MATRIXHEIGHT

	def validPiecePlacement(self, matrix, piece, adj_X = 0, adj_Y = 0):
		for x in range(PIECEWIDTH):
			for y in range(PIECEHEIGHT):
				TopOfBoard = y + piece['y'] + adj_Y < 0
				if TopOfBoard or (
					PIECES[piece['shape']][piece['rotation']][y][x] == BLANK):
					continue
				if not self.onMatrix(
					x + piece['x'] + adj_X, y + piece['y'] + adj_Y):
					return False
				if matrix[
				x + piece['x'] + adj_X][y + piece['y'] + adj_Y] != BLANK:
					return False
		return True

	def validCompletedLine(self, matrix, y):
		for x in range(MATRIXWIDTH):
			if matrix[x][y] == BLANK:
				return False
		return True

	def removeCompletedLines(self, matrix):
		numLinesCleared = 0
		y = MATRIXHEIGHT - 1
		while y >= 0:
			if self.validCompletedLine(matrix, y):
				for i in range(y, 0, -1):
					for x in range(MATRIXWIDTH):
						matrix[x][i] = matrix[x][i - 1]
				for x in range(MATRIXWIDTH):
					matrix[x][0] = BLANK
				numLinesCleared += 1
			else:
				y -= 1
		return numLinesCleared, matrix
		

	

class Game(Pieces):
	def __init__(self):
		super().__init__()
		# Game Setup Variables
		self.Left = False
		self.Right = False
		self.FallReset = time.time()
		self.MoveDownReset = time.time()
		self.MoveSidewaysReset = time.time()
		self.SidewaysRate = 0.075
		self.DownRate = 0.05
		self.Down = False
		self.score = 0
		self.difficulty, self.fallRate = evaluatedifficulty_fallrate(
																self.score)
		self.pieceDrop = None
		self.nextPiece = None
		# AI Variables, alpha = LearningRate, phi = DiscountFactor
		self.gamesCompleted = 0
		self.weights = [-1, -1, -1, -30]
		self.learning = 0.5
		self.currentMove = [0, 0]
		self.alpha = 0.01
		self.phi = 0.9


	def Start(self, FPS):
		# Reset Variables
		self.FallReset = time.time()
		self.MoveDownReset = time.time()
		self.MoveSidewaysReset = time.time()
		self.score = 0
		self.difficulty, self.fallRate = evaluatedifficulty_fallrate(
																self.score)
		self.reward = 0
		self.currentMove = [0, 0]
		matrix = self.createMatrix()
		self.pieceDrop = self.makePieces()
		self.nextPiece = self.makePieces()


		while True:
			if self.pieceDrop is None:
				self.pieceDrop = self.nextPiece
				self.nextPiece = self.makePieces()
				self.FallReset = time.time()

				if not self.validPiecePlacement(matrix, self.pieceDrop):
					self.gamesCompleted += 1
					return 
				self.currentMove, self.weights = self.gradientDescent(matrix,
					self.pieceDrop, self.weights, self.learning)

				if self.learning > 0.001:
					self.learning = self.learning * 0.99
				else:
					self.learning = 0


			self.quit()
			self.currentMove = self.makeMove(self.currentMove)

			self.movement(matrix)
			self.SCREEN.fill(BACKGROUND)
			self.displayMatrix(matrix)
			self.drawStatus()
			self.drawNewPiece(self.nextPiece)
			if self.pieceDrop != None:
				self.drawPiece(self.pieceDrop)

			pygame.display.update()
			CLOCK.tick(FPS)


	def Results(self):
		print("Game Number ", self.gamesCompleted,
			" achieved a score of: ", self.score)
		scoreArray.append(self.score)
		gameIndexArray.append(self.gamesCompleted)
		weight0Array.append(-self.weights[0])
		weight1Array.append(-self.weights[1])
		weight2Array.append(-self.weights[2])
		weight3Array.append(-self.weights[3])
		self.clearscreen()
		self.presentText('Game Over')
		if self.gamesCompleted >= MAXGAMES:
			plot.figure(1)
			plot.subplot(211)
			plot.plot(gameIndexArray, scoreArray, 'k-')
			plot.xlabel('Game Number')
			plot.ylabel('Game Score')
			plot.title('Learning Curve')
			plot.xlim(1, max(gameIndexArray))
			plot.ylim(0, max(scoreArray) * 1.1)
			plot.subplot(212)
			plot.xlabel('Game Number')
			plot.ylabel('Weights')
			plot.title('Learning Curve')
			axis = plot.gca()
			axis.set_yscale('log')
			plot.plot(gameIndexArray, weight0Array, label="Aggregate Height")
			plot.plot(gameIndexArray, weight1Array, label="Unevenness")
			plot.plot(gameIndexArray, weight2Array, label="Maximum Height")
			plot.plot(gameIndexArray, weight3Array, label="Number of Holes")
			plot.legend(loc='lower left')
			plot.xlim(0, max(gameIndexArray))
			plot.ylim(0.0001, 100)
			plot.show()



pygame.init()
exhibit = Display(SCREENWIDTH, SCREENHEIGHT) # Synonyms for display
grid = Matrix()
tetromino = Pieces()
pressing = Inputs()
run = Game()


def main():
	exhibit.presentText('TetraAI')
	time.sleep(2)
	exhibit.clearscreen()
	while True:
		run.Start(FPS)
		run.Results()
main()



# Fix bugs kl

