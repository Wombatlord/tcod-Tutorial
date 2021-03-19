from typing import Tuple


class Entity:
    """
    A generic object representing players, enemies, items, etc.
    """
    def __init__(self, x: int, y: int, char: str, colour: tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy