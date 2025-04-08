import asyncio

from Game import *

"""
This is the main file used for running the game on browser. 
Ignore if just running the game from terminal.
"""


# Try to declare all your globals at once to facilitate compilation later.
WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
BG_COLOR = BLACK # (15,10,25,255)
PLAYER_SPEED = 700
LASER_SPEED = 600
OXYGEN_DEPLETION_RATE = 2.8 
FONT_SIZE = 120
POINTS_FONT_SIZE = 40
OXYGEN_FONT_SIZE = 70
MAX_ASTEROID_SPEED = [200,250]

# load all game assets now to prevent lag at runtime or network errors
game_assets = Assets()
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

game_assets.get_asset_music("game_music.mp3")

game_assets.get_asset_sound("ammo_collect.wav")
game_assets.get_asset_sound("bubble.wav")
game_assets.get_asset_sound("button_click.wav")
game_assets.get_asset_sound("crash.wav")
game_assets.get_asset_sound("explosion.wav")
game_assets.get_asset_sound("freeze_sfx.wav")
game_assets.get_asset_sound("game_over.wav")
game_assets.get_asset_sound("heart_collect.wav")
game_assets.get_asset_sound("laser.wav")
game_assets.get_asset_sound("treasure_collect.wav")


async def run_optimized(self): # This is basically the main(self): method
        """
        Main game loop that handles menu navigation, game state transitions,
        and drawing appropriate buttons based on game state. 
        Uses DoublyLinkedStack data structure for better efficiency.

        """
        
        global WINDOW_WIDTH, WINDOW_HEIGHT 
        global BG_COLOR
        global PLAYER_SPEED 
        global LASER_SPEED 
        global OXYGEN_DEPLETION_RATE 
        global FONT_SIZE 
        global POINTS_FONT_SIZE 
        global OXYGEN_FONT_SIZE 
        global MAX_ASTEROID_SPEED

        # Initialize with the main menu state
        self._menu._menu_state_stack.push("main_menu")
        
        while not window_should_close() and not self.should_exit_menu_status():
            begin_drawing()
            clear_background(BG_COLOR)
            
            # This current_state is used to determine what new menu to now run
            current_state = self._menu._menu_state_stack.top()
            
            # Menu screen to run based on current game state
            if current_state in self._screens:
                self._screens[current_state]()
            else:
                print(current_state + " not recognized.")

            end_drawing()

        # store the games data to be saved (city data, player leaderboard)
        saved_data["Game Leaderboard"] = self._menu._leaderboard
        saved_data["City selected"] = self._city_custom
        saved_data["City temperature"] = self._game_temperature_custom
        saved_data["City wind speed range"] = self._max_speed_range_custom
        save_game_data_file(saved_data)
        

        # Close the game
        self.cleanup_asteroids_game()

if __name__ == '__main__': 
    game_test = SpaceGame()
    game_test.run_optimized() 