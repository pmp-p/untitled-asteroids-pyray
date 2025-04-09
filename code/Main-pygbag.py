import asyncio
from Game import *

"""
This is the main file used for running the game on browser. 
Ignore if just running the game from terminal.
"""


# Try to declare all your globals at once to facilitate compilation later.
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
BG_COLOR = BLACK  # (15,10,25,255)
PLAYER_SPEED = 700
LASER_SPEED = 600
OXYGEN_DEPLETION_RATE = 2.8
FONT_SIZE = 120
POINTS_FONT_SIZE = 40
OXYGEN_FONT_SIZE = 70
MAX_ASTEROID_SPEED = [200, 250]

# load all game assets now to prevent lag at runtime or network errors
game_assets.get_asset_font("slkscr.ttf")
game_assets.get_asset_font("slkscreb.ttf")

game_assets.get_asset_texture("diamond.png")
game_assets.get_asset_texture("emerald.png")
game_assets.get_asset_texture("empty_heart_container.png")
game_assets.get_asset_texture("fiery_meteor.png")
game_assets.get_asset_texture("green_laser.png")
game_assets.get_asset_texture("green_ship.png")
game_assets.get_asset_texture("health_power_up.png")
game_assets.get_asset_texture("heart_container.png")
game_assets.get_asset_texture("icy_meteor.png")
game_assets.get_asset_texture("iron.png")
game_assets.get_asset_texture("laser_powerup.png")
game_assets.get_asset_texture("loading_screen.png")
game_assets.get_asset_texture("meteor.png")
game_assets.get_asset_texture("ruby.png")
game_assets.get_asset_texture("star.png")
game_assets.get_asset_texture("water_tank.png")
game_assets.get_asset_texture("water.png")

game_assets.get_asset_music("game_music.ogg")

game_assets.get_asset_sound("ammo_collect.ogg")
game_assets.get_asset_sound("bubble.ogg")
game_assets.get_asset_sound("button_click.ogg")
game_assets.get_asset_sound("crash.ogg")
game_assets.get_asset_sound("explosion.ogg")
game_assets.get_asset_sound("freeze_sfx.ogg")
game_assets.get_asset_sound("game_over.ogg")
game_assets.get_asset_sound("heart_collect.ogg")
game_assets.get_asset_sound("laser.ogg")
game_assets.get_asset_sound("treasure_collect.ogg")


async def main():
    """
    For running the game on a web browser.
    """
    game_test = SpaceGame()
    game_test.run_optimized_web()


if __name__ == "__main__":
    # run the web browser version of the game here
    asyncio.run(main())
