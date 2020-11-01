# async-console-game

Small console game about wandering in space among tons of garbage. The game is driven by the power of coroutines. Btw, game is also about lasers and explosions. 

## How to run the game?

- You need Python 3 installed on your system. (3.7+)
- To start the game just run `python3 main.py`

## Controls

- Use **ARROWS** on your keyboard to control a spaceship;
- Press **SPACE** to shoot a laser gun (btw, it is locked in the very beginning);

## Config

You can freely change `config.py` and experiment with the game.

- Try `BORDERS = True` to see borders of the obstacles;
- Change `START_YEAR` to `2020` to unlock the gun right from the start;
- `STAR_DENSITY` is a percentage of stars on the screen. Increase it to behold a star chaos;
- Add new characters to `STARS` to see new stars in the game;
- Update `START_DELTA` to change start position of the ship;
- Change `LASER_SPEED` or `SPACESHIP_SPEED` to modify difficulty;

The pace of the game might seem a little bit slow. You can make the game 2x faster by changing `TIC_TIMEOUT` to `0.05` or even 10x faster by changing it to `0.01` (Hard mode).
