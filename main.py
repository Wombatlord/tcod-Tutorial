import tcod

sheetColumns = 32
sheetRows = 8
tilePath = r"C:\Users\Owner\PycharmProjects\tcodTutorial\assets\dejavu10x10_gs_tc.png"


def main() -> None:
    screenWidth = 80
    screenHeight = 50

    tileset = tcod.tileset.load_tilesheet(
        tilePath,
        sheetColumns,
        sheetRows,
        tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new_terminal(
            screenWidth,
            screenHeight,
            tileset=tileset,
            title="Yet Another Roguelike Tutorial",
            vsync=True,
    ) as context:
        rootConsole = tcod.Console(screenWidth, screenHeight, order="F")
        while True:
            rootConsole.print(x=int(screenWidth / 2), y=int(screenHeight / 2), string="@")

            context.present(rootConsole)

            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()


if __name__ == "__main__":
    main()
