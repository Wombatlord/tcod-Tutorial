from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from src.engine.renderFunctions import renderBar
from src.engine.inputHandlers import MainGameEventHandler

if TYPE_CHECKING:
    from src.entities.entity import Actor
    from src.map.gameMap import GameMap
    from src.engine.inputHandlers import EventHandler


class Engine:
    gameMap: GameMap

    def __init__(self, player: Actor):
        self.eventHandler: EventHandler = MainGameEventHandler(self)
        self.player = player

    def handleEnemyTurns(self) -> None:
        for entity in set(self.gameMap.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

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

        renderBar(
            console=console,
            currentValue=self.player.fighter.hp,
            maxValue=self.player.fighter.maxHP,
            totalWidth=20,
        )

        # console.print(
        #     x=1,
        #     y=47,
        #     string=f"HP: {self.player.fighter.hp}/{self.player.fighter.maxHP}",
        #     # string="HP: " + "|" * self.player.fighter.hp,
        # )

        context.present(console)
        console.clear()
