
import pygame
from pygame.locals import *

pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Maze Runner")

# Define colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


# Define maze layouts
maze1 = [
    "####################",
    "#..................#",
    "#.##.###.###.###.##.#",
    "#.#.................#",
    "#.#.##.#####.##.###.#",
    "#.#.#............#.#",
    "#.....###.####.....#",
    "#####.....#....#####",
    "#...............#.##",
    "#.###.####.#####...#",
    "#.#..............#.#",
    "#.###.##.##.###.##.#",
    "#..................#",
    "###.#############.##",
    "#................###",
    "#.######.###.####..#",
    "#.................##",
    "####################",
]

maze2 = [
    "####################",
    "#............#.....#",
    "#.#####.####.#.#####",
    "#.#............#...#",
    "#.#.##.#########.###",
    "#.#.#............#.#",
    "#.....###.######...#",
    "#####.....#....#####",
    "#...............#.##",
    "#.###.####.######..#",
    "#.#...............##",
    "#.###.##.##.###.####",
    "#..................#",
    "###.#############.##",
    "#.................##",
    "#.######.###.####..#",
    "#.................##",
    "####################",
]

# Define cell size
cell_size = min(window_width // len(maze1[0]), window_height // len(maze1))

# Define Runner properties
Runner_radius = cell_size // 4
Runner_speed = 1  # Adjust the speed here

# Define pellet properties
pellet_radius = cell_size // 10
pellet_spacing = cell_size // 2

# Create a list to store the pellet positions
pellet_positions = []

# Define game variables
current_level = 1
in_game = False

# Define timer properties
timer_duration = 60 # in seconds
start_time = pygame.time.get_ticks()

# Add images
background_image = pygame.image.load("background.jpg").convert_alpha()
you_win = pygame.image.load("you win.jpg").convert_alpha()
game_over = pygame.image.load("Game over.jpg").convert_alpha()
level_image = pygame.image.load("L 1.jpg").convert_alpha()
background_surface = pygame.transform.scale(background_image, (window_width, window_height))
level_image_surface = pygame.transform.scale(level_image, (window_width, window_height))
you_win_surface = pygame.transform.scale(you_win, (window_width, window_height))
game_over_surface = pygame.transform.scale(game_over, (window_width, window_height))

#Adding sounds 
win_sound = pygame.mixer.Sound("win.ogg")
eat_sound = pygame.mixer.Sound("eat.wav")
level_sound = pygame.mixer.Sound("select.mp3")
lose_sound = pygame.mixer.Sound("lose.wav")
mm_sound = pygame.mixer.music.load("main menu.mp3")

# Load the runner sprite sheets for each direction
right = pygame.image.load("right.png").convert_alpha()
up = pygame.image.load("up.png").convert_alpha()
down = pygame.image.load("down.png").convert_alpha()
left = pygame.image.load("left.png").convert_alpha()

# Define the size of the Pac-Man sprite
R_size = cell_size//1.3

# Create a variable to keep track of Pac-Man's direction
R_direction = "right"

#Define fade transparency level
fade = 230  # Adjust this value to change the fade intensity


# Game clock
clock = pygame.time.Clock()


def reset_game(level):
    global maze, pellet_positions, start_x, start_y, Runner_x, Runner_y, start_time
    if level == 1:
        maze = maze1
    elif level == 2:
        maze = maze2

    start_x = len(maze[0]) // 2
    start_y = len(maze) // 2

    Runner_x = (start_x * cell_size) + (cell_size // 2)
    Runner_y = (start_y * cell_size) + (cell_size // 2)

    pellet_positions.clear()
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == '.':
                pellet_x = col * cell_size + pellet_spacing
                pellet_y = row * cell_size + pellet_spacing
                pellet_positions.append((pellet_x, pellet_y))


    start_time = pygame.time.get_ticks()

def draw_menu():
    # Draw the background image
    window.blit(background_image, (0, 0))
    window.blit(background_surface, (0, 0)) 

    font = pygame.font.Font("fonts/arcade.ttf", 55)
    title_text = font.render("Maze Runner", True, YELLOW)
    window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 80))

    font = pygame.font.Font("fonts/arcade.ttf", 26)
    rule_text = font.render("RULES:", True, BLUE)
    window.blit(rule_text, (window_width // 2 - rule_text.get_width() // 2, 180))

    rule_text = font.render("1. Eat all pellets to win", True, WHITE)
    window.blit(rule_text, (window_width // 2 - rule_text.get_width() // 2, 230))

    rule_text = font.render("2. Avoid the maze walls", True, WHITE)
    window.blit(rule_text, (window_width // 2 - rule_text.get_width() // 2, 270))

    rule_text = font.render("3. Complete the level in time", True, WHITE)
    window.blit(rule_text, (window_width // 2 - rule_text.get_width() // 2, 310))

    font = pygame.font.Font("fonts/arcade.ttf", 28)
    level_text = font.render("SELECT LEVEL:", True, BLUE)
    window.blit(level_text, (window_width // 2 - level_text.get_width() // 2, 450))

    font = pygame.font.Font("fonts/arcade.ttf", 16)
    level_text = font.render("Press 1 for Level 1", True, WHITE)
    window.blit(level_text, (window_width // 2 - level_text.get_width() // 2, 480))

    level_text = font.render("Press 2 for Level 2", True, WHITE)
    window.blit(level_text, (window_width // 2 - level_text.get_width() // 2, 500))

    pygame.display.update()

def draw_game():
    window.fill(BLACK)
    window.blit(level_image, (0, 0))
    window.blit(level_image_surface, (0, 0))

    # Draw maze walls
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == '#':
                wall_x = col * cell_size
                wall_y = row * cell_size

                 # Draw outer borders around the wall cell
                pygame.draw.line(window, BLACK, (wall_x, wall_y), (wall_x + cell_size, wall_y), 3)  # Top border
                pygame.draw.line(window, BLACK, (wall_x, wall_y), (wall_x, wall_y + cell_size), 3)  # Left border
                pygame.draw.line(window, BLACK, (wall_x + cell_size, wall_y), (wall_x + cell_size, wall_y + cell_size), 3)  # Right border
                pygame.draw.line(window, BLACK, (wall_x, wall_y + cell_size), (wall_x + cell_size, wall_y + cell_size), 3)  # Bottom border

   # Draw pellets
    for position in pellet_positions:
        pygame.draw.circle(window, WHITE, position, pellet_radius)


    # Calculate remaining time
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    remaining_time = max(timer_duration - elapsed_time, 0)

    # Draw timer
    font = pygame.font.Font(None, 36)
    timer_text = font.render("Time: {}s".format(remaining_time), True, WHITE)
    timer_text_rect = timer_text.get_rect()
    timer_text_rect.topright = (window_width - 10, 10)
    window.blit(timer_text, timer_text_rect)

  
     # Draw Pac-Man based on the current direction
    if R_direction == "up":
        pacman_sprite = pygame.transform.scale(up, (R_size, R_size))
    elif R_direction == "down":
        pacman_sprite = pygame.transform.scale(down, (R_size, R_size))
    elif R_direction == "left":
        pacman_sprite = pygame.transform.scale(left, (R_size, R_size))
    else:  # pacman_direction == "right"
        pacman_sprite = pygame.transform.scale(right, (R_size, R_size))

    window.blit(pacman_sprite, (Runner_x - R_size // 2, Runner_y - R_size // 2))


    pygame.display.update()


# Game loop


mm_sound = pygame.mixer.music.play()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not in_game:
        if keys[K_1]:
            current_level = 1
            reset_game(current_level)
            in_game = True
            mm_sound = pygame.mixer.music.stop()
            level_sound.play(maxtime=1000)


        elif keys[K_2]:
            current_level = 2
            reset_game(current_level)
            in_game = True
            mm_sound = pygame.mixer.music.stop()
            level_sound.play(maxtime=1000)

        elif keys[K_q]:
            running = False
        else:
            draw_menu()

    else:
        # Handle Runner movement
        next_x = start_x
        next_y = start_y

        if keys[K_LEFT]:
            next_x -= 1
            R_direction = "left"
        elif keys[K_RIGHT]:
            next_x += 1
            R_direction = "right"
        elif keys[K_UP]:
            next_y -= 1
            R_direction = "up"
        elif keys[K_DOWN]:
            next_y += 1
            R_direction = "down"

    

        # Check if the next cell is not a wall
        if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze) and maze[next_y][next_x] != '#':
            start_x = next_x
            start_y = next_y

        Runner_x = (start_x * cell_size) + (cell_size // 2)
        Runner_y = (start_y * cell_size) + (cell_size // 2)

        # Check for pellet collision
        for position in pellet_positions:
            pellet_x, pellet_y = position
            if abs(Runner_x - pellet_x) <= Runner_radius and abs(Runner_y - pellet_y) <= Runner_radius:
                pellet_positions.remove(position)
                eat_sound.play()

        draw_game()

        if len(pellet_positions) == 0:
            in_game = False
         
            win_sound.play(maxtime=2000)
       
            window.blit(you_win, (0, 0))
            window.blit(you_win_surface, (0, 0)) 
            pygame.display.update()
            pygame.time.wait(3000)
            mm_sound = pygame.mixer.music.play(-1)

        else:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) // 1000
            remaining_time = max(timer_duration - elapsed_time, 0)
            if remaining_time == 0:
                in_game = False

                lose_sound.play(maxtime=4000) 

                window.blit(game_over, (0, 0))
                window.blit(game_over_surface, (0, 0))
                pygame.display.update()
                pygame.time.wait(3000)
                mm_sound = pygame.mixer.music.play(-1)

    clock.tick(10)

pygame.quit()
