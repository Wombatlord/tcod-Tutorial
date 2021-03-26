from __future__ import annotations
from typing import TYPE_CHECKING, Iterable
import numpy as np  # type: ignore
from tcod.console import Console

from src.map import tileTypes

if TYPE_CHECKING:
    from src.entities.entities import Entity


class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tileTypes.wall, order='F')

        # Tiles currently in view.
        self.visible = np.full((width, height), fill_value=False, order="F")

        # Tiles the player has seen before.
        self.explored = np.full((width, height), fill_value=False, order="F")

    def inBounds(self, x: int, y: int) -> bool:
        """Return True if x and y are within the bounds of this map"""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, draw it with "light" colours.
        If it isn't, but is in the "explored" array, draw it with "dark" colours.
        Else, default is "SHROUD". This draws tiles not in either array as black.
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tileTypes.SHROUD
        )

        for entity in self.entities:
            # Only print entities in FOV.
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.colour)
