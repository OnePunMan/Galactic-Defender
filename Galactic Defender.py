# Author: Jackie Xu
# Date: 11/16/2016
# Content: My second game using pygame (Galactic Defender)
#import pygame
#import random
import math
import time
from properties import *
from classes import *

pygame.init()

# local variables
enemies = []
enemyFire = []
shield = False
update = True
clock = pygame.time.Clock()

# UI stuff
start_button = Button(200, 30, "Start", green, small_font, lambda: False)
quit_button = Button(200, 30, "Quit", red, small_font, lambda: False)

#S Surface (Display of the game)
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Galactic Defender')

powerup_time, t = pygame.USEREVENT + 1,5000
spawnrate_time, spawnTime = pygame.USEREVENT + 2,30000


# Collision detector
def collide (x1, y1, l1, w1, x2, y2, l2, w2):
    if x1 < x2 + l2 and x1 + l1 > x2 and \
       y1 < y2 + w2 and y1 + w1 > y2:
        return True

    else:
        return False


def spawn_enemies(amount, up, down, left, right):
    enemyList = []
    for count in range (0,amount):
        move = random.randrange(1,6)
        if move == 1:
            dx = random.randrange(-7,8)
            w = 10 * random.randrange(2, 5)
            h = 10 * random.randrange(2, 4)
            
        else:
            dx = 0
            w = 20
            h = 20
            
        randX = random.randrange(left, right - w)
        randY = random.randrange(up, down)
        dy = random.randrange(1, 5) / 10
        enemyList.append(Ship(randX, randY, w, h, 10 * random.randrange(1,4), dx, dy))
        
    return enemyList

def spawn_boss(surface, hp = 100, up = 0, down = 0, left = 0, right = 0):
    #randX = random.randrange(left, right)
    #randY = random.randrange(up, down)
    boss = BigShip(-100, 10)
    return boss

# Game Intro
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(pwrup_sound)
                    intro = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))
        msg_to_screen(gameDisplay, "Welcome to Galactic Defender!", red, WIDTH/2, HEIGHT/2 - 40, size = "large")
        msg_to_screen(gameDisplay, "Press 'Space' to start", blue, WIDTH/2, HEIGHT/2 + 20, size = "medium")
        
        start_button.draw(gameDisplay, WIDTH / 3, HEIGHT * 2./3)
        quit_button.draw(gameDisplay, WIDTH * 2./ 3, HEIGHT * 2./3)
        
        pygame.display.update()
        clock.tick(FPS)


# Gameloop
def gameLoop():
    global gameExit
    global gameOver
    global enemyFire
    global shield
    global update

    score = 0
    streak = 1
    
    hp = 100
    ship_X = WIDTH / 2
    ship_Y = HEIGHT - shipSize - 10
    ship_dx = 10
    shell_dy = -20
    shellEnemy_dy = 10
    fire = []
    enemyFire = []
    enemies = []
    bosses = []
    pwrups = []
    lastShot = 0
    fallTime = 0
    spawnCount = 10
    SHOT_DELAY = 250
    drop = False
    spawn = True
    specialLaser = False
    bossActive = False
    shield = False
    pause = False
    turbo = False
    specialBullet = 0
    shieldColour = white
    bg_y = 0
    scroll_speed = 1
    

    gameExit = False
    gameOver = False

    enemies = spawn_enemies (spawnCount, -1/4 * HEIGHT, 1/4 * HEIGHT, 0, WIDTH)
    
    pygame.mixer.music.play(-1)
    #PWR UP SPAWN TIME
    pygame.time.set_timer(powerup_time, t)
    pygame.time.set_timer(spawnrate_time, spawnTime)
    
    while not gameExit:

        while gameOver:
            if update:
                pygame.mixer.music.stop()
                msg_to_screen(gameDisplay, "Game over!", red, WIDTH / 2, HEIGHT / 2 - 40, size = "large") 
                msg_to_screen(gameDisplay, "Your score is: " + str(score), blue, WIDTH / 2, HEIGHT / 2, size = "medium")
                
                msg_to_screen(gameDisplay, "Press C to play again", white, WIDTH / 2, HEIGHT / 2 + 100, size = "small")
                msg_to_screen(gameDisplay, "Press Q to quit", white, WIDTH / 2, HEIGHT / 2 + 130, size = "small")
                update = False
                            
            pygame.display.update()
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        score = 0
                        gameOver = False
                        fire = []
                        enemies = []
                        bosses = []
                        pwrups = []
                        lastShot = 0
                        fallTime = 0
                        streak = 1
                        hp = 100
                        update = True
                        specialLaser = False
                        shield = False
                        pause = False
                        spawnCount = 5
                        enemies = spawn_enemies (spawnCount, -1/4 * HEIGHT, 1/4 * HEIGHT, 0, WIDTH)
                        enemyFire = []
                        score = 0
                        SHOT_DELAY = 250
                        shieldColour = white
                        bg_y = 0
                        scroll_speed = 1
                        pygame.mixer.music.play(-1)

        while pause:
            for event in pygame.event.get():            
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_p:
                        pause = False
                        pygame.mixer.music.unpause()
                          
        # In game--------------------------
        keys = pygame.key.get_pressed()
        gameDisplay.fill(black)

        rel_bg_y = bg_y % bg.get_rect().height
        gameDisplay.blit(bg, (0, rel_bg_y - bg.get_rect().height))
        if rel_bg_y < HEIGHT:
            gameDisplay.blit(bg, (0, rel_bg_y))
            
        bg_y = bg_y + scroll_speed
        if bg_y % HEIGHT == 0:
            bg_y = 0
        
        now = pygame.time.get_ticks()

        if hp > 0:
            #pygame.draw.rect(gameDisplay, blue, [ship_X, ship_Y, shipSize, shipSize])
            #pygame.draw.rect(gameDisplay, white, [ship_X + shipSize / 2 - bulletSize / 2, ship_Y - bulletSize, bulletSize, bulletSize])
            gameDisplay.blit(playerShip, (ship_X, ship_Y))
        else:
            gameOver = True
        
 
        if len(enemies) <= 10 and spawn:
            spawnCount = spawnCount + 5
            spawn = False

            if spawnCount >= 65:
                SHOT_DELAY = max(100, SHOT_DELAY - 10)
                scroll_speed = 4
            elif spawnCount >= 60:
                SHOT_DELAY = 120
                scroll_speed = 3
            elif spawnCount >= 50:
                SHOT_DELAY = 150
                scroll_speed = 2
            elif spawnCount >= 40:
                SHOT_DELAY = 200
            elif spawnCount >= 35:
                SHOT_DELAY = 230
            elif spawnCount >= 30:
                SHOT_DELAY = 240
                

        if shield:
            pygame.draw.rect(gameDisplay, shieldColour, [0, 3/4 * HEIGHT, WIDTH, 5])
            b = 255
            m = -255 / SHIELD_TIME
            c = m * (now - shieldTime) + b
            shieldColour = (c, c, c)
            if now - shieldTime > SHIELD_TIME:
                shield = False
    
                                             
        for enemy in enemies:
            enemy.move()
            gone = False

            if enemy.y > HEIGHT:
                gameOver = True

            if now - enemy.time > enemy.attackTime:
                enemy.time = now
                enemy.attackTime = 100 * random.randrange(10, 41)

                shoot = random.randrange(0, 5)
                if shoot == 0:
                    dmg = 10 * random.randrange(1,3)
                    dx = 0

                    if dmg == 10:
                        colour = green
                        l = 10
                        w = 20
                        dy = 10
                    else:
                        colour = red
                        l = 10
                        w = 10
                        dy = 5
                        
                    rand = random.randrange(0,3)
                
                    if rand == 1 and colour == red:
                        dx = random.randrange(-7, 8)
                    elif rand == 2:
                        distance_y = ship_Y - enemy.y
                        distance_x = ship_X - enemy.x
                        l = w = 10
                        dx = distance_x * dy / distance_y
                                                      
                    enemyFire.append(Bullet(enemy.x + enemySize / 2 - bulletSize / 2, enemy.y, dmg, dx, dy, colour, l, w))

            if shield and collide (enemy.x, enemy.y, enemy.width, enemy.height, 0, 3/4 * HEIGHT, WIDTH, 5):
                pygame.mixer.Sound.play(explode_sound)
                enemies.remove(enemy)
                gone = True                
                    
            if collide (enemy.x, enemy.y, enemy.width, enemy.height, ship_X, ship_Y, shipSize, shipSize):
                hp = hp - 25
                streak = 1
                # print (score)
                enemies.remove(enemy)
                pygame.mixer.Sound.play(explode_sound)
                gone = True

            if not gone:
                enemy.draw(gameDisplay)
            
            
        if len(bosses) == 0:
            bossActive = False
            if len(enemies) <= 10:
                enemies.extend(spawn_enemies (5, -1/3 * HEIGHT, -1/10 * HEIGHT, 0, WIDTH))
            
        else:
            bossActive = True
            for boss in bosses:
            
                boss.move()
                boss.draw(gameDisplay)
                
                if boss.special:
                    boss.specialAttack(gameDisplay, shield)
                    if collide (boss.laser.x, boss.laser.y, boss.laser.width,boss.laser.height, ship_X, ship_Y, shipSize, shipSize):
                        hp = hp - boss.laser.damage
                        
                if now - boss.time > BOSSATTACK_TIME:
                    boss.time = now
                    boss.attack(enemyFire)

                    
        for item in pwrups:
            if item.hp >= -4:
                gameDisplay.blit(item.img, (item.x, item.y))
            else:
                pygame.draw.rect(gameDisplay, item.colour, [item.x, item.y, enemySize, enemySize])
            
        drop = False
        attack = False


        for shell in fire:
            shell.allyClr()
            hit = False

            if specialBullet <= 0:
                specialLaser = False
    
            if shell.y - bulletSize >= -1/4 * HEIGHT:
                for enemy in enemies:
                    if collide (shell.x, shell.y, shell.width, shell.height, enemy.x, enemy.y, enemy.width, enemy.height) and not hit:
                        
                        fire.remove(shell)
                        enemy.hp = enemy.hp - shell.damage
                        enemy.update()
                        hit = True
                        
                        if enemy.hp <= 0:
                            pygame.mixer.Sound.play(explode_sound)
                            score = score + 10 * streak
                            enemies.remove(enemy)
                        else:
                            pygame.mixer.Sound.play(hit_sound)
                            score = score + 2 * streak
                        streak = min(streak + 1, 100)
                        # print (score)
                        
                for boss in bosses:
                    if collide (shell.x, shell.y, shell.width, shell.height, boss.x, boss.y, boss.width, boss.height) and not hit:
                        
                        fire.remove(shell)
                        boss.hp = boss.hp - shell.damage
                        hit = True
                        
                        if boss.hp <= 0:
                            pygame.mixer.Sound.play(explode_sound)
                            score = score + 100 * streak
                            bosses.remove(boss)
                        else:
                            pygame.mixer.Sound.play(hit_sound)
                            score = score + 2 * streak
                        streak = streak + 1
                    
                       # print (score)
                    
                            
                for item in pwrups:
                    if collide (shell.x, shell.y, shell.width, shell.height, item.x, item.y, enemySize, enemySize) and not hit:
                        pygame.mixer.Sound.play(pwrup_sound)
                        fire.remove(shell)
                        hit = True

                        if item.hp == -1:
                            hp = 100
                            
                        elif item.hp == -2:
                  
                            for enemy in enemies:
                                enemy.y = enemy.y - 80
                                
                        elif item.hp == -3:
                            number = random.randrange(15, 41)
                            for count in range (0,number):
                                randX = random.randrange(0, WIDTH - enemySize)
                                dmg = 10 * random.randrange(0,4)
                                if dmg == 0:
                                    dmg = 20
                                else:
                                    dmg = 10
                                fire.append(Bullet(randX, ship_Y, dmg))
                        elif item.hp == -4:                            
                            specialBullet += 40
                            specialLaser = True

                        elif item.hp == -5:
                            shield = True
                            shieldTime = now
                            shieldColour = white
                                                            
                        pwrups.remove(item)
                        score = score + 15 * streak
                        # print (score)
                        
                       
                if not hit:        
                    shell.y = shell.y + shell_dy
                    #shell.draw(gameDisplay)
                
            else:
                del fire[0]
                streak = 1

        for shell in fire:
            shell.draw(gameDisplay)

        for shell in enemyFire:
            shell.move()

            if shell.y >= HEIGHT:                
                enemyFire.remove(shell)
            
            else:
                gone = False
                if shield and collide (shell.x, shell.y, shell.width, shell.height, 0, 3/4 * HEIGHT, WIDTH, 5):
                    enemyFire.remove(shell)
                    
                if collide (shell.x, shell.y, shell.width, shell.height, ship_X, ship_Y, shipSize, shipSize):
                    enemyFire.remove(shell)
                    hp = hp - shell.damage
                    pygame.mixer.Sound.play(hit_sound)
                    streak = 1
                    # print (score)

                    
        for shell in enemyFire:
            shell.draw(gameDisplay)

        # HP bar
        pygame.draw.rect(gameDisplay, black, [ship_X, ship_Y + shipSize, shipSize, 5])
        if hp > 0:
            if hp > 50:
                colour = green
            elif hp > 30:
                colour = orange
            else:
                colour = red
            pygame.draw.rect(gameDisplay, colour, [ship_X, ship_Y + shipSize, shipSize * hp / 100, 5])
        else:
            pygame.mixer.Sound.play(explode_sound)


        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                gameExit = True
                
            if event.type == pygame.KEYDOWN:
                #----------- DEBUG CHEATS--------------
                if event.key == pygame.K_q:
                    bosses.append(BigShip(-100, 10))
                    bossActive = True
                if event.key == pygame.K_1:
                    hp = 100
                if event.key == pygame.K_2:
                    enemies = []
                if event.key == pygame.K_3:
                    randX = random.randrange(0, WIDTH - enemySize)
                    randY = random.randrange(0, 1/4 * HEIGHT)
                    pwrups.append(Ship(randX, randY, enemySize, enemySize, -random.randrange(1, 6)))
                    
                if event.key == pygame.K_4:
                    shield = True
                    shieldTime = now
                    shieldColour = white

                if event.key == pygame.K_0:
                    enemies.extend(spawn_enemies (5, -1/3 * HEIGHT, -1/10 * HEIGHT, 0, WIDTH))

                if event.key == pygame.K_p:
                    pause = True
                    pygame.mixer.music.pause()
                    msg_to_screen(gameDisplay, "Paused, press 'P' to continue" , white, WIDTH / 2, HEIGHT / 2, size = "medium")
                    pygame.display.update()
                    
                #---------------------------------
        
            if event.type == powerup_time:
                chance = random.randrange(0,3)
                if chance == 0:
                    chance = -1 * random.randrange(1,6)
                    randX = random.randrange(0, WIDTH - enemySize)
                    randY = random.randrange(0, 1/4 * HEIGHT)
                    pwrups.append(Ship(randX, randY, enemySize, enemySize, chance))
            if event.type == spawnrate_time and bossActive == False:
                enemies.extend(spawn_enemies (spawnCount, -1/4 * HEIGHT, 0, 0, WIDTH))
                direction = random.randrange(0,2)
                if direction == 0:
                    direction = -100
                else:
                    direction = WIDTH
                bosses.append(BigShip(direction, 10))
                spawn = True
                bossActive = True

        if keys [pygame.K_a]:
            turbo = True
            ship_dx = 20
        else:
            turbo = False
            
        if keys [pygame.K_LEFT] and ship_X - ship_dx >= 0:
            ship_X = ship_X - ship_dx
            
        if keys [pygame.K_RIGHT] and ship_X + shipSize + ship_dx <= WIDTH:
            ship_X = ship_X + ship_dx
            

        
        if keys [pygame.K_SPACE] and not turbo:
            ship_dx = 5
            now = pygame.time.get_ticks()
                
            if now - lastShot >= SHOT_DELAY:
                pygame.mixer.Sound.play(shoot_sound)

                if specialLaser:
                    specialBullet = specialBullet - 1
                    damage = 20
                else:
                    damage = 10
                    
                fire.append(Bullet(ship_X + shipSize / 2 - bulletSize / 2, ship_Y, damage))
                lastShot = now
                
        else:
            ship_dx = 10

        msg_to_screen(gameDisplay, "Score: " + str(score), white, 10, 10, "topleft")
        if specialLaser:
            msg_to_screen(gameDisplay, "Special Laser: " + str(specialBullet), white, WIDTH - 10, 10, "topright")
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

# Main
game_intro()
gameLoop()

