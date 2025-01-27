from sprites import *


class SpaceGame():
    def __init__(self):
        self._stars = []
        self.make_stars()
        self._asteroids = []
        self._max_asteroids = 6
        self._max_speed_range = [200,250]
        self._asteroid_spawn_cycle = 0 
        self._asteroid_speed_cycle = 0
        self._asteroid_spawn_timer = Timer(4, True, True, self.capped_asteroid_spawn_timer)
        self._asteroid_speed_increase_timer = Timer(10, True, False, self.capped_asteroid_speed_timer)
        self._power_ups = []
        self._treasure = []
        self._players = [Spaceship()]
        self._game_clock = Clock(game_sprites.get_global_font('slkscr.ttf'))
        self._menu = Menu()

    def reset_game(self):
        self._stars.clear()
        self.make_stars()
        self._asteroids.clear()
        self._max_asteroids = 6
        self._max_speed_range = [200,250]
        self._asteroid_spawn_cycle = 0
        self._asteroid_speed_cycle = 0
        self._asteroid_spawn_timer = Timer(4, True, True, self.capped_asteroid_spawn_timer)
        self._asteroid_speed_increase_timer = Timer(10, True, False, self.capped_asteroid_speed_timer)
        self._asteroid_speed_increase_timer.active = False
        self._power_ups.clear()
        self._treasure.clear()
        for player in self._players:
            player.reset_player()
        self._game_clock.reset_time()
        self._menu._in_death_menu = True

    def capped_asteroid_speed_timer(self):
        if self._asteroid_speed_cycle < 6:
            self._asteroid_speed_cycle += 1
            for i in range(len(self._max_speed_range)): 
                self._max_speed_range[i] += 70
            #print(f"Speed cycle {self._asteroid_speed_cycle}: Max asteroids = {self._max_speed_range}")

    def capped_asteroid_spawn_timer(self):
        if self._asteroid_spawn_cycle < 7:
            self._asteroid_spawn_cycle += 1
            self._max_asteroids += 2
            #print(f"Spawn cycle {self._asteroid_spawn_cycle}: Max asteroids = {self._max_asteroids}")

    def initiate_asteroid_spawning_mechanics(self):
        if self._asteroid_spawn_cycle == 7:
            self._asteroid_speed_increase_timer.activate()
            self._asteroid_speed_increase_timer.update()
        else:
            self._asteroid_spawn_timer.update()
            
    def make_stars(self):
        for i in range(50):
            random_star_pos = Vector2(randint(0,WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
            self._stars.append(Star(game_sprites.get_global_texture('star.png'), random_star_pos, 0, Vector2(15,15), Vector2(0,0)))

    def draw_outer_space(self):
        for star in (self._stars):
            star.dynamically_grow()
            star.movement_update(Vector2(0,0), 0, Vector2(0, 0), WHITE)

    def draw_treasure(self):
        treasure_variations = choice(['diamond.png', 'emerald.png', 'emerald.png', 'ruby.png', 'iron.png', 'iron.png', 'iron.png', 'iron.png', 'emerald.png', 'ruby.png', 'iron.png'])
        treasure_speed = 200
        if len(self._treasure) < 1:
            random_treasure_pos = Vector2(randint(20, WINDOW_WIDTH - 60), randint(-4000, -1000)) 
            treasure_direction =  Vector2(0, 1)
            treasure = Treasure(random_treasure_pos, treasure_speed, treasure_direction)
            treasure.set_texture(game_sprites.get_global_texture(treasure_variations))
            self._treasure += [treasure]
        for treasure in self._treasure[:]:
            treasure.movement_update(treasure.get_direction(), 0, Vector2(0, 0), WHITE)
            pos = treasure.get_position()
            if pos.y > WINDOW_HEIGHT:
                self._treasure.remove(treasure)

    def draw_asteroids(self):
        if len(self._asteroids) < self._max_asteroids:
            random_asteroid_pos = Vector2(randint(-15, WINDOW_WIDTH + 30), randint(-100, -50)) 
            random_asteroid_speed = randint(self._max_speed_range[0], self._max_speed_range[1])
            random_asteroid_direction =  Vector2(randint(-1,1), 1) 
            select_asteroid = randint(0,4)
            if select_asteroid > 0:
                current_asteroid = Asteroid(random_asteroid_pos, random_asteroid_speed, random_asteroid_direction)
            else:
                current_asteroid = Asteroid(random_asteroid_pos, random_asteroid_speed, random_asteroid_direction, Vector2(101, 84), game_sprites.get_global_texture('fiery_meteor.png'))
            self._asteroids += [current_asteroid]

        for asteroid in self._asteroids[:]:
            asteroid.dynamically_rotate()
            asteroid.project_asteroid() 
        
            pos = asteroid.get_position()
            if pos.y > WINDOW_HEIGHT or (pos.x < -15 or pos.x > WINDOW_WIDTH + 30):
                self._asteroids.remove(asteroid)
    
    def draw_power_ups(self):
        select_pwrup = choice(["O2", "O2", "O2", "O2", "O2", "HP", "HP", "HP", "Ammo", "Ammo", "Ammo", "Ammo", "Ammo"])
        pwrup_speed = 300

        self._power_up_stats = {"O2" : {"class" : O2_PowerUP, "rarity" : 13, "pos" : Vector2(randint(20, WINDOW_WIDTH - 60), 
        randint(-1500, -500)), "direction" : Vector2(0,1)}, "Ammo" :{"class" : Ammo_PowerUP, "rarity" : 4, "pos" : Vector2(randint(-3000, -500), 
        randint(20, WINDOW_HEIGHT - 60)), "direction" : Vector2(1,0)}, "HP" : {"class" : HeartCapsule_PowerUP, "rarity" : 1, 
        "pos" : Vector2(randint(WINDOW_WIDTH, 3000), randint(20, WINDOW_HEIGHT - 60)), "direction" : Vector2(-1,0)}}
        
        if len(self._power_ups) < 1 and not any(isinstance(pwrup, self._power_up_stats[select_pwrup]["class"]) for pwrup in self._power_ups):
            select_pwrup_stats = self._power_up_stats[select_pwrup]
            self._power_ups.append(select_pwrup_stats["class"](select_pwrup_stats["pos"], pwrup_speed, select_pwrup_stats["direction"]))

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

    def asteroid_collision_check(self):
         for asteroid in self._asteroids:
            asteroid_hitbox = Rectangle(asteroid.get_position().x - asteroid._sprite_texture.width / 2, asteroid.get_position().y - asteroid._sprite_texture.width / 2, asteroid.get_size().x, asteroid.get_size().y)
            center = Vector2(int(asteroid.get_position().x), int(asteroid.get_position().y))
            radius = asteroid_hitbox.width / 2
            #draw_circle_lines(int(center.x), int(center.y), radius, PURPLE)
            for player in self._players:
                player_hitbox = Rectangle(player.get_position().x, player.get_position().y, player.get_size().x, player.get_size().y)
                v1 = Vector2(player_hitbox.x + player_hitbox.width/2, player_hitbox.y - 8)
                v2 = Vector2(player_hitbox.x , player_hitbox.y + player_hitbox.height)
                v3 = Vector2(player_hitbox.x + player_hitbox.width, player_hitbox.y + player_hitbox.height)
                #draw_triangle_lines(v1,v2,v3,RED)
                if player._spaceship_oxygen.get_current_oxygen_level() == 0:
                    self.reset_game()
                if check_collision_circle_line(center, radius, v1, v2) or check_collision_circle_line(center, radius, v1, v3) or check_collision_circle_line(center, radius, v2, v3): # check_collision_recs(asteroid_hitbox, player_hitbox):
                    crash = game_sprites.get_global_sound("crash.wav")
                    set_sound_volume(crash, 0.4)
                    play_sound(crash)
                    self._asteroids.remove(asteroid)
                    player.get_player_points().reset_multiplier()
                    if asteroid.get_texture() ==  game_sprites.get_global_texture('fiery_meteor.png'):
                        for i in range(3):
                            player.take_damage()
                    else:
                        player.take_damage()
                    if player._current_hp == 0:
                        self.reset_game() # test game end
                for laser in player.get_lasers():
                    laser_hitbox = Rectangle(laser.get_position().x, laser.get_position().y, laser.get_size().x, laser.get_size().y)
                    if check_collision_circle_rec(center, radius, laser_hitbox):
                        player._lasers.remove(laser)

    def collect_item(self, item, collect_sfx):
        sound = game_sprites.get_global_sound(collect_sfx)
        set_sound_volume(sound, 0.5)
        play_sound(sound)
        self._power_ups.remove(item)

    def powerup_collision_check(self):
        for powerup in self._power_ups:
            power_up_hitbox = Rectangle(powerup.get_position().x, powerup.get_position().y, powerup.get_size().x, powerup.get_size().y)
            # draw_rectangle_lines_ex(power_up_hitbox, 1, RED)
            for player in self._players:
                player_hitbox = Rectangle(player.get_position().x, player.get_position().y, player.get_size().x, player.get_size().y)
                if check_collision_recs(power_up_hitbox, player_hitbox):
                    if isinstance(powerup, O2_PowerUP) and powerup.get_lock_status() == False:
                        player.get_oxygen_meter().increase_oxygen()
                        self.collect_item(powerup, "bubble.wav")
                        player.get_player_points().increase_points(50)
                        player.get_player_points().increase_multiplier(.1)
                    elif isinstance(powerup, Ammo_PowerUP):
                        player.increase_ammo()
                        self.collect_item(powerup, "ammo_collect.wav")
                        player.get_player_points().increase_points(50)
                        player.get_player_points().increase_multiplier(.1)
                    elif isinstance(powerup, HeartCapsule_PowerUP):
                        player.increase_health()
                        self.collect_item(powerup, "heart_collect.wav")
                        player.get_player_points().increase_points(50)
                        player.get_player_points().increase_multiplier(.1)
                for laser in player.get_lasers():
                    laser_hitbox = Rectangle(laser.get_position().x, laser.get_position().y, laser.get_size().x, laser.get_size().y)
                    # draw_rectangle_lines_ex(laser_hitbox, 1, GREEN)
                    if isinstance(powerup, O2_PowerUP) and powerup.get_lock_status() == True and check_collision_recs(power_up_hitbox, laser_hitbox):
                        explosion = game_sprites.get_global_sound("explosion.wav")
                        set_sound_volume(explosion, 0.1)
                        play_sound(explosion)
                        powerup.change_lock_status(False)
                        player._lasers.remove(laser)

    def treasure_collision_check(self):
        treasure_points = {game_sprites.get_global_texture("iron.png"): 50, game_sprites.get_global_texture("diamond.png"): 200,
        game_sprites.get_global_texture("emerald.png"): 100, game_sprites.get_global_texture("ruby.png"): 75}
        for treasure in self._treasure[:]:
            treasure_hitbox = Rectangle(treasure.get_position().x, treasure.get_position().y, treasure.get_size().x, treasure.get_size().y)
            # draw_rectangle_lines_ex(treasure_hitbox, 1, RED)
            for player in self._players:
                player_hitbox = Rectangle(player.get_position().x, player.get_position().y, player.get_size().x, player.get_size().y)
                if check_collision_recs(treasure_hitbox, player_hitbox):
                        collect = game_sprites.get_global_sound("treasure_collect.wav")
                        set_sound_volume(collect, 0.8)
                        play_sound(collect)
                        self._treasure.remove(treasure)
                        player.get_player_points().increase_points(treasure_points[treasure.get_texture()])
                        player.get_player_points().increase_multiplier(.1)
                        
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
        for player in self._players:
            player.initialize_player_mechanics()
        self._game_clock.run_clock()
        self.initialize_collision_checks()

    def get_menu_status(self):
        return self._menu._in_menu
    
    def should_exit_menu_status(self):
        return self._menu._exit_clicked

    def run(self):
        while not window_should_close() and not self.should_exit_menu_status():
            begin_drawing()
            clear_background(BG_COLOR)
            if self.get_menu_status() == True:
                self._menu.run_menu()
            elif self._menu._in_death_menu == True:
                self._menu.run_death_menu()
            else:
                self.initialize_game()
                #print(len(self._asteroids))
            end_drawing()
        game_sprites.unload()
        close_audio_device()
        close_window()
    
class Menu():
    def __init__(self):
        self._buttons = {}
        self._in_menu = True
        self._in_death_menu = False
        self._exit_clicked = False
        self._leaderboard = []
        self._title = "untitled asteroids game"
        self.create_buttons()

    def create_buttons(self):
        self._buttons["start"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 450), 620, 80, "START", game_sprites.get_global_font('slkscreb.ttf'), 60)
        self._buttons["stats"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 550), 620, 80, "LEADERBOARD", game_sprites.get_global_font('slkscreb.ttf'), 60)
        self._buttons["exit"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 650), 620, 80, "EXIT", game_sprites.get_global_font('slkscreb.ttf'), 60)
        self._buttons["main menu"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 550 ), 620, 80, "MAIN MENU", game_sprites.get_global_font('slkscreb.ttf'), 60)
    
    def draw_buttons(self):
        if self._in_menu == True:
            self._buttons["start"].draw_text_rectangle(RED, BLACK)
            self._buttons["stats"].draw_text_rectangle(RED, BLACK)
        elif self._in_death_menu:
            self._buttons["main menu"].draw_text_rectangle(RED, BLACK)
        self._buttons["exit"].draw_text_rectangle(RED, BLACK)

    def draw_title(self):
        title_text_dimensions = measure_text_ex(game_sprites.get_global_font('slkscreb.ttf'), self._title, 80, 0)
        centered_title_width = (WINDOW_WIDTH - title_text_dimensions.x) / 2
        draw_text_ex(game_sprites.get_global_font('slkscreb.ttf'), self._title, Vector2(centered_title_width, 120), 80, 0, WHITE)

    def play_button_click_sfx(self):
        button_click = game_sprites.get_global_sound("button_click.wav")
        set_sound_volume(button_click, 0.4)
        play_sound(button_click)

    def check_button_clicks(self):
        if self._in_menu:
            if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["start"].get_rectangle()):
                self._in_menu = False
                self.play_button_click_sfx()
        elif self._in_death_menu:
            if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["main menu"].get_rectangle()):
                self._in_death_menu = False
                self._in_menu = True
                self.play_button_click_sfx()
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["exit"].get_rectangle()):
            self._exit_clicked = True

    def run_menu(self):
        self.draw_buttons()
        self.draw_title()
        self.check_button_clicks()

    def run_death_menu(self):
        self.draw_buttons()
        self.check_button_clicks()
        title_text_dimensions = measure_text_ex(game_sprites.get_global_font('slkscreb.ttf'), "GAME OVER", 200, 0)
        centered_title_width = (WINDOW_WIDTH - title_text_dimensions.x) / 2
        centered_title_height = (WINDOW_HEIGHT - title_text_dimensions.y) / 2
        draw_text_ex(game_sprites.get_global_font('slkscreb.ttf'), "GAME OVER", Vector2(centered_title_width, int(centered_title_height / 1.5)), 200, 0, WHITE)

if __name__ == '__main__':
    game_test = SpaceGame()
    game_test.run()
    

# save game data, but also delete previous game data (create new Spacegame object) (implement leaderboard)
# intro tutorial screen (brief timers to each)

# add menu and game music
# go back and refractor code
# go back and comment
# adjust game diffuclty as need