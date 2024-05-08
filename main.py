import pygame
import random
import math

pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_WIDTH = 80
TARGET_HEIGHT = 80

# Загрузка изображений
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра Утиная охота")
icon = pygame.image.load('img/duck_hunt.png')
pygame.display.set_icon(icon)
duck_image = pygame.image.load('img/duck.png')
cloud_image = pygame.image.load('img/cloud.png')  # Изображение облака перьев

# Начальные параметры цели
target_x = -TARGET_WIDTH
target_y_start = SCREEN_HEIGHT // 2
amplitude = random.randint(50, 250)
frequency = 0.01

# Загрузка изображения фона
background_image = pygame.image.load('img/background.jpg').convert()

# Установка курсора прицела
pygame.mouse.set_visible(False)  # Скрываем стандартный курсор
crosshair_image = pygame.image.load('img/crosshair.png').convert_alpha()

# Звук выстрела
shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')


def update_target():
    global target_x, target_y_start, amplitude, frequency

    target_x += 5
    target_y = target_y_start + amplitude * math.sin(frequency * target_x)

    if target_x > SCREEN_WIDTH:
        target_x = -TARGET_WIDTH
        target_y_start = random.randint(SCREEN_HEIGHT // 4, 3 * SCREEN_HEIGHT // 4)
        amplitude = random.randint(50, 150)
        frequency = 0.005

    screen.blit(duck_image, (target_x, target_y))

    return (target_x, target_y)


def main():
    global target_x, target_y_start, amplitude, frequency
    running = True
    clock = pygame.time.Clock()
    duck_hit = False  # Флаг для отслеживания попадания в утку
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(shoot_sound)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                target_pos = update_target()
                if target_pos[0] <= mouse_x <= target_pos[0] + TARGET_WIDTH and \
                        target_pos[1] <= mouse_y <= target_pos[1] + TARGET_HEIGHT:
                    duck_hit = True  # Установка флага, если утка была убита
                    screen.blit(cloud_image, (target_pos[0], target_pos[1]))
                    pygame.display.flip()
                    pygame.time.wait(1000)  # Ожидание 1 секунды

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(background_image, (0, 0))  # Отрисовываем фон
        if not duck_hit:
            update_target()  # Обновление положения утки, если она не была убита
        else:
            duck_hit = False  # Сброс флага
            target_x = -TARGET_WIDTH  # Сброс позиции утки для появления новой с левого края экрана
            target_y_start = random.randint(SCREEN_HEIGHT // 4, 3 * SCREEN_HEIGHT // 4)
            amplitude = random.randint(50, 150)
            frequency = 0.005

        screen.blit(crosshair_image,
                    (mouse_x - crosshair_image.get_width() // 2, mouse_y - crosshair_image.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
