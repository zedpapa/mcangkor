import pygame
import json

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Grid")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Grid settings
block_size = 20
grid_width = width // block_size
grid_height = (height - 80) // block_size # Adjust grid height for palette and info bar

# Axis settings
start_x = 0
start_y = 0

# Font
pygame.font.init()
font = pygame.font.SysFont('monospace', 20)

# Grid colors
grid_colors = [[white for _ in range(grid_width)] for _ in range(grid_height)]

# Color palette
palette_colors = [white, black, red, green, blue]
active_color = black

def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            pygame.draw.rect(screen, grid_colors[y][x], rect)
            pygame.draw.rect(screen, gray, rect, 1)

def draw_palette():
    for i, color in enumerate(palette_colors):
        rect = pygame.Rect(i * 40, height - 80, 40, 40)
        pygame.draw.rect(screen, color, rect)

def draw_info_bar():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x = mouse_x // block_size + start_x
    grid_y = mouse_y // block_size + start_y

    coord_text = f"Coords: ({grid_x}, {grid_y})"
    text_surface = font.render(coord_text, True, black)
    screen.blit(text_surface, (10, height - 35))

def save_grid():
    data = {
        "grid_colors": grid_colors,
        "start_x": start_x,
        "start_y": start_y
    }
    with open("grid_save.json", "w") as f:
        json.dump(data, f)

def load_grid():
    global grid_colors, start_x, start_y
    try:
        with open("grid_save.json", "r") as f:
            data = json.load(f)
            grid_colors = data["grid_colors"]
            start_x = data["start_x"]
            start_y = data["start_y"]
    except (FileNotFoundError, json.JSONDecodeError):
        print("Could not load grid from file.")

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if palette is clicked
            if mouse_y >= height - 80:
                color_index = mouse_x // 40
                if color_index < len(palette_colors):
                    active_color = palette_colors[color_index]
            # Check if grid is clicked
            else:
                grid_x = mouse_x // block_size
                grid_y = mouse_y // block_size
                if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
                    grid_colors[grid_y][grid_x] = active_color
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                start_x -= 1
            if event.key == pygame.K_RIGHT:
                start_x += 1
            if event.key == pygame.K_UP:
                start_y -= 1
            if event.key == pygame.K_DOWN:
                start_y += 1
            if event.key == pygame.K_s:
                save_grid()
            if event.key == pygame.K_l:
                load_grid()
    # Drawing
    screen.fill(white)
    draw_grid()
    draw_palette()
    draw_info_bar()
    pygame.display.flip()

# Quit Pygame
pygame.quit()
