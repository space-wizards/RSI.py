"""
Used for converting a single .rsi file into mutiple smaller ones
"""
from rsi import Rsi
from typing import List, Optional
from abc import ABC
from pathlib import Path


class RsiSplitter(ABC):
    """
    This encapsulates all of the data needed to split a Rsi into several smaller Rsi somewhat cleanly
    """

    def __init__(self, rsi: Rsi) -> None:
        self.rsi = rsi

    def _split(self) -> List[Rsi]:
        raise NotImplementedError

    def _get_name(self, rsi: Rsi):
        """
        Get the name of a split rsi
        :param rsi:
        :return:
        """
        raise NotImplementedError

    def split_to(self, path: Path, indents: Optional[int] = None) -> None:
        for rsi in self._split():
            rsi_path = path.joinpath(self._get_name(rsi)).with_suffix(".rsi")
            rsi.write(rsi_path, indent=indents)


class SimpleSplitter(RsiSplitter):
    """
    Split each Rsi state into its own Rsi
    """

    def _split(self) -> List[Rsi]:
        result = []

        for name, state in self.rsi.states.items():
            state_rsi = Rsi(self.rsi.size)
            state_rsi.set_state(state, name)
            state_rsi.license = self.rsi.license
            state_rsi.copyright = self.rsi.copyright
            result.append(state_rsi)

        return result

    def _get_name(self, rsi: Rsi):
        assert len(rsi.states.keys()) == 1
        return list(rsi.states.values())[0].name


class HyphenSplitter(RsiSplitter):
    """
    Split each rsi based on hyphens where Rsi states with the same prefix are grouped together
    e.g. ak-20, ak-40, and ak-60 would all be grouped into ak.
    """

    def _split(self) -> List[Rsi]:
        groups = {}

        for name, state in self.rsi.states.items():
            prefix = name.split("-")[0]
            suffix = name.split("-")[-1]
            state_rsi = groups.setdefault(prefix, Rsi(self.rsi.size))

            if prefix != suffix:
                state.name = suffix
                state_rsi.set_state(state, suffix)
            else:
                state_rsi.set_state(state, name)

        return list(groups.values())

    def _get_name(self, rsi: Rsi):
        return list(rsi.states.values())[0].name.split("-")[0]
