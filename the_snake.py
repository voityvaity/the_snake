from random import randint, choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для всех игровых объектов.

    Атрибуты:
        position (tuple): Позиция объекта на экране (координаты x и y).
        body_color (tuple): Цвет объекта, представленный в формате RGB.
    """

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        # Не вижу причин не удалять self.body_color.
        self.body_color = None

    def draw(self):
        """По идеи все общие элементы подклассов я могу написать тута"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self) -> None:
        """
        Инициализирует объект с начальной позицией.
        В центре экрана и без цвета.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Случайным образом определяет новую позицию на игровом поле."""
        self.position = (
            randint(0, (SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
            randint(0, (SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE)
        # b = None  # Инициализация b
        # a = None
        # active = True

        # while active:
        #     b = randint(1, SCREEN_HEIGHT)
        #     a = randint(1, SCREEN_WIDTH) # Генерация числа
        #     if b % 20 == 0 and a % 20 == 0:  # Проверка, делится число на 20
        #         active = False  # Завершение цикла, если условие выполнено
        # self.position = (a, b)

    def draw(self):
        """Отрисовывает яблоко на экране в текущей позиции."""
        super().draw()


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
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        # Список цветов для змейки
        self.colors = [
            (0, 255, 0),
            (255, 255, 0),
            (0, 0, 255),
            (255, 0, 255),
            (255, 165, 0),
            (255, 20, 147),
            (0, 255, 255),
            (128, 0, 128)
        ]
        self.body_color = choice(self.colors)  # Случайный стартовый цвет

    def update_direction(self):
        """Обновляет направление движения змеи."""
        if self.next_direction:
            if (self.next_direction[0] * -1,
                    self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змеи"""
        # Метод который возвращает текущее положение
        # головы змейки (первый элемент в списке positions).
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

        # Перемещаем голову змейки на противоположную сторону,
        # если вышла за границу
        new_x = new_head[0] % SCREEN_WIDTH
        new_y = new_head[1] % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверяем столкновение с собой
        if new_head in self.positions[1:]:
            print("Snake collided with itself, resetting...")
            self.reset()
            return

        # Обновляем список позиций: добавляем новую голову
        self.positions = [new_head] + self.positions[:self.length - 1]

    def grow(self):
        """Увеличивает длину змеи на 1, добавляя новый сегмент в конец."""
        self.body_color = choice(self.colors)
        self.length += 1
        self.positions.append(self.positions[-1])

    def draw(self):
        """Отрисовывает тело змеи на экране."""
        if not self.positions:
            return  # Если список пуст, ничего не рисуем

        print("Рисуем змейку:", self.body_color)  # Отладка
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

    def reset(self):
        """Сбрасывает параметры змеи к начальному состоянию."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


# Функция обработки действий пользователя


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

# Метод обновления направления после нажатия на кнопку


def main():
    """
    Главная функция игры.
    Инициализирует игровые объекты и запускает основной игровой цикл.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
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
