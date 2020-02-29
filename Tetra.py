import pygame, random, time, sys
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

# Init Properties
BLANK = '0'
global CLOCK
CLOCK = pygame.time.Clock()

def evaluatedifficulty_fallrate(score):
	difficulty = int(score / 10) + 1
	fallRate = 0.22 - (difficulty * 0.02)
	return difficulty, fallRate



def exit():
	pygame.quit()
	quit()
	sys.exit()



class Inputs():

	def __init__(self):
		pass

	def checkForExit(self):
		for event in pygame.event.get(QUIT):
			exit()
		for event in pygame.event.get(KEYUP):
			if event.key == K_ESCAPE:
				exit()
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
			self.validPiecePlacement(matrix, pieceDrop, adj_Y = 1)):
			self.pieceDrop['y'] += 1
			self.MoveDownReset = time.time()

		if time.time() - self.FallReset > self.fallRate:

			if not self.validPiecePlacement(matrix, self.pieceDrop, adj_Y = 1):
				self.addToMatrix(matrix, self.pieceDrop)
				self.score += self.removeCompletedLines(matrix)
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

		pressKeySCR, pressKeyREND = self.maketext('Press a key to play',
		 									  	   self.SMALLFONT,
		 									  	   BLUE)

		pressKeyREND.center = (int(SCREENWIDTH / 2),
							   int(SCREENHEIGHT / 2) + 100)
		self.SCREEN.blit(pressKeySCR, pressKeyREND)

		while super().checkForKeyInput() == None:
			pygame.display.update()
			CLOCK.tick()


	def quit(self):
		return super().checkForExit()

	def drawStatus(self):
		scoreSCR = self.SMALLFONT.render(
			f"Score: {self.score}", True, TEXTCL)
		scoreREND = scoreSCR.get_rect()
		scoreREND.topleft = (SCREENWIDTH - 150, 20)
		self.SCREEN.blit(scoreSCR, scoreREND)

		diffiSCR = self.SMALLFONT.render(
			f"Level: {self.difficulty}", True, TEXTCL)
		diffiREND = diffiSCR.get_rect()
		diffiREND.topleft = (SCREENWIDTH - 150, 50)
		self.SCREEN.blit(diffiSCR, diffiREND)


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


class Pieces(Matrix, Display):
	def __init__(self):
		super().__init__()
		self.Left = False
		self.Right = False
		self.FallReset = time.time()
		self.MoveDownReset = time.time()
		self.MoveSidewaysReset = time.time()
		self.SidewaysRate = 0.15
		self.DownRate = 0.1
		self.Down = False
		self.score = 0
		self.difficulty, self.fallRate = evaluatedifficulty_fallrate(
																self.score)
		self.pieceDrop = None
		self.nextPiece = None
	
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
		if pixel_x == None and pixel_y == None:
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
		return numLinesCleared


	def gameplay(self, matrix):
		super().movement(matrix)

	def Start(self, matrix, FPS):
		self.pieceDrop = self.makePieces()
		self.nextPiece = self.makePieces()

		while True:
			if self.pieceDrop == None:
				self.pieceDrop = self.nextPiece
				self.nextPiece = self.makePieces()
				self.FallReset = time.time()

			if not self.validPiecePlacement(matrix, self.pieceDrop):
				return

			self.quit()

			self.gameplay(matrix)
			self.SCREEN.fill(BACKGROUND)
			self.displayMatrix(matrix)
			self.drawStatus()
			self.drawNewPiece(self.nextPiece)
			if self.pieceDrop != None:
				self.drawPiece(self.pieceDrop)

			pygame.display.update()
			CLOCK.tick(FPS)



pygame.init()
exhibit = Display(SCREENWIDTH, SCREENHEIGHT) # Synonyms for display
grid = Matrix()
tetromino = Pieces()
pressing = Inputs()




def Game():
	matrix = grid.createMatrix()
	tetromino.Start(matrix, FPS)

def main():
	exhibit.presentText('TetraAI')
	exhibit.clearscreen()
	while True:
		Game()
		exhibit.clearscreen()
		exhibit.presentText('Game Over')

main()



# Fix bugs kl

