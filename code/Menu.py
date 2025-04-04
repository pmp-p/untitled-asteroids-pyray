from pyray import *
from raylib import *
from MyTimer import *
from Assets import *

class Menu():
    def __init__(self):
        self._buttons = {}
        self._in_main_menu = True
        self._in_death_menu = False
        self._exit_clicked = False
        self._start_game = False
        self._in_leaderboard = False
        self._in_options = False
        self._leaderboard = []
        self._title = "untitled asteroids game"
        self.create_buttons()
        self._start_timer = Timer(4, False, False, self.start_game_after_delay)

    def score_sort(self, entry):
        return entry[1]
    
    def sort_leaderboard(self):
        self._leaderboard.sort(key=self.score_sort, reverse=True)

    def draw_leaderboard_stats(self):
        if len(self._leaderboard) > 0:
            self.sort_leaderboard()
        text_height = 120
        place = 1
        for player_data in self._leaderboard:
            player_data = player_data[0] + "    score: " + str(player_data[1]) + "    time: " + str(player_data[2])
            text_dimensions = measure_text_ex(game_assets.get_asset_font('slkscreb.ttf'), player_data, 55, 0)
            centered_txt_width = (WINDOW_WIDTH - text_dimensions.x) / 2
            draw_text_ex(game_assets.get_asset_font('slkscreb.ttf'), str(place) + ". " + player_data, Vector2(centered_txt_width, text_height), 55, 0, YELLOW)
            text_height += 60
            place += 1

    def start_game_after_delay(self):
        self._start_game = True

    def create_buttons(self):
        self._buttons["start"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 450), 620, 80, "START", game_assets.get_asset_font('slkscreb.ttf'), 60)
        self._buttons["stats"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 550), 620, 80, "LEADERBOARD", game_assets.get_asset_font('slkscreb.ttf'), 60)
        self._buttons["exit"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 650), 620, 80, "EXIT", game_assets.get_asset_font('slkscreb.ttf'), 60)
        self._buttons["main menu"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 550), 620, 80, "MAIN MENU", game_assets.get_asset_font('slkscreb.ttf'), 60)
        self._buttons["options"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 750), 620, 80, "OPTIONS", game_assets.get_asset_font('slkscreb.ttf'), 60)
        self._buttons["difficulty"] = Button(Vector2(WINDOW_WIDTH/2 - 310, 750), 620, 80, "DIFFICULTY", game_assets.get_asset_font('slkscreb.ttf'), 60)
            
    def draw_title(self):
        title_text_dimensions = measure_text_ex(game_assets.get_asset_font('slkscreb.ttf'), self._title, 80, 0)
        centered_title_width = (WINDOW_WIDTH - title_text_dimensions.x) / 2
        draw_text_ex(game_assets.get_asset_font('slkscreb.ttf'), self._title, Vector2(centered_title_width, 120), 80, 0, WHITE)

    def play_button_click_sfx(self):
        button_click = game_assets.get_asset_sound("button_click.wav")
        set_sound_volume(button_click, 0.4)
        play_sound(button_click)

    def check_button_clicks(self):
        if self._in_main_menu:
            if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["start"].get_rectangle()):
                self._in_main_menu = False
                self.play_button_click_sfx()
                self._start_timer.activate()
            elif is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["stats"].get_rectangle()):
                self._in_leaderboard = True
                self._in_main_menu = False
                self.play_button_click_sfx()
            elif is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["options"].get_rectangle()):
                self._in_main_menu = False
                self._in_options = True
                self.play_button_click_sfx()
        elif self._in_death_menu:
            if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["main menu"].get_rectangle()):
                self._in_death_menu = False
                self._in_main_menu = True
                self.play_button_click_sfx()
        elif self._in_leaderboard:
            if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["main menu"].get_rectangle()):
                self._in_main_menu = True
                self._in_leaderboard = False
                self.play_button_click_sfx()
        elif self._in_options:
            if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["main menu"].get_rectangle()):
                self._in_main_menu = True
                self._in_options = False
                self.play_button_click_sfx()
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self._buttons["exit"].get_rectangle()):
            self._exit_clicked = True

    def run_menu(self):
        self._buttons["start"].draw_button(RED, BLACK, Vector2(WINDOW_WIDTH/2 - 310, 450))
        self._buttons["stats"].draw_button(RED, BLACK, Vector2(WINDOW_WIDTH/2 - 310, 550))
        self._buttons["options"].draw_button(RED, BLACK, Vector2(WINDOW_WIDTH/2 - 310, 650))
        self._buttons["exit"].draw_button(RED, BLACK, Vector2(WINDOW_WIDTH/2 - 310, 750))
        self.draw_title()
        self.check_button_clicks()     

    def run_leaderboard_menu(self):
        self._buttons["main menu"].draw_button(RED, BLACK, Vector2(WINDOW_WIDTH/2 - 310, 850))
        self.check_button_clicks()
        self.draw_leaderboard_stats()
        #self.print_leaderboard()

    def run_death_menu(self):
        self._buttons["main menu"].draw_button(RED, BLACK, Vector2(WINDOW_WIDTH/2 - 700, 550))
        self._buttons["exit"].draw_button(RED, BLACK, Vector2(WINDOW_WIDTH/2 + 40, 550))
        self.check_button_clicks()
        title_text_dimensions = measure_text_ex(game_assets.get_asset_font('slkscreb.ttf'), "GAME OVER", 200, 0)
        centered_title_width = (WINDOW_WIDTH - title_text_dimensions.x) / 2
        centered_title_height = (WINDOW_HEIGHT - title_text_dimensions.y) / 2
        draw_text_ex(game_assets.get_asset_font('slkscreb.ttf'), "GAME OVER", Vector2(centered_title_width, int(centered_title_height / 1.5)), 200, 0, WHITE)

    def run_options_menu(self):
        self._buttons["main menu"].draw_button(RED, BLACK, Vector2(WINDOW_WIDTH/2 - 310, 850))
        self._buttons["difficulty"].draw_button(RED, BLACK, Vector2(WINDOW_WIDTH/2 - 310, 250))
        self.check_button_clicks()

class Button():
    def __init__(self, pos, width, height, text, font, font_size):
        self._pos = pos
        self._text = text
        self._font = font
        self._font_size = font_size
        self._width = width
        self._height = height
        self._rectangle = Rectangle(self._pos.x, self._pos.y, self._width, self._height)
        

    def reposition_button(self, pos):
        self._pos = pos
        self._rectangle = Rectangle(self._pos.x, self._pos.y, self._width, self._height)
        
    def is_hovered(self):
        # returns true if cursor is hovering over the button
        mouse_pos = get_mouse_position()
        in_rectangle_width = self._pos.x <= mouse_pos.x <= self._pos.x + self._width
        in_rectangle_height = self._pos.y <= mouse_pos.y <= self._pos.y + self._height
        return in_rectangle_width and in_rectangle_height
  
    def draw_button(self, color1, color2, pos):
        self.reposition_button(pos)
        box_color = color1
        text_color = color2
        if self.is_hovered():
            box_color = GRAY
            text_color = LIGHTGRAY
            if not self._hovered_yet:
                button_click = game_assets.get_asset_sound("button_hover.wav")
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
        draw_rectangle_lines_ex(self._rectangle, 5.0, WHITE)
        
    def get_rectangle(self):
        return self._rectangle