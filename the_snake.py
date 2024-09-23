from random import randint, choice
from typing import List, Tuple, Optional
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: Tuple[int, int] = (0, -1)
DOWN: Tuple[int, int] = (0, 1)
LEFT: Tuple[int, int] = (-1, 0)
RIGHT: Tuple[int, int] = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Tuple[int, int, int] = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Tuple[int, int, int] = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Tuple[int, int, int] = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: Tuple[Tuple[int, int, int], ...] = (
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
        self.position: Tuple[int, int] = (
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color: Optional[Tuple[int, int, int]] = None

    def draw(self) -> None:
        """Просто абстрактный метод"""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self) -> None:
        """Случайным образом определяет новую позицию на игровом поле."""
        self.position = (
            randint(0, (SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
            randint(0, (SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE
        )

    def draw(self) -> None:
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
        direction (tuple): Текущее направление движения змеи.
        next_direction (tuple): Направление, в котором змея должна повернуть.
        body_color (tuple): Цвет тела змеи.
    """

    def __init__(self) -> None:
        super().__init__()
        self.length: int = 1
        self.positions: List[Tuple[int, int]] = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.last: Optional[Tuple[int, int]] = None
        self.body_color: Tuple[int, int, int] = choice(SNAKE_COLOR)

    def update_direction(self) -> None:
        """Обновляет направление движения змеи."""
        if self.next_direction:
            if (
                self.next_direction[0] * -1, self.next_direction[1] * -1
            ) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> Tuple[int, int]:
        """Метод который возвращает текущее положение головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Перемещает змею в новом направлении."""
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

        # Обновляем список позиций
        self.positions = [new_head] + self.positions[:self.length - 1]

    def reset(self) -> None:
        """Cброс змейки"""
        self.__init__()

    def grow(self) -> None:
        """Увеличивает длину змеи на 1."""
        self.body_color = choice(SNAKE_COLOR)
        self.length += 1
        self.positions.append(self.positions[-1])

    def draw(self) -> None:
        """Отрисовывает тело змеи на экране."""
        if not self.positions:
            return

        print("Рисуем змейку:", self.body_color)
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

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object: Snake) -> None:
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


def main() -> None:
    """Главная функция игры."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
