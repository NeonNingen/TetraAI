import pygame 

RED = (255,0,0)
BLACK = (0,0,0)

class game_window:

	def __init__(self, screen_WIDTH, screen_HEIGHT):
		self.screen_WIDTH = screen_WIDTH
		self.screen_HEIGHT = screen_HEIGHT
		self.BACKGROUND_C = RED
		self.screen = pygame.display.set_mode((screen_WIDTH, screen_HEIGHT))


	def create_screen(self):
		pygame.display.set_caption("Tetra_Display Test")
		pygame.init()
		self.screen.fill(self.BACKGROUND_C)
		pygame.display.flip()

		running = True

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False


game_screen = game_window(800, 600)
game_screen.create_screen()


