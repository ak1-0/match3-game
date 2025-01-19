import pygame
import random
import time

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
animations = []  # Хранение анимаций

# Хранение информации о выбранных квадратах
selected_square = None


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = grid[row][col]
            if color:  # Рисуем только, если значение не None
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


def check_matches():
    to_remove = set()

    # Проверяем горизонтальные совпадения
    for row in range(ROWS):
        for col in range(COLS - 2):  # Ограничиваем, чтобы не выходить за границы
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                to_remove.update([(row, col), (row, col + 1), (row, col + 2)])

    # Проверяем вертикальные совпадения
    for col in range(COLS):
        for row in range(ROWS - 2):  # Ограничиваем, чтобы не выходить за границы
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                to_remove.update([(row, col), (row + 1, col), (row + 2, col)])

    # Удаляем совпавшие квадратики
    return to_remove


def add_animation(row, col, action):
    """Добавление анимации для квадратиков."""
    animations.append({"row": row, "col": col, "action": action, "progress": 0})


def animate():
    global animations
    finished = True

    for animation in animations[:]:
        row, col = animation["row"], animation["col"]
        action = animation["action"]

        if grid[row][col] is None and action == "fade":
            animations.remove(animation)
            continue

        if action == "fade":
            alpha = 255 - int(255 * animation["progress"])
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            surface.set_alpha(alpha)
            surface.fill(grid[row][col])
            screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

        elif action == "fall":
            y_offset = int(SQUARE_SIZE * animation["progress"])
            if grid[row][col] is not None:
                pygame.draw.rect(
                    screen,
                    grid[row][col],
                    (col * SQUARE_SIZE, row * SQUARE_SIZE - y_offset, SQUARE_SIZE, SQUARE_SIZE),
                )

        animation["progress"] += 0.05
        if animation["progress"] >= 1:
            row, col = animation["row"], animation["col"]
            if animation["action"] == "fade":
                grid[row][col] = None
            animations.remove(animation)

    if animations:
        finished = False

    return finished


def fill_empty_spaces():
    for col in range(COLS):
        empty_spaces = [row for row in range(ROWS) if grid[row][col] is None]
        for empty_row in empty_spaces:
            for row in range(empty_row, 0, -1):
                grid[row][col] = grid[row - 1][col]
                add_animation(row, col, "fall")
            grid[0][col] = random.choice(COLORS)


def remove_single_match():
    """Удаляет только одну последовательность совпадений."""
    to_remove = check_matches()
    if not to_remove:
        return False  # Если совпадений нет, выходим

    # Берем только первую найденную группу совпадений
    first_match = set()
    first_color = None
    for row, col in to_remove:
        if first_color is None:
            first_color = grid[row][col]
        if grid[row][col] == first_color:
            first_match.add((row, col))

    for row, col in first_match:
        if grid[row][col] is not None:
            add_animation(row, col, "fade")
            # grid[row][col] = None  # Убираем изменение здесь

    return True


def main():
    global selected_square
    running = True
    state = "waiting"  # Текущее состояние игры
    last_remove_time = time.time()  # Время последнего удаления
    delay_between_removals = 0.5  # Задержка в секундах между удалениями

    while running:
        screen.fill((0, 0, 0))  # очищаем экран
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "waiting" and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = get_square_at((x, y))

                if selected_square is None:
                    selected_square = (row, col)
                else:
                    if (row, col) != selected_square:
                        swap_squares(selected_square, (row, col))
                        selected_square = None
                        state = "removing"
                    else:
                        selected_square = None

        # Управляем состояниями
        if state == "removing":
            # Ждем завершения анимации и добавляем задержку
            if animate() and time.time() - last_remove_time >= delay_between_removals:
                if remove_single_match():
                    last_remove_time = time.time()  # Обновляем время удаления
                else:
                    state = "falling"  # Переходим к падению после удаления всех совпадений

        elif state == "falling":
            if animate():  # Ждем завершения анимации падения
                fill_empty_spaces()
                if not check_matches():  # Если нет совпадений, ждем действия игрока
                    state = "waiting"
                else:
                    state = "removing"

        pygame.display.flip()


if __name__ == "__main__":
    main()