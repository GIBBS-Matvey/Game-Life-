import pygame
import random
from copy import deepcopy


RES = W, H = 700, 700
TILE_SIZE = 20
M = 600 // TILE_SIZE
N = 600 // TILE_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
fps = 60

pygame.init()
display = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


def valid_position(i, j, m, n):
    valid_row = (i >= 0) and (i < m)
    valid_col = (j >= 0) and (j < n)
    return valid_row and valid_col


def get_neighbours(i, j, m, n):
    neighbours = list()

    if valid_position(i, j - 1, m, n):
        neighbours.append([i, j - 1])

    if valid_position(i - 1, j, m, n):
        neighbours.append([i - 1, j])

    if valid_position(i, j + 1, m, n):
        neighbours.append([i, j + 1])

    if valid_position(i + 1, j, m, n):
        neighbours.append([i + 1, j])

    return neighbours


def get_next_generation(cur_field):
    copy_field = deepcopy(cur_field)

    for i in range(M):
        for j in range(N):
            live_adj_number = 0
            neighbours = get_neighbours(i, j, M, N)
            for adj in neighbours:

                if copy_field[adj[0]][adj[1]] == 1:
                    live_adj_number += 1

            if live_adj_number > 3 or live_adj_number < 2:
                cur_field[i][j] = 0

            elif copy_field[i][j] == 0 and live_adj_number == 3:
                cur_field[i][j] = 1

            elif copy_field[i][j] == 1 and (live_adj_number == 2 or live_adj_number == 3):
                cur_field[i][j] = 1

    return cur_field


def draw_field(cur_field):
    for x in range(0, M):
        for y in range(0, N):
            if cur_field[y][x]:
                draw_cell(x, y)


def draw_cell(x, y):
    pygame.draw.rect(display, pygame.Color(WHITE),
                     (x * TILE_SIZE + 2, y * TILE_SIZE + 2, TILE_SIZE - 2, TILE_SIZE - 2))


def game_loop():

    prev_field = list()
    cur_field = [[random.randint(0, 1) for i in range(M)] for j in range(N)]
    button_next_generation = pygame.Rect(650, 100, 50, 50)
    button_die = pygame.Rect(650, 200, 50, 50)

    button_list = list()
    for x in range(0, M):
        for y in range(0, N):
            tmp_button = pygame.Rect(x * TILE_SIZE + 2, y * TILE_SIZE + 2, TILE_SIZE - 2, TILE_SIZE - 2)
            button_list.append(tmp_button)

    while True:

        display.fill(pygame.Color(BLACK))
        [pygame.draw.line(display, pygame.Color(BLACK), (x, 0), (x, H)) for x in range(0, W, TILE_SIZE)]
        [pygame.draw.line(display, pygame.Color(BLACK), (0, y), (W, y)) for y in range(0, H, TILE_SIZE)]

        pygame.draw.rect(display, BLUE, button_next_generation)
        pygame.draw.rect(display, RED, button_die)

        draw_field(cur_field)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                for button in button_list:
                    if button.collidepoint(mouse_pos):
                        real_y = (button.x - 2) // 20
                        real_x = (button.y - 2) // 20
                        if cur_field[real_x][real_y]:
                            cur_field[real_x][real_y] = 0
                        else:
                            cur_field[real_x][real_y] = 1

                        draw_field(cur_field)

                if button_next_generation.collidepoint(mouse_pos):
                    draw_field(cur_field)
                    cur_field = [[random.randint(0, 1) for i in range(M)] for j in range(N)]

                if button_die.collidepoint(mouse_pos):
                    for x in range(0, M):
                        for y in range(0, N):
                            cur_field[x][y] = 0

                    draw_field(cur_field)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:

                    next_state_field = get_next_generation(cur_field)
                    prev_field = deepcopy(cur_field)
                    cur_field = deepcopy(next_state_field)

                if event.type == pygame.K_LEFT:
                    cur_field = deepcopy(prev_field)
                    prev_field = deepcopy(cur_field)

                if event.key == pygame.K_SPACE:
                    for x in range(0, M):
                        for y in range(0, N):
                            cur_field[x][y] = 0

                draw_field(cur_field)

        pygame.display.flip()
        clock.tick(fps)


game_loop()
