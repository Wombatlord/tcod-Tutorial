from __future__ import annotations

from typing import TYPE_CHECKING

from src.display import colours

if TYPE_CHECKING:
    from tcod import Console
    from src.engine.engine import Engine
    from src.map.gameMap import GameMap


def getNamesAtLocation(x: int, y: int, gameMap: GameMap) -> str:
    if not gameMap.inBounds(x, y) or not gameMap.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in gameMap.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def renderBar(
        console: Console, currentValue: int, maxValue: int, totalWidth: int
) -> None:
    barWidth = int(float(currentValue) / maxValue * totalWidth)

    console.draw_rect(x=0, y=45, width=20, height=1, ch=1, bg=colours.barEmpty)

    if barWidth > 0:
        console.draw_rect(
            x=0, y=45, width=barWidth, height=1, ch=1, bg=colours.barFilled
        )

    console.print(
        x=1, y=45, string=f"HP: {currentValue}/{maxValue}", fg=colours.barText
    )


def renderNamesAtMouseLocation(
        console: Console, x: int, y: int, engine: Engine
) -> None:
    mouseX, mouseY = engine.mouseLocation

    namesAtMouseLocation = getNamesAtLocation(
        x=mouseX, y=mouseY, gameMap=engine.gameMap
    )

    console.print(x=x, y=y, string=namesAtMouseLocation)
