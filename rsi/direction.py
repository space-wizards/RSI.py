from enum import Enum


class Direction(Enum):
    SOUTH = 0
    NORTH = 1
    EAST = 2
    WEST = 3

    SOUTH_EAST = 4
    SOUTH_WEST = 5
    NORTH_EAST = 6
    NORTH_WEST = 7

    def to_byond(self) -> int:
        BY_NORTH = 1
        BY_SOUTH = 2
        BY_EAST = 4
        BY_WEST = 8

        if self == Direction.NORTH:
            return BY_NORTH
        elif self == Direction.SOUTH:
            return BY_SOUTH
        elif self == Direction.EAST:
            return BY_EAST
        elif self == Direction.WEST:
            return BY_WEST
        elif self == Direction.SOUTH_EAST:
            return BY_SOUTH | BY_EAST
        elif self == Direction.SOUTH_WEST:
            return BY_SOUTH | BY_WEST
        elif self == Direction.NORTH_EAST:
            return BY_NORTH | BY_EAST
        elif self == Direction.NORTH_WEST:
            return BY_NORTH | BY_WEST
        else:
            raise ValueError()
