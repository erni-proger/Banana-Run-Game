import os
import sys
import random

import pygame

WIDTH, HEIGHT = 1200, 600

# группы спрайтов
all_sprites = pygame.sprite.Group()
grounds = pygame.sprite.Group()
heroes = pygame.sprite.Group()
mouse_sprite = pygame.sprite.Group()
buttons = pygame.sprite.Group()
bananas = pygame.sprite.Group()


# путь к картинке
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


path = resource_path(os.path.join('data', 'monkeyface.ico'))
pygame.display.set_icon(pygame.image.load(path))

path = resource_path(os.path.join('data', 'monkey.png'))
hero_image = pygame.transform.scale(pygame.image.load(path), (40, 50))

path = resource_path(os.path.join('data', 'ground.png'))
ground_image = pygame.image.load(path)

path = resource_path(os.path.join('data', 'tree.jpg'))
tree_image = pygame.image.load(path)

backgrounds = []

path = resource_path(os.path.join('data', 'back1.jpg'))
back1_image = pygame.image.load(path)
backgrounds.append(pygame.transform.scale(back1_image, (WIDTH, HEIGHT)))

path = resource_path(os.path.join('data', 'back2.jpg'))
back2_image = pygame.image.load(path)
backgrounds.append(pygame.transform.scale(back2_image, (WIDTH, HEIGHT)))

path = resource_path(os.path.join('data', 'back3.png'))
back3_image = pygame.image.load(path)
backgrounds.append(pygame.transform.scale(back3_image, (WIDTH, HEIGHT)))

path = resource_path(os.path.join('data', 'menu.jpg'))
menu_image = pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))

path = resource_path(os.path.join('data', 'menu2.png'))
menu2_image = pygame.transform.scale(pygame.image.load(path), (int(WIDTH / 3), 350))


def terminate():
    pygame.quit()
    sys.exit()


# веревка
def rope(x_hero, y_hero, x, y):
    pygame.draw.line(screen, (0, 150, 0), [x_hero + 15, y_hero + 5], [x, y], 3)
    length = (((x - x_hero) ** 2) + (y - y_hero) ** 2) ** 0.5
    return length - 0.5


# создание уровня
def update_lvl():
    for i in range(len(down)):
        down[i].new()
        up[i].new()
        bananas_lvl[i].new((up[i].get_y()[0], down[i].get_y()[1]))
        if random.randint(0, 10) >= 3:
            bananas_lvl[i].delete()


def menu(*args):
    global start
    if not start:
        screen.blit(menu_image, (0, 0))
        for i in range(3):
            screen.blit(menu2_image, (i * int(WIDTH / 3), 0))
        buttons.draw(screen)
        if args[0].type == pygame.MOUSEBUTTONDOWN:
            if pygame.sprite.spritecollideany(mouse, buttons):
                start = True


def show_scores(scores, record):
    fontSize = 40
    myFont = pygame.font.SysFont('Calibri', fontSize)
    text = str(f'scores: {scores}')
    text2 = str(f'record: {record}')
    fontImage = myFont.render(str(text), 9, (255, 255, 0))
    fontImage2 = myFont.render(str(text2), 9, (255, 255, 0))
    screen.blit(fontImage, (0, 0))
    screen.blit(fontImage2, (0, fontSize))


# кнопка
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(all_sprites)
        self.size = w, h
        self.path = resource_path(os.path.join('data', "start.png"))
        self.image = pygame.transform.scale(pygame.image.load(self.path), self.size)
        self.rect = self.image.get_rect()
        self.add(buttons)
        self.rect.x = x
        self.rect.y = y


# мышка
class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.add(mouse_sprite)
        self.rect.x = 0
        self.rect.y = 0

    def posit(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]


# земля
class Ground(pygame.sprite.Sprite):
    def __init__(self, down, x):
        super().__init__(all_sprites)
        self.down = down
        self.x = x
        self.size = 60, random.randrange(10, 230)
        self.image = pygame.transform.scale(tree_image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x * self.size[0]
        self.rect.y = 0
        if self.down is True:
            self.rect.y = HEIGHT - self.size[1]
            self.image = pygame.transform.scale(ground_image, self.size)
        self.add(grounds)

    def new(self):
        self.size = 60, random.randrange(10, 230)
        self.image = pygame.transform.scale(tree_image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * self.size[0]
        self.rect.y = 0
        if self.down is True:
            self.rect.y = HEIGHT - self.size[1]
            self.image = pygame.transform.scale(ground_image, self.size)

    def get_y(self):
        return self.size[1], self.rect.y


# банан
class Banana(pygame.sprite.Sprite):
    def __init__(self, x, limits):
        super().__init__(all_sprites)
        self.x = x
        self.path = resource_path(os.path.join('data', "banana.png"))
        self.image = pygame.transform.scale(pygame.image.load(self.path), (80, 40))
        self.rect = self.image.get_rect()
        self.rect.x = self.x * 60 - 10
        self.rect.y = random.randrange(limits[0] + 50, limits[1] - 50)
        self.add(bananas)

    def new(self, limits):
        self.image = pygame.transform.scale(pygame.image.load(self.path), (80, 40))
        self.rect = self.image.get_rect()
        self.rect.x = self.x * 60 - 10
        self.rect.y = random.randrange(limits[0] + 50, limits[1] - 50)

    def delete(self):
        self.image = pygame.Surface((0, 0))
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        global scores
        global record
        if pygame.sprite.spritecollideany(self, heroes):
            scores += 10
            if scores > record:
                record = scores
            self.delete()


# герой
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = hero_image
        self.rect = self.image.get_rect()
        self.add(heroes)
        self.rect.x = 50
        self.rect.y = 250
        self.v = 0
        self.direction = False
        self.m_pos = (WIDTH, 0)
        self.phys_on = False

    def change_dir(self, *args):
        # проверяем направление
        if args[0].type == pygame.KEYDOWN:
            if args[0].key == pygame.K_SPACE:
                self.phys_on = True
                if self.rect.x < self.m_pos[0]:
                    self.direction = False
                else:
                    self.direction = True

    def update(self, *args):
        global start
        global scores
        # проверка коллизии
        if pygame.sprite.spritecollideany(self, grounds):
            start = False
            self.rect.x = 50
            self.rect.y = 250
            self.phys_on = False
            scores = 0

        # физика
        if self.phys_on:
            if rope_on:
                self.m_pos = pygame.mouse.get_pos()
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE]:

                    # высчитываем длину
                    if not self.direction:
                        self.rect.x += self.v
                        length = rope(self.rect.x - self.v, self.rect.y, self.m_pos[0],
                                      self.m_pos[1])
                    else:
                        self.rect.x -= self.v
                        length = rope(self.rect.x + self.v, self.rect.y, self.m_pos[0],
                                      self.m_pos[1])

                    # вычисляем скорость
                    self.v = (length - abs(self.rect.x - self.m_pos[0]) + 3) * 0.14

                    # высчитываем y
                    try:
                        y = ((length ** 2) - (self.rect.x - self.m_pos[0]) ** 2) ** 0.5 + \
                            self.m_pos[1]
                        self.rect.y = y
                    except TypeError:
                        self.direction = not self.direction

            self.rect.y += 2

        # переход уровня
        if self.rect.x > WIDTH:
            self.rect.x = 50
            self.rect.y = 250
            self.phys_on = False
            return True


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Banana Run')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    fps = 25
    n = 0
    up = []
    down = []
    bananas_lvl = []
    # создаем героя
    hero = Hero()
    mouse = Mouse()

    scores = 0
    record = 0

    # создаем уровень
    for i in range(20):
        down.append(Ground(True, i))
        up.append(Ground(False, i))
        bananas_lvl.append(Banana(i, (up[i].get_y()[0], down[i].get_y()[1])))
        if random.randint(0, 10) >= 3:
            bananas_lvl[i].delete()

    start = False
    button = Button(WIDTH / 2 - 150, HEIGHT / 2, 400, 300)

    # игровой цикл
    while running:
        rope_on = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            hero.change_dir(event)

        pos = pygame.mouse.get_pos()
        mouse.posit(pos)

        menu(event)

        if start:
            if pygame.sprite.spritecollideany(mouse, grounds):
                rope_on = True

            screen.blit(backgrounds[n], (0, 0))

            grounds.draw(screen)
            heroes.draw(screen)
            bananas.draw(screen)
            show_scores(scores, record)
            bananas.update()
            if hero.update(event):
                update_lvl()
                n += 1
            if n == 3:
                n = 0

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()
