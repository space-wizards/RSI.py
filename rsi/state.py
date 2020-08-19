from typing import List, Tuple, Dict, Any
from PIL import Image
from pathlib import Path


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


def rsi_state_diff(source: Path, target: Path, output: Path) -> None:
    """
    Gets the pixels in the source image that aren't in the target image and outputs to the output image.
    This does NOT get the color difference between the 2 pixels.
    Can also account for multiple frames.
    This whole thing is very .rsi specialized so it's not recommended to use this for other types of image operations.
    :param output:
    :param target:
    :param source:
    :return:
    """

    source_image: Image = Image.open(source).convert("RGB")
    target_image: Image = Image.open(target).convert("RGB")

    if source_image.size < target_image.size:
        raise Exception("Source image must be larger than or equal to target size")

    # I must be dumb but PIL doesn't seem to have a native tool for getting image diffs
    # there is an "ImageChops.difference" but that gets the actual color difference rather than different pixels
    diff = Image.new(mode="RGBA", size=source_image.size)
    frame_size = target_image.size

    # source can have or 1 more frames but target must have 1 frame only
    for column in range(int(source_image.size[0] / frame_size[0])):
        for row in range(int(source_image.size[1] / frame_size[1])):
            for x in range(frame_size[0]):
                for y in range(frame_size[1]):
                    offset_x = x + column * frame_size[0]
                    offset_y = y + row * frame_size[1]
                    source_color = source_image.getpixel((offset_x, offset_y))

                    # if source is already transparent then just skip
                    if source_color == (0, 0, 0):
                        continue

                    target_color = target_image.getpixel((x, y))

                    if source_color == target_color:
                        diff.putpixel((offset_x, offset_y), (0, 0, 0, 0))
                        continue

                    diff.putpixel((offset_x, offset_y), source_color)

    diff.save(output)
