from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from src.engine.inputHandlers import EventHandler
from src.gameState.entities import Entity
from src.map.gameMap import GameMap


class Engine:
    def __init__(self, entities: Set[Entity], eventHandler: EventHandler, gameMap: GameMap, player: Entity):
        self.entities = entities
        self.eventHandler = eventHandler
        self.gameMap = gameMap
        self.player = player
        self.updateFOV()

    def handleEvents(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.eventHandler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.updateFOV()  # Update FOV before player's next action.

    def updateFOV(self):
        """Recompute the visible area based on the players point of view."""
        self.gameMap.visible[:] = compute_fov(
            self.gameMap.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
            light_walls=True,
        )
        # If a tile is "visible" it should be added to "explored".
        self.gameMap.explored |= self.gameMap.visible

    def render(self, console: Console, context: Context) -> None:
        self.gameMap.render(console)
        for entity in self.entities:
            # Only print entities in FOV.
            if self.gameMap.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.colour)

        context.present(console)
        console.clear()
