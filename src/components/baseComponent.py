from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine.engine import Engine
    from src.entities.entity import Entity
    from src.map.gameMap import GameMap


class BaseComponent:
    parent: Entity  # Owning entity instance.

    @property
    def gameMap(self) -> GameMap:
        return self.parent.gameMap

    @property
    def engine(self) -> Engine:
        return self.gameMap.engine
