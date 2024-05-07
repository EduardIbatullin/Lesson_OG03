
import pygame
import random


pygame.init()  # инициализация PyGame


SCREEN_WIDTH = 800  # ширина экрана
SCREEN_HEIGHT = 600  # высота экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # размеры экрана


pygame.display.set_caption("Игра Тир")  # заголовок окна
icon = pygame.image.load('img/duck_hunt.png')  # иконка окна
pygame.display.set_icon(icon)  # иконка окна


target_image = pygame.image.load('img/target.png')  # картинка цели
target_width = 50  # ширина картинки цели
target_height = 50  # высота картинки цели


target_x = random.randint(0, SCREEN_WIDTH - target_width)  # координаты цели по оси X
target_y = random.randint(0, SCREEN_HEIGHT - target_height)  # координаты цели по оси Y


color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # цвет фона окна


# цикл обработки событий игры
running = True
while running:
    pass


pygame.quit()
