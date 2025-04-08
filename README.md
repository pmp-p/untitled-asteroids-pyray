# An Untitled Asteroids Game

A retro-styled Asteroids game clone where you survive as long as possible avoiding asteroids while collecting powerups to keep you alive and treasure to increase your score. 

## Core Gameplay

This game utilizes a state stack system to manage various game screens, enabling smooth transitions between menus and gameplay. The core gameplay loop activates when the game enters the Gameplay state. The game involves avoiding randomly spawning asteroids, collecting treasures, and managing resources, with a progressive difficulty system that adapts as the player survives. 

### Asteroids
Asteroids spawn randomly from the top of the screen and are deleted upon exiting the edges of the game window. Asteroids come in three types: Normal (Deals regular damage to the player upon collision), Icy (Deals less damage but freezes the player for a brief period), Fiery (Deals more damage to the player)

### Player

While avoiding asteroids, the player can collect various items; Treasure increases the player's score, Ammo refills the player's ammo capacity, Health packs restore player health, and Oxygen tanks can be shot to collect the resulting oxygen bubble to. Player oxygen drains over time and the player must manage ammo to collect enough oxygen bubbles to survive. The player's score multiplier also increases as they collect treasures and power-ups while avoiding asteroid collisions. However, the multiplier resets if the player is hit by an asteroid.

### Difficulty Progression

The game features a dynamic difficulty system that adjusts based on the player’s survival time: 

Asteroid Frequency: Initially, asteroids spawn at regular intervals. As the player survives, the number of asteroids increases.

Asteroid Speed: Over time, the speed range of asteroids increases in a set number of intervals, making the game more challenging.

There is a difficulty progression system as the player survives. First, the asteroids begin spawning at regular intervals at greater amounts each internal. Then, the speed range of the asteroids increase for a set number of intervals. 

A weather API is used to collect temperature and windspeed information for a city when a player types a city into the difficulty button in options. THe tmepreature is mapped to a dcionary that matches with a spawn distrbutions of teh asteroid types to simulate weather impacted asteroid spawning. The windspeed is used to set the default speed of the spawning asteroids.

When the player dies, time survived along with points is stored in a leaderboard and is sorted to have 5 players tracked up to. 

The game uses a save/load feature to save the difficulty setting of the game (temperature and windspeed) as well.


