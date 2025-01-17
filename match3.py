import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры игры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 8  # Размер сетки
TILE_SIZE = 50  # Размер каждой плитки
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Список цветов для плиток
COLORS = [BLUE, RED, GREEN, YELLOW]

# Экран игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Match 3 Game")

# Игровая сетка (матрица)
grid = [[random.choice(COLORS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = grid[y][x]
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

def find_matches():
    matches = []
    # Проверка строк на совпадения
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y][x + 1] == grid[y][x + 2]:
                matches.append(((y, x), (y, x + 1), (y, x + 2)))

    # Проверка столбцов на совпадения
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y + 1][x] == grid[y + 2][x]:
                matches.append(((y, x), (y + 1, x), (y + 2, x)))

    return matches

def remove_matches(matches):
    for match in matches:
        for (y, x) in match:
            grid[y][x] = random.choice(COLORS)

def game_loop():
    clock = pygame.time.Clock()

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Поиск совпадений
        matches = find_matches()
        if matches:
            remove_matches(matches)

        # Отображение
        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()