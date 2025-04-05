from pyray import *
from raylib import *
from DoublyLinkedStack import *
from Assets import game_assets

class InputBox:
    """
    A rectangle that acts as a text box. 
    
    Features:
    - You can change the color for the rectangle borders, interior, as well as the text. 
    - The input box tracks whether your mouse is hoving over the box, and will highlight it if so. 
    - You can only type if your mouse is hoving over the box
    - A maximum character limit will be given
    - Input is stored after you press enter (box will exit out of type mode if you press enter, or dont hover over the space)
    - You can choose to hide box after input has been saved
    - Input box can be placed anywhere and can be resized
    - typing backspace will remove the last character
    - sound is placed after a letter is typed/deleted
    - x icon will be placed to the left/right for the user to exit out of the input box w/o pressing enter
    
    Note: with the menu class, the self._difficulty_clicked will be used to show whether box should be shown
    """
    def __init__(self, pos, font, font_size, width, height, character_limit, border_color, interior_color, text_color):
        self._input_box_pos = pos
        self._character_limit = character_limit
        self._border_color = border_color
        self._interior_color = interior_color
        self._text_color = text_color
        self._mouse_is_hovering = False # To track if the mouse is hovering over the input box
        self._is_enabled = False # used by the game.py class and menu class, if difficulty button clicked twice remove box UI
        self._input_box_text = "" # Text input to be displayed on the input box UI
        self._text_to_save = ""  # The text to be saved when the user presses Enter
        self._input_box_font = font
        self._input_box_font_size = font_size
        self._input_box_width = width
        self._input_box_height = height
        self._input_box_rectangle = Rectangle(self._input_box_pos.x, self._input_box_pos.y, self._input_box_width, self._input_box_height)
        self._accepted_characters = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        

    def draw_input_box(self):
        """
        Draw the input box rectangle on the screen with appropriate border and color,
        based on if the mouse is hovering over it or not
        """
        if self.mouse_in_input_box():
            draw_rectangle_v(self._input_box_pos, Vector2(self._input_box_width, self._input_box_height), GRAY)
            draw_rectangle_lines_ex(self._input_box_rectangle, 10, WHITE)
        else:
            draw_rectangle_v(self._input_box_pos, Vector2(self._input_box_width, self._input_box_height), self._interior_color)
            draw_rectangle_lines_ex(self._input_box_rectangle, 10, self._border_color)
    
    def mouse_in_input_box(self):
        mouse_pos = get_mouse_position()
        in_rectangle_width = self._input_box_pos.x <= mouse_pos.x <= self._input_box_pos.x + self._input_box_width
        in_rectangle_height = self._input_box_pos.y <= mouse_pos.y <= self._input_box_pos.y + self._input_box_height
        return in_rectangle_width and in_rectangle_height

    def handle_input(self):
        """
        Handle user input: character typing, backspace, and enter
        """
        if self.mouse_in_input_box():
            self._mouse_is_hovering = True
        else:
            self._mouse_is_hovering = False
        
        if self._mouse_is_hovering:  # If the mouse is hovering, allow typing
            user_character = chr(get_char_pressed()) # convert unicode to char
            if user_character in self._accepted_characters and len(self._input_box_text) <= self._character_limit:
                self._input_box_text += user_character # add character to be displayed on input box UI
                # delete the last character by saving a new copy of the input string with the end sliced off
            if is_key_pressed(KEY_BACKSPACE) and len(self._input_box_text) > 0:
                self._input_box_text = self._input_box_text[:-1]
                # reset the input box UI and save text after hitting enter
            if is_key_pressed(KEY_ENTER):
                self._text_to_save = self._input_box_text
                if len(self._text_to_save) > 0: # only consider reformatting for strings of atleast 1 character
                    self.adjust_saved_text() # so that only the first character is capitalized and the rest is lower case
                self._input_box_text = ""
                print(self._text_to_save) # for testing
    
    def get_saved_text(self):
        return self._text_to_save

    # written in order to have a standardized text format to be saved after hitting enter, for the API's use
    def adjust_saved_text(self):
        self._text_to_save = self._text_to_save.lower() # convert all characters to lowercase
        first_character = self._text_to_save[0]
        # after getting first_character make it upper case and save it as the new first character
        first_character = first_character.upper() 
        self._text_to_save = first_character + self._text_to_save[1:]

    def draw_text_input_UI(self):
        # Check if the input box is empty and set the appropriate text
        if len(self._input_box_text) == 0:
            display_text = "Enter City"
        else:
            display_text = self._input_box_text

        # Measure the text dimensions (for both placeholder and input text)
        text_dimensions = measure_text_ex(self._input_box_font, display_text, self._input_box_font_size, 0)
        text_width = text_dimensions.x
        text_height = text_dimensions.y

        # Draw the text (either placeholder or input text)
        draw_text_pro(self._input_box_font, display_text, Vector2(self._input_box_pos.x + self._input_box_width / 2 - text_width / 2, 
        self._input_box_pos.y + self._input_box_height / 2 - text_height / 2), Vector2(0, 0), 0, self._input_box_font_size, 0.0, self._text_color)


    def enable_input_box(self):
        self.draw_input_box()
        self.handle_input()
        self.draw_text_input_UI()

    def reset_input_box(self):
        self._input_box_text = ""
        self._text_to_save = ""

if __name__ == "__main__":

    test_input_box = InputBox(Vector2(get_screen_width() / 2 - 250, get_screen_height() / 2 - 65), game_assets.get_asset_font('slkscreb.ttf'), 40, 500, 130, 9, RED, ORANGE, WHITE)
    while not window_should_close():
        begin_drawing()
        clear_background(BLACK)
        test_input_box.enable_input_box()
        end_drawing()
    close_window()