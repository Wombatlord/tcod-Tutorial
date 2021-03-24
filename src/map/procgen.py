import random
import tcod
from typing import Iterator, Tuple
from src.map.gameMap import GameMap
from src.map import tileTypes


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def centre(self) -> Tuple[int, int]:
        centreX = int((self.x1 + self.x2) / 2)
        centreY = int((self.y1 + self.y2) / 2)

        return centreX, centreY

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)


def tunnelBetween(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance
        # Move Horizontal, then Vertical.
        cornerX, cornerY = x2, y1
    else:
        # Move Vertically, then Horizontal.
        cornerY, cornerX = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (cornerX, cornerY)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((cornerX, cornerY), (x2, y2)).tolist():
        yield x, y


def generateDungeon(mapWidth, mapHeight) -> GameMap:
    dungeon = GameMap(mapWidth, mapHeight)

    room1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room2 = RectangularRoom(x=35, y=13, width=10, height=20)

    dungeon.tiles[room1.inner] = tileTypes.floor
    dungeon.tiles[room2.inner] = tileTypes.floor

    for x, y in tunnelBetween(room2.centre, room1.centre):
        dungeon.tiles[x, y] = tileTypes.floor

    return dungeon
