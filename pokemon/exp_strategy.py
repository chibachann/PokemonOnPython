from abc import ABC, abstractmethod
import math

class ExpStrategy(ABC):
    @abstractmethod
    def calculate_exp(self, level: int) -> int:
        pass

class Exp600k(ExpStrategy):
    def calculate_exp(self, level: int) -> int:
        if 2 <= level <= 50:
            return math.floor(level**3 * (100 - level) / 50)
        elif 50 < level <= 68:
            return math.floor(level**3 * (150 - level) / 100)
        elif 68 < level <= 98:
            return math.floor(level**3 * math.floor((637 - 10*level) / 3) / 500)
        elif level == 99:
            return math.floor(level**3 * (160 - level) / 100)
        else:
            raise ValueError("Invalid level")

class Exp800k(ExpStrategy):
    def calculate_exp(self, level: int) -> int:
        return math.floor(0.8 * level**3)

class Exp1000k(ExpStrategy):
    def calculate_exp(self, level: int) -> int:
        return level**3

class Exp1050k(ExpStrategy):
    def calculate_exp(self, level: int) -> int:
        return math.floor(1.2 * level**3 - 15 * level**2 + 100 * level - 140)

class Exp1250k(ExpStrategy):
    def calculate_exp(self, level: int) -> int:
        return math.floor(1.25 * level**3)

class Exp1640k(ExpStrategy):
    def calculate_exp(self, level: int) -> int:
        if 2 <= level <= 15:
            return math.floor(level**3 * (24 + math.floor((level + 1) / 3)) / 50)
        elif 15 < level <= 36:
            return math.floor(level**3 * (14 + level) / 50)
        elif 36 < level <= 100:
            return math.floor(level**3 * (32 + math.floor(level / 2)) / 50)
        else:
            raise ValueError("Invalid level")
