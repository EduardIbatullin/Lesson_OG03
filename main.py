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
target_width = 80  # ширина картинки цели
target_height = 80  # высота картинки цели

target_x = random.randint(0, SCREEN_WIDTH - target_width)  # координаты цели по оси X
target_y = random.randint(0, SCREEN_HEIGHT - target_height)  # координаты цели по оси Y

color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # цвет фона окна

# цикл обработки событий игры
running = True
while running:
    screen.fill(color)  # заливка фона окна цвет
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # если нажали на крестик
            running = False  # выход из цикла обработки событий игры
        elif event.type == pygame.MOUSEBUTTONDOWN:  # если нажали на мышь
            mouse_x, mouse_y = pygame.mouse.get_pos()  # координаты курсора
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                target_x = random.randint(0, SCREEN_WIDTH - target_width)  # координаты цели по оси X изменились
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)  # координаты цели по оси Y изменились
    screen.blit(target_image, (target_x, target_y))  # вывод картинки цели на экран
    pygame.display.update()  # обновление экрана

pygame.quit()
