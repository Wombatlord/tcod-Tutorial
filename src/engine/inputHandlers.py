from __future__ import annotations

from typing import Optional, TYPE_CHECKING
import tcod.event

from src.engine.actions import Action, EscapeAction, BumpAction

if TYPE_CHECKING:
    from src.engine.engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handleEvents(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handleEnemyTurns()
            self.engine.updateFOV()  # Update FOV before player's next action.

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        player = self.engine.player

        if key == tcod.event.K_KP_8:
            action = BumpAction(player, dx=0, dy=-1)
        elif key == tcod.event.K_KP_2:
            action = BumpAction(player, dx=0, dy=1)
        elif key == tcod.event.K_KP_4:
            action = BumpAction(player, dx=-1, dy=0)
        elif key == tcod.event.K_KP_6:
            action = BumpAction(player, dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)

        return action
