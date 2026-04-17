import enum


class Status(enum.Enum):
    """
    Enum representing the Status of a position on a goban
    """

    WHITE = 1
    BLACK = 2
    EMPTY = 3
    OUT = 4

DIRECTIONS = (
    (0, -1), # down
    (0, 1),  # up
    (-1, 0), # left
    (1, 0)   # right
)

class Goban:
    def __init__(self, goban: list[str]) -> None:
        self.goban = goban

    def get_status(self, x: int, y: int) -> Status:
        """
        Get the status of a given position

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            a Status
        """
        if (
            not self.goban
            or x < 0
            or y < 0
            or y >= len(self.goban)
            or x >= len(self.goban[0])
        ):
            return Status.OUT
        elif self.goban[y][x] == ".":
            return Status.EMPTY
        elif self.goban[y][x] == "o":
            return Status.WHITE
        elif self.goban[y][x] == "#":
            return Status.BLACK
        raise ValueError(f"Unknown goban value {self.goban[y][x]}")

    def is_taken(self, x: int, y: int) -> bool:
        stone_status = self.get_status(x, y)
        if stone_status not in (Status.WHITE, Status.BLACK):
            return False # No stone here

        seen: set[tuple[int, int]] = {(x, y)}
        remaining = [(x, y)] 

        while remaining:
            ix, iy = remaining.pop()

            for dx, dy in DIRECTIONS:
                neighbour = (ix + dx, iy + dy)
                neighbour_status = self.get_status(*neighbour)

                if neighbour_status == Status.EMPTY:
                    return False # liberty found -> not taken 
                
                if neighbour_status == stone_status and neighbour not in seen:
                    seen.add(neighbour)
                    remaining.append(neighbour)
            
        return True # no liberties -> taken