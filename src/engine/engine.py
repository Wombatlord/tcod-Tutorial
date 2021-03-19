from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from src.engine.actions import EscapeAction, MovementAction
from src.engine.inputHandlers import EventHandler
from src.gameState.entities import Entity
from src.map.gameMap import GameMap


class Engine:
    def __init__(self, entities: Set[Entity], eventHandler: EventHandler, gameMap: GameMap,player: Entity):
        self.entities = entities
        self.eventHandler = eventHandler
        self.gameMap = gameMap
        self.player = player

    def handleEvents(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.eventHandler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        self.gameMap.render(console)
        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.colour)

        context.present(console)
        console.clear()
