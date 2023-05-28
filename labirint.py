from pygame import *
from time import time as timer
from random import *

'''Шрифты для текста в игре'''
font.init()
font2 = font.SysFont('Comic Sans MS', 20) #шрифт для параметров на экране(кол-во патронов, гранат и т.д.)
font = font.SysFont('Times New Roman', 80) #шрифт для проигрыша, выигрыша, начало уровня
win = font.render('YOU WIN!', True, (0, 225, 0)) #текст победы
lose = font.render('YOU LOSE!', True, (255, 0, 0)) #текст проигрыша

level1_text = font.render('LEVEL 1', True, (255, 255, 255))

BLACK = (255, 255, 255) #черный цвет RGB

'''Показатели и задачи'''
bullet_amount = 0
grenade_amount = 0
weapon = 'Is not!'
weapon2 = 'Colt 1902'
weapon3 = 'Barrett XM109'
b_text = font2.render('Cartridges:', True, BLACK)
g_text = font2.render('Grenades:', True, BLACK)
w_text = font2.render('Weapon:', True, BLACK)
b_amount = font2.render(str(bullet_amount), True, BLACK)
g_amount = font2.render(str(grenade_amount), True, BLACK)
weapon_text = font2.render(weapon, True, BLACK)
task = 'Task: take the colt'
task2 = 'Task: take the grenade'
task3 = 'Task: take the treasure'
task4 = 'Task: take the key'
task5 = 'Task: get out of the dungeon'
task_text = font2.render(task, True, BLACK)

'''Все спрайты в игре'''
img_cave = 'main1.jpg'
img_hero = 'hero1.png'
img_enemy = 'enemy.png'
img_enemy2 = 'enemy2.png'
img_final = 'final_door.png'
img_bullet = 'bullet.png'
img_grenade = 'grenade.png'
img_gun = 'gun.png'
img_hero2 = 'hero_gun.png'
img_treasure = 'treasure.png'
img_key = 'key.png'

mixer.init() #подключаем музыку and звуки
shut = mixer.Sound('shut.ogg') #звук выстрела
bum = mixer.Sound('bum.ogg') #звук взрыва гранаты

'''Основной класс'''
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.w = width
        self.h =height
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self): #метод прогрузки спрайта на окне
        window.blit(self.image, (self.rect.x, self.rect.y))

'''Класс для персонажа'''
class Player(GameSprite):
    def update(self): #метод движения
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self): #метод выстрела
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery, 24, 25, 10)
        bullets.add(bullet)
    def g_fire(self,): #метод кидания гранаты
        grenade = Grenade(img_grenade, self.rect.right, self.rect.centery, 28, 30, 6)
        grenades.add(grenade)

'''Классы монстров'''
class Enemy(GameSprite):
    side = 'left'
    def update(self): #метод движения первого монстра
        if self.rect.y <= 180:
            self.side = 'down'
        elif self.rect.y >= 330:
            self.side = 'up'
        if self.side == 'down':
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
class Enemy2(GameSprite):
    side = 'up'
    def update(self): #метод движения второго монстра
        if self.rect.x >= 800:
            self.side = 'left'
        elif self.rect.x <= 400:
            self.side = 'right'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

'''Класс стены'''
class Wall(sprite.Sprite):
    def __init__(self, red, green, blue, wall_x, wall_y, wall_width, wall_height): #в свойства добавляется rgb цвета для стены
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.w = wall_width
        self.h = wall_height
        self.image = Surface((self.w, self.h))
        self.image.fill((red, green, blue))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

'''Класс пули'''
class Bullet(GameSprite):
    def update(self): #метод движения пули вправо
        self.rect.x += self.speed
        if self.rect.x > win_width + 5:
            self.kill()

'''Класс гранаты'''
class Grenade(GameSprite):
    def update(self): #метод движения гранаты вправо
        self.rect.x += self.speed
        if self.rect.x > win_width + 5:
            self.kill()

'''Создания окна и фона'''
win_width = 1000
win_height = 700
display.set_caption('Game') #называем окно
window = display.set_mode((win_width, win_height)) #создаем само окно
back = transform.scale(image.load(img_cave), (win_width, win_height)) #загружаем основной фон

'''Создание экземпляров классов'''
hero = Player(img_hero, 5, win_height - 80, 65, 65, 10)
enemy = Enemy(img_enemy, 470, 200, 100, 65, 5)
enemy2 = Enemy2(img_enemy2, 300, 610, 100, 90, 3)
final = GameSprite(img_final, win_width - 150, win_height - 120, 150, 120, 0)
grenade_item = GameSprite(img_grenade, 500, 20, 65, 65, 0)
gun_item = GameSprite(img_gun, 50, 320, 65, 65, 0)
treasure = GameSprite(img_treasure, 420, 430, 65, 65, 0)
key_item = GameSprite(img_key, 250, 620, 65, 65, 0)

'''Создание стен'''
w1 = Wall(38, 35, 74, 200, 500, 20, 200)
w2 = Wall(38, 35, 74, 200, 500, 150, 20)
w3 = Wall(38, 35, 74, 350, 270, 20, 330)
w4 = Wall(38, 35, 74, 350, 400, 150, 20)
w5 = Wall(38, 35, 74, 500, 400, 20, 150)
w6 = Wall(38, 35, 74, 500, 550, 250, 20)
w7 = Wall(38, 35, 74, 750, 350, 20, 220)
w8 = Wall(38, 35, 74, 0, 400, 150, 20)
w9 = Wall(38, 35, 74, 150, 100, 20, 320)
w10 = Wall(38, 35, 74, 250, 150, 200, 20)
w11 = Wall(38, 35, 74, 450, 0, 20, 170)
w12 = Wall(38, 35, 74, 450, 100, 150, 20)
w13 = Wall(38, 35, 74, 600, 100, 20, 200)
w14 = Wall(38, 35, 74, 600, 200, 200, 20)
w15 = Wall(38, 35, 74, 900, 0, 20, 100)
w16 = Wall(38, 35, 75, 850, 300, 20, 150)
w17 = Wall(38, 35, 74, 850, 450, 150, 20)
w18 = Wall(38, 35, 74, 350, 500, 150, 20)

'''Создание группы спрайтов для стен и добавление в него всех стен'''
walls = sprite.Group()
walls.add(w1)
walls.add(w2)
walls.add(w3)
walls.add(w4)
walls.add(w5)
walls.add(w6)
walls.add(w7)
walls.add(w8)
walls.add(w9)
walls.add(w10)
walls.add(w11)
walls.add(w12)
walls.add(w13)
walls.add(w14)
walls.add(w15)
walls.add(w16)
walls.add(w17)
walls.add(w18)

'''Группа спрайтов для монстров'''
monsters = sprite.Group()
monsters.add(enemy)
monsters.add(enemy2)

'''Группы спрайтов для снарядов(пуль и гранат)'''
bullets = sprite.Group()
grenades = sprite.Group()

'''Некоторые игровые переменные'''
now_weapon = weapon #нынешнее оружие игрока
start_l1 = False #переменная показывает, начал ли движение(уровень) игрок
grenade_on = False #переменная показывает взял ли игрок гранату
key_on = False #взял ли игрок ключ
treasure_on = False #взял ли игрок сокровища
play = True
finish = False
clock = time.Clock()
FPS = 60

'''Игровой цикл'''
while play:
    for e in event.get():
        if e.type == QUIT: #если пользователь вышел из игры
            play = False
        if e.type == KEYDOWN: #если пользователь зажал клавишу
            if now_weapon == weapon2: #если нынешнее оружие это кольт
                if e.key == K_q and bullet_amount > 0: #если пользователь нажал q и кол-во пуль больше 0
                    hero.fire() #выстрел
                    shut.play() #звук выстрела
                    bullet_amount -= 1 #отнимаем одну пулю
                    b_amount = font2.render(str(bullet_amount), True, BLACK) #текст с новым кол-вом пуль
            if e.key == K_TAB and grenade_amount > 0: #если нажал tab и кол-во гранат больше 0
                hero.g_fire() #кидание гранаты
                grenade_amount -= 1 #отнимаем 1 гранату от общего кол-ва
                g_amount = font2.render(str(grenade_amount), True, BLACK) #текст с новым кол-вом гранат
    if finish != True:
            if e.type == KEYDOWN: #если пользователь зажимает клавишу
                start_l1 = True 
            window.blit(back, (0,0)) # рисуем фон в окне
            '''появление всех спрайтов с помощью методов reset(GameSprite) и update'''
            hero.reset()
            hero.update()
            final.reset()
            monsters.update()
            monsters.draw(window)
            walls.draw(window)
            bullets.draw(window)
            bullets.update()
            grenades.draw(window)
            grenades.update()
            if key_on == False: #спрайт ключа рисуется пока его не тронул пользователь
                key_item.reset()
            if treasure_on == False: #тоже самое с сокровищем
                treasure.reset()
            if now_weapon != weapon2: # с спрайтов кольта
                gun_item.reset()
            if grenade_on == False: # с спрайтом гранаты 
                grenade_item.reset()

            '''Столкновения пуль со стенами и монстрами'''
            sprite.groupcollide(bullets, walls, True, False) #первое True значит что пули исчезают, второе False значит что стены НЕ исчезают
            sprite.groupcollide(bullets, monsters, True, True) #тут два True, значит оба столкнувшихся элемента исчезают

            '''Столкновения персонажа и спрайта гранаты'''
            if sprite.collide_rect(hero, grenade_item):
                if grenade_on == False:
                    task_text = font2.render(task3, True, BLACK)
                    grenade_amount += 1
                    g_amount = font2.render(str(grenade_amount), True, BLACK)
                    grenade_on = True
            
            '''Персонаж и скоровище'''
            if sprite.collide_rect(hero, treasure):
               treasure_on = True
               task_text = font2.render(task4, True, BLACK)
               grenade_amount = 2
               g_amount = font2.render(str(grenade_amount), True, BLACK)
               treasure.kill()

            '''Персонаж и кольт'''
            if sprite.collide_rect(hero, gun_item):
                now_weapon = weapon2
                weapon_text = font2.render(weapon2, True, BLACK)
                task_text = font2.render(task2, True, BLACK)
                bullet_amount = 5
                b_amount = font2.render(str(bullet_amount), True, BLACK)
                hero.image = transform.scale(image.load(img_hero2), (hero.w, hero.h))

            '''Персонаж с ключом и финал(дверь)'''
            if sprite.collide_rect(hero, final) and key_on == True:
                finish = True
                window.blit(win, (325, 270))

            '''Персонаж и ключ'''
            if sprite.collide_rect(hero, key_item):
                key_on = True
                task_text = font2.render(task5, True, BLACK)

            '''Персонаж и стена'''
            if sprite.spritecollide(hero, walls, False):
                finish = True
                window.blit(lose, (325, 270))
                
            if start_l1 == False:
                window.blit(level1_text, (325, 270))

            if sprite.groupcollide(grenades, walls, True, True) or sprite.groupcollide(grenades, monsters, True, True):
                bum.play()
            
            if sprite.spritecollide(final, grenades, True):
                finish = True
                window.blit(lose, (325, 270))

            if sprite.spritecollide(hero, monsters, False):
                finish = True
                window.blit(lose, (200, 200))

            '''Рисование текста в окне'''
            window.blit(g_amount, (120, 40))
            window.blit(b_amount, (130, 20))
            window.blit(b_text, (20, 20))
            window.blit(g_text, (20, 40))
            window.blit(w_text, (180, 20))
            window.blit(weapon_text, (265, 20))
            window.blit(task_text, (690, 20))

    display.update() #обновление окна
    clock.tick(FPS) #фпс