import pygame
import random
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Load Background Music, Food Sound & Hit Sound
music_path = "/storage/emulated/0/Game/background.mp3"
food_sound_path = "/storage/emulated/0/Game/food.mp3"
hit_sound_path = "/storage/emulated/0/Game/hit.wav"

# File to Store Highest Score
high_score_file = "/storage/emulated/0/Game/highscore.txt"

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

# Screen Size
WIDTH, HEIGHT = 1080, 2130  
CELL_SIZE = 40  

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Mobile")

# Load High Score
def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            return int(file.read().strip())
    return 0

# Save High Score
def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

# Load the Best Score
best_score = load_high_score()

# Start Background Music
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)  
    pygame.mixer.music.set_volume(0.04)
    pygame.mixer.music.play(-1)

# Load Sound Effects
food_sound = pygame.mixer.Sound(food_sound_path) if os.path.exists(food_sound_path) else None
hit_sound = pygame.mixer.Sound(hit_sound_path) if os.path.exists(hit_sound_path) else None

# Snake Initialization
snake = [(WIDTH // 2, HEIGHT // 2)]
snake_dir = (0, CELL_SIZE)  
speed = 10  
score = 0  

# Function to Generate Food
def generate_food():
    while True:
        food_x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        food_y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        food = (food_x, food_y)
        if food not in snake:
            return food

food = generate_food()

# Game Loop
clock = pygame.time.Clock()
running = True
game_over = False
swipe_start = None

# Restart Button Position
button_width, button_height = 400, 150
button_x = (WIDTH - button_width) // 2
button_y = (HEIGHT // 2) + 100
restart_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Function to Show Game Over Screen
def show_game_over():
    global game_over, best_score

    pygame.mixer.music.stop()  

    if hit_sound:
        hit_sound.play()  

    screen.fill(BLACK)

    # Update Best Score if Current Score is Higher
    if score > best_score:
        best_score = score
        save_high_score(best_score)  # Save new best score

    # Display "GAME OVER" text
    font = pygame.font.Font(None, 120)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text, text_rect)

    # Show Final Score & Best Score
    score_font = pygame.font.Font(None, 80)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    best_text = score_font.render(f"Best: {best_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    best_rect = best_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_rect)
    screen.blit(best_text, best_rect)

    # Draw Restart Button
    pygame.draw.rect(screen, GRAY, restart_rect, border_radius=20)
    restart_font = pygame.font.Font(None, 80)
    restart_text = restart_font.render("RESTART", True, BLACK)
    restart_text_rect = restart_text.get_rect(center=restart_rect.center)
    screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.FINGERDOWN:
                touch_x, touch_y = event.x * WIDTH, event.y * HEIGHT
                if restart_rect.collidepoint(touch_x, touch_y):
                    game_over = False
                    restart_game()

# Function to Restart the Game
def restart_game():
    global snake, snake_dir, speed, food, game_over, score
    snake = [(WIDTH // 2, HEIGHT // 2)]  
    snake_dir = (0, CELL_SIZE)  
    speed = 10
    food = generate_food()
    score = 0  
    game_over = False
    pygame.mixer.music.play(-1)  

while running:
    screen.fill(BLACK)

    if game_over:
        show_game_over()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.FINGERDOWN:
            swipe_start = (event.x * WIDTH, event.y * HEIGHT)
        elif event.type == pygame.FINGERUP and swipe_start:
            swipe_end = (event.x * WIDTH, event.y * HEIGHT)
            dx = swipe_end[0] - swipe_start[0]
            dy = swipe_end[1] - swipe_start[1]

            if abs(dx) > abs(dy):  
                if dx > 0 and snake_dir != (-CELL_SIZE, 0):  
                    snake_dir = (CELL_SIZE, 0)  
                elif dx < 0 and snake_dir != (CELL_SIZE, 0):  
                    snake_dir = (-CELL_SIZE, 0)  
            else:
                if dy > 0 and snake_dir != (0, -CELL_SIZE):  
                    snake_dir = (0, CELL_SIZE)  
                elif dy < 0 and snake_dir != (0, CELL_SIZE):  
                    snake_dir = (0, -CELL_SIZE)  

    # Move Snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

    # **Boundary Hit Condition**
    if new_head in snake or new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        game_over = True
        continue

    snake.insert(0, new_head)

    # **Play Food Sound & Generate New Food**
    if abs(new_head[0] - food[0]) < CELL_SIZE and abs(new_head[1] - food[1]) < CELL_SIZE:
        if food_sound:
            food_sound.play()  
        food = generate_food()  
        speed += 1  
        score += 10  
    else:
        snake.pop()  

    # Draw Snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Draw Food
    pygame.draw.circle(screen, RED, (food[0] + CELL_SIZE // 2, food[1] + CELL_SIZE // 2), CELL_SIZE // 2)

    # **Draw Blue Borders**
    border_thickness = 10
    pygame.draw.line(screen, BLUE, (0, 0), (WIDTH, 0), border_thickness)  # Top
    pygame.draw.line(screen, BLUE, (0, 0), (0, HEIGHT), border_thickness)  # Left
    pygame.draw.line(screen, BLUE, (WIDTH - border_thickness, 0), (WIDTH - border_thickness, HEIGHT), border_thickness)  # Right
    pygame.draw.line(screen, BLUE, (0, HEIGHT - border_thickness), (WIDTH, HEIGHT - border_thickness), border_thickness)  # Bottom

    # Display Score and Best Score
    score_font = pygame.font.Font(None, 80)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    best_text = score_font.render(f"Best: {best_score}", True, WHITE)
    screen.blit(score_text, (20, 20))  
    screen.blit(best_text, (20, 100))  

    pygame.display.flip()
    clock.tick(speed)  

pygame.quit()