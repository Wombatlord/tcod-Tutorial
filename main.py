import copy
import tcod
from src.engine.engine import Engine
from src.entities import entityFactories
from src.map.procgen import generateDungeon
from src.display import colours

# Screen Constants
WIDTH = 80
HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 43

# Tileset constants.
SHEET_COLS = 32
SHEET_ROWS = 8
TILE_PATH = r"C:\Users\Owner\PycharmProjects\tcodTutorial\assets\dejavu10x10_gs_tc.png"

# Room constants.
MAX_ROOM_SIZE = 10
MIN_ROOM_SIZE = 6
MAX_ROOMS = 30
MAX_MONSTERS_PER_ROOM = 2


def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        TILE_PATH,
        SHEET_COLS,
        SHEET_ROWS,
        tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entityFactories.player)
    engine = Engine(player=player)

    engine.gameMap = generateDungeon(
        maxRooms=MAX_ROOMS,
        minRoomSize=MIN_ROOM_SIZE,
        maxRoomSize=MAX_ROOM_SIZE,
        mapWidth=MAP_WIDTH,
        mapHeight=MAP_HEIGHT,
        maxMonstersPerRoom=MAX_MONSTERS_PER_ROOM,
        engine=engine,
    )

    engine.updateFOV()

    engine.messageLog.addMessage(
        "Welcome to the dungeon! We've got fun and games!", colours.welcomeText
    )

    with tcod.context.new_terminal(
            WIDTH,
            HEIGHT,
            tileset=tileset,
            title="Yet Another Roguelike Tutorial",
            vsync=True,
    ) as context:
        rootConsole = tcod.Console(WIDTH, HEIGHT, order="F")
        while True:
            engine.render(console=rootConsole, context=context)

            engine.eventHandler.handleEvents()


if __name__ == "__main__":
    main()
