from src.components.ai import HostileEnemy
from src.components.fighter import Fighter
from src.entities.entity import Actor

player = Actor(
    char="@",
    colour=(255, 255, 255),
    name="Player",
    aiCLS=HostileEnemy,
    fighter=Fighter(hp=30, defence=2, power=5),
)

orc = Actor(
    char="o",
    colour=(63, 127, 63),
    name="Orc",
    aiCLS=HostileEnemy,
    fighter=Fighter(hp=10, defence=0, power=3),
)

troll = Actor(
    char="T",
    colour=(0, 127, 0),
    name="Troll",
    aiCLS=HostileEnemy,
    fighter=Fighter(hp=16, defence=1, power=4),
)