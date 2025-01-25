from settings import *

class Global_textures:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'GAME')
        init_audio_device()
        self._global_textures = {}

    def get_global_texture(self, key):
        if key in self._global_textures:
            return self._global_textures[key]
        else:
            self._global_textures[key] = load_texture(join("images", key))
            return self._global_textures[key]
        
    def get_global_font(self, key):
        if key in self._global_textures:
            return self._global_textures[key]
        else:
            self._global_textures[key] = load_font(join("font", key))
            return self._global_textures[key]
        
    def get_global_sound(self, key):
        if key in self._global_textures:
            return self._global_textures[key]
        else:
            self._global_textures[key] = load_sound(join("audio", key))
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