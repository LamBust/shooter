from pygame import *
import random
import time as tm

font.init()
font = font.SysFont('Arial', 65)

win_width = 1200
win_height = 675

window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
display.set_caption('shooter')

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

hero_height = 100
hero_width = 100
hero_x = 500
hero_y = win_height - hero_height - 10
reloadind_time = 1

enemy_height = 100
enemy_width = 100

asteroid_height = 100
asteroid_width = 100
asteroid_speed = 2

bullet_height = 25
bullet_width = 25
bullet_speed = 6

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_height, player_width))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y
        self.height = player_width
        self.width = player_height
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))          

class Bullet(GameSprite):
    def update(self):
        if self.rect.y > + 5:
            self.rect.y -= self.speed
        else:
            self.kill()

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height, reloadind_time):
        super().__init__(player_image, player_x, player_y, player_speed, player_width, player_height)
        self.time = tm.time()
        self.total_shots = 0
        self.reloadind_time = reloadind_time
    def update(self, keys):
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - self.width - 10:
            self.rect.x += self.speed
    def fire(self, keys):
        if keys[K_SPACE]:
            if self.total_shots < 5:
                if tm.time() - self.time > 0.1:
                    bullet = Bullet('bullet.png', self.rect.centerx - 12, self.rect.top, bullet_speed, bullet_height, bullet_width)
                    bullets.add(bullet)
                    self.total_shots += 1
                self.time = tm.time()
            else:
                if tm.time() - self.time >= self.reloadind_time:
                    self.total_shots = 0
        if self.total_shots >= 5 and tm.time() - self.time < self.reloadind_time:
            reload_text = font.render('Перезарядка. Осталось: ' + str(round((self.reloadind_time - (tm.time() - self.time)), 2)), 1, (255, 255, 255))
            window.blit(reload_text, (100, win_height - 50))

class Enemy(GameSprite):
    def update(self):
        global skipped
        if self.rect.y < win_height + self.height + 10:
            self.rect.y += self.speed
        else:
            self.rect.y =  -self.height - 10
            self.rect.x = random.randint(10, win_width - self.width - 10)
            skipped += 1

class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_height):
        super().__init__(player_image, player_x, player_y, player_speed, player_width, player_height)
        self.time = tm.time()
        self.allow = True
    def update(self):
        if self.rect.y < win_height + self.height + 10:
            self.rect.y += self.speed
        else:
            self.rect.y =  -self.height - 10
            self.rect.x = random.randint(10, win_width - self.width - 10)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png', random.randint(10, win_width - asteroid_width - 10), -enemy_height -10, asteroid_speed, asteroid_height, asteroid_width)
    asteroids.add(asteroid)

monsters = sprite.Group()
for i in range(6):
    monster = Enemy('ufo.png', random.randint(10, win_width - enemy_width - 10), -enemy_height -10, random.randint(1, 6), enemy_height, enemy_width)
    monsters.add(monster)

bullets = sprite.Group()

player = Player('rocket.png', hero_x, hero_y, 10, hero_height, hero_width, reloadind_time) 

clock = time.Clock()
FPS = 60

win_text = font.render('Вы выиграли!', 1, (0, 255, 0))
lose_text = font.render('Вы програли.', 1, (255, 0, 0))
draw_text = font.render('Ничья', 1, (255, 255, 0))

hp_3 = font.render('3', 1, (255, 255, 255))
hp_2 = font.render('2', 1, (0, 255, 0))
hp_1 = font.render('1', 1, (255, 255, 0))
hp_0 = font.render('0', 1, (255, 0, 0))

skipped = 0
killed = 0
lifes = 3

allow = True
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    text_skip = font.render('Пропущено: ' + str(skipped), 1, (255, 255, 255))
    text_kill = font.render('Счёт: ' + str(killed), 1, (255, 255, 255))
    window.blit(text_kill, (10, 70))
    window.blit(text_skip, (10, 10))
    display.update() 
    keys_pressed = key.get_pressed()
    window.blit(background, (0, 0))
    clock.tick(FPS)
    player.show()
    monsters.draw(window)
    bullets.draw(window)
    asteroids.draw(window)
    if lifes == 3:
        window.blit(hp_3, (win_width-50, 50))
    elif lifes == 2:
        window.blit(hp_2, (win_width-50, 50))
    elif lifes == 1:
        window.blit(hp_1, (win_width-50, 50))
    else:
        window.blit(hp_0, (win_width-50, 50))
    
    if skipped < 3 and killed < 7 and lifes > 0:
    #if True:
        groups_list = sprite.groupcollide(monsters, bullets, True, True)    
        for c in groups_list:
            killed += 1
            monster = Enemy('ufo.png', random.randint(10, win_width - enemy_width - 10), -enemy_height -10, i+1, enemy_height, enemy_width)
            monsters.add(monster)

        sprites_list = sprite.spritecollide(player, monsters, True)
        for c in sprites_list:
            monster = Enemy('ufo.png', random.randint(10, win_width - enemy_width - 10), -enemy_height -10, i+1, enemy_height, enemy_width)
            monsters.add(monster)
            if allow:
                attack_time = tm.time()
                allow = False
                lifes -= 1
            if tm.time() - attack_time >= 0.5:
                allow = True

        asteroids_list = sprite.spritecollide(player, asteroids, False)
        for c in asteroids_list:
            if allow:
                attack_time = tm.time()
                allow = False
                lifes -= 1
            if tm.time() - attack_time >= 0.5:
                allow = True 

        groups_list_2 = sprite.groupcollide(asteroids, monsters, False, True)
        for c in groups_list_2:
            monster = Enemy('ufo.png', random.randint(10, win_width - enemy_width - 10), -enemy_height -10, i+1, enemy_height, enemy_width)
            monsters.add(monster)

        groups_list = sprite.groupcollide(bullets, asteroids, True, False)
        player.fire(keys_pressed)
        bullets.update()
        monsters.update()
        asteroids.update()
        player.update(keys_pressed)
    else:
        if skipped >= 3 and killed >= 10:
            window.blit(draw_text, (win_width/2, win_height/2))
        else:
            if skipped >= 3 or lifes <= 0:
                window.blit(lose_text, (win_width/2, win_height/2))
            if killed >= 7:
                window.blit(win_text, (win_width/2, win_height/2))