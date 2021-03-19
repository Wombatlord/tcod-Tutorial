from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from src.engine.actions import EscapeAction, MovementAction
from src.engine.inputHandlers import EventHandler
from src.gameState.entities import Entity


class Engine:
    def __init__(self, entities: Set[Entity], eventHandler: EventHandler, player: Entity):
        self.entities = entities
        self.eventHandler = eventHandler
        self.player = player

    def handleEvents(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.eventHandler.dispatch(event)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)

            elif isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.colour)

        context.present(console)
        console.clear()
