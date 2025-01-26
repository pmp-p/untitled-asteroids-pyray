from settings import *
from custom_timer import Timer
from random import randint
from global_textures import *

class Sprite2D():
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
    
    def update_pos(self):
        deltatime = get_frame_time()
        self._pos.x += self._direction.x * self._speed * deltatime
        self._pos.y += self._direction.y * self._speed * deltatime

    def set_direction(self, direction):
        self._direction = direction

    def set_texture(self, texture):
        self._sprite_texture = texture

    def movement_update(self,direction_vector, rotation, origin, tint):
        self.set_direction(direction_vector)
        self.update_pos()
        source_rect = Rectangle(0,0, self.get_texture().width, self.get_texture().height)
        dest_rect = Rectangle(self.get_position().x,self.get_position().y, self._size.x, self._size.y)
        draw_texture_pro(self.get_texture(), source_rect, dest_rect, origin, rotation, tint)
        # draw_rectangle_lines(int(self.get_position().x), int(self.get_position().y), int(self._size.x), int(self._size.y), GREEN )

class Spaceship(Sprite2D):
    def __init__(self, texture=game_sprites.get_global_texture('player_ship.png'), pos=Vector2(WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2), speed=PLAYER_SPEED, size=Vector2(112,75), direction=Vector2()):
        super().__init__(pos, speed, size, direction, texture)
        self._lasers = []
        self._health_bar = []
        self._max_hp = 9
        self._current_hp = 9
        self.generate_health()
        self._ammo_bar = []
        self._ammo = 6
        self._max_ammo = 6
        self.generate_ammo()
        self._spaceship_oxygen = OxygenMeter(game_sprites.get_global_font('slkscreb.ttf'))
        self._player_points = Points(game_sprites.get_global_font('slkscreb.ttf'))

    def reset_player(self):
        self._lasers.clear()
        self._health_bar.clear()
        self._current_hp = 9
        self.generate_health()
        self._ammo_bar.clear()
        self._max_ammo = 6
        self.generate_ammo()
        self._spaceship_oxygen.reset_oxygen()
        self._player_points.reset_points()
        self._pos = Vector2(WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2)

    def get_current_health(self):
        return self._current_hp

    def get_current_ammo(self):
        return self._ammo
    
    def get_lasers(self):
        return self._lasers

    def generate_health(self):
        sprite_offset = 0
        for i in range(self.get_current_health()):
            current_heart = HP(Vector2(50 + sprite_offset, 1000))
            self._health_bar += [current_heart]
            sprite_offset += current_heart.get_size().x
    
    def display_hp(self):
        for heart in self._health_bar:
            heart.draw_heart()

    def take_damage(self):
        if self.get_current_health() > 0:
            self._health_bar[self.get_current_health() - 1].switch_heart_texture(True)
            self._current_hp -= 1
        else:
            self._health_bar[self.get_current_health()].switch_heart_texture(True)
    
    def increase_health(self):
        if self._current_hp < self._max_hp:
            self._health_bar[self.get_current_health()].switch_heart_texture(False)
            self._current_hp += 1
        else:
            self._health_bar[self.get_current_health() - 1].switch_heart_texture(False)

    def generate_ammo(self):
        self._ammo_bar.clear()
        sprite_offset = 0
        for i in range(self._ammo):
            current_ammo = Ammo(Vector2(60 + sprite_offset, 870))
            self._ammo_bar += [current_ammo]
            sprite_offset += current_ammo.get_size().x

    def increase_ammo(self):
        if self.get_current_ammo() < self._max_ammo:
            self._ammo += 1
            self.generate_ammo()

    def remove_ammo(self):
        if self._ammo > 0:
            self._ammo_bar.remove(self._ammo_bar[-1])
            self._ammo -= 1
        else:
            self._ammo_bar.remove(self._ammo_bar[-1])

    def display_ammo(self):
        for ammo in self._ammo_bar:
            ammo.draw_laser_ammo()
            
    def get_oxygen_meter(self):
        return self._spaceship_oxygen
    
    def drain_spaceship_oxygen(self):
        self.get_oxygen_meter().run_oxygen_depletion_clock()

    def get_player_points(self):
        return self._player_points
    
    def draw_player_points(self):
        self.get_player_points().draw_points()
        self.get_player_points().draw_multiplier()

    def check_window_boundaries(self): 
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
        if is_key_pressed(KEY_P) and len(self.get_lasers()) < 10:
            if self._ammo > 0:
                beam = game_sprites.get_global_sound("laser.wav")
                set_sound_volume(beam, 0.5)
                play_sound(beam)
                laser_align_pos = Vector2(self.get_position().x + self.get_texture().width / 2 - 3, self.get_position().y - 30)
                current_laser = Laser(laser_align_pos)
                self._lasers += [current_laser]
                self.remove_ammo()

        for laser in self.get_lasers()[:]: 
            laser.movement_update(laser.get_direction(), 0, Vector2(0, 0), WHITE)
            if laser.get_position().y < 0:
                self._lasers.remove(laser)
    
    def initialize_player_mechanics(self):
        self.movement_update(Vector2(int(is_key_down(KEY_D)) - int(is_key_down(KEY_A)), int(is_key_down(KEY_S)) - int(is_key_down(KEY_W))), 0, Vector2(), WHITE)
        self.shoot_laser()
        self.display_hp()
        self.drain_spaceship_oxygen()
        self.draw_player_points()
        self.display_ammo()
        self.check_window_boundaries()
    
class Laser(Sprite2D):
    def __init__(self, pos=Vector2(0, 0), speed=LASER_SPEED, size=Vector2(9,54), direction=Vector2(0,-1), texture=game_sprites.get_global_texture('greenlaser.png')):
        super().__init__(pos, speed, size, direction, texture)

class Asteroid(Sprite2D):
    def __init__(self, pos, speed, direction, size=Vector2(101, 84), texture = game_sprites.get_global_texture('meteor.png')):
        super().__init__(pos, speed, size, direction, texture)
        self._rotation = randint(0, 90)

    def dynamically_rotate(self):
        dt = get_frame_time()
        rotation_speed = 100
        if self._rotation > 360:
            self._rotation -= 360
        else:
            self._rotation += dt * rotation_speed

    def get_rotation(self):
        return self._rotation
    
    def project_asteroid(self): 
        self.update_pos()
        asteroid_source = Rectangle(0,0, self.get_texture().width, self.get_texture().height)
        asteroid_dest = Rectangle(self.get_position().x,self.get_position().y, self.get_texture().width, self.get_texture().height)
        asteroid_center = Vector2(self.get_texture().width / 2, self.get_texture().height / 2)
        draw_texture_pro(self.get_texture(), asteroid_source, asteroid_dest, asteroid_center, self._rotation, WHITE)

class O2_PowerUP(Sprite2D):
    def __init__(self, pos, speed, direction, size=Vector2(65, 65), texture=game_sprites.get_global_texture('water_tank.png'), is_locked=True):
        super().__init__(pos, speed, size, direction, texture)
        self._is_locked = is_locked

    def change_lock_status(self, update_bool):
        if update_bool:
            self._is_locked = True
            self._sprite_texture = game_sprites.get_global_texture('water_tank.png')
        else:
            self._is_locked = False
            self._sprite_texture = game_sprites.get_global_texture('uncased_oxygen_tank.png')
    
    def get_lock_status(self):
        return self._is_locked

class Ammo_PowerUP(Sprite2D):
    def __init__(self, pos, speed, direction, size=Vector2(65,65), texture=game_sprites.get_global_texture('laser_powerup.png')):
        super().__init__(pos, speed, size, direction, texture)

class HeartCapsule_PowerUP(Sprite2D):
    def __init__(self, pos, speed, direction, size=Vector2(65, 65), texture=game_sprites.get_global_texture('health_up.png')):
        super().__init__(pos, speed, size, direction, texture)

class Treasure(Sprite2D):
    def __init__(self, pos, speed, direction, size=Vector2(61, 63), texture=game_sprites.get_global_texture('diamond.png')):
        super().__init__(pos, speed, size, direction, texture)

class Clock(Sprite2D):
    def __init__(self, font, texture = None, pos=Vector2(WINDOW_WIDTH / 2 - 37, 0), speed=0, size=Vector2(0,0), direction=Vector2()):
        super().__init__(pos, speed, size, direction, texture)
        self._current_time = 0
        self._time = Timer(1, True, True, self.count_up)
        self._font = font 

    def reset_time(self):
        self._current_time = 0

    def get_current_time(self):
        return self._current_time
        
    def count_up(self):
        self._current_time += 1

    def draw_time(self):
        pos_offset = 0
        if self.get_current_time() > 99:
            pos_offset = 85
        elif self.get_current_time() > 9 and self.get_current_time() <= 99:
            pos_offset = 50
        draw_text_ex(self._font, str(self.get_current_time()), Vector2(self.get_position().x - pos_offset, self.get_position().y), FONT_SIZE, 10.0, WHITE)
            
    def run_clock(self):
        self._time.update()
        self.draw_time()  

class OxygenMeter(Sprite2D):
    def __init__(self, font, texture = None, pos=Vector2(50, 930), speed=0, size=Vector2(), direction=Vector2()):
        super().__init__(pos, speed, size, direction, texture)
        self._current_oxygen_level = 100
        self._oxygen_clock = Timer(OXYGEN_DEPLETION_RATE, True, True, self.deplete_oxygen)
        self._font = font

    def reset_oxygen(self):
        self._current_oxygen_level = 100

    def get_current_oxygen_level(self):
        return self._current_oxygen_level

    def draw_oxygen_level(self):
        if self.get_current_oxygen_level() >= 75:
            color = WHITE
        elif self.get_current_oxygen_level() >= 45:
            color = YELLOW
        else:
            color = RED
        draw_text_ex(self._font, str(self.get_current_oxygen_level()), self.get_position(), OXYGEN_FONT_SIZE, 10.0, color)
        print(self._current_oxygen_level)

    def deplete_oxygen(self):
        if self.get_current_oxygen_level() > 0:
            self._current_oxygen_level -= 5

    def increase_oxygen(self):
        if self.get_current_oxygen_level() >= 70 and self.get_current_oxygen_level() <= 100 :
            self._current_oxygen_level = 100
        else:
            self._current_oxygen_level += 30

    def run_oxygen_depletion_clock(self):
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
        self._size = Vector2(size.x + self._size_variation, size.y + self._size_variation) 
        self._min_size = size.x
        self._max_size = size.x * 1.8
        self._continue_increasing = True
        self._sprite_texture = texture
    
    def proportionally_increase_size(self, size_factor):
        self._size.x += size_factor
        self._size.y += size_factor

    def dynamically_grow(self):
        dt = get_frame_time()
        growth_speed = 12
        if self._continue_increasing and (self.get_size().x) < self._max_size:
            self.proportionally_increase_size(dt * growth_speed)
        elif self.get_size().x >= self._max_size:
            self._continue_increasing = False
            self.proportionally_increase_size(-dt * growth_speed)
        elif not self._continue_increasing and (self.get_size().x) > self._min_size:
            self.proportionally_increase_size(-dt * growth_speed)
        else:
            self._continue_increasing = True
            self.proportionally_increase_size(dt * growth_speed)
            
class HP(Sprite2D):
    def __init__(self, pos, speed=0, direction=Vector2(), size=Vector2(30,70), texture = game_sprites.get_global_texture('full_heart_2.png'), is_empty=False):
        super().__init__(pos, speed, size, direction, texture)
        self._is_empty = is_empty

    def draw_heart(self):
        draw_texture_v(self.get_texture(), self.get_position(), WHITE)

    def switch_heart_texture(self, update_bool):
        if update_bool:
            self._is_empty = True
            self._sprite_texture = game_sprites.get_global_texture('empty_heart_2.png')
        else:
            self._sprite_texture = game_sprites.get_global_texture('full_heart_2.png') 
            self._is_empty = False

class Ammo(Sprite2D):
    def __init__(self, pos, speed = 0, direction=Vector2(), size=Vector2(20,60), texture=game_sprites.get_global_texture('greenlaser.png')):
        super().__init__(pos, speed, size, direction, texture)

    def draw_laser_ammo(self):
        draw_texture_v(self.get_texture(), self.get_position(), WHITE)

class Button():
    def __init__(self, pos, width, height, text, font, font_size):
        self._pos = pos
        self._text = text
        self._font = font
        self._font_size = font_size
        self._width = width
        self._height = height
        self._rectangle = Rectangle(self._pos.x, self._pos.y, self._width, self._height)
        self._hovered_yet = False

    def is_hovered(self):
        mouse_pos = get_mouse_position()
        in_rectangle_width = self._pos.x <= mouse_pos.x <= self._pos.x + self._width
        in_rectangle_height = self._pos.y <= mouse_pos.y <= self._pos.y + self._height
        return in_rectangle_width and in_rectangle_height
    
    def draw_text_rectangle(self, color1, color2):
        box_color = color1
        text_color = color2
        if self.is_hovered():
            box_color = GRAY
            text_color = LIGHTGRAY
            if not self._hovered_yet:
                button_click = game_sprites.get_global_sound("button_hover.wav")
                set_sound_volume(button_click, 0.4)
                play_sound(button_click)
                self._hovered_yet = True
        else:
            self._hovered_yet = False
        draw_rectangle_pro(self._rectangle, Vector2(0,0), 0, box_color)
        text_dimensions = measure_text_ex(self._font, self._text, self._font_size, 0.0)
        text_width = text_dimensions.x
        text_height = text_dimensions.y
        draw_text_pro(self._font, self._text, Vector2(self._pos.x + self._rectangle.width / 2 - text_width/2, 
        self._pos.y + self._rectangle.height / 2 - text_height/2), Vector2(0,0), 0, self._font_size, 0.0, text_color)
        
    def get_rectangle(self):
        return self._rectangle