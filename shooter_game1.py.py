import pygame
from pygame import sprite, transform, image, key, event, display, font, mixer
from random import randint
from pygame.locals import *

pygame.init()
font.init()

font1 = font.SysFont(None, 80)
font2 = font.SysFont(None, 36)

win = font1.render("YOU WIN!", True, (255, 255, 255))
lose_text = font1.render("YOU LOSE!", True, (180, 0, 0))

score = 0
lose = 0
goal = 10
max_lose = 5

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

win_width = 700
win_height = 500

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # Ensure size_x and size_y are positive
        size_x = max(1, size_x)
        size_y = max(1, size_y)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            lose += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(50, win_width - 50), 40, 50, 50, randint(1, 5))
    monsters.add(monster)

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

bullets = sprite.Group()
player = Player('rocket.png', 0, 425, 80, 100, 10)

game = True
finish = False
clock = pygame.time.Clock()
FPS = 60

fire_sound = mixer.Sound("fire.ogg")

while game:
    for e in event.get():
        if e.type == pygame.QUIT:
            game = False
        elif e.type == pygame.KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if not finish:
        window.blit(background, (0, 0))
        player.update()
        player.reset(window)
        monsters.update()
        bullets.update()

        monsters.draw(window)
        bullets.draw(window)

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (20, 10))
        text_lose = font2.render("Missed: " + str(lose), 1, (255, 255, 255))
        window.blit(text_lose, (20, 40))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 50, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or lose >= max_lose:
            finish = True
            window.blit(lose_text, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
    else:
        finish = False
        score = 0
        lose = 0
        bullets.empty()
        monsters.empty()
        for i in range(1, 6):
            monster = Enemy("ufo.png", randint(50, win_width - 50), 40, 50, 50, randint(1, 5))
            monsters.add(monster)
        pygame.time.delay(3000)

    display.update()
    clock.tick(FPS)

pygame.quit()
