from typing import List, Reversible, Tuple
import textwrap

import tcod

from src.display import colours


class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plainText = text
        self.fg = fg
        self.count = 1

    @property
    def fullText(self) -> str:
        """The full text of the message, including the count if necessary."""
        if self.count > 1:
            return f"{self.plainText} (x{self.count})"
        return self.plainText


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def addMessage(
            self, text: str, fg: Tuple[int, int, int] = colours.white, *, stack: bool = True,
    ) -> None:
        """Add a message to this log.
        'text' is the message text, 'fg' is text colour.
        If 'stack' is True then the message can stack with a previous message
        of the same text."""

        if stack and self.messages and text == self.messages[-1].plainText:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
            self, console: tcod.Console, x: int, y: int, width: int, height: int,
    ) -> None:
        """Render this log over the given area.
        'x', 'y', 'width', 'height', is the rectangular region
        to render onto the 'console'.
        """
        self.renderMessages(console, x, y, width, height, self.messages)

    @staticmethod
    def renderMessages(
            console: tcod.Console,
            x: int,
            y: int,
            width: int,
            height: int,
            messages: Reversible[Message],
    ) -> None:
        """Render the messages provided.
        The 'messages' are rendered starting at the last message
        and working backwards."""
        yOffset = height - 1

        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.fullText, width)):
                console.print(x=x, y=y + yOffset, string=line, fg=message.fg)
                yOffset -= 1
                if yOffset < 0:
                    return  # No more space to print messages.
