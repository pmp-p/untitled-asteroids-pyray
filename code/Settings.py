from pyray import *
from raylib import *
from tkinter import *



# Get the scaled width and height for consistency. CHANGING will break the game
TARGET_SCREEN_WIDTH, TARGET_SCREEN_HEIGHT = 1280, 720 
root = Tk()
DEVICE_WIDTH, DEVICE_HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

# Used for scaling elements of the game based on screensize
SCALE_X = DEVICE_WIDTH / TARGET_SCREEN_WIDTH
SCALE_Y = DEVICE_HEIGHT / TARGET_SCREEN_HEIGHT

print(DEVICE_WIDTH, DEVICE_HEIGHT )
SCALE_FACTOR = min(SCALE_X, SCALE_Y)
ADJUSTED_WIDTH, ADJUSTED_HEIGHT = int(TARGET_SCREEN_WIDTH * SCALE_X), int(TARGET_SCREEN_HEIGHT * SCALE_Y)


BG_COLOR = BLACK  # (15,10,25,255)
PLAYER_SPEED = 700
LASER_SPEED = 600
OXYGEN_DEPLETION_RATE = 2.8
FONT_SIZE = 120
POINTS_FONT_SIZE = 40
OXYGEN_FONT_SIZE = 40
MAX_ASTEROID_SPEED = [200, 250]
