from __future__ import annotations

from typing import TYPE_CHECKING

from src.display import colours

if TYPE_CHECKING:
    from tcod import Console


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
