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

	tetromino_WIDTH: int = 6
	tetromino_HEIGHT: int = 6
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
	
    def __init__(self, game_WIDTH, game_HEIGHT):
        pygame.display.set_caption('$s') % 'TetraAI'
        self.game_WIDTH = game_WIDTH
        self.game_HEIGHT = game_HEIGHT
        self.gameDisplay = pygame.display.set_mode((game_WIDTH, game_HEIGHT+60))
        self.BOX_SIZE: int = 30
        self.BOARD_WIDTH: int = 20
    	self.BOARD_HEIGHT: int = 30
    	self.EMPTY: str = '0'
    	self.MOVELEFTANDRIGHT_RATE: float = 0.050
    	self.MOVEDOWNWARDS_RATE: float = 0.025
        self.BORDER_C = YELLOW
        self.BACKGROUND_C = BLACK
        self.TEXT_C = WHITE
        self.COLOURS = (ORANGE, BLUE, YELLOW, PURPLE, TEALGRAY)
        self.score: int = 0
        self.games_achieved: int = 0 # games_completed
        self.step_reward: int = 0 # one_step_reward = 0
		self.GAME_MARGIN = int((game_WIDTH - self.BOARD_WIDTH * self.BOX_SIZE) / 2)
		self.TOP_MARGIN = game_HEIGHT - (self.BOARD_HEIGHT * self.BOX_SIZE) - 5

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
		DISPLAYSURF.fill(self.BACKGROUND_C)
		draw_screen(screen)
		draw_handler(self.score, level, current_position)
		if falling_piece is not None:
			draw_piece(falling_piece)
		pygame.display.update()
		FPSCLOCK.tick(60)


		def Valid_Quit():    # import pygame.locals as * replaces keys
		    for event in pygame.event.get(QUIT): 
		        terminate()
		    for event in pygame.event.get(KEYUP): # get all the KEYUP events
		        if event.key == K_ESCAPE:
		            terminate() 
		        pygame.event.post(event) 

		def makeTextObjs(text, font, colour): #surf -> text_obj
		    text_obj = font.render(text, True, colour)
		    return text_obj, text_obj.get_rect()

		def show_text_on_screen(self, text):
		    # Create big text!
		    title_text_obj, title_rect = makeTextObjs(text, big_FONT, shadowCOLOUR)
		    title_rect.center = (int(self.game_WIDTH / 2), int(self.game_HEIGHT / 2))
		    DISPLAYSURF.blit(title_text_obj, title_rect)

		    # Create Text!
		    title_text_obj, title_rect = makeTextObjs(text, big_FONT, textCOLOUR)
		    title_rect.center = (int(self.game_WIDTH / 2) - 3, int(self.game_HEIGHT / 2) - 3)
		    DISPLAYSURF.blit(title_text_obj, title_rect)

		    # Draw mini text!
		    press_key_text_obj, press_key_rect = makeTextObjs('Please wait to advance.',
		                                                    small_FONT, textCOLOR)
		    press_key_rect.center = (int(self.game_WIDTH / 2), int(self.game_HEIGHT / 2) + 100)
		    DISPLAYSURF.blit(press_key_text_obj, press_key_rect)

		    pygame.display.update()
		    FPSCLOCK.tick()
		    time.sleep(0.5)


		def terminate():
		    pygame.quit()
		    quit()


		def checkForKeyPress():
			# Look for a keyup event, if event is found then returb a keydown
		    Valid_Quit()
		    for event in pygame.event.get([KEYUP, KEYDOWN]):
		        if event.type == KEYDOWN:
		            continue
		        return event.key
		    return None

		def fall_frequency_and_level(score):
			# Score and level system
		    level = int(score / 10) + 1
		    fall_frequency = 0.07 * math.exp(
		        (1 - level) / 3) 
		    return level, fall_frequency


		def return_new_piece(self):
		    # Makes random forms of tetraminos then returns them
		    # Starts at the top of the board
		    shapes = random.choice(list(PIECES.keys()))
		    new_pieces = {
		        'shape': shapes,
		        'rotation': random.randint(0, len(PIECES[shapes]) - 1),
		        'x': int(self.BOARD_WIDTH / 2) - int(tetromino_WIDTH / 2),
		        'y': -2, 
		        'color': random.randint(1, len(self.COLOURS) - 1)
		    }
		    return new_pieces

		def create_box(self, box_x, box_y, colour, cord_x = None, cord_y = None): #pixelx = cord_x, draw_box -> create_box
			# creates a box with each tetromino taking up a grid on the box
			# if cord_x or cord_y == True then store cords, used in the converter
		    if colour == BLANK:
		        return
		    if cordx is None and cord_y is None:
		        cord_x, cord_y = convert_to_pixel_coords(box_x, box_y)
		    pygame.draw.rect(DISPLAYSURF, self.COLOURS[colour],
		                     (cord_x + 1, cord_y + 1, self.BOX_SIZE - 1, self.BOX_SIZE - 1))
		    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color],
		                     (cord_x + 1, cord_y + 1, self.BOX_SIZE - 4, self.BOX_SIZE - 4))


		def create_board(self, board):
		    # Create board
		    pygame.draw.rect(DISPLAYSURF, self.BORDER_C,
		                     (GAME_MARGIN - 3, TOP_MARGIN - 7, (self.BOARD_WIDTH * self.BOX_SIZE) + 8,
		                      (self.BOARD_HEIGHT * self.BOX_SIZE) + 8), 5)

		    # make background
		    pygame.draw.rect(
		        DISPLAYSURF, self.BACKGROUND_C, 
		        (GAME_MARGIN, TOP_MARGIN, self.BOX_SIZE * self.BOARD_WIDTH, self.BOX_SIZE * self.BOARD_HEIGHT))
		    # draw the individual grids on the board
		    # Each grid represents a box that is placed on the board
		    for x in range(self.BOARD_WIDTH):
		        for y in range(self.BOARD_HEIGHT):
		            create_box(x, y, board[x][y])

		def get_blank_board(self):
			# Make blank board
		    board = []
		    for i in range(self.BOARD_WIDTH):
		        board.append(['0'] * self.BOARD_HEIGHT)
		    return board

		def add_to_board(self, board, piece):
		    # add pieces to board dependent to location
		    for x in range(self.tetromino_WIDTH):
		        for y in range(self.tetromino_HEIGHT):
		            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK and x + piece['x'] < 10 and y + piece['y'] < 20:
		                board[x + piece['x']][y + piece['y']] = piece['color']
		                # DEBUGGING NOTE: SOMETIMES THIS IF STATEMENT ISN'T
		                # SATISFIED, WHICH NORMALLY WOULD RAISE AN ERROR.
		                # NOT SURE WHAT CAUSES THE INDICES TO BE THAT HIGH.
		                # THIS IS A BAND-AID FIX
		                

		def is_on_board(self, x, y):
		    return y < self.BOARD_HEIGHT and x >= 0 and x < self.BOARD_WIDTH 


		def correct_position(self, board, piece, adj_x=0, adj_y=0):
		    # True if piece do not colide
		    for x in range(self.tetromino_WIDTH):
		        for y in range(self.tetromino_HEIGHT):
		            is_above_board = y + piece['y'] + adj_y < 0
		            if is_above_board or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
		                continue
		                # not on board
		            if not is_on_board(x + piece['x'] + adj_x, y + piece['y'] + adj_y):
		                return False  
		                # collision
		            if board[x + piece['x'] + adj_x][y + piece['y'] + adj_y] != BLANK:
		                return False  
		    return True


		def is_complete_line(self, board, y):
		    # True if no gaps
		    for x in range(self.BOARD_WIDTH):
		        if board[x][y] == BLANK:
		            return False
		    return True


		def remove_complete_lines(self, board):
			# Remove finished lines and makes all above lines move down
		    lines_removed = 0
		    y = self.BOARD_HEIGHT - 1 
		    while y >= 0:
		        if is_complete_line(board, y):
		            # above line blank #Flipped
		            for x in range(self.BOARD_WIDTH):
		                board[x][0] = BLANK
		            lines_removed += 1
		           	# moves lines down
		            for pull_down_y in range(y, 0, -1):
		                for x in range(self.BOARD_WIDTH):
		                    board/[x][pull_down_y] = board[x][pull_down_y - 1]
		        else:
		        	# checks new row
		            y -= 1
		    return lines_removed, board

# Completed Segment


def main():
	Tetra = Game()









