import tcod
from src.engine.actions import EscapeAction, MovementAction
from src.engine.inputHandlers import EventHandler

WIDTH = 80
HEIGHT = 50
SHEETCOLS = 32
SHEETROWS = 8
TILEPATH = r"C:\Users\Owner\PycharmProjects\tcodTutorial\assets\dejavu10x10_gs_tc.png"


def main() -> None:
    playerX = int(WIDTH / 2)
    playerY = int(HEIGHT / 2)

    tileset = tcod.tileset.load_tilesheet(
        TILEPATH,
        SHEETCOLS,
        SHEETROWS,
        tcod.tileset.CHARMAP_TCOD
    )

    eventHandler = EventHandler()

    with tcod.context.new_terminal(
            WIDTH,
            HEIGHT,
            tileset=tileset,
            title="Yet Another Roguelike Tutorial",
            vsync=True,
    ) as context:
        rootConsole = tcod.Console(WIDTH, HEIGHT, order="F")
        while True:
            rootConsole.print(x=playerX, y=playerY, string="@")

            context.present(rootConsole)

            rootConsole.clear()

            for event in tcod.event.wait():
                action = eventHandler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    playerX += action.dx
                    playerY += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()
