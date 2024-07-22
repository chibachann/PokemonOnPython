import os
from .data_loader import DataLoader

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')

    @classmethod
    def load_data(cls, filename):
        return DataLoader.load_data(os.path.join(cls.DATA_DIR, filename))

    MOVES_DATA = None
    POKEMON_DATA = None
    NATURES = None

    @classmethod
    def initialize(cls):
        cls.MOVES_DATA = cls.load_data('moves_data.yml')
        cls.POKEMON_DATA = cls.load_data('pokemon_data.yml')
        cls.NATURES = cls.load_data('natures.yml')

# Config の初期化
Config.initialize()
