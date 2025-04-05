from Sprites import *
from WeatherApi import *
from Menu import *
from random import *
from InputBox import *

# Handles the game mechanics
class SpaceGame():
    # game uses a difficulty system: a temperature and asteroid speed is given that affects the type 
    # of asteroids that spawn and their speed (given by a range list)
    def __init__(self, city="Default", difficulty_temp=65, difficulty_wdsp=MAX_ASTEROID_SPEED):
        self._stars_list = [] # list of stars to display in the background
        self.make_stars() # initilize the list of stars
        self._asteroids_list = [] # list of asteroids to hold
        self._max_asteroids = 6
        self._game_temperature_custom = difficulty_temp # custom temperature to be set using user input
        self._max_speed_range_custom =  difficulty_wdsp # custom speed to be set using user input
        self._city_custom = city # custom sity to be set using user input
        self._max_speed_range_default = MAX_ASTEROID_SPEED # defualts to use for reseting
        self._game_temperature_default = 65 # defaults to use for resetting
        self._city_default = city
        # both speed and spawn cycles are using to control the difficulty progression of the game
        self._asteroid_spawn_cycle = 0 # number of spawn cycles (each spawn cycle increases number of asteroids)
        self._asteroid_speed_cycle = 0 # number of speed cycles (each speed cycle increases speed range)
        self._asteroid_spawn_timer = Timer(4, True, False, self.capped_asteroid_spawn_timer) # timer to increase spawn every few seconds
        self._asteroid_speed_increase_timer = Timer(10, True, False, self.capped_asteroid_speed_timer) # timer to increase speed range every few seconds
        self._power_ups = [] # list of powerup objects
        self._treasure = [] # list of treasure objects
        self._player = Spaceship()
        self._game_clock = Clock(game_assets.get_asset_font('slkscr.ttf'))
        self._menu = Menu() # integrates menu system used by the game
        self._game_music = game_assets.get_asset_music("game_music.mp3")
        set_music_volume(self._game_music, 0.4)
        self._is_music_playing = False
        # Mapping temperature ranges to asteroid type spawning chances that will be applied to the game
        self._temperature_to_asteroid_chance = {(-float('inf'), -16) : {"normal" : 20, "icy" : 80, "fiery" : 0}, (-15, -1) : 
        {"normal" : 30, "icy" : 70, "fiery" : 0}, (0, 32) : {"normal" : 40, "icy" : 60, "fiery" : 0}, (33, 49) : 
        {"normal" : 55, "icy" : 40, "fiery" : 0}, (50, 65) : {"normal" : 70, "icy" : 15, "fiery" : 15}, 
        (66, 70) : {"normal" : 15, "icy" : 20, "fiery" : 65 }, (71, 79) : {"normal" : 25, "icy" : 0, "fiery" : 75 }, 
        (76, 200) : {"normal" : 5, "icy" : 0, "fiery" : 95 }}
        # used to make a random name
        self._char_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        # be sure to position input box near the difficulty button
        self._user_input_box = InputBox(Vector2(WINDOW_WIDTH/2 - 300, 365), game_assets.get_asset_font('slkscr.ttf'), 40, 600, 80, 18, RED, WHITE, BLACK)

    def start_music(self):
        if not self._is_music_playing:
            play_music_stream(self._game_music)
            self._is_music_playing = True

    def stop_music(self): 
        if self._is_music_playing:
            stop_music_stream(self._game_music)
            self._is_music_playing = False
    
    # Resets the game state (e.g., score, time, and objects)
    def reset_game(self):
        # the score and time lasted are stored along with a randomly generated name
        random_name = ''.join(choices(self._char_string, k=4)) 
        score = self._player._score_tracker.get_current_points()
        time = self._game_clock.get_current_time()
        # in the leaderboard menu of the game menu class, add the users data
        # new score can simply be added to the end of the leaderboard if its less than 5 players
        if len(self._menu._leaderboard) < 5:
            self._menu._leaderboard.append((random_name, score, time))
        # if there are already 5 entries on the leaderboard, only add 
        elif score >= self._menu._leaderboard[-1][1]:
            # this assumes leaderboard is sorted already
            # remove the last element through list slicing
            # add the new data to the end
            # note: a function in the menu class with resort as necessary
            self._menu._leaderboard = self._menu._leaderboard[:-1]
            self._menu._leaderboard.append((random_name, score, time))
        # reset stars and asteroid list, and reset spawn rates and cycles
        self._stars_list.clear()
        self.make_stars()
        self._asteroids_list.clear()
        self._max_asteroids = 6
        self._max_speed_range_custom = self._max_speed_range_default 
        self._asteroid_spawn_cycle = 0
        self._asteroid_speed_cycle = 0
        self._asteroid_spawn_timer = Timer(4, True, False, self.capped_asteroid_spawn_timer)
        self._asteroid_speed_increase_timer = Timer(10, True, False, self.capped_asteroid_speed_timer)
        # clear powerup and treasure list
        self._power_ups.clear()
        self._treasure.clear()
        # reset player start 
        self._player.reset_player()
        self._game_clock.reset_time()
        # player should now be on death screen, where they can either exit or go to main menu
        self._menu._in_death_menu = True
        self._menu._start_game = False
        game_over = game_assets.get_asset_sound("game_over.wav")
        set_sound_volume(game_over, 0.2)
        play_sound(game_over)
        self.stop_music()
       
    def capped_asteroid_speed_timer(self):
        if self._asteroid_speed_cycle < 6:
            self._asteroid_speed_cycle += 1
            # updates the low end and the high end of the speed range by 70 for each speed cycle increase
            for i in range(len(self._max_speed_range_default)): 
                self._max_speed_range_default[i] += 70
            # print(f"Speed cycle {self._asteroid_speed_cycle}: Max asteroids = {self._max_speed_range_default}")

    def capped_asteroid_spawn_timer(self):
        # For a certain number of times, increase the max asteroids on screen by 2
        if self._asteroid_spawn_cycle < 7:
            self._asteroid_spawn_cycle += 1
            self._max_asteroids += 2
            # print(f"Spawn cycle {self._asteroid_spawn_cycle}: Max asteroids = {self._max_asteroids}")

    def initiate_asteroid_spawning_mechanics(self):
        # only begin increasing asteroid speeds after the spawn cycle increases have completed
        if self._asteroid_spawn_cycle == 7:
            self._asteroid_speed_increase_timer.active = True
            self._asteroid_speed_increase_timer.update()
        else:
            self._asteroid_spawn_timer.active = True
            self._asteroid_spawn_timer.update()
            
    def make_stars(self):
        for i in range(50):
            random_star_pos = Vector2(randint(0,WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
            self._stars_list.append(Star(game_assets.get_asset_texture('star.png'), random_star_pos, 0, Vector2(15,15), Vector2(0,0)))

    def draw_outer_space(self):
        # draws all the twinkling stars in the background
        for star in (self._stars_list):
            star.dynamically_grow()
            star.movement_update(Vector2(0,0), 0, Vector2(0, 0), WHITE)

    def draw_treasure(self):
        # choose a random treasure texture
        treasure_variations = choice(['diamond.png', 'emerald.png', 'emerald.png', 'ruby.png', 'iron.png', 'iron.png', 'iron.png', 'iron.png', 'emerald.png', 'ruby.png', 'iron.png'])
        treasure_speed = 200

        # only allow one treasure object to be on the screen at one time
        if len(self._treasure) < 1:
            random_treasure_pos = Vector2(randint(20, WINDOW_WIDTH - 60), randint(-4000, -1000)) 
            treasure_direction =  Vector2(0, 1)
            # create a treasure object with a random texture, position and direction
            treasure = Treasure(random_treasure_pos, treasure_speed, treasure_direction)
            treasure.set_texture(game_assets.get_asset_texture(treasure_variations))
            self._treasure += [treasure]
        for treasure in self._treasure[:]:
            # remove treasure objects as they exit the sides of the screens
            treasure.movement_update(treasure.get_direction(), 0, Vector2(0, 0), WHITE)
            pos = treasure.get_position()
            if pos.y > WINDOW_HEIGHT:
                self._treasure.remove(treasure)

    def determine_asteroids_temperature_chance(self):
        # get the current game_temperature instance variable
        temperature = self._game_temperature_custom
       # Default asteroid spawn distribution if temperature doesn't match any range
        chances = {"normal" : 33, "icy" : 33, "fiery" : 34}
        for temp_range in self._temperature_to_asteroid_chance:
            # look through each key and check if the temperature is within any one the rnages
            if temp_range[0] <= temperature <= temp_range[1]:
                # If a matching range is found, update the chances accordingly
                chances = self._temperature_to_asteroid_chance[temp_range]
                break
        return chances

    def draw_asteroids(self):
        # Determine the type chances based on the current temperature conditions
        type_chances = self.determine_asteroids_temperature_chance()
        # Select an asteroid type based on the determined chances
        asteroid_type = choices(["normal", "icy", "fiery"],weights=[type_chances["normal"], type_chances["icy"], type_chances["fiery"]],k=1)[0]

        if len(self._asteroids_list) < self._max_asteroids:
            random_asteroid_pos = Vector2(randint(-15, WINDOW_WIDTH + 30), randint(-100, -50)) 
            random_asteroid_speed = randint(self._max_speed_range_default[0], self._max_speed_range_default[1])
            random_asteroid_direction =  Vector2(randint(-1,1), 1) 
            # different skins of the asteroid based on what type
            if asteroid_type == "fiery":
                current_asteroid = Asteroid(random_asteroid_pos, random_asteroid_speed, random_asteroid_direction, Vector2(101, 84), game_assets.get_asset_texture('fiery_meteor.png'))
            elif asteroid_type == "icy":
                current_asteroid = Asteroid(random_asteroid_pos, random_asteroid_speed, random_asteroid_direction, Vector2(101, 84), game_assets.get_asset_texture('icy_meteor.png'))
            else: 
                current_asteroid = Asteroid(random_asteroid_pos, random_asteroid_speed, random_asteroid_direction)
            self._asteroids_list += [current_asteroid]
        
        # update the position of each asteroid on the screen, and remove those that go off screen
        for asteroid in self._asteroids_list[:]:
            asteroid.dynamically_rotate()
            asteroid.project_asteroid() 
        
            pos = asteroid.get_position()
            if pos.y > WINDOW_HEIGHT or (pos.x < -15 or pos.x > WINDOW_WIDTH + 30):
                self._asteroids_list.remove(asteroid)
    
    def draw_power_ups(self):
        select_pwrup = choice(["O2", "O2", "O2", "O2", "O2", "HP", "HP", "HP", "Ammo", "Ammo", "Ammo", "Ammo", "Ammo"])
        pwrup_speed = 300

        # based on the powerup choice, use a dictionary to 
        # determine the type of powerup object to spawn, as well as the specified direction
        self._power_up_stats = {"O2" : {"class" : O2_PowerUP, "rarity" : 13, "pos" : Vector2(randint(20, WINDOW_WIDTH - 60), 
        randint(-1500, -500)), "direction" : Vector2(0,1)}, "Ammo" :{"class" : Ammo_PowerUP, "rarity" : 4, "pos" : Vector2(randint(-3000, -500), 
        randint(20, WINDOW_HEIGHT - 60)), "direction" : Vector2(1,0)}, "HP" : {"class" : HeartCapsule_PowerUP, "rarity" : 1, 
        "pos" : Vector2(randint(WINDOW_WIDTH, 3000), randint(20, WINDOW_HEIGHT - 60)), "direction" : Vector2(-1,0)}}
        
        if len(self._power_ups) < 1 and not any(isinstance(pwrup, self._power_up_stats[select_pwrup]["class"]) for pwrup in self._power_ups):
            select_pwrup_stats = self._power_up_stats[select_pwrup]
            self._power_ups.append(select_pwrup_stats["class"](select_pwrup_stats["pos"], pwrup_speed, select_pwrup_stats["direction"]))

        # check when powerups leave the screen and remove as necessary
        # O2 Power ups fall downwards, Ammo moves right, Hearts move left
        for power_up in self._power_ups[:]:
            power_up.movement_update(power_up.get_direction(), 0, Vector2(0, 0), WHITE)
            pos = power_up.get_position()
            if isinstance(power_up, O2_PowerUP):
                if pos.y > WINDOW_HEIGHT:
                    self._power_ups.remove(power_up)
            elif isinstance(power_up, Ammo_PowerUP):
                if pos.x > WINDOW_WIDTH:
                    self._power_ups.remove(power_up)
            elif isinstance(power_up, HeartCapsule_PowerUP):
                if pos.x < -15:
                    self._power_ups.remove(power_up)

    # handles asteroid collisions with player and lasers 
    def asteroid_collision_check(self):
         for asteroid in self._asteroids_list:
            # create an asteroid bounding circle and player bounding triangle for checking collisions
            asteroid_hitbox = Rectangle(asteroid.get_position().x - asteroid._sprite_texture.width / 2, asteroid.get_position().y - asteroid._sprite_texture.width / 2, asteroid.get_size().x, asteroid.get_size().y)
            center = Vector2(int(asteroid.get_position().x), int(asteroid.get_position().y))
            radius = asteroid_hitbox.width / 2
            player_hitbox = Rectangle(self._player.get_position().x, self._player.get_position().y, self._player.get_size().x, self._player.get_size().y)
            v1 = Vector2(player_hitbox.x + player_hitbox.width/2, player_hitbox.y - 8)
            v2 = Vector2(player_hitbox.x , player_hitbox.y + player_hitbox.height)
            v3 = Vector2(player_hitbox.x + player_hitbox.width, player_hitbox.y + player_hitbox.height)
            #draw_circle_lines(int(center.x), int(center.y), radius, PURPLE) for debugging (asteroid collision circles)
            #draw_triangle_lines(v1,v2,v3,RED) for debugging (player collision triangle)

            # end game if player oxygen meter reaches zero
            if self._player._oxygen_meter.get_current_oxygen_level() == 0:
                self.reset_game()

            # check if asteroid type object collides with player
            if check_collision_circle_line(center, radius, v1, v2) or check_collision_circle_line(center, radius, v1, v3) or check_collision_circle_line(center, radius, v2, v3): # check_collision_recs(asteroid_hitbox, player_hitbox):
                crash = game_assets.get_asset_sound("crash.wav")
                set_sound_volume(crash, 0.2)
                self._asteroids_list.remove(asteroid)
                # resets the player points when hit by asteroid and depending on asteroid type take a certain amount of damage

                self._player.get_player_points().reset_multiplier()
                if asteroid.get_texture() ==  game_assets.get_asset_texture('fiery_meteor.png'):
                    for i in range(3):
                        self._player.take_damage()
                    play_sound(crash)
                elif asteroid.get_texture() ==  game_assets.get_asset_texture('icy_meteor.png'):
                    self._player.freeze_player()
                    # player._unfreeze_player_timer.activate()
                    self._player.take_damage()
                else:
                    for i in range(2):
                        self._player.take_damage()
                    play_sound(crash)
                if self._player._current_health == 0:
                    self.reset_game() # test game end

            # destroy lasers upon contact with asteroids and remove from the screen 
            for laser in self._player.get_lasers():
                laser_hitbox = Rectangle(laser.get_position().x, laser.get_position().y, laser.get_size().x, laser.get_size().y)
                if check_collision_circle_rec(center, radius, laser_hitbox):
                    self._player._laser_projectiles.remove(laser)
                
    def collect_item(self, item, collect_sfx):
        sound = game_assets.get_asset_sound(collect_sfx)
        set_sound_volume(sound, 0.5)
        play_sound(sound)
        self._power_ups.remove(item)

    def powerup_collision_check(self):
        for powerup in self._power_ups:
            # create bounding box for both powerup and player to check collisions
            power_up_hitbox = Rectangle(powerup.get_position().x, powerup.get_position().y, powerup.get_size().x, powerup.get_size().y)
            player_hitbox = Rectangle(self._player.get_position().x, self._player.get_position().y, self._player.get_size().x, self._player.get_size().y)
            # draw_rectangle_lines_ex(power_up_hitbox, 1, RED) (for debugging powerup hitbox)

            # handles behavior for collisions, different player stats are effected based on the 
            # type (or texture) of the powerup

            if check_collision_recs(power_up_hitbox, player_hitbox):
                # O2 powerups can only be collective if they have been unlocked after
                # being shot by laser
                if isinstance(powerup, O2_PowerUP) and powerup.get_lock_status() == False:
                    self._player.get_oxygen_meter().increase_oxygen()
                    self.collect_item(powerup, "bubble.wav")
                    self._player.get_player_points().increase_points(50)
                    self._player.get_player_points().increase_multiplier(.1)
                elif isinstance(powerup, Ammo_PowerUP):
                    self._player.increase_ammo()
                    self.collect_item(powerup, "ammo_collect.wav")
                    self._player.get_player_points().increase_points(50)
                    self._player.get_player_points().increase_multiplier(.1)
                elif isinstance(powerup, HeartCapsule_PowerUP):
                    self._player.increase_health()
                    self.collect_item(powerup, "heart_collect.wav")
                    self._player.get_player_points().increase_points(50)
                    self._player.get_player_points().increase_multiplier(.1)

            # handle behavior for lasers shooting and unlocking an O2 powerup
            for laser in self._player.get_lasers():
                laser_hitbox = Rectangle(laser.get_position().x, laser.get_position().y, laser.get_size().x, laser.get_size().y)
                # draw_rectangle_lines_ex(laser_hitbox, 1, GREEN)
                if isinstance(powerup, O2_PowerUP) and powerup.get_lock_status() == True and check_collision_recs(power_up_hitbox, laser_hitbox):
                    explosion = game_assets.get_asset_sound("explosion.wav")
                    set_sound_volume(explosion, 0.1)
                    play_sound(explosion)
                    powerup.change_lock_status(False)
                    self._player._laser_projectiles.remove(laser)

    def treasure_collision_check(self):
        # points assigned for each treasure type
        treasure_points = {game_assets.get_asset_texture("iron.png"): 50, game_assets.get_asset_texture("diamond.png"): 200,
        game_assets.get_asset_texture("emerald.png"): 100, game_assets.get_asset_texture("ruby.png"): 75}
        for treasure in self._treasure[:]:
            # make a collision bounding box and a player bounding to check collisions
            treasure_hitbox = Rectangle(treasure.get_position().x, treasure.get_position().y, treasure.get_size().x, treasure.get_size().y)
            player_hitbox = Rectangle(self._player.get_position().x, self._player.get_position().y, self._player.get_size().x, self._player.get_size().y)
            # draw_rectangle_lines_ex(treasure_hitbox, 1, RED) for debugging
            if check_collision_recs(treasure_hitbox, player_hitbox):
                # if there's a collision, play a collect sfx, remove treasure, and increase 
                # player points and score multiplier
                collect = game_assets.get_asset_sound("treasure_collect.wav")
                set_sound_volume(collect, 0.2)
                play_sound(collect)
                self._treasure.remove(treasure)
                self._player.get_player_points().increase_points(treasure_points[treasure.get_texture()])
                self._player.get_player_points().increase_multiplier(.1)
                        
    def initialize_collision_checks(self):
        self.asteroid_collision_check()
        self.powerup_collision_check()
        self.treasure_collision_check()

    def spawn_obstacles_collectibles(self):
        self.initiate_asteroid_spawning_mechanics()
        self.draw_asteroids()
        self.draw_power_ups()
        self.draw_treasure()
        self.draw_outer_space()

    def initialize_game(self):
        self.spawn_obstacles_collectibles()
        self._player.initialize_player_mechanics()
        self._game_clock.run_clock()
        self.initialize_collision_checks()
        self.start_music()
        update_music_stream(self._game_music)
    
    def display_loading_screen(self):
        loading_texture = game_assets.get_asset_texture("loading_screen.png")
        loading_texture_source = Rectangle(0, 0, loading_texture.width, loading_texture.height)
        loading_texture_dest = Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        draw_texture_pro(loading_texture, loading_texture_source,loading_texture_dest, Vector2(), 0, WHITE)

    def should_exit_menu_status(self):
        return self._menu._exit_clicked

    # API integration
    def change_game_difficulty(self, city): # city is the user input variable stored in self._text_to_save of the InputBox when pressing enter after typing
        city_data = get_city_temp_wspd(city)
        if "temperature" in city_data and "windspeed" in city_data:
            # A correct return from the get_city_temp_wdsp looks like: {'temperature': 42, 'windspeed': 2} for some city
            wind_speed_range = [city_data["windspeed"] * 100, city_data["windspeed"] * 100 + 50] # create some arbrituary range based on the city windspeed
            self._city_custom = city
            self._game_temperature_custom = city_data["temperature"] # temperature returned
            self._max_speed_range_custom = wind_speed_range # speed range returned
        else:
            self._city_custom = self._city_default
            self._game_temperature_custom =  self._game_temperature_default
            self._max_speed_range_custom = self._max_speed_range_default
    
    def run(self):
        while not window_should_close() and not self.should_exit_menu_status():
            begin_drawing()
            clear_background(BG_COLOR)
            if self._menu._in_main_menu: 
                self._menu.run_menu()
                self._user_input_box.reset_input_box()
            elif self._menu._in_death_menu:
                self._menu.run_death_menu()
            elif self._menu._in_leaderboard:
                self._menu.run_leaderboard_menu()
            elif self._menu._in_options:
                self._menu.run_options_menu()
                self._menu.draw_difficulty_information(self._city_custom, str(self._game_temperature_custom), str(self._max_speed_range_custom))
                if self._menu._difficulty_clicked: # only display input_box if difficulty button hasn't been clicked already
                    self._user_input_box.enable_input_box()
                    if self._user_input_box._enter_is_pressed:
                        city_typed = self._user_input_box._text_to_save
                        self.change_game_difficulty(city_typed)
                        self._user_input_box.reset_input_box() # reset _text_to_save and _input_text ui, as well as enter_is_pressed
            elif self._menu._start_game:
                self.initialize_game()
            else:
                self.display_loading_screen()
                self._menu._start_timer.update()
            end_drawing()
        game_assets.unload()
        close_audio_device()
        close_window()
    

if __name__ == '__main__': # REMOVE LATER: replace with diffuclty setting by user input in-game
    # test with api
    """
    user_input = "Lawrenceville" # str(input("Enter a city: "))
    city_data = get_city_temp_wspd(user_input)
    temp_key = user_input + " temperature"
    wind_key = user_input + " wind speed"
    wind_speed_range = [city_data[wind_key] * 100, city_data[wind_key] * 100 + 50]
    game_test = SpaceGame(user_input, city_data[temp_key], wind_speed_range)
    game_test.run() # fix this function, this is the master function that involves the menu
    """
    game_test = SpaceGame()
    game_test.run() 
