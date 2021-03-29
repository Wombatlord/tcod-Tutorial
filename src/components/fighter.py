from __future__ import annotations
from typing import TYPE_CHECKING
from src.components.baseComponent import BaseComponent
from src.engine.inputHandlers import GameOverEventHandler
from src.map.renderOrder import RenderOrder
from src.display import colours

if TYPE_CHECKING:
    from src.entities.entity import Actor


class Fighter(BaseComponent):
    parent: Actor

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
        if self._hp == 0 and self.parent.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.parent:
            deathMessage = "fucked it."
            deathMessageColour = colours.playerDie
            self.engine.eventHandler = GameOverEventHandler(self.engine)
        else:
            deathMessage = f"{self.parent.name} is dead!"
            deathMessageColour = colours.enemyDie

        self.parent.char = "%"
        self.parent.colour = (191, 0, 0)
        self.parent.blocksMovement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.renderOrder = RenderOrder.CORPSE

        self.engine.messageLog.addMessage(deathMessage, deathMessageColour)

    def heal(self, amount: int) -> int:
        if self.hp == self.maxHP:
            return 0

        newHPValue = self.hp + amount

        if newHPValue > self.maxHP:
            newHPValue = self.maxHP

        amountRecovered = newHPValue - self.hp

        self.hp = newHPValue

        return amountRecovered

    def takeDamage(self, amount: int) -> None:
        self.hp -= amount