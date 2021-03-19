import tcod
from src.engine.engine import Engine
from src.engine.inputHandlers import EventHandler
from src.gameState.entities import Entity

WIDTH = 80
HEIGHT = 50
SHEETCOLS = 32
SHEETROWS = 8
TILEPATH = r"C:\Users\Owner\PycharmProjects\tcodTutorial\assets\dejavu10x10_gs_tc.png"


def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        TILEPATH,
        SHEETCOLS,
        SHEETROWS,
        tcod.tileset.CHARMAP_TCOD
    )
    eventHandler = EventHandler()

    player = Entity(int(WIDTH / 2), int(HEIGHT / 2), '@', (255, 255, 255))
    npc = Entity(int((WIDTH / 2) - 5), int((HEIGHT / 2) - 5), '@', (255, 0, 255))
    entities = {npc, player}

    engine = Engine(entities=entities, eventHandler=eventHandler, player=player)

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
