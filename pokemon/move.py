from dataclasses import dataclass

@dataclass
class Move:
    name: str
    type: str
    power: int
    accuracy: int
    pp: int
    max_pp: int
    category: str
