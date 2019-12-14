"""
Project TetraAI 
Made by Zain Cheema
Just a personal thing,
I used var: datatype = value, because I like how it is able to describe the data type of a variable so everyone understands it.
Each of the individual slices can optionally be adjointed (to adjoint a matrix means to transpose and conjugate it) -> adj_x or adj_y
"""

import pygame, sys, numpy, copy, math, time, pyautogui
from pygame.locals import *
import matplotlib.pyplot as plts
from Tetra_Pieces import Pieces

#Setting up the body of the program

class Game:
	"""
	Colours
	White = Ingame Text
	BLACK = Colour of the background
	Magenta Pop Color Palette:
	ORANGE = (240,115,73)
	BLUE = (17,55,84)
	YELLOW = (212,154,42)
	PURPLE = (161,0,105)
	TEALGRAY = (85,115,137)
	Each colour for a tetromino
	"""

	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	ORANGE = (240,115,73)
	BLUE = (17,55,84)
	YELLOW = (212,154,42)
	PURPLE = (161,0,105)
	TEALGRAY = (85,115,137)

	# Settings for the bot
	pyautogui.FAILSAFE: bool = True
	pyautogui.PAUSE: float = 0.03
	ALPHA: float = 0.01	# Learning parameters
	GAMAA: float = 0.9
	MAX_GAMES_PLAYED: int = 100
	random_chance: float = 0.5
	weights = [-1, -1, -1, -30]  # Starting weight values

	tetromino = Pieces()
	
	# Dict for the pieces
	PIECES = {     
    'S': tetromino.piece_S(),
    'Z': tetromino.piece_Z(),
    'J': tetromino.piece_J(),
    'L': tetromino.piece_L(),
    'I': tetromino.piece_I(),
    'O': tetromino.piece_O(),
    'T': tetromino.piece_T()
}
	
    def __init__(self, game_width, game_height, fps):
        pygame.display.set_caption('$s') % 'TetraAI'
        self.game_width = game_width
        self.game_height = game_height
        self.FPS = fps
        self.gameDisplay = pygame.display.set_mode((game_width, game_height+60))
        self.BOX_SIZE: int = 30
        self.BOARD_WIDTH: int = 20
    	self.BOARD_HEIGHT: int = 30
    	self.EMPTY: str = '0'
    	self.MOVELEFTANDRIGHT_RATE: float = 0.050
    	self.MOVEDOWNWARDS_RATE: float = 0.025
        self.BORDER_C = YELLOW
        self.BACKGROUND_C = BLACK
        self.TEXT_C = WHITE
        self.COLORS = (ORANGE, BLUE, YELLOW, PURPLE, TEALGRAY)
        self.score: int = 0
        self.games_achieved: int = 0 # games_completed
        self.step_reward: int = 0 # one_step_reward = 0

	"""
    The gameplay function is the handler of the game. It performs the game construction aswell as the learning segment of the AI. It consists of 2 arguments, 
	[Arguments]
	The self is used to call variables from the __init__ method. Such as self.score for example.
    The weights that is a list holding 4 integer values. Tbe 4 values are, Maximum height, Total column heights, difference between the column heightsand the nummber of empty spaces on the board 
	The random_chance is a float value that is between 0 to 1 because it determines the best move by giving a random input. The AI will learn through given reward and this will give is various values of rewards without a bias. Making it unpredicatable at first.

	Then the returns:
	[Returns]
		The new_score being the new value it earns after completing the game.
		The random_chance being the same as the argumentation version but allowing the learning to happen throughout the game
		The weights being the same as the argumentation version but allowing the learning to happen throughout the game
    """

    def time_position(num):
    	if num = 0:
    		last_direction_down_time = time.time() # last_move_down_time = time.time()
    		last_directional_time = time.time() # last_lateral_time = time.time()
			last_directional_falling_time = time.time() # last_fall_time = time.time()
		elif num = 1:
			last_direction_down_time = time.time()
		elif num = 2:
    		last_directional_time = time.time()
		elif num = 3: 
			last_directional_falling_time = time.time()
		else:
			print('ERROR')

	def gameplay(self, weights, random_chance): # explore_change -> random_chance
		screen = screen_empty() # board = get_blank_board()
		current_position = [0. 0] # Relative Rotation, lateral movement
		direction_down: bool = False # moving_down = False  
		direction_right: bool = False # moving_right = False
		direction_left: bool = False # moving_left = False
		falling_piece = return_new_piece()  # get_new_piece()
		next_piece = return_new_piece()
		time_position(0)
		fall_frequency, level = fall_frequency_and_level(self.score) # level, fall_freq = get_level_and_fall_freq(score)
		
	while True:
		if falling_piece is None:
            falling_piece = next_piece
            next_piece = return_new_piece()
            last_fall_time = time.time()  # reset last_fall_time

            if not correct_position(screen, falling_piece): # Instead of board it is screen. is_valid_position
            	return self.score, weights, random_chance
            weights, current = gradient_descent(screen, falling_piece, weights, random_chance)

            if random_chance > 0.0005: 
            	random_chance *= 0.99
            else:
            	random_chance = 0
        check_quit_method()
        current_position = move_made(current_position)  # current_position = current_move


        # Rotating Pieces (checks if there is space in said rotation)
        for event in pygame.event.get():
			if event.type == keys.KEYDOWN:
        		if (event.key == keys.K_UP or event.key == keys.K_W):
        			falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(PIECES[falling_piece['shape']])
        			if not correct_position(screen, falling_piece):
        				falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(PIECES[falling_piece['shape']])

        		elif (event.key == keys.K_q):
        			falling_piece['rotation'] = (falling_piece['rotation'] - 1) % len(PIECES[falling_piece['shape']])
        			if not correct_position(screen, falling_piece):
        				falling_piece['rotation'] = (falling_piece['rotation'] + 1) % len(PIECES[falling_piece['shape']])

        # Moving side to side
        		elif (event.key == keys.K_LEFT) or (event.keys == keys.K_a) and correct_position(screen, falling_piece, adj_x = -1):
        			falling_piece['x'] -= 1
        			direction_left = True
        			direction_right, direction_down  = False
        			time_position(2)

        		elif (event.key == keys.K_RIGHT) or (event.keys == keys.K_a) and correct_position(screen, falling_piece, adj_x = -1):
        			falling_piece['x'] -= 1
        			direction_left, direction_down = False
        			direction_right = True
        			time_position(2)


        # Piece will drop immediatly 
        		elif event.key == keys.K_SPACE:
        			direction_right, direction_left, direction_down = False
					for i in range(1, self.BOARD_HEIGHT):
						if not correct_position(screen, falling_piece, adj_y = i)
						break
					falling_piece['y'] += i - 1

		# Fall faster not immediate
				elif (event.key == keys.K_DOWN) or (event.key == keys.K_s):
					direction_down = True
					if correct_position(screen, falling_piece, adj_y = 1):
						falling_piece['y'] += 1
					time_position(1)

		# handing the inputs made by the AI
		if (direction_left or direction_right) and time.time() - time_position(2) > self.MOVELEFTANDRIGHT_RATE:
			if direction_left and correct_position(screen, falling_piece, adj_x = -1):
				falling_piece['x'] -= 1
			elif direction_right and correct_position(screen, falling_piece, adj_x = -1):
				falling_piece['x'] += 1
			time_position(2)

		if direction_down and time.time() - time_position(1) > self.MOVEDOWNWARDS_RATE and correct_position(screen, falling_piece, adj_y = 1):
			falling_piece['y'] += 1
			time_position(1)
			games_achieved += 1

		# validation section: Validate in the piece has reached the bottom of the board
		if time.time() - time_position(3) > fall_frequency:
			if not correct_position(screen, falling_piece, adj_y = 1):
				add_to_board(screen, falling_piece)
				screen, lines = remove_finished_lines(screen)
				self.score += lines * lines
				fall_frequency, level = fall_frequency_and_level(self.score)
				falling_piece = None
			else:
				falling_piece['y'] += 1
				time_position(3)
				games_achieved += 1
		# Draw all this on the screen
		DISPLAYSURF.fill*(self.BACKGROUND_C)
		draw_screen(screen)
		draw_handler(self.score, level, current_position)
		if falling_piece is not None:
			draw_piece(falling_piece)
		pygame.display.update
		FPSCLOCK.tick(self.FPS)

# Completed Section


def Valid_Quit():    # import pygame.locals  as key
    for event in pygame.event.get(QUIT): 
        terminate()
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() 
        pygame.event.post(event) k

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def main():
	Tetra = Game()









