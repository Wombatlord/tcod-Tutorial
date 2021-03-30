from __future__ import annotations

from typing import Optional, TYPE_CHECKING
import tcod.event

from src.engine import actions
from src.engine.actions import (
    Action,
    BumpAction,
    WaitAction,
    PickupAction,
)

from src.display import colours
from src.engine import exceptions
from src.entities.entity import Item

if TYPE_CHECKING:
    from src.engine.engine import Engine

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handleEvents(self, event: tcod.event.Event) -> None:
        self.handleAction(self.dispatch(event))

    def handleAction(self, action):
        """
        Handle actions returned from event methods.
        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.messageLog.addMessage(exc.args[0], colours.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.handleEnemyTurns()

        self.engine.updateFOV()
        return True

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.gameMap.inBounds(event.tile.x, event.tile.y):
            self.engine.mouseLocation = event.tile.x, event.tile.y

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def onRender(self, console: tcod.Console) -> None:
        self.engine.render(console)


class AskUserEventHandler(EventHandler):
    """Handles user input for actions which require special input."""

    def handleAction(self, action: Optional[Action]) -> bool:
        """Return to the main event handler when a valid action was performed."""
        if super().handleAction(action):
            self.engine.eventHandler = MainGameEventHandler(self.engine)
            return True
        return False

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """By default any key exists this input handler."""
        if event.sym in {  # Ignore modifier keys.
            tcod.event.K_LSHIFT,
            tcod.event.K_RSHIFT,
            tcod.event.K_LCTRL,
            tcod.event.K_RCTRL,
            tcod.event.K_LALT,
            tcod.event.K_RALT,
        }:
            return None
        return self.onExit()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
        """By default any mouse click exits this input handler."""
        return self.onExit()

    def onExit(self) -> Optional[Action]:
        """Called when the user is trying to exit or cancel an action.
        By default this returns to the main event handler.
        """
        self.engine.eventHandler = MainGameEventHandler(self.engine)
        return None


class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.
    What happens depends on the subclass.
    """
    TITLE = "<missing title>"

    def onRender(self, console: tcod.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory,
        and the letter to select them.

        Will move to a different position based on where the player is located,
        so the player can always see where they are."""
        super().onRender(console)
        numberOfItemsInInventory = len(self.engine.player.inventory.items)

        height = numberOfItemsInInventory + 2

        if height <= 3:
            height = 3

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if numberOfItemsInInventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                itemKey = chr(ord("a") + i)
                console.print(x + 1, y + i + 1, f"({itemKey}) {item.name}")

        else:
            console.print(x + 1, y + 1, "(Empty)")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <= index <= 26:
            try:
                selectedItem = player.inventory.items[index]
            except IndexError:
                self.engine.messageLog.addMessage("Invalid entry.", colours.invalid)
                return None
            return self.onItemSelected(selectedItem)
        return super().ev_keydown(event)

    def onItemSelected(self) -> Optional[Action]:
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class InventoryActiveHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "Select an item to use"

    def onItemSelected(self, item: Item) -> Optional[Action]:
        """Return the action for the selected item."""
        return item.consumeable.getAction(self.engine.player)


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "Select an item to drop."

    def onItemSelected(self, item: Item) -> Optional[Action]:
        """Drop this item."""
        return actions.DropAction(self.engine.player, item)


class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        player = self.engine.player

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)

        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.K_ESCAPE:
            raise SystemExit()

        elif key == tcod.event.K_g:
            action = PickupAction(player)

        elif key == tcod.event.K_i:
            self.engine.eventHandler = InventoryActiveHandler(self.engine)

        elif key == tcod.event.K_d:
            self.engine.eventHandler = InventoryDropHandler(self.engine)

        elif key == tcod.event.K_v:
            self.engine.eventHandler = HistoryViewer(self.engine)

        # No valid key was pressed.
        return action


class GameOverEventHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_ESCAPE:
            raise SystemExit()


CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}


class HistoryViewer(EventHandler):
    """Print the message log on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.logLength = len(engine.messageLog.messages)
        self.cursor = self.logLength - 1

    def onRender(self, console: tcod.Console) -> None:
        super().onRender(console)  # Draw the main state as the background.

        logConsole = tcod.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        logConsole.draw_frame(0, 0, logConsole.width, logConsole.height)
        logConsole.print_box(
            0, 0, logConsole.width, 1, "┤Message History├", alignment=tcod.CENTER
        )

        # Render the message log using the cursor parameter.
        self.engine.messageLog.renderMessages(
            logConsole,
            1,
            1,
            logConsole.width - 2,
            logConsole.height - 2,
            self.engine.messageLog.messages[: self.cursor + 1],
        )
        logConsole.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        # Fancy conditional movement ot make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]

            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.logLength - 1

            elif adjust > 0 and self.cursor == self.logLength - 1:
                # Same with bottom to top movement.
                self.cursor = 0

            else:
                # Otherwise move while staying clamped to the bounds of the history.
                self.cursor = max(0, min(self.cursor + adjust, self.logLength - 1))

        elif event.sym == tcod.event.K_HOME:
            self.cursor = 0  # Move directly to top message.

        elif event.sym == tcod.event.K_END:
            self.cursor = self.logLength - 1  # Move directly to the last message.

        else:  # Any other key moves back to main game state.
            self.engine.eventHandler = MainGameEventHandler(self.engine)
