import json
import math
from pathlib import Path
from typing import Dict, Tuple, Union, cast, TextIO, Any, List, TypeVar, Type
from PIL import Image
from .direction import Direction
from .helpers import state_name
from .state import State

T = TypeVar("T")
RSI_LATEST_COMPATIBLE = 1


class Rsi(object):
    def __init__(self, size: Tuple[int, int]) -> None:
        # Keys are the same as the name on disk (name+flag+flag+flag...)
        self.states = {}  # type: Dict[str, State]
        self.size = size  # type: Tuple[int, int]

    def get_state(self, name: str, selectors: List[str] = None) -> State:
        return self.states.get(state_name(name, selectors))

    def set_state(self, state: State, name: str, selectors: List[str] = None) -> None:
        self.states[state_name(name, selectors)] = state

    def new_state(self, directions: int, name: str, selectors: List[str] = None) -> State:
        newstate = State(name, selectors, self.size, directions)
        self.set_state(newstate, name, selectors)
        return newstate

    def write(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)

        # Make sure the write target is valid.
        if path.exists():
            if not path.is_dir():
                raise IOError("Attempted to write RSI to a non-directory.")

        else:
            path.mkdir()

        # Write metadata json file.
        metapath = path.joinpath("meta.json")  # type: Path
        metajson = {}  # type: Dict[str, Any]
        metajson["version"] = RSI_LATEST_COMPATIBLE
        metajson["size"] = {"x": self.size[0], "y": self.size[1]}

        states = []  # type: List[Dict[str, Any]]
        for state in self.states.values():
            statedict = {}  # type: Dict[str, Any]
            statedict["name"] = state.name
            statedict["select"] = state.selectors
            statedict["flags"] = state.flags
            statedict["directions"] = state.directions
            statedict["delays"] = state.delays
            # Non-standard, but removed after the sort so the sort can use it.
            statedict["fullname"] = state.full_name

            states.append(statedict)

        states.sort(key=lambda x: x["fullname"])

        for statedata in states:
            del statedata["fullname"]

        metajson["states"] = states

        with metapath.open("w") as f:
            f.write(json.dumps(metajson))

        # Write PNG files.
        for state in self.states.values():
            # Amount of columns is the square root of the amount of icons rounded up.
            # Amount of rows is the amount of icons divided by the above rounded up.
            # This ensures it's always as square as possible while being more horizontal if needed.
            count = 0
            for iconlist in state.icons:
                count += len(iconlist)

            horizontal = math.ceil(math.sqrt(count))
            sheetdimensions = horizontal, math.ceil(
                count / horizontal)
            image = Image.new(mode="RGBA", size=(
                self.size[0] * sheetdimensions[0], self.size[1] * sheetdimensions[1]))

            count = 0
            for iconlist in state.icons:
                for icon in iconlist:
                    row = count % sheetdimensions[0]
                    column = count // sheetdimensions[0]

                    point = row * self.size[0], column * \
                        self.size[1]
                    image.paste(icon, box=point)

                    count += 1
                # break

            pngpath = path.joinpath(state.full_name + ".png")  # type: Path
            image.save(pngpath, "PNG")

    @classmethod
    def open(cls: Type[T], path: Union[str, Path]) -> "Rsi":
        if isinstance(path, str):
            path = Path(path)

        if not path.is_dir():
            raise ValueError("Non-directory passed to open().")

        metapath = path.joinpath("meta.json")  # type: Path
        with metapath.open() as f:
            meta = json.loads(f.read())  # type: Dict[str, Any]

        print(meta)

        rsi = Rsi((meta["size"]["x"], meta["size"]["y"]))  # type: Rsi

        for state in meta["states"]:
            newstate = rsi.new_state(
                state["directions"], state["name"], state["select"])  # type: State
            newstate.flags = state["flags"]

            image = Image.open(path.joinpath(
                newstate.full_name + ".png"))  # type: Image.Image

            sheetdimensions = image.width // rsi.size[0], image.height // rsi.size[1]

            totaldone = 0  # type: int
            for direction in range(newstate.directions):
                todo = 1  # type: int
                if state.get("delays") is not None and state["delays"][direction]:
                    todo = len(state["delays"][direction])
                    newstate.delays[direction] = state["delays"][direction]

                newstate.icons[direction] = [None] * todo

                # Crop the icons.
                for x in range(todo):
                    # Get coordinates to cut at from main image.
                    box = ((totaldone % sheetdimensions[0]) * rsi.size[0],
                           (totaldone // sheetdimensions[0]) * rsi.size[1])

                    cropped = image.crop(
                        (box[0], box[1], box[0] + rsi.size[0], box[1] + rsi.size[1]))
                    newstate.icons[direction][x] = cropped
                    totaldone += 1

        return rsi

    @classmethod
    def from_dmi(cls: Type[T], path: Union[str, Path]) -> "Rsi":
        try:
            from byond.DMI import DMI
        except ImportError:
            raise ImportError("Unable to import byondtoolsv3.")

        if isinstance(path, Path):
            path = str(path)

        # N3X15, if you are reading this:
        # You are awful at API design.
        dmi = DMI(path)
        dmi.loadAll()
        rsi = Rsi((dmi.icon_width, dmi.icon_height))

        for dmstate in dmi.states.values():
            if dmstate.dirs == 8:
                continue

            rsstate = rsi.new_state(dmstate.dirs, dmstate.name)  # type: State

            # BYOND does not permit direction specific delays so this is easy.
            for x in range(rsstate.directions):
                direction = Direction(x)
                rsstate.delays[x] = []
                for y in range(dmstate.frames):
                    print(y, dmstate.frames, dmstate.delay)
                    # Circumvent around a BYOND bug (?)
                    # where states have more delays than actual frames.
                    if dmstate.frames <= y:
                        break

                    if dmstate.frames != 1:
                        delay = float(dmstate.delay[y])
                    else:
                        delay = 1.0
                    rsstate.delays[x].append(delay)
                    rsstate.icons[x].append(dmstate.getFrame(direction.to_byond(), y))

        return rsi
