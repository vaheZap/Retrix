import sys
import pygame
import random

pygame.init()

# Bad/Game Over Facts
GFACTS = ['F']

# Good/Victory Facts
VFACTS = ['Fact 1', 'Fact 2', 'Fact 3', 'Fact 4', 'Fact 5', 'etc...']

#FACTS
vic = random.choice(VFACTS)
gam = random.choice(GFACTS)

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
GRID_SIZE = 25

# Colors
WHITE = (79,76,176)
GRAY = (22, 21,9)
BLACK = (0, 0,0)
RED = (255, 0, 0)
BLUE = (148, 137, 63)
GREEN = (51, 47, 21)
COLORS = [GRAY, BLUE, GREEN]

# Tetromino shapes
SHAPES = [
    [
    	['.....',
         '.....',
         '..O..',
         '.....',
         '.....']
    ],
    [
        ['.....',
         '.....',
         '.....',
         'OOOO.',
         '.....'],
        ['.....',
         '..O..',
         '..O..',
         '..O..',
         '..O..']
    ],
    [
        ['.....',
         '.....',
         '..O..',
         '.OOO.',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '..OO.',
         '..O..',
         '.....']
    ],
    [
        [
         '.....',
         '.....',
         '..OO.',
         '.OO..',
         '.....'],
        ['.....',
         '.....',
         '.OO..',
         '..OO.',
         '.....'],
        ['.....',
         '.O...',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '.O...',
         '.....']
    ],
    [
        ['.....',
         '..O..',
         '..O.',
         '..OO.',
         '.....'],
        ['.....',
         '...O.',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '.OO..',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '.O...',
         '.....']
    ],
]

# PLAYER 2
# px, py = 400, 575
# fpx, fpy = 0, 0
# player = pygame.Rect(px, py, 25, 25)

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS) # You can choose different colors for each shape
        self.rotation = 0

class Player:
	def __init__(self, x, y, shape, sprite: pygame.sprite.Sprite):
		self.x = x
		self.y = y
		self.shape = shape
		self.color = WHITE 
		self.rotation = 0
		self.sprite = sprite

	def draw(self, screen, j, i):
		self.sprite.rect = self.sprite.image.get_rect(bottomleft=(((self.x + j) * GRID_SIZE, (self.y + i) * GRID_SIZE)))
		# self.rect.center = (self.x, self.y)
		screen.blit(self.sprite.image, self.sprite.rect)


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.current_player = self.new_player()
        self.game_over = False
        self.victory = False

    def new_piece(self):
        # Choose a random shape
        shape = random.choice(SHAPES)

        # Return a new Tetromino object
        return Tetromino(self.width // 4, 0, shape)

    def new_player(self):
    	shape = SHAPES[0]

    	# load the player's sprite
    	player_sprite = pygame.sprite.Sprite()
    	player_sprite.image = pygame.image.load('earth.png').convert_alpha()
    	return Player(self.width // 4, 0, shape, player_sprite)

    def valid_move(self, piece, x, y, rotation):
        """Check if the piece can move to the given position"""
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O' and (self.grid[piece.y + i + y][piece.x + j + x] != 0):
                        return False
                except IndexError:
                    return False
        return True

    def valid_player_move(self, piece, x, y, rotation):
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O' and (self.grid[piece.y + i + y][piece.x + j + x] != 0):
                        return False
                except IndexError:
                    return False
        return True

    def clear_lines(self):
        """Clear the lines that are full and return the number of cleared lines"""
        lines_cleared = 0
        for i, row in enumerate(self.grid[:-1]):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])
        return lines_cleared

    def lock_piece(self, piece):
        """Lock the piece in place and create a new piece"""
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.grid[piece.y + i][piece.x + j] = piece.color
        lines_cleared = self.clear_lines()
        # Create a new piece
        self.current_piece = self.new_piece()
        # self.current_player = self.new_player()
        # Check if the game is over
        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True
        return lines_cleared

    def lose_player(self, piece):
        """Lock the piece in place and create a new piece"""
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.grid[piece.y + i][piece.x + j] = piece.color
        # Check if the game is over
        if not self.valid_player_move(self.current_player, 0, 0, 0):
            self.victory = True

    def update(self):
        """Move the tetromino down one cell"""
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)
                # self.lose_player(self.current_player)

    def draw(self, screen):
        """Draw the grid and the current piece"""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        if self.current_piece:
            for i, row in enumerate(self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        pygame.draw.rect(screen, self.current_piece.color, ((self.current_piece.x + j) * GRID_SIZE, (self.current_piece.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        if self.current_player:
            for i, row in enumerate(self.current_player.shape[self.current_player.rotation % len(self.current_player.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                       # pygame.draw.rect(screen, self.current_player.color, ((self.current_player.x + j) * GRID_SIZE, (self.current_player.y + i) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))
                       self.current_player.draw(screen, j, i)
    
    
def draw_game_over(screen, x, y):
    """Draw the game over text on the screen"""
    font = pygame.font.Font(None, 48)

    text = font.render("Aww you lost! But the planet won...", True, RED)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)

    text_new = font.render("Take care of the planet that your future generations will live on. ", True, RED)
    text_rect_new = text.get_rect(center=(WIDTH/2-175, HEIGHT/2+50))
    screen.blit(text_new, text_rect_new)

def draw_victory(screen, x, y):
    """Draw the game over text on the screen"""
    font = pygame.font.Font(None, 48)

    text = font.render("Hooray, you won!!! But did you really...", True, RED)
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)

    text_new = font.render("Take care of the planet that your future generations will live on. ", True, RED)
    text_rect_new = text.get_rect(center=(WIDTH/2-175, HEIGHT/2+50))
    screen.blit(text_new, text_rect_new)


def main():
    # Initialize pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    # Create a clock object
    clock = pygame.time.Clock()
    # Create a Tetris object
    game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
    fall_time = 0
    fall_speed = 50  # You can adjust this value to change the falling speed, it's in milliseconds
    game.current_player.x = 10
    game.current_player.y = 19
    while True:
        # Fill the screen with black
        screen.fill(BLACK) 
        for event in pygame.event.get():
            # Check for the QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for the KEYDOWN event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.current_piece.x != -2:
                    if game.valid_move(game.current_piece, -1, 0, 0):
                        game.current_piece.x -= 1 # Move the piece to the left
                        print(game.current_piece.x)


                if event.key == pygame.K_RIGHT and game.current_piece.x != 30:
                    if game.valid_move(game.current_piece, 1, 0, 0):
                        game.current_piece.x += 1 # Move the piece to the right
                        print(game.current_piece.x)

                if event.key == pygame.K_DOWN:
                    if game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1 # Move the piece down
                if event.key == pygame.K_UP:
                    if game.valid_move(game.current_piece, 0, 0, 1):
                        game.current_piece.rotation += 1 # Rotate the piece
                if event.key == pygame.K_SPACE:
                    while game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1 # Move the piece down until it hits the bottom
                    game.lock_piece(game.current_piece) # Lock the piece in place

                if event.key == pygame.K_a:
                    if game.valid_player_move(game.current_player, -1, 0, 0):
                        game.current_player.x -= 1 # Move the piece to the left

                if event.key == pygame.K_d:
                    if game.valid_player_move(game.current_player, 1, 0, 0):
                        game.current_player.x += 1 # Move the piece to the right

                if event.key == pygame.K_s:
                    if game.valid_player_move(game.current_player, 0, 1, 0):
                        game.current_player.y += 1 # Move the piece down
                if event.key == pygame.K_w:
                    if game.valid_player_move(game.current_player, 0, 0, 1):
                        game.current_player.y -= 1 # Rotate the piece

               	if game.valid_player_move(game.current_player, 0, 0, 1) != True:
               		game.victory = True
        # Get the number of milliseconds since the last frame
        delta_time = clock.get_rawtime() 
        # Add the delta time to the fall time
        fall_time += delta_time 
        if fall_time >= fall_speed:
            # Move the piece down
            game.update()
            # Reset the fall time
            fall_time = 0
        # Draw the grid and the current piece
        game.draw(screen)
        if game.game_over:
            # Draw the "Game Over" message
            screen.fill(BLACK)
            draw_game_over(screen, WIDTH // 2 - 100, HEIGHT // 2 - 30)  # Draw the "Game Over" message
            # You can add a "Press any key to restart" message here
            # Check for the KEYDOWN event
            if event.type == pygame.KEYDOWN:
                # Create a new Tetris object
                game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
        if game.victory:
        	# Draw the "Victory" message
        	screen.fill(BLACK)
        	draw_victory(screen, WIDTH // 2 - 100, HEIGHT // 2 - 30) # Draw the "Victory" message
        	# You can add a "Press any key to restart" message here
        	# Check for the KEYDOWN event
        	if event.type == pygame.KEYDOWN:
        		# Create a new Tetris object
        		game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
        		game.current_player.x = 10
        		game.current_player.y = 19

        # Update the display
        pygame.display.flip()
        # Set the framerate
        clock.tick(60)


if __name__ == "__main__":
    main()