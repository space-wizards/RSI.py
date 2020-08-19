"""
Used for converting a single .rsi file into mutiple smaller ones
"""
from rsi import Rsi
from typing import Dict, List, Optional
from abc import ABC
from pathlib import Path
import re


class RsiSplitter(ABC):
    """
    This encapsulates all of the data needed to split a Rsi into several smaller Rsi somewhat cleanly
    """

    def __init__(self, rsi: Rsi) -> None:
        self.rsi = rsi
        # Store the name to use for each rsi group
        self.names: Dict[Rsi, str] = {}

    def _split(self) -> List[Rsi]:
        raise NotImplementedError

    def split_to(self, path: Path, indents: Optional[int] = None) -> None:
        for rsi in self._split():
            rsi.license = self.rsi.license
            rsi.copyright = self.rsi.copyright
            rsi_path = path.joinpath(self.names[rsi]).with_suffix(".rsi")
            rsi.write(rsi_path, indent=indents)

        self.names.clear()


class SimpleSplitter(RsiSplitter):
    """
    Split each Rsi state into its own Rsi
    """

    def _split(self) -> List[Rsi]:
        result = []

        for name, state in self.rsi.states.items():
            state_rsi = Rsi(self.rsi.size)
            state_rsi.set_state(state, name)
            result.append(state_rsi)
            self.names[state_rsi] = state.name

        return result


class HyphenSplitter(RsiSplitter):
    """
    Split each rsi based on hyphens where Rsi states with the same prefix are grouped together
    e.g. ak-20, ak-40, and ak-60 would all be grouped into ak.
    """

    def _split(self) -> List[Rsi]:
        groups: Dict[str, Rsi] = {}

        for name, state in self.rsi.states.items():
            prefix = name.split("-")[0]
            suffix = name.split("-")[-1]
            state_rsi = groups.setdefault(prefix, Rsi(self.rsi.size))

            if prefix != suffix:
                state.name = suffix
                state_rsi.set_state(state, suffix)
                self.names[state_rsi] = prefix
            else:
                state_rsi.set_state(state, name)
                self.names[state_rsi] = name

        return list(groups.values())


class UnderscoreSplitter(RsiSplitter):
    """
    Like the hyphensplitter but for underscores.
    """

    def _split(self) -> List[Rsi]:
        groups: Dict[str, Rsi] = {}

        for name, state in self.rsi.states.items():
            prefix = name.split("_")[0]
            suffix = name.split("_")[-1]
            state_rsi = groups.setdefault(prefix, Rsi(self.rsi.size))

            if prefix != suffix:
                state.name = suffix
                state_rsi.set_state(state, suffix)
                self.names[state_rsi] = prefix
            else:
                state_rsi.set_state(state, name)
                self.names[state_rsi] = name

        return list(groups.values())


class NumberSplitter(RsiSplitter):
    """
    Splits states based on the suffix number
    e.g. infected, infected0, infected1 are all in the same rsi
    """

    def _split(self) -> List[Rsi]:
        groups: Dict[str, Rsi] = {}
        pattern = re.compile("([^0-9]*)([0-9]*)")

        for name, state in self.rsi.states.items():
            match = pattern.match(name)
            prefix = match.group(1)
            suffix = match.group(2) if len(match.groups()) > 1 else ""
            state_rsi = groups.setdefault(prefix, Rsi(self.rsi.size))

            if prefix != suffix:
                state.name = suffix
                state_rsi.set_state(state, suffix)
                self.names[state_rsi] = prefix
            else:
                state_rsi.set_state(state, name)
                self.names[state_rsi] = name

        return list(groups.values())
