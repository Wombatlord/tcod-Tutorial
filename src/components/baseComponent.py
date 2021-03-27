from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine.engine import Engine
    from src.entities.entity import Entity


class BaseComponent:
    entity: Entity  # Owning entity instance.

    @property
    def engine(self) -> Engine:
        return self.entity.gameMap.engine
