import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры экрана и поля
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Цвета для кубиков
COLORS = [BLUE, RED, GREEN, YELLOW]

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match 3")

# Сетка для игры
grid = [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

# Хранение информации о выбранных квадратах
selected_square = None


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = grid[row][col]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)


def get_square_at(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col


def swap_squares(pos1, pos2):
    row1, col1 = pos1
    row2, col2 = pos2
    grid[row1][col1], grid[row2][col2] = grid[row2][col2], grid[row1][col1]


def main():
    global selected_square
    running = True
    while running:
        screen.fill((0, 0, 0))  # очищаем экран
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = get_square_at((x, y))

                if selected_square is None:
                    # Если ничего не выбрано, выбрали первый квадрат
                    selected_square = (row, col)
                else:
                    # Если уже есть выбранный квадрат, пробуем поменять местами
                    if (row, col) != selected_square:
                        swap_squares(selected_square, (row, col))
                    # Сбросить выбранный квадрат после обмена
                    selected_square = None

        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()