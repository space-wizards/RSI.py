from enum import Enum


class Direction(Enum):
    SOUTH = 0
    NORTH = 1
    EAST = 2
    WEST = 3

    def to_byond(self) -> int:
        if self == Direction.NORTH:
            return 1
        elif self == Direction.SOUTH:
            return 2
        elif self == Direction.EAST:
            return 4
        elif self == Direction.WEST:
            return 8
        else:
            raise ValueError()
