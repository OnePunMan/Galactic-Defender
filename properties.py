import pygame
# colours: RGB
white = (255, 255, 255)
black = (0, 0, 0)
cyan = (20, 220, 220)
pink = (255, 0, 255)
red = (255, 0, 0)
purple = (100, 0, 100)
orange = (255, 153, 51)
green = (0, 155, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Window size
WIDTH = 800
HEIGHT  = 600

# CONSTANTS
FPS = 30
FALL_TIME = 3000
LASER_TIME = 5000
SHIELD_TIME = 10000
BOSSATTACK_TIME = 8000

# entity properties
shipSize = 40
bulletSize = 10
enemySize = 20	


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
# sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
explode_sound = pygame.mixer.Sound("explode.wav")
pwrup_sound = pygame.mixer.Sound("pwrup.wav")
pygame.mixer.music.load("bg.wav")

# images
medpack = pygame.image.load('health.png')
boostUp = pygame.image.load('up.png')
barrage = pygame.image.load('barrage.png')
purpleLaser = pygame.image.load('purple.png')
playerShip = pygame.image.load('ship_new.png')
bg = pygame.image.load('space.png') # .convert()

# fonts
pygame.font.init()
small_font = pygame.font.SysFont(None, 25)
medium_font = pygame.font.SysFont(None, 40)
large_font = pygame.font.SysFont(None, 60)

