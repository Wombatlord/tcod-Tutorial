from __future__ import annotations
from typing import Tuple, TypeVar, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from src.map.gameMap import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object representing players, enemies, items, etc.
    """
    def __init__(
            self,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            colour: tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocksMovement: bool = False,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.name = name
        self.blocksMovement = blocksMovement

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy