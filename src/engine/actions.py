from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING
from src.display import colours
from src.engine import exceptions

if TYPE_CHECKING:
    from src.engine.engine import Engine
    from src.entities.entity import Entity, Actor, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gameMap.engine

    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform this action with the objects needed to determine its scope.

        'self.engine' is the scope this action is being performed in.

        'self.entity' is the object performing the action.

        This method must be overridden by Action Subclasses
        """
        raise NotImplementedError()


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actorLocationX = self.entity.x
        actorLocationY = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.gameMap.items:
            if actorLocationX == item.x and actorLocationY == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Inventory is full.")

                self.engine.gameMap.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.messageLog.addMessage(f"You pick up the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    def __init__(
            self, entity: Actor, item: Item, targetXY: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not targetXY:
            targetXY = entity.x, entity.y
        self.targetXY = targetXY

    @property
    def targetActor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.gameMap.getActorAtLocation(*self.targetXY)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        self.item.consumeable.activate(self)


class DropAction(ItemAction):
    def perform(self) -> None:
        self.entity.inventory.drop(self.item)


class WaitAction(Action):
    def perform(self) -> None:
        pass


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def destXY(self) -> Tuple[int, int]:
        """Returns the actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blockingEntity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination."""
        return self.engine.gameMap.getBlockingEntityAtLocation(*self.destXY)

    @property
    def targetActor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.gameMap.getActorAtLocation(*self.destXY)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.targetActor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defence
        attackDesc = f"{self.entity.name.capitalize()} attacks {target.name}"

        if self.entity is self.engine.player:
            attackColour = colours.playerAtk
        else:
            attackColour = colours.enemyAtk

        if damage > 0:
            self.engine.messageLog.addMessage(
                f"{attackDesc} for {damage} hit points.",
                fg=attackColour
            )
            target.fighter.hp -= damage
        else:
            self.engine.messageLog.addMessage(
                f"{attackDesc} but does no damage.",
                fg=attackColour
            )


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        destX, destY = self.destXY

        if not self.engine.gameMap.inBounds(destX, destY):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")

        if not self.engine.gameMap.tiles['walkable'][destX, destY]:
            # Destination blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")

        if self.engine.gameMap.getBlockingEntityAtLocation(destX, destY):
            # Destination blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.targetActor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
