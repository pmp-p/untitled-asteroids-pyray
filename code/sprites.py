from Settings import *
from MyTimer import Timer
from random import randint
from Assets import *


class Sprite2D():
    """
    represents a 2D sprite, which could be either moving or stationary.

    Attributes:
    pos: Position, represented by a Vector2 object with x and y specifications
    speed: Speed, given by an integer
    size: Size, represented represented by a Vector2 object with x and y specifications
    direction: Direction, represented by a Vector2 object with x and y specifications
    texture: Texture, represented by a Texture2D object
    """
    def __init__(self, pos, speed, size, direction, texture):
        self._pos = pos
        self._speed = speed
        self._size = size
        self._direction = direction
        self._sprite_texture = texture

    def get_position(self):
        return self._pos
    
    def get_speed(self):
        return self._speed

    def get_size(self):
        return self._size
    
    def get_direction(self):
        return self._direction

    def get_texture(self):
        return self._sprite_texture
    
    # This method updates the position of the sprite each frame based on its direction and speed.
    def update_pos(self):
        deltatime = get_frame_time() # deltatime (time passed since last frame), used to ensure consistent movement regardless of framerate
        self._pos.x += self._direction.x * self._speed * deltatime
        self._pos.y += self._direction.y * self._speed * deltatime

    def set_direction(self, direction):
        self._direction = direction

    def set_texture(self, texture):
        self._sprite_texture = texture

    # draw the sprites current frame based on the updated position and current direction
    def movement_update(self,direction_vector, rotation, origin, tint):
        self.set_direction(direction_vector)
        self.update_pos()

        # The source_rect defines the portion of the texture to draw
        # The dest_rect defines where the sprite will be drawn on the screen
        source_rect = Rectangle(0,0, self.get_texture().width, self.get_texture().height)
        dest_rect = Rectangle(self.get_position().x,self.get_position().y, self._size.x, self._size.y)

        draw_texture_pro(self.get_texture(), source_rect, dest_rect, origin, rotation, tint)

        # draw_rectangle_lines(int(self.get_position().x), int(self.get_position().y), int(self._size.x), int(self._size.y), GREEN ) for debugging to see hitboxes

class Spaceship(Sprite2D):
    """
    Spaceship controlled by the player.

    Handles movement, UI (current hp, lasers, oxygen_meter, points), shooting lasers
    and collecting power ups to increase stats. Includes behavior for game world 
    interactions (ex, taking damage from an asteroid, being frozen by and icy asteroid,
    boundaries).
    """
    def __init__(self, texture=game_assets.get_asset_texture('green_ship.png'), pos=Vector2(WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2), speed=PLAYER_SPEED, size=Vector2(112,75), direction=Vector2()):
        super().__init__(pos, speed, size, direction, texture)
        self._laser_projectiles = [] # list of laser objects fired
        self._health_display = [] # list of heart sprites for HP UI
        self._max_health = 9 # max hp used to fill health bar
        self._current_health = 9 # current hp level
        self.generate_health() # fill self._health_display for HP UI
        self._ammo_display = [] # List of ammo sprites for Ammo UI
        self._current_ammo = 6 # current ammo 
        self._max_ammo = 6 # max ammo to fill self._ammo_display
        self.generate_ammo() # fill self._current_ammo bar for ammo UI
        self._oxygen_meter = OxygenMeter(game_assets.get_asset_font('slkscreb.ttf')) # Oxygen meter UI
        self._score_tracker = Points(game_assets.get_asset_font('slkscreb.ttf')) # Points UI
        self._is_frozen = False 
        self._unfreeze_player_timer = Timer(5, False, False, self.unfreeze_player) # Timer used to unfreeze player

    def freeze_player(self):

        if not self._is_frozen:
            # while the player is frozen, reduce the speed temporarily and start a timer that will
            # unfreeze the player after some time
            self._speed = 200
            self._is_frozen = True
            self._unfreeze_player_timer.activate()
            freeze = game_assets.get_asset_sound("freeze_sfx.wav")
            set_sound_volume(freeze, 0.2)
            play_sound(freeze)
            
    def unfreeze_player(self):
        # restore the players speed to original value
        if self._is_frozen:
            self._speed = PLAYER_SPEED
            self._is_frozen = False

    def reset_player(self):
        # Resets player to their initial state
        # reset ammo, points, health, oxygen displays to default values
        # restore players current health and ammo capacity
        # restore movement speed and starting position
        self._laser_projectiles.clear()
        self._health_display.clear()
        self._current_health = 9
        self.generate_health()
        self._ammo_display.clear()
        self._current_ammo = 6
        self._max_ammo = 6
        self.generate_ammo()
        self._oxygen_meter.reset_oxygen()
        self._score_tracker.reset_points()
        self._pos = Vector2(WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2)
        self._is_frozen = False
        self._speed = PLAYER_SPEED

    def get_current_health(self):
        return self._current_health

    def get_current_ammo(self):
        return self._current_ammo
    
    def get_lasers(self):
        return self._laser_projectiles

    def generate_health(self):
        sprite_offset = 0 # offset to help position heart sprites next to each other in the UI
        for i in range(self.get_current_health()):
            # create a Heart Sprite and add it to the health_display list to be draw later
            current_heart = HP(Vector2(50 + sprite_offset, 1000))
            self._health_display += [current_heart]
            # readjust offset each time based on the hearts size
            sprite_offset += current_heart.get_size().x
    
    def display_hp(self):
        for heart in self._health_display:
            heart.draw_heart()

    def take_damage(self):
        if self.get_current_health() > 0:
            # Switch the right most heart in the UI to be empty sprite texture
            self._health_display[self.get_current_health() - 1].switch_heart_texture(True)
            self._current_health -= 1
        else:
            # Switch the left most heart in the UI to be empty sprite texture
            self._health_display[self.get_current_health()].switch_heart_texture(True)
    
    def increase_health(self):
        if self._current_health < self._max_health:
            # Switch the right most heart in the UI to filled heart sprite texture
            self._health_display[self.get_current_health()].switch_heart_texture(False)
            self._current_health += 1
        else:
            # Switch the left most heart in the UI to filled heart sprite texture
            self._health_display[self.get_current_health() - 1].switch_heart_texture(False)

    def generate_ammo(self):
        # reset the previous ammo ui display
        self._ammo_display.clear()
        # use the offset to position ammo in the UI next to each other
        sprite_offset = 0
        for i in range(self._current_ammo):
            # create a ammo Sprite and add it to the ammo_display list to be draw later
            current_ammo = Ammo(Vector2(60 + sprite_offset, 870))
            self._ammo_display += [current_ammo]
            sprite_offset += current_ammo.get_size().x

    def increase_ammo(self):
        # increase ammo count if possible and redraw the ammo bar with the current ammo amount
        if self.get_current_ammo() < self._max_ammo:
            self._current_ammo += 1
            self.generate_ammo()

    def remove_ammo(self):
        # decrease ammo count if possible and remove the right most ammo from the UI
        if self._current_ammo > 0:
            self._ammo_display.remove(self._ammo_display[-1])
            self._current_ammo -= 1
        else:
            self._ammo_display.remove(self._ammo_display[-1])

    def display_ammo(self):
        for ammo in self._ammo_display:
            ammo.draw_laser_ammo()
            
    def get_oxygen_meter(self):
        return self._oxygen_meter
    
    def drain_spaceship_oxygen(self):
        # Start depleting oxygen level (shown on the UI) every couple of seconds
        self.get_oxygen_meter().run_oxygen_depletion_clock()

    def get_player_points(self):
        return self._score_tracker
    
    def draw_player_points(self):
        # draw the players points and current multiplier on the UI
        self.get_player_points().draw_points()
        self.get_player_points().draw_multiplier()

    def check_window_boundaries(self): 
        """
        Check if the spaceship is within the window boundaries.
        If it goes out of bounds, it is repositioned to stay within the screen.
        """
        x_margin = self.get_texture().width
        y_margin = self.get_texture().height
        if self.get_position().x < 0:  # Left edge
            self._pos.x = 0
        elif self.get_position().x + x_margin > WINDOW_WIDTH:  # Right edge
            self._pos.x = WINDOW_WIDTH - x_margin
        if self.get_position().y < 0:  # Top edge
            self._pos.y = 0
        elif self.get_position().y + y_margin> WINDOW_HEIGHT:  # Bottom edge
            self._pos.y = WINDOW_HEIGHT - y_margin
        
    def shoot_laser(self):
        """
        Handle the player's shooting mechanics.
        The laser is fired when the spacebar is pressed, and ammo is deducted
        A laser sound is played, and lasers are added to the projectiles list
        """
        if is_key_pressed(KEY_SPACE) and len(self.get_lasers()) < 10:
            if self._current_ammo > 0:
                beam = game_assets.get_asset_sound("laser.wav")
                set_sound_volume(beam, 0.5)
                play_sound(beam)
                # create a laser object aligned with the position of the player
                laser_align_pos = Vector2(self.get_position().x + self.get_texture().width / 2 - 3, self.get_position().y - 30)
                current_laser = Laser(laser_align_pos)
                self._laser_projectiles += [current_laser] # laser is added to the current list of lasers on screen
                self.remove_ammo() # ammo is removed from the UI

        # update the position of each laser on the screen and remove them as they go off screen
        for laser in self.get_lasers()[:]: 
            laser.movement_update(laser.get_direction(), 0, Vector2(0, 0), WHITE)
            if laser.get_position().y < 0:
                self._laser_projectiles.remove(laser)
    
    def initialize_player_mechanics(self):
        if self._is_frozen:
            # start the player timer to be unfreezed
            self._unfreeze_player_timer.update()
            # update the ship position based on input; spaceship is tinted blue while frozen
            self.movement_update(Vector2(int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT)), int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))), 0, Vector2(), SKYBLUE)
        else:
            # update ship position based on input
            self.movement_update(Vector2(int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT)), int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))), 0, Vector2(), WHITE)
        # turn on laser shooting, draw ammo and health UI, display draining oxygen, and check window boundaries
        self.shoot_laser()
        self.display_hp()
        self.drain_spaceship_oxygen()
        self.draw_player_points()
        self.display_ammo()
        self.check_window_boundaries()
        
class Laser(Sprite2D):
    # Lasers have speed, along with a position, size, direction, and texture
    def __init__(self, pos=Vector2(0, 0), speed=LASER_SPEED, size=Vector2(9,54), direction=Vector2(0,-1), texture=game_assets.get_asset_texture('green_laser.png')):
        super().__init__(pos, speed, size, direction, texture)

class Asteroid(Sprite2D):
    def __init__(self, pos, speed, direction, size=Vector2(101, 84), texture = game_assets.get_asset_texture('meteor.png')):
        super().__init__(pos, speed, size, direction, texture)
        # each asteroid starts with a different rotation
        self._rotation = randint(0, 90)

    def dynamically_rotate(self):
        # each asteroid will rotate "dynamically", meaning they will be rotating with respect to a 
        # different starting rotation 
        # use dt to rotate each asteroid the same speed consistently regardless of framerate
        dt = get_frame_time()
        rotation_speed = 100
        if self._rotation > 360:
            self._rotation -= 360
        else:
            self._rotation += dt * rotation_speed

    def get_rotation(self):
        return self._rotation
    
    def project_asteroid(self): 
        # update asteroid position
        self.update_pos()
        # 
        asteroid_source = Rectangle(0,0, self.get_texture().width, self.get_texture().height)
        asteroid_dest = Rectangle(self.get_position().x,self.get_position().y, self.get_texture().width, self.get_texture().height)
        asteroid_center = Vector2(self.get_texture().width / 2, self.get_texture().height / 2)
        draw_texture_pro(self.get_texture(), asteroid_source, asteroid_dest, asteroid_center, self._rotation, WHITE)

class O2_PowerUP(Sprite2D):
    
    def __init__(self, pos, speed, direction, size=Vector2(65, 65), texture=game_assets.get_asset_texture('water_tank.png'), is_locked=True):
        super().__init__(pos, speed, size, direction, texture)
        self._is_locked = is_locked

    # O2_PowerUps are sprites that change their appearance depending on whether or not they are unlocked
    def change_lock_status(self, update_bool):
        if update_bool:
            self._is_locked = True
            self._sprite_texture = game_assets.get_asset_texture('water_tank.png')
        else:
            self._is_locked = False
            self._sprite_texture = game_assets.get_asset_texture('water.png')
    
    def get_lock_status(self):
        return self._is_locked

class Ammo_PowerUP(Sprite2D):
    # Basic 2D sprite, with ammo powerup sprite being used
    def __init__(self, pos, speed, direction, size=Vector2(65,65), texture=game_assets.get_asset_texture('laser_powerup.png')):
        super().__init__(pos, speed, size, direction, texture)

class HeartCapsule_PowerUP(Sprite2D):
    # Basic 2D sprite, with the health uo powerup sprite being used
    def __init__(self, pos, speed, direction, size=Vector2(65, 65), texture=game_assets.get_asset_texture('health_power_up.png')):
        super().__init__(pos, speed, size, direction, texture)

class Treasure(Sprite2D):
    # Basic 2D sprite, with diamond sprite being used (by default)
    def __init__(self, pos, speed, direction, size=Vector2(61, 63), texture=game_assets.get_asset_texture('diamond.png')):
        super().__init__(pos, speed, size, direction, texture)

class Clock(Sprite2D):
    def __init__(self, font, texture = None, pos=Vector2(WINDOW_WIDTH / 2 - 37, 0), speed=0, size=Vector2(0,0), direction=Vector2()):
        super().__init__(pos, speed, size, direction, texture)
        self._current_time = 0 # time to be displayed on screen
        self._time = Timer(1, True, False, self.count_up) # timer used to count up
        self._font = font 

    def reset_time(self):
        self._current_time = 0
        self._time = Timer(1, True, False, self.count_up)

    def get_current_time(self):
        return self._current_time
        
    def count_up(self):
        self._current_time += 1

    def draw_time(self):
        # draw the current time. center the time drawn based on the number of digits
        pos_offset = 0
        if self.get_current_time() > 99:
            pos_offset = 85
        elif self.get_current_time() > 9 and self.get_current_time() <= 99:
            pos_offset = 50
        draw_text_ex(self._font, str(self.get_current_time()), Vector2(self.get_position().x - pos_offset, self.get_position().y), FONT_SIZE, 10.0, WHITE)
            
    def run_clock(self):
        # starts the game clock
        self._time.active = True
        self._time.update()
        self.draw_time()  

class OxygenMeter(Sprite2D):
    def __init__(self, font, texture = None, pos=Vector2(50, 930), speed=0, size=Vector2(), direction=Vector2()):
        super().__init__(pos, speed, size, direction, texture)
        # oxygen level to be drawn on the screen
        self._current_oxygen_level = 100
        # timer to deplete oxygen over time
        self._oxygen_clock = Timer(OXYGEN_DEPLETION_RATE, True, False, self.deplete_oxygen)
        self._font = font

    def reset_oxygen(self):
        self._current_oxygen_level = 100
        self._oxygen_clock = Timer(OXYGEN_DEPLETION_RATE, True, False, self.deplete_oxygen)

    def get_current_oxygen_level(self):
        return self._current_oxygen_level

    def draw_oxygen_level(self):
        # draw the current oxygen_level on screen, with the color based on the level
        if self.get_current_oxygen_level() >= 65:
            color = WHITE
        elif self.get_current_oxygen_level() >= 35:
            color = YELLOW
        elif self.get_current_oxygen_level():
            color = RED
        draw_text_ex(self._font, str(self.get_current_oxygen_level()), self.get_position(), OXYGEN_FONT_SIZE, 10, color)
        # print(self._current_oxygen_level)

    def deplete_oxygen(self):
        if self.get_current_oxygen_level() > 0:
            self._current_oxygen_level -= 5

    def increase_oxygen(self):
        if self.get_current_oxygen_level() >= 70 and self.get_current_oxygen_level() <= 100 :
            self._current_oxygen_level = 100
        else:
            self._current_oxygen_level += 30

    def run_oxygen_depletion_clock(self):
        self._oxygen_clock.active = True
        self._oxygen_clock.update()
        self.draw_oxygen_level()

class Points(Sprite2D):
    def __init__(self, font, texture=None, pos=Vector2(50, 50), speed=0, size=Vector2(), direction=Vector2()):
        super().__init__(pos, speed, size,  direction, texture)
        self._current_points = 0
        self._font = font
        self._multiplier = 1
    
    def reset_points(self):
        self._current_points = 0
        self._multiplier = 1

    def get_multiplier(self):
        return self._multiplier

    def reset_multiplier(self):
        self._multiplier = 1
        
    def increase_multiplier(self, factor):
        if self.get_multiplier() < 3:
            self._multiplier += factor
            if self._multiplier > 3:
                self._multiplier = 3  # Ensure the multiplier doesn't exceed 3
            self._multiplier = round(self._multiplier, 1)
        
    def get_current_points(self):
        return self._current_points
    
    def draw_points(self):
        draw_text_ex(self._font, "score:" + str(self.get_current_points()), self.get_position(), POINTS_FONT_SIZE, 8.0, YELLOW)

    def draw_multiplier(self):
        if self.get_multiplier() > 1:
            draw_text_ex(self._font, str(self._multiplier) + "x", Vector2(50,90), POINTS_FONT_SIZE - 5, 8.0, WHITE)

    def decrease_points(self, amt):
        if amt >= self._current_points:
            self._current_points = 0
        self._current_points -= amt

    def increase_points(self, amt):
        self._current_points += int(amt * self._multiplier)
 
class Star(Sprite2D):
    def __init__(self, texture, pos, speed, size, direction):
        super().__init__(pos, speed, size, direction, texture)
        self._size_variation = randint(0, 12)
        # initializes a random starting size for each star
        self._size = Vector2(size.x + self._size_variation, size.y + self._size_variation) 
        self._min_size = size.x
        self._max_size = size.x * 1.8 # maximum size for each star to increase
        # used to dynamically grow and shrink star over time based on whether it has reached the max size/min size
        self._continue_increasing = True
        self._sprite_texture = texture
    
    def proportionally_increase_size(self, size_factor):
        self._size.x += size_factor
        self._size.y += size_factor

    def dynamically_grow(self):
        """ 
        This method is responsible for making the star grow or shrink over time. 
        The size of the star fluctuates within a range between _min_size and _max_size. 
        The growth is smooth and dynamic
        """
        dt = get_frame_time()
        growth_speed = 12
        
        # If the star is still increasing in size and hasn't reached its max size, grow it
        if self._continue_increasing and (self.get_size().x) < self._max_size:
            self.proportionally_increase_size(dt * growth_speed)
        # If the star has reached the max size, stop increasing and start decreasing
        elif self.get_size().x >= self._max_size:
            self._continue_increasing = False
            self.proportionally_increase_size(-dt * growth_speed)
        # If the star has started shrinking and hasn't reached the min size, shrink it
        elif not self._continue_increasing and (self.get_size().x) > self._min_size:
            self.proportionally_increase_size(-dt * growth_speed)
        # If the star has reached the minimum size, reverse the shrinking and start growing again
        else:
            self._continue_increasing = True
            self.proportionally_increase_size(dt * growth_speed)
            
class HP(Sprite2D):
    def __init__(self, pos, speed=0, direction=Vector2(), size=Vector2(30,70), texture = game_assets.get_asset_texture('heart_container.png'), is_empty=False):
        super().__init__(pos, speed, size, direction, texture)
        self._is_empty = is_empty

    def draw_heart(self):
        draw_texture_v(self.get_texture(), self.get_position(), WHITE)

    def switch_heart_texture(self, update_bool):
        # changed the texture used for the HP used for the AI, based on whether it should be empty or not
        # note: is_empty will change for each heart throughtout the course of the game
        if update_bool:
            self._is_empty = True
            self._sprite_texture = game_assets.get_asset_texture('empty_heart_container.png')
        else:
            self._sprite_texture = game_assets.get_asset_texture('heart_container.png') 
            self._is_empty = False

class Ammo(Sprite2D):
    def __init__(self, pos, speed = 0, direction=Vector2(), size=Vector2(20,60), texture=game_assets.get_asset_texture('green_laser.png')):
        super().__init__(pos, speed, size, direction, texture)

    def draw_laser_ammo(self):
        draw_texture_v(self.get_texture(), self.get_position(), WHITE)

