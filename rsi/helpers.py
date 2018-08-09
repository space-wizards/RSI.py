from typing import List, Optional


def state_name(name: str, selectors: Optional[List[str]] = None) -> str:
    if selectors:
        name += "+" + "+".join(sorted(selectors))

    return name
