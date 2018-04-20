from typing import List


def state_name(name: str, selectors: List[str]) -> str:
    if selectors is not None and selectors:
        name += "+" + "+".join(sorted(selectors))

    return name
