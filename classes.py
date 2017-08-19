#import pygame
import random
from properties import *

def text_objects(text, colour, size):
    #textSurface = small_font.render(text, True, colour)
    textSurface = eval(size + "_font").render(text, True, colour)
    return textSurface, textSurface.get_rect()

def msg_to_screen (display, msg, colour, posX, posY, anchor = "center", size = "small"):
    textSurf, textRect = text_objects(msg, colour, size)
    setattr(textRect, anchor, (posX, posY))
    #textRect.center = posX, posY
    display.blit (textSurf, textRect)

class Bullet:

    def __init__(self, x, y, damage, dx = 0, dy = 10, colour = (255, 255, 0), width = 10, height = 20):
        self.bullets = []
        self.damage = damage
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.colour = colour

    def draw (self, surface):
        pygame.draw.rect(surface, self.colour, [self.x, self.y, self.width, self.height])
        
    def allyClr (self):
        if self.damage == 10:
            self.colour = (255, 255, 0)
        else:
            self.colour = (255, 0, 255)

    def move (self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

class Ship:    
    def __init__(self, x, y, width, height, hp, dx = 0, dy = 0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.hp = hp
        self.attackTime = 100 * random.randrange(10, 41)
        self.time = pygame.time.get_ticks()
        self.update()

        if self.hp <= -1:
            if self.hp == -1:
                self.img = medpack
            elif self.hp == -2:
                self.img = boostUp
            elif self.hp == -3:
                self.img = barrage
            elif self.hp == -4:
                self.img = purpleLaser
            else:
                self.img = None

    
    def move(self):
        if self.x + self.dx <= 0 or self.x + self.width + self.dx >= WIDTH:
            self.dx = -self.dx
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, [self.x, self.y, self.width, self.height])


    def update (self):
        if self.hp <= -1:
            self.colour = white
        elif self.hp == 10:
            self.colour = red
        elif self.hp == 20:
            self.colour = orange
        else:
            self.colour = purple

class BigShip:
    
    def __init__(self, x, y, dx = 5, dy = 0, width = 60, height = 40, hp = 100):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy 
        self.width = width
        self.height = height
        self.hp = hp
        self.totalHP = hp
        self.colour = red
        self.special = False
        self.time = pygame.time.get_ticks()

    
    def draw (self, surface):
        if self.hp > 0:
            pygame.draw.rect(surface, self.colour, [self.x, self.y, self.width, self.height])
            pygame.draw.rect(surface, black, [self.x, self.y + 0.9 * self.height, self.width, 0.1 * self.height])
            pygame.draw.rect(surface, green, [self.x, self.y + 0.9 * self.height, float(self.hp) / self.totalHP * self.width, 0.1 * self.height])

        else:
            pygame.draw.rect(surface, black, [self.x, self.y + 0.9 * self.height, self.width, 0.1 * self.height])
      
         
    def attack (self, enemy_list):
        tpe = random.randrange(1,3)
        
        if tpe == 1:        
            for count in range(-10, 11):
                enemy_list.append(Bullet(self.x + self.width/2 - 10/2, self.y + self.height, 10, count, 5, yellow, 10, 10))
        else:
            self.special = True
            self.time = pygame.time.get_ticks()
            self.laser = Bullet(self.x + 1./4 * self.width, self.y + self.height, 4, 0, 0, cyan, 1./2 * self.width, 0)
            
    def specialAttack (self, display, shield):
        if self.special:
            self.laser.x = self.x + 1./4 * self.width
            if shield:
                shieldHeight = 3./4 * HEIGHT - self.laser.y
            else:
                shieldHeight = HEIGHT
            self.laser.height = min(self.laser.height + 20, HEIGHT, shieldHeight)
            self.laser.draw(display)
            
            if pygame.time.get_ticks() - self.time > LASER_TIME:
                self.special = False
    
    def move(self, margin = 100):
        if self.x + self.dx <= 0 - margin or self.x + self.width + self.dx >= WIDTH + margin:
            self.dx = -self.dx
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def hit(self, damage):
        self.hp = self.hp - damage


class Button:
    # class (static) method
    @staticmethod
    def text_to_button(display, text, colour, x, y, width, height, size = "small", anchor = "center"):
        textSurf, textRect = text_objects(text, colour, size)
        textRect.center = (x + width/2, y + height/2)
        display.blit (textSurf, textRect)

    def __init__(self, x, y, width, height, text, colour, font, on_click):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.font = font
        self.on_click = on_click

    def is_hover(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

    def draw(self, display, hover = False):
        clr = self.colour
        if hover:
            clr = (min(255, self.colour[0] + 50), min(255, self.colour[1] + 50), min(255, self.colour[2] + 50))

        pygame.draw.rect(display, clr, (self.x, self.y, self.width, self.height))
        Button.text_to_button(display, self.text, (255,255,255), self.x, self.y, self.width, self.height)