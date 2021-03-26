from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from src.engine.inputHandlers import EventHandler
from src.entities.entities import Entity
from src.map.gameMap import GameMap


class Engine:
    def __init__(self, eventHandler: EventHandler, gameMap: GameMap, player: Entity):
        self.eventHandler = eventHandler
        self.gameMap = gameMap
        self.player = player
        self.updateFOV()

    def handleEnemyTurns(self) -> None:
        for entity in self.gameMap.entities - {self.player}:
            print(f"The {entity.name} prepares spaghet")

    def handleEvents(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.eventHandler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            self.handleEnemyTurns()
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
        context.present(console)
        console.clear()
