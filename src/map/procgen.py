from __future__ import annotations
import random
import tcod
from typing import Iterator, Tuple, List, TYPE_CHECKING
from src.map.gameMap import GameMap
from src.map import tileTypes

if TYPE_CHECKING:
    from src.gameState.entities import Entity


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

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def tunnelBetween(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance
        # Move Horizontal, then Vertical.
        cornerX, cornerY = x2, y1
    else:
        # Move Vertically, then Horizontal.
        cornerX, cornerY = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (cornerX, cornerY)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((cornerX, cornerY), (x2, y2)).tolist():
        yield x, y


def generateDungeon(
    maxRooms: int,
    minRoomSize: int,
    maxRoomSize: int,
    mapWidth: int,
    mapHeight: int,
    player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(mapWidth, mapHeight)

    rooms: List[RectangularRoom] = []

    for r in range(maxRooms):
        roomWidth = random.randint(minRoomSize, maxRoomSize)
        roomHeight = random.randint(minRoomSize, maxRoomSize)

        x = random.randint(0, dungeon.width - roomWidth - 1)
        y = random.randint(0, dungeon.height - roomHeight - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        newRoom = RectangularRoom(x, y, roomWidth, roomHeight)

        # Run through the other rooms and see if they intersect with this one.
        if any(newRoom.intersects(otherRoom) for otherRoom in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[newRoom.inner] = tileTypes.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.x, player.y = newRoom.centre
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnelBetween(rooms[-1].centre, newRoom.centre):
                dungeon.tiles[x, y] = tileTypes.floor

        # Finally, append the new room to the list.
        rooms.append(newRoom)

    return dungeon
