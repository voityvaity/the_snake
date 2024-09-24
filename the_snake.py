from random import randint, choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: tuple[int, int] = (0, -1)
DOWN: tuple[int, int] = (0, 1)
LEFT: tuple[int, int] = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR: tuple[int, int, int] = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR: tuple[int, int, int] = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR: tuple[tuple[int, int, int], ...] = (
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (255, 165, 0),
    (255, 20, 147),
    (0, 255, 255),
    (128, 0, 128)
)

# Скорость движения змейки:
SPEED: int = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для всех игровых объектов.

    Атрибуты:
        position (tuple): Позиция объекта на экране (координаты x и y).
        body_color (tuple): Цвет объекта, представленный в формате RGB.
    """

    def __init__(self) -> None:
        self.position: tuple[int, int] = (
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        )
        self.body_color: tuple[int, int, int] | None = None

    def draw(self):
        """
        Просто обстрактный метод.
        Метод для рисования предметов.
        Должен быть переопределен в подклассе.
        """
        raise NotImplementedError(
            "Метод 'draw' должен быть переопределен в дочернем классе.")


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self) -> None:
        """
        Инициализирует объект с начальной позицией.
        В центре экрана и без цвета.
        """
        super().__init__()
        self.body_color: tuple[int, int, int] = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Случайным образом определяет новую позицию на игровом поле."""
        self.position = (
            randint(0, (SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
            randint(0, (SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко на экране в текущей позиции."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, представляющий змею в игре.

    Атрибуты:
        length (int): Длина змеи.
        positions (list): Список координат (кортежей), представляющих тело.
        direction (str): Текущее направление движения змеи.
        next_direction (str): Направление, в котором змея должна повернуть.
        body_color (tuple): Цвет тела змеи.
    """

    def __init__(self) -> None:
        """
        Инициализирует змею с длиной 1.
        Начальной позицией в центре экрана и направлением вправо.
        """
        super().__init__()
        self.reset()
        self.last: tuple[int, int] | None = None
        self.body_color: tuple[int, int, int] = choice(SNAKE_COLOR)

    def reset(self):
        """Метод сброса"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змеи."""
        if self.next_direction:
            if (self.next_direction[0] * -1,
                    self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """
        Метод который возвращает текущее положение головы змейки.
        Первый элемент в списке positions.
        """
        return self.positions[0]

    def move(self):
        """
        Перемещает змею в новом направлении.
        Сбрасывает, если змея сталкивается с собой.
        """
        current_head = self.get_head_position()

        new_head = (
            current_head[0] + self.direction[0] * GRID_SIZE,
            current_head[1] + self.direction[1] * GRID_SIZE
        )

        new_x = new_head[0] % SCREEN_WIDTH
        new_y = new_head[1] % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверяем столкновение с собой
        if new_head in self.positions[1:]:
            print("Змейка столкнулась с собой")
            self.reset()
            return

        # Обновляем список позиций: добавляем новую голову
        self.positions = [new_head] + self.positions[:self.length - 1]

    def grow(self):
        """Увеличивает длину змеи на 1, добавляя новый сегмент в конец."""
        self.body_color = choice(SNAKE_COLOR)
        self.length += 1
        self.positions.append(self.positions[-1])

    def draw(self):
        """Отрисовывает тело змеи на экране."""
        if not self.positions:
            return  # Если список пуст, ничего не рисуем

        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и обновляет направление движения змеи."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Главная функция игры.
    Инициализирует игровые объекты и запускает основной игровой цикл.
    """
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:

        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.grow()  # Увеличиваем длину змейки
            apple.randomize_position()  # Перемещаем яблоко

        # Отрисовываем объекты
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
