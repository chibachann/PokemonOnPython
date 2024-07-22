import yaml
import os
from typing import Dict

class DataLoader:
    @staticmethod
    def load_data(file_path: str) -> Dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"{file_path} が見つかりません。")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAMLファイルの読み込み中にエラーが発生しました: {e}")
