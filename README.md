# An Untitled Asteroids Game

A retro-styled Asteroids game clone where you survive as long as possible avoiding asteroids while collecting powerups to keep you alive and treasure to increase your score. 

## Prequisities

* Knowledge of Object-Oriented Programming, Inheritance, File Opening, Data Strutures
* PyRay/RayLib libraries install on your computer (see To Run Below)
* Python 3 installed
* Works on Windows, Likely works on Mac (must test)*
  
## Core Gameplay

This game utilizes a state stack system to manage various game screens, enabling smooth transitions between menus and gameplay. The core gameplay loop activates when the game enters the Gameplay state. The game involves avoiding randomly spawning asteroids, collecting treasures, and managing resources, with a progressive difficulty system that adapts as the player survives.

#### Asteroids
Asteroids spawn randomly from the top of the screen and are deleted upon exiting the edges of the game window. Asteroids come in three types: Normal (Deals regular damage to the player upon collision), Icy (Deals less damage but freezes the player for a brief period), Fiery (Deals more damage to the player)

#### Player

While avoiding asteroids, the player can collect various items; Treasure increases the player's score, Ammo refills the player's ammo capacity, Health packs restore player health, and Oxygen tanks can be shot to collect the resulting oxygen bubble to. Player oxygen drains over time and the player must manage ammo to collect enough oxygen bubbles to survive. The player's score multiplier also increases as they collect treasures and power-ups while avoiding asteroid collisions. However, the multiplier resets if the player is hit by an asteroid.

#### Difficulty Progression

The game features a dynamic difficulty system that adjusts based on the player’s survival time: 

Asteroid Frequency: Initially, asteroids spawn at regular intervals. As the player survives, the number of asteroids increases.

Asteroid Speed: Over time, the speed range of asteroids increases in a set number of intervals, making the game more challenging.

#### Weather API Usage

https://rapidapi.com/oktamovshohjahon/api/weather-api138/playground/apiendpoint_acb2971f-25d4-4a29-b5d6-87b9f3f8131b

A weather API collects temperature and wind speed information for a city entered by the player through the Difficulty button in the options menu. The temperature is used to modify the distribution of asteroid types, simulating weather-impact on asteroid spawning. The wind speed influences the default speed at which asteroids spawn.

#### Save/Load Feature

The game includes a save/load feature that allows players to save their difficulty settings (temperature and wind speed). This ensures that the game will remember the player's last difficulty configuration when resumed. The player can also click a button in settings to reset data to a fresh save file.

#### Leaderboard

Upon death, the player’s time survived and points are recorded in a leaderboard, which tracks the top 5 players. This leaderboard allows players to compete for the highest scores and longest survival times.

## To Run

This program uses the RayLib/PyRay libraries for graphics. To run the program, first install these libraries to your computer.

https://pypi.org/project/raylib/

First, make sure latest pip is installed:

python3 -m pip install --upgrade pip

Then install:

python3 -m pip install setuptools
python3 -m pip install raylib==5.5.0.0

Then clone:

git clone (link of this repo)
Go to the project directory
Run!


## Game Controls

* Move Player - Arrow Keys
* Shoot Asteroid - Spacebar

## ScreenShots/Video

## Author's Note

### Project Structure
The codebase is organized into several modules:

* Game.py handles game mechanics, difficulty, traversing menu screens
* Sprites.py contains classes for game entities
* WeatherApi.py handles API calls for weather data
* MyTimer.py handles timers used for various game/player mechanics
* Assets.py manages the loading of textures (including sound, music)
* Settings.py has constants used by the other python files
* GameSaver.py handles game saving/loading/erasing of player data
* Menu
* DoublyLinkedStack.py is the data structure used for menu traversal
* InputBox.py handles a text input box used for city selection

## Credits

Sprite Assets:

* Hearts and Heealth Bar by VampireGirl, itch.io https://fliflifly.itch.io/hearts-and-health-bar (Creative Commons 0)
* Space Shooter Redux by Kenny, https://www.kenney.nl/assets/space-shooter-redux (Creative Commons 0)
* Water Cannon VFX by anton_chi, https://anton-chi.itch.io/water-cannon (Free for Personal and Commercial Use, no redistribution)
* Treasure+ by SchiGho, https://ninjikin.itch.io/treasure, (Creative Commons BY 4.0)
* 8-Bit Screen By Tisã, https://samplefocus.com/samples/8-bit-scream (Standard License, Royalty Free)
* Spacebar, https://www.pixilart.com/art/spacebar-55abfeff259a667
* The King's Heart (loop) by Free Game Music 1, https://soundcloud.com/rmaren/movement-while-my-heart-still, (Creative Commons License)

Pixabay Content License (https://pixabay.com/service/license-summary/):

* https://pixabay.com/sound-effects/retro-coin-4-236671/
* https://pixabay.com/sound-effects/coin-recieved-230517/ 
* https://pixabay.com/sound-effects/sci-fi-bubble-pop-89059/ 
* https://pixabay.com/sound-effects/mag-in-82094/
* https://pixabay.com/sound-effects/lighter-click-271118/
* https://pixabay.com/sound-effects/menu-button-88360/
* https://pixabay.com/sound-effects/siren-alert-96052/
* https://pixabay.com/sound-effects/breaking-glass-84819/ 

