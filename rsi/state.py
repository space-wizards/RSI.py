from typing import List, Tuple, Dict, Any
from PIL import Image

class State(object):
    def __init__(self,
                 name: str,
                 size: Tuple[int, int],
                 directions: int = 1) -> None:
        self.name = name  # type: str
        self.flags = {}  # type: Dict[str, Any]
        self.size = size  # type: Tuple[int, int]
        self.directions = directions  # type: int

        self.delays = [[] for i in range(self.directions)]  # type: List[List[float]]
        self.icons = [[] for i in range(self.directions)]  # type: List[List[Image.Image]]
