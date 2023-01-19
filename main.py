import pygame
import os
import sys
import random
WIDTH = 800
HEIGHT = 600
PLAYER_HEALTH = 100
MOVE_EVENT_TIME = 120
SPAWN_TIME = 1600
DMG = 20
WAVES = 5
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('doomed')


def load_image(name, colorkey=None):
    fullname = os.path.join('img_files', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


skul = load_image('skul.png')
pygame.display.set_icon(skul)


class HP_bar(pygame.sprite.Sprite):
    bars = [load_image('hp_bar/health_bar10.png'), load_image('hp_bar/health_bar9.png'),
            load_image('hp_bar/health_bar8.png'), load_image('hp_bar/health_bar7.png'),
            load_image('hp_bar/health_bar6.png'), load_image('hp_bar/health_bar5.png'),
            load_image('hp_bar/health_bar4.png'), load_image('hp_bar/health_bar3.png'),
            load_image('hp_bar/health_bar2.png'), load_image('hp_bar/health_bar1.png')
            ]

    def __init__(self):
        super().__init__()
        self.index = 0
        self.hp_status = HP_bar.bars
        self.image = self.hp_status[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        if self.index == len(self.hp_status):
            self.index -= 1
        self.image = self.hp_status[self.index]


hp = HP_bar()


class Title(pygame.sprite.Sprite):
    titl = load_image('title.png')

    def __init__(self):
        super().__init__()
        self.image = Title.titl
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.x = 1000


class Gun(pygame.sprite.Sprite):
    gun_frames = [load_image('shoot_frames/003.png'), load_image('shoot_frames/004.png'),
                  load_image('shoot_frames/005.png'), load_image('shoot_frames/006.png'),
                  load_image('shoot_frames/007.png'), load_image('shoot_frames/008.png'),
                  load_image('shoot_frames/009.png')
                  ]

    def __init__(self, x):
        super().__init__()
        self.health = PLAYER_HEALTH
        self.hurt = False
        self.shooting = False
        self.index = 0
        self.shoot_frame = Gun.gun_frames
        self.image = self.shoot_frame[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 320

    def update(self):
        self.image = self.shoot_frame[self.index]
        self.index += 1
        if self.index == len(self.shoot_frame):
            self.index = 0
            self.shooting = False
        self.image = self.shoot_frame[self.index]


gun = Gun(300)


class Enemy(pygame.sprite.Sprite):
    guys = [
            load_image('attack_frames/7.png'), load_image('attack_frames/9.png'),
            load_image('attack_frames/11.png'), load_image('attack_frames/13.png')]
    attack = [load_image('attack_frames/1.png'), load_image('attack_frames/2.png'),
              load_image('attack_frames/3.png'), load_image('attack_frames/4.png'),
              load_image('attack_frames/5.png'), load_image('attack_frames/6.png')]
    explode = [load_image('enemy_explode/013.png'), load_image('enemy_explode/012.png'),
               load_image('enemy_explode/011.png'), load_image('enemy_explode/010.png'),
               load_image('enemy_explode/009.png'), load_image('enemy_explode/008.png'),
               load_image('enemy_explode/007.png'), load_image('enemy_explode/006.png'),
               load_image('enemy_explode/005.png'), load_image('enemy_explode/004.png'),
               load_image('enemy_explode/003.png'), load_image('enemy_explode/002.png'),
               load_image('enemy_explode/001.png'), load_image('enemy_explode/000.png'),
               load_image('enemy_explode/0.png')]
    dead = load_image('dead.gif')

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.walk = True
        self.attack = False
        self.death = False
        self.index = 3
        self.walk_frames = []
        self.attack_frames = Enemy.attack
        self.explode = Enemy.explode
        self.walk_frames.extend(Enemy.guys)
        self.image = self.walk_frames[self.index]
        self.image_dead = Enemy.dead
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100
        self.size = -20

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and not self.death:
            self.health -= DMG
            if self.health <= 0:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('img_files/imp_dead.wav'))
                self.death = True
                self.walk = False
                self.attack = False
                self.index = 0
        if self.walk and not args and not self.death:
            self.image = self.walk_frames[self.index]
            self.image = pygame.transform.scale(self.image, (self.image.get_height() + self.size,
                                                             self.image.get_width() + self.size))
            self.rect = self.image.get_rect()
            self.rect.x = self.x - self.size / 2
            self.rect.y = self.y
            self.size += 10
            self.index += 1
            if self.index >= len(self.walk_frames):
                self.index = 0
            if self.size > 200:
                self.walk = False
                self.attack = True
                self.index = 0

        if self.attack and not args:
            self.image = self.attack_frames[self.index]
            self.image = pygame.transform.scale(self.image, (self.image.get_height() + self.size,
                                                             self.image.get_width() + self.size))
            self.index += 1
            if self.index == len(self.attack_frames):
                self.index = 0
                gun.health -= 10
                hp.index += 1
                hp.update()
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('img_files/player_hurt.wav'))
            self.rect = self.image.get_rect()
            self.rect.y = self.y
            self.rect.x = self.x
        if self.death and not args:
            self.image = pygame.transform.scale(self.explode[self.index], (self.image.get_height() + self.size / 2,
                                                             self.image.get_width() + self.size / 2))
            if self.index == len(self.explode) - 1:
                self.kill()
            self.index += 1


pause_screen = pygame.font.Font(None, 100)
titlescreen = Title()
geym = load_image('gay_over.png')
background = load_image('backdrop.webp')
crosshair = load_image('crosshair.png')
crosshair = pygame.transform.scale(crosshair, (50, 50))
enemies = pygame.sprite.Group()

splats = pygame.sprite.Group()
enemy_draw = []
clock = pygame.time.Clock()
FPS = 60
running = True
MOVE_EVENT = pygame.USEREVENT+1
ENEMY_SPAWN = pygame.USEREVENT+2
WAVE = pygame.USEREVENT+3
pygame.time.set_timer(WAVE, 3000)
pygame.time.set_timer(MOVE_EVENT, MOVE_EVENT_TIME)
pygame.time.set_timer(ENEMY_SPAWN, SPAWN_TIME)
gun.shooting = False
pause = False
gamover = False
title = True
while running:
    while title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                title = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                titlescreen.update(event)
                title = False
                guy = Enemy(100, 120)
                enemies.add(guy)
                enemy_draw.append(guy)
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('img_files/ost.mp3'), loops=-1)
            screen.blit(titlescreen.image, (0, 0))
            pygame.display.update()
            pygame.display.flip()

    screen.blit(background, (0, -200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == WAVE:
            if WAVES > 0:
                SPAWN_TIME -= 200
                MOVE_EVENT_TIME -= 25
                WAVES -= 1

        if event.type == MOVE_EVENT:
            enemies.update()
        if event.type == ENEMY_SPAWN:
            enemy = Enemy(random.randrange(-20, 500), 120)
            enemies.add(enemy)
            enemy_draw.append(enemy)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            gun.shooting = True
            pygame.mixer.music.load('img_files/shoot_sound.mp3')
            pygame.mixer.music.play(0)
            for guy in enemies:
                enemies.update(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pause = True
            pygame.mixer.Channel(2).pause()
    if gun.health <= 0:
        gamover = True
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('img_files/fail.mp3'))
    while gamover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamover = False
                running = False
        screen.blit(geym, (0, 0))
        pygame.display.update()
        pygame.display.flip()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pause = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = False
                pygame.mixer.Channel(2).unpause()
        for imp in enemy_draw[::-1]:
            screen.blit(imp.image, (imp.rect.x, imp.rect.y))
        screen.blit(gun.image, (gun.rect.x, gun.rect.y))
        screen.blit(hp.image, (340, 10))
        screen.blit(pause_screen.render('PAUSED', True, (225, 255, 255)), (260, 220))
        pygame.display.update()
        pygame.display.flip()

    if gun.shooting:
        gun.update()
    splats.update()
    clock.tick(FPS)
    for imp in enemy_draw[::-1]:
        screen.blit(imp.image, (imp.rect.x, imp.rect.y))
    screen.blit(gun.image, (gun.rect.x, gun.rect.y))
    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_focused():
        screen.blit(crosshair, (x - 25, y - 25))
        gun.rect.x = x - 120
    screen.blit(hp.image, (340, 10))
    pygame.display.update()
    pygame.display.flip()
