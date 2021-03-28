from __future__ import annotations
from typing import TYPE_CHECKING
from src.components.baseComponent import BaseComponent
from src.map.renderOrder import RenderOrder

if TYPE_CHECKING:
    from src.entities.entity import Actor


class Fighter(BaseComponent):
    entity: Actor

    def __init__(self, hp: int, defence: int, power: int):
        self.maxHP = hp
        self._hp = hp
        self.defence = defence
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> int:
        self._hp = max(0, min(value, self.maxHP))
        if self._hp == 0 and self.entity.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.entity:
            deathMessage = "fucked it."
        else:
            deathMessage = f"{self.entity.name} is dead!"

        self.entity.char = "%"
        self.entity.colour = (191, 0, 0)
        self.entity.blocksMovement = False
        self.entity.ai = None
        self.entity.name = f"remains of {self.entity.name}"
        self.entity.renderOrder = RenderOrder.CORPSE

        print(deathMessage)