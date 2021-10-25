import pygame
import sys
import random
import argparse
from operator import add

parser = argparse.ArgumentParser(description='Snake game')
parser.add_argument('--manual', help="play game with manual control", action="store_true")
args = parser.parse_args()

frame_size = 600
block_size = 30

pygame.init()
pygame.display.set_caption('Snake')
game_display = pygame.display.set_mode((frame_size, frame_size))
clock = pygame.time.Clock()


snake_body = [[(block_size*i), 0] for i in reversed(range(1,4))]
snake_head = snake_body[0]

food_pos = [random.randrange(1, (frame_size//block_size)) * block_size, random.randrange(1, (frame_size//block_size)) * block_size]

direction = 'RIGHT'

dir_map = {
    "DOWN": [0, block_size],
    "UP": [0, -block_size],
    "LEFT": [-block_size, 0],
    "RIGHT": [block_size, 0]
}

# Calculate total blocks in game
def generate_blank_sheet(fx, fy, block):
    temp = []
    for x in range(fx//block):
        for y in range(fy//block):
            temp.append([x*block, y*block])
    return temp

# Basic implementation of hamiltonian cycle. Zig Zag down and shoot back up
def hamiltonian_cycle(fx, fy, block, sx, sy, dir):
    if (fx/block) % 2 == 0 and (fy/block) % 2 == 0:
        if dir == "DOWN":
            if sy % (block_size*2) == 0:
                return "RIGHT"
            else:
                return "LEFT"
        elif dir == "UP":
            if sy == 0:
                return "RIGHT"
        if sx == fx-block:
            return "DOWN"
        elif sx == block and sy != fy-block and sy != 0:
            return "DOWN"
        elif sy == fy-block and sx == 0:
            return "UP"
    return dir

# Game over procedure
def game_over():
    pygame.quit()
    sys.exit()

# Reference of total blocks in game
total_blocks = generate_blank_sheet(frame_size, frame_size, block_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()

        # Manual Movements
        elif event.type == pygame.KEYDOWN and args.manual:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    # Call AI for next move 
    if not args.manual:
        direction = hamiltonian_cycle(frame_size, frame_size, block_size, snake_head[0], snake_head[1], direction)
         
    # Moving the snake
    snake_head = list(map(add, snake_head, dir_map[direction]))
    snake_body.insert(0, list(snake_head))
    if snake_head == food_pos:
        food_arr = [f for f in total_blocks if f not in snake_body]
        if len(food_arr) == 0:
            print("Game Over")
            break

        food_pos = random.choice(food_arr)
    else:
        snake_body.pop()

    # Draw Game
    game_display.fill(pygame.Color(0, 0, 0))
    for block in snake_body:
        pygame.draw.rect(game_display, pygame.Color(0, 255, 0), pygame.Rect(block[0], block[1], block_size-2, block_size-2))
    pygame.draw.rect(game_display, pygame.Color(255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], block_size-2, block_size-2))

    # Game Over Conditions
    if  snake_head[0] < 0 or \
        snake_head[0] > frame_size-block_size or \
        snake_head[1] < 0 or \
        snake_head[1] > frame_size-block_size:
        game_over()

    for block in snake_body[1:]:
        if snake_head == block:
            game_over()

    
    pygame.display.update()
    clock.tick(30)

