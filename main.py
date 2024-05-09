import pygame
import random
import math

pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Размеры утки и максимальное количество уток и промахов
TARGET_WIDTH = 80
TARGET_HEIGHT = 80
MAX_DUCKS = 7
MAX_MISSED_DUCKS = 5

# Начальные значения для утки и параметры движения
target_x = -TARGET_WIDTH
target_y = 0
target_y_start = SCREEN_HEIGHT // 2
amplitude = random.randint(50, 250)
frequency = 0.01

# Переменные для отслеживания статистики и состояния игры
ducks_shot = 0
ducks_missed = 0
score = 0
game_over = False
game_win = False

# Создание окна приложения
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра Утиная охота")

# Загрузка изображений
icon = pygame.image.load('img/duck_hunt.png')
pygame.display.set_icon(icon)
duck_image = pygame.image.load('img/duck.png')
cloud_image = pygame.image.load('img/cloud.png')
background_image = pygame.image.load('img/background.jpg').convert()
crosshair_image = pygame.image.load('img/crosshair.png').convert_alpha()
shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')


# Функция для обновления положения утки
def update_target():
    global target_x, target_y, target_y_start, amplitude, frequency, game_over, game_win

    if not game_over and not game_win:
        # Обновление координат утки в соответствии с движением
        target_x += 5  # Скорость движения утки
        target_y = target_y_start + amplitude * math.sin(frequency * target_x)

        # Проверка, если утка вышла за пределы экрана
        if target_x > SCREEN_WIDTH:
            # Перемещение утки в начало экрана со случайными параметрами
            target_x = -TARGET_WIDTH
            target_y_start = random.randint(SCREEN_HEIGHT // 4, 3 * SCREEN_HEIGHT // 4)
            amplitude = random.randint(50, 150)
            frequency = 0.005

        # Отрисовка утки на экране
        screen.blit(duck_image, (target_x, target_y))
    else:
        # Перемещение утки за пределы экрана, если игра окончена
        target_x = SCREEN_WIDTH

    return target_x, target_y


# Основная функция игры
def main():
    global target_x, target_y_start, amplitude, frequency, ducks_shot, ducks_missed, score, game_over, game_win
    running = True
    clock = pygame.time.Clock()
    duck_hit = False  # Флаг для отслеживания попадания в утку
    font = pygame.font.Font(None, 36)  # Шрифт для отображения текста

    pygame.mouse.set_visible(False)  # Скрываем системный курсор

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and not game_win:
                    # Воспроизведение звука выстрела при клике мыши
                    pygame.mixer.Sound.play(shoot_sound)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    target_pos = update_target()
                    # Проверка попадания по утке
                    if target_pos[0] <= mouse_x <= target_pos[0] + TARGET_WIDTH and \
                            target_pos[1] <= mouse_y <= target_pos[1] + TARGET_HEIGHT:
                        duck_hit = True
                        # Отображение облака при попадании
                        screen.blit(cloud_image, (target_pos[0], target_pos[1]))
                        pygame.display.flip()
                        pygame.time.wait(500)  # Ожидание 0.5 секунды
                        score += 100  # Увеличение счета при попадании
                        ducks_shot += 1
                    else:
                        score -= 50  # Уменьшение счета при промахе

        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(background_image, (0, 0))  # Отображение фона

        if not game_over:
            if not duck_hit:
                update_target()  # Обновление положения утки, если она не была убита
                if target_x == -TARGET_WIDTH:  # Проверка, если утка вышла за пределы экрана
                    ducks_missed += 1
                    if ducks_missed >= MAX_MISSED_DUCKS:
                        game_over = True  # Установка флага окончания игры
            else:
                duck_hit = False  # Сброс флага попадания
                # Сброс параметров для появления новой утки
                target_x = -TARGET_WIDTH
                target_y_start = random.randint(SCREEN_HEIGHT // 4, 3 * SCREEN_HEIGHT // 4)
                amplitude = random.randint(50, 150)
                frequency = 0.005

            # Отображение счета
            text = font.render("Очки: {}".format(score), True, (255, 165, 0))  # Огненно-оранжевый цвет
            screen.blit(text, (10, 10))

            # Отображение курсора прицела
            screen.blit(crosshair_image,
                        (mouse_x - crosshair_image.get_width() // 2, mouse_y - crosshair_image.get_height() // 2))

        # Проверка условия победы
        if ducks_shot + ducks_missed >= MAX_DUCKS:
            game_win = True  # Установка флага победы

        # Вывод сообщения об окончании игры
        if game_over:
            text = font.render(f"Вы упустили {MAX_MISSED_DUCKS} уток. Вы проиграли!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.mouse.set_visible(True)  # Сделаем курсор видимым снова

        elif game_win:
            text = font.render("Вы выиграли. Очки: {}".format(score), True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.mouse.set_visible(False)  # Сделаем курсор видимым снова

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
