# An Untitled Asteroids Game

A retro-styled Asteroids game clone where you survive as long as possible avoiding asteroids while collecting powerups to keep you alive and treasure to increase your score. 

## Core Gameplay

The game uses a state stack system to determine what menu screen should be displayed, while also allowing smooth transitions between menu screens and the game play itself. 
If the program's current state is gameplay, the core gameplay loop will begins. 

Asteroids will randomly spawn from the top of the screen and will be deleted upon exiting the edges of the game window. The asteroids will spawn with different types: Normal (normal damage done to player upon collision), Icy (less damage done to the player, but player freezes for a brief period of time), and Fiery (more damage done to the player). If the player loses all health, the game loop ends and the player is sent to the death screen menu state.

While avoiding the asteroids, the player can collect treasure to increase their score. The player can also collect powerups to increase their stats (collect ammo to refill their ammo capacity, recover health by collecting hearts, and recover oxygen by shooting an oxygen tank and collecting the oxygen bubble.). As the player collects these objects while avoiding getting hit by asteroids, the score multiplier increases. The score mulitplier is stacked with the score of each item to increase points gained. THe score multipleir resets when the player gets hit once.

There is a difficulty progression system as the player survives. First, the asteroids begin spawning at regular intervals at greater amounts each internal. Then, the speed range of the asteroids increase for a set number of intervals. 

A weather API is used to collect temperature and windspeed information for a city when a player types a city into the difficulty button in options. THe tmepreature is mapped to a dcionary that matches with a spawn distrbutions of teh asteroid types to simulate weather impacted asteroid spawning. The windspeed is used to set the default speed of the spawning asteroids.

When the player dies, time survived along with points is stored in a leaderboard and is sorted to have 5 players tracked up to. 

The game uses a save/load feature to save the difficulty setting of the game (temperature and windspeed) as well 


