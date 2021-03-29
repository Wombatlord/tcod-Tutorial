from __future__ import annotations

from typing import  Optional, TYPE_CHECKING

from src.engine import actions
from src.display import colours
from src.components.baseComponent import BaseComponent
from src.engine.exceptions import Impossible

if TYPE_CHECKING:
    from src.entities.entity import Actor, Item


class Consumeable(BaseComponent):
    parent: Item

    def getAction(self, consumer: Actor) -> Optional[actions.Action]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        """
        Invoke this item's ability.
        'action' is the context for this activation.
        """
        raise NotImplementedError()


class HealingConsumeable(Consumeable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amountRecovered = consumer.fighter.heal(self.amount)

        if amountRecovered > 0:
            self.engine.messageLog.addMessage(
                f"You consume the {self.parent.name} and recover {amountRecovered} HP!",
                colours.healthRecovered,
            )
        else:
            raise Impossible("You are already at full HP.")