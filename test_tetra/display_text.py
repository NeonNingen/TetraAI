import pygame, random, time
from pygame.locals import *
from Tetra_Pieces import *
#Importing my piece module

piece = Pieces_Array()
print(piece.piece_S())

PIECES = {'S': piece.piece_S()}

RED = (255,0,0)
BLACK = (0,0,0)
LIGHTBLUE = (20,20,175)
WHITE = (255,255,255)
BLANK = '0'
colour_TEXT = WHITE
colour_PIECES = (RED, LIGHTBLUE)
color_BORDER = LIGHTBLUE

class game_window:

	def __init__(self, screen_WIDTH, screen_HEIGHT):
		pygame.init()
		self.screen_WIDTH = screen_WIDTH
		self.screen_HEIGHT = screen_HEIGHT
		self.grid_WIDTH = 10
		self.grid_HEIGHT = 20
		self.size_box = 25
		self.tetromino_WIDTH = 5
		self.tetromino_HEIGHT = 5
		self.BACKGROUND_C = BLACK
		self.big_FONT = pygame.font.Font('fonts/Tetris.ttf', 150)
		self.normal_FONT = pygame.font.Font('fonts/Minecraft.ttf', 18)
		self.score = 0
		self.level = 0 # Make more advance changes to this later
		self.screen = pygame.display.set_mode((screen_WIDTH, screen_HEIGHT))
		self.X_MARGIN = int((screen_WIDTH - self.grid_WIDTH * self.size_box) / 2)
		self.Y_MARGIN = screen_HEIGHT - (self.grid_HEIGHT * self.size_box) - 5


	def draw_Board(self):
		board = []
		for i in range(self.grid_WIDTH):
			board.append([BLANK] * self.grid_HEIGHT)
		pygame.draw.rect(self.screen, color_BORDER, (self.X_MARGIN - 3, self.Y_MARGIN - 7, (self.grid_WIDTH * self.size_box) + 8, (self.grid_HEIGHT * self.size_box) + 8), 5)
		pygame.draw.rect(self.screen, self.BACKGROUND_C, (self.X_MARGIN, self.Y_MARGIN, self.size_box * self.grid_WIDTH, self.size_box * self.grid_HEIGHT))
		pygame.display.update()

	def make_Text_Objs(self, text, font, color):
		rend = font.render(text, True, color)
		return rend, rend.get_rect()

	def show_Text_Screen(self, text):
		# This method presents the big and small text on the main screen.
		# Draw the big text.
		title_Rend, title_Rect = self.make_Text_Objs(text, self.big_FONT, WHITE)
		title_Rect.center = (int(self.screen_WIDTH / 2) - 3, int(self.screen_HEIGHT / 2) - 3)
		self.screen.blit(title_Rend, title_Rect)

		# Draw small text..
		pressKeyRend, pressKeyRect = self.make_Text_Objs('Press down key to play!', self.normal_FONT, WHITE)
		pressKeyRect.center = (int(self.screen_WIDTH / 2), int(self.screen_HEIGHT / 2) + 100)
		self.screen.blit(pressKeyRend, pressKeyRect)
		pygame.display.update()

	def draw_Status(self):
		# draw the score text
		score_Rend = self.normal_FONT.render('Score: %s' % self.score, True, WHITE)
		score_Rect = score_Rend.get_rect()
		score_Rect.topleft = (self.screen_WIDTH - 150, 20)
		self.screen.blit(score_Rend, score_Rect)

		# draw the level text
		level_Rend = self.normal_FONT.render('Level: %s' % self.level, True, WHITE)
		level_Rect = level_Rend.get_rect()
		level_Rect.topleft = (self.screen_WIDTH - 150, 50)
		self.screen.blit(level_Rend, level_Rect)

	def get_New_Piece(self):
	    # return a rotation and color
	    shape = random.choice(list(PIECES.keys()))
	    print(shape)
	    # Dictionary for the new piece
	    newPiece = {'shape': shape,
	    			'rotation': random.randint(0, len(PIECES[shape]) - 1),
	                'x': int(self.grid_WIDTH / 2) - int(self.tetromino_WIDTH / 2),
	                'y': -2, # start it above the board (i.e. less than 0)
	                'color': random.randint(0, len(colour_PIECES)-1)}
	    return newPiece

	def add_To_Board(self, board, piece):
		for x in range(self.tetromino_WIDTH):
			for y in range(self.tetromino_HEIGHT):
				if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK and x + piece['x'] < 10 and y + piece['y'] < 20:
					board[x + piece['x']][y + piece['y']] = piece['color']

	def draw_Piece(self, piece, pixel_x=None, pixel_y=None):
		shapeToDraw = PIECES[piece['shape']][piece['rotation']]
		for x in range(self.tetromino_WIDTH):
				for y in range(self.tetromino_HEIGHT):
					if shapeToDraw[y][x] != BLANK:
						if colour_PIECES == BLANK:
							return 0
						pygame.draw.rect(self.screen, colour_PIECES[piece['color']], (pixel_x + 1, pixel_y + 1, self.size_box - 1, self.size_box - 1))

	def get_Blank_Board(self):
	    # create and return a new blank board data structure
	    board = []
	    for i in range(self.grid_WIDTH):
	        board.append([BLANK] * self.grid_WIDTH)
	    return board
    

	def create_screen(self):
		pygame.display.set_caption("TetraAI")
		self.screen.fill(self.BACKGROUND_C)
		pygame.display.flip()


	def run(self):

		running = True

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

game_screen = game_window(800, 600)
game_screen.create_screen()
def run_Game():
	new_t_piece = game_screen.get_New_Piece()
	game_screen.draw_Piece(new_t_piece, pixel_x = 800 - 120, pixel_y=100)
	game_screen.draw_Board()
	game_screen.draw_Status()
	board = game_screen.get_Blank_Board()
	game_screen.add_To_Board(board, new_t_piece)
	pygame.display.update()
	game_screen.run()
	pygame.display.update()

def main_title():
	game_screen.show_Text_Screen('TetraAI')
	while True:
		for event in pygame.event.get(QUIT): #Fixed Quit Issue!
			pygame.quit()
			quit()
			sys.exit()
		for event in pygame.event.get(KEYDOWN):
			if event.key == K_DOWN:
				game_screen.create_screen()
				run_Game()

main_title() 