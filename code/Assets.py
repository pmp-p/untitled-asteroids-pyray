from pyray import *
from raylib import *
from Settings import *
import os

class Assets:
    def __init__(self):
        # initialize the window and audio device needed for rendering and sound
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, 'GAME')  # set up the window size
        init_audio_device() # initialize the audio system
        self._assets = {} # dictionary to store loaded assets

    """
    The structure of the get asset methods was chosen because it allows textures to be loaded when needed.
    Calling the load function repeatedly impacts memory, so all assets that are brand new to the program are loaded for the 
    first time only and the music/texture/font/sound objects are stored to be easily accessed without loading in the future.
    """
    
    def get_asset_texture(self, key):
        if key in self._assets:
            return self._assets[key]
        else:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../images/" + key)) 
            self._assets[key] = load_texture(base_path)
            return self._assets[key]
        
    def get_asset_font(self, key):
        # check if the font is already loaded and return loaded font if so
        if key in self._assets:
            return self._assets[key]
        else:
             # load font from the file if not already loaded and add key to access it in the asset dictionary
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../font/" + key)) 
            self._assets[key] = load_font(base_path)
            return self._assets[key]
        
    def get_asset_sound(self, key):
        # check if the sound is already loaded and return loaded sound if so
        if key in self._assets:
            return self._assets[key]
        else:
            # load sound from the file if not already loaded and add key to access it in the asset dictionary
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../audio/" + key)) 
            self._assets[key] = load_sound(base_path)
            return self._assets[key]
    
    def get_asset_music(self, key):
         # check if the music is already loaded and return loaded music if so
        if key in self._assets:
            return self._assets[key]
        else:
            # load music from the file if not already loaded and add key to access it in the asset dictionary
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../audio/" + key))  
            self._assets[key] = load_music_stream(base_path)
            return self._assets[key]
    
    def unload(self):
        # loop through all loaded assets and unload them 
        for texture in self._assets:
            if type(texture) == Texture2D:
                unload_texture(texture)
            elif type(texture) == Font:
                unload_font(texture)
            elif type(texture) == Sound:
                unload_sound(texture)
            elif type(texture) == Music:
                unload_music_stream(texture)
        self._assets.clear() # clear the asset dictionary

# create an instance of the Assets class to manage assets
game_assets = Assets()