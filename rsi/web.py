"""
Web helpers to download .dmi files as .rsi
"""
from pathlib import Path
from io import BytesIO
from typing import Optional
from urllib.request import urlopen

from rsi import Rsi


def web_dmi_to_rsi(url: str) -> "Rsi":
    """
    Takes a web-url of a Dmi blob and returns an Rsi object
    """

    with urlopen(url) as response, BytesIO() as buffer:
        buffer.write(response.read())
        rsi = Rsi.from_dmi(buffer)

    rsi.copyright = url

    return rsi


def export_web_dmi_to_rsi(
    url: str,
    path: Path,
    rsi_license: Optional[str] = None,
    splitter=None,
    indents: Optional[int] = None) -> None:
    """
    Takes a web-url of a Dmi blob and outputs it to the specified path.
    :param url: Dmi blob location
    :param path: Filepath target
    :param rsi_license: Optional license to use for the .rsi
    :param splitter: How the .rsi should be split (if applicable)
    :param indents:
    :return:
    """
    rsi = web_dmi_to_rsi(url)
    rsi.license = rsi_license
    rsi.copyright = url

    if splitter is None:
        rsi.write(path.with_suffix(".rsi"), make_parent_dirs=True, indent=indents)
        return
    else:
        splitter = splitter(rsi)

    splitter.split_to(path, indents=indents)
