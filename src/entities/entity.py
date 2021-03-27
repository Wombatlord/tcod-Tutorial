from __future__ import annotations
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from src.components.ai import BaseAI
    from src.components.fighter import Fighter
    from src.map.gameMap import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object representing players, enemies, items, etc.
    """

    gameMap: GameMap

    def __init__(
            self,
            gameMap: Optional[GameMap] = None,
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
        if gameMap:
            # If gameMap isn't provided now then it will be set later.
            self.gameMap = gameMap
            gameMap.entities.add(self)

    def spawn(self: T, gameMap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gameMap = gameMap
        gameMap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gameMap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location. Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gameMap:
            if hasattr(self, "gameMap"):  # Possibly un-initialized.
                self.gameMap.entities.remove(self)
            self.gameMap = gameMap
            gameMap.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy


class Actor(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            colour: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            aiCLS: Type[BaseAI],
            fighter: Fighter
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            colour=colour,
            name=name,
            blocksMovement=True
        )

        self.ai: Optional[BaseAI] = aiCLS(self)

        self.fighter = fighter
        self.fighter.entity = self

    @property
    def isAlive(self) -> bool:
        """Returns True as long as thie actor can perform actions."""
        return bool(self.ai)