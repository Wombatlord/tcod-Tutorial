from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphicDt = np.dtype(
    [
        ('ch', np.int32),  # Unicode codepoint.
        ('fg', '3B'),  # 3 unsigned bytes for RGB.
        ('bg', '3B'),
    ]
)

# Tile struct used for statically defined tile data.
tileDt = np.dtype(
    [
        ('walkable', np.bool),  # True if this tile can be walked over.
        ('transparent', np.bool),  # True if this tile doesn't block FOV.
        ('dark', graphicDt),  # Graphics for tile out of FOV.
    ]
)


def newTile(
        *,  # Enforce the use of keywords, so that parameter order doesn't matter.
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types."""
    return np.array((walkable, transparent, dark), dtype=tileDt)


floor = newTile(
    walkable=True, transparent=True, dark=(ord(' '), (255, 255, 255), (50, 50, 150))
)
wall = newTile(
    walkable=False, transparent=False, dark=(ord('#'), (255, 255, 255), (0, 0, 100))
)
