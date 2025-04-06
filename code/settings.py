from pyray import *
from raylib import *
from random import randint, uniform, choice
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
BG_COLOR = BLACK # (15,10,25,255)
PLAYER_SPEED = 700
LASER_SPEED = 600
OXYGEN_DEPLETION_RATE = 2.8 
FONT_SIZE = 120
POINTS_FONT_SIZE = 40
OXYGEN_FONT_SIZE = 70
MAX_ASTEROID_SPEED = [200,250]


