from pygame import *
from random import randint
from time import time as tm



class GameSprite(sprite.Sprite):
    def __init__(self,player_image,palyer_x,player_y,w,h,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = palyer_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 645:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lost       
        if self.rect.y > 500:
            self.rect.y = -65
            self.rect.x = randint(0,635)
            lost = lost + 1


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y > 500:
            self.rect.y = -65
            self.rect.x = randint(0,635)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()     
        

window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.3)
fire_music = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial',70)
font2 = font.SysFont('Arial',30)
win = font1.render('YOU WIN!',True,(255,215,0))
lose = font1.render('YOU LOSE!',True,(255,215,0))



player = Player('rocket.png',100,420,55,75,5)
enemys = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png',randint(0,635),-65,65,55,randint(1,3))
    enemys.add(enemy)


bullets = sprite.Group()


asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png',randint(0,635),-65,65,55,1)
    asteroids.add(asteroid)


clock = time.Clock()
FPS = 60
game = True
finish = False
score = 0
lost = 0
num_fire = 0
rel_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    fire_music.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    old_time = tm()
    
    if finish != True:
        window.blit(background,(0,0))
        text_lose = font2.render('Пропущено ' + str(lost), 1, (255,255,255))
        text_win = font2.render('Счёт ' + str(score), 1, (255,255,255))
        reload_gun = font2.render('Перезарядка...',1,(255,0,0))
        window.blit(text_lose,(10,10))
        window.blit(text_win,(10,40))
        
        player.update()
        enemys.update()
        player.reset()
        enemys.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)


        if rel_time == True:
            new_time = tm()
            if new_time - old_time < 3:
                window.blit(reload_gun,(300,450))
            else:
                num_fire = 0
                rel_time = False


        sprite_list = sprite.groupcollide(enemys,bullets,True,True)
        for i in sprite_list:
            score += 1
            enemy = Enemy('ufo.png',randint(0,635),-65,65,55,randint(1,3))
            enemys.add(enemy)
        if score >= 10:
            finish = True
            window.blit(win,(200,200))
        if lost >= 3 or sprite.spritecollide(player,enemys,False) or sprite.spritecollide(player,asteroids,False):
            finish = True
            window.blit(lose,(200,200))


    clock.tick(FPS)
    display.update()