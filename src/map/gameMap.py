import numpy as np  # type: ignore
from tcod.console import Console

from src.map import tileTypes


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tileTypes.wall, order='F')

    def inBounds(self, x: int, y: int) -> bool:
        """Return True if x and y are within the bounds of this map"""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles['dark']
