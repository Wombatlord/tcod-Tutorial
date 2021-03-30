from __future__ import annotations
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union
from src.map.renderOrder import RenderOrder
import copy

if TYPE_CHECKING:
    from src.components.ai import BaseAI
    from src.components.consumeable import Consumeable
    from src.components.fighter import Fighter
    from src.components.inventory import Inventory
    from src.map.gameMap import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object representing players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
            self,
            parent: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            colour: tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocksMovement: bool = False,
            renderOrder: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.name = name
        self.blocksMovement = blocksMovement
        self.renderOrder = renderOrder
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gameMap(self) -> GameMap:
        return self.parent.gameMap

    def spawn(self: T, gameMap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gameMap
        gameMap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gameMap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location. Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gameMap:
            if hasattr(self, "parent"):  # Possibly un-initialized.
                if self.parent is self.gameMap:
                    self.gameMap.entities.remove(self)
            self.parent = gameMap
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
            fighter: Fighter,
            inventory: Inventory,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            colour=colour,
            name=name,
            blocksMovement=True,
            renderOrder=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = aiCLS(self)

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

    @property
    def isAlive(self) -> bool:
        """Returns True as long as thie actor can perform actions."""
        return bool(self.ai)


class Item(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            colour: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            consumeable: Consumeable,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            colour=colour,
            name=name,
            blocksMovement=False,
            renderOrder=RenderOrder.ITEM,
        )

        self.consumeable = consumeable
        self.consumeable.parent = self
