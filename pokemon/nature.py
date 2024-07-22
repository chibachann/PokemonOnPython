from dataclasses import dataclass
from typing import Optional

@dataclass
class Nature:
    name: str
    increased_stat: Optional[str]
    decreased_stat: Optional[str]

    def get_multiplier(self, stat: str) -> float:
        if stat == self.increased_stat:
            return 1.1
        elif stat == self.decreased_stat:
            return 0.9
        return 1.0
