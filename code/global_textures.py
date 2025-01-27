from settings import *
import os

class Global_textures:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'GAME')
        init_audio_device()
        self._global_textures = {}

    def get_global_texture(self, key):
        if key in self._global_textures:
            return self._global_textures[key]
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../images/" + key)) 
            self._global_textures[key] = load_texture(base_path)
            return self._global_textures[key]
        
    def get_global_font(self, key):
        if key in self._global_textures:
            return self._global_textures[key]
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../font/" + key)) 
            self._global_textures[key] = load_font(base_path)
            return self._global_textures[key]
        
    def get_global_sound(self, key):
        if key in self._global_textures:
            return self._global_textures[key]
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../audio/" + key)) 
            self._global_textures[key] = load_sound(base_path)
            return self._global_textures[key]
    
    def unload(self):
        for texture in self._global_textures:
            if type(texture) == Texture2D:
                unload_texture(texture)
            elif type(texture) == Font:
                unload_font(texture)
            elif type(texture) == Sound:
                unload_sound(texture)
        self._global_textures.clear()

game_sprites = Global_textures()

#   base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../images")) (use this for relative)