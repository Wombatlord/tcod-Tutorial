from src.entities.entities import Entity

player = Entity(char="@", colour=(255, 255, 255), name="Player", blocksMovement=True)

orc = Entity(char="o", colour=(63, 127, 63), name="Orc", blocksMovement=True)
troll = Entity(char="T", colour=(0, 127, 0), name="Troll", blocksMovement=True)