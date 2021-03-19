import tcod
from src.engine.engine import Engine
from src.gameState.entities import Entity
from src.map.gameMap import GameMap
from src.engine.inputHandlers import EventHandler

WIDTH = 80
HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
SHEET_COLS = 32
SHEET_ROWS = 8
TILE_PATH = r"C:\Users\Owner\PycharmProjects\tcodTutorial\assets\dejavu10x10_gs_tc.png"


def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        TILE_PATH,
        SHEET_COLS,
        SHEET_ROWS,
        tcod.tileset.CHARMAP_TCOD
    )
    eventHandler = EventHandler()

    player = Entity(int(WIDTH / 2), int(HEIGHT / 2), '@', (255, 255, 255))
    npc = Entity(int((WIDTH / 2) - 5), int(HEIGHT / 2), '@', (255, 0, 255))
    entities = {npc, player}

    gameMap = GameMap(MAP_WIDTH, MAP_HEIGHT)

    engine = Engine(entities=entities, eventHandler=eventHandler, gameMap=gameMap, player=player)

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
