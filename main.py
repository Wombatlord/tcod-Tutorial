import tcod
from src.engine.engine import Engine
from src.entities.entities import Entity
from src.engine.inputHandlers import EventHandler
from src.map.procgen import generateDungeon

# Screen Constants
WIDTH = 80
HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45

# Tileset constants.
SHEET_COLS = 32
SHEET_ROWS = 8
TILE_PATH = r"C:\Users\Owner\PycharmProjects\tcodTutorial\assets\dejavu10x10_gs_tc.png"

# Room constants.
MAX_ROOM_SIZE = 10
MIN_ROOM_SIZE = 6
MAX_ROOMS = 30


def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        TILE_PATH,
        SHEET_COLS,
        SHEET_ROWS,
        tcod.tileset.CHARMAP_TCOD
    )

    eventHandler = EventHandler()
    player = Entity(int(WIDTH / 2), int(HEIGHT / 2), '@', (255, 255, 255))

    gameMap = generateDungeon(
        maxRooms=MAX_ROOMS,
        minRoomSize=MIN_ROOM_SIZE,
        maxRoomSize=MAX_ROOM_SIZE,
        mapWidth=MAP_WIDTH,
        mapHeight=MAP_HEIGHT,
        player=player
    )

    engine = Engine(eventHandler=eventHandler, gameMap=gameMap, player=player)

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

            events = tcod.event.wait()

            engine.handleEvents(events)


if __name__ == "__main__":
    main()
