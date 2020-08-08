"""
Web helpers to download .dmi files as .rsi
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from urllib.request import urlopen

from rsi import Rsi


def web_dmi_to_rsi(url: str) -> "Rsi":
    """
    Takes a web-url of a Dmi blob and returns an Rsi object
    """
    with TemporaryDirectory() as tmpdir_name:
        file_name = Path().joinpath(tmpdir_name, url.split("/")[-1])

        with urlopen(url) as response, open(file_name, "wb") as target_file:
            target_file.write(response.read())

        rsi = Rsi.from_dmi(file_name)
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

    if splitter is None:
        rsi.write(path.with_suffix(".rsi"), make_parent_dirs=True, indent=indents)
        return
    else:
        splitter = splitter(rsi)

    splitter.split_to(path, indents=indents)
