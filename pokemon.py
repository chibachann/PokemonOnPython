import yaml
import random
import math

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"{file_path} が見つかりません。")
        return None
    except yaml.YAMLError as e:
        print(f"YAMLファイルの読み込み中にエラーが発生しました: {e}")
        return None


class Pokemon:
    moves_data = None

    @classmethod
    def initialize_moves_data(cls):
        if cls.moves_data is None:
            cls.moves_data = load_data('moves_data.yml')

    def __init__(self, name, types, base_stats, level_up_moves, exp_growth,level=1):
        self.initialize_moves_data()
        self.name = name
        self.nature = random.choice(NATURES)
        self.types = types if isinstance(types, list) else [types]
        self.base_stats = base_stats
        self.stat_names = {
            'hp': 'HP',
            'attack': 'こうげき',
            'defense': 'ぼうぎょ',
            'sp_attack': 'とくこう',
            'sp_defense': 'とくぼう',
            'speed': 'すばやさ'
        }
        self.level = level
        self.ivs = {stat:random.randint(0, 31) for stat in base_stats}
        self.evs = {stat:0 for stat in base_stats}
        self.stats = {stat:0 for stat in base_stats}
        self.moves = []
        self.level_up_moves = level_up_moves
        self.exp_growth = exp_growth
        self.exp = 0
        self.set_level(level)
        
        self.calculate_stats()
        
    
    def set_ivs(self, ivs):
        self.ivs.update(ivs)
        self.calculate_stats()

    def set_evs(self, evs):
        self.evs.update(evs)
        self.calculate_stats()

    def set_level(self, level):
        self.level = level
        self.calculate_stats()

    """
    HP : ( 種族値*2 + 個体値 + 努力値÷4 ) * レベル ÷ 100 + レベル + 10
    他のステータス : ( ( 種族値*2 + 個体値 + 努力値÷4 ) * レベル ÷ 100 + 5 ) * 性格補正
    小数点以下切り捨て
    """
    def calculate_stats(self):
        for stat, base in self.base_stats.items():
            if stat == 'hp':
                self.stats[stat] = int((2 * base + self.ivs[stat] 
                                        + int(self.evs[stat]/4)) * self.level / 100) + self.level + 10
            else:
                stat_value = int(((2 * base + self.ivs[stat]
                                   + int(self.evs[stat]/4)) * self.level / 100) + 5)
                # 性格補正                                   
                stat_value = int(stat_value * self.nature.get_multiplier(stat))
                self.stats[stat] = stat_value

    def learn_move(self, new_move_name):
        if len(self.moves) < 4:
            self.add_move(new_move_name)
            print(f"{self.name}は{new_move_name}をおぼえた!")
        else:
            print(f"{self.name}は新しく{new_move_name}を覚えようとしている！")
            print(f"{self.name}はすでに４つのわざをおぼえています。わすれさせるわざを選んでください。")
            for i, move in enumerate(self.moves):
                print(f"{i+1}: {move['name']}")
            print(f"5: {new_move_name}をおぼえるのをやめる")
            print("\n")

            print("どのわざをわすれさせますか？")
            try:
                choice = int(input("わすれさせるわざのばんごうをえらんでください。"))
            except ValueError:
                print("ばんごうがまちがっています。わざをおぼえなかった")
                return
            if 1 <= choice <= 4:
                forggoten_move = self.moves[choice-1]["name"]
                self.moves[choice-1] = {
                    'name': new_move_name,
                    'type': self.moves_data[new_move_name]['type'],
                    'power': self.moves_data[new_move_name]['power'],
                    'accuracy': self.moves_data[new_move_name]['accuracy'],
                    'pp': self.moves_data[new_move_name]['pp'],
                    'max_pp': self.moves_data[new_move_name]['pp'],
                    'category': self.moves_data[new_move_name]['category'],
                }
                print(f"{self.name}は{forggoten_move}をわすれて{new_move_name}をおぼえました!")
            elif choice == 5:
                print(f"{self.name}は{new_move_name}をおぼえなかった")
            else:
                print("ばんごうがまちがっています。わざをおぼえなかった")
    
    def add_move(self, move_name):
        new_move = {
            'name': move_name,
            'type': self.moves_data[move_name]['type'],
            'power': self.moves_data[move_name]['power'],
            'accuracy': self.moves_data[move_name]['accuracy'],
            'pp': self.moves_data[move_name]['pp'],
            'max_pp': self.moves_data[move_name]['pp'],
            'category': self.moves_data[move_name]['category'],
        }
        if len(self.moves) < 4:
            self.moves.append(new_move)

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name}は{amount}のけいけんちをもらった！")
        
        while self.exp >= self.exp_to_next_level():
            initial_level = self.level
            self.level_up()

            # 次のレベルに必要な経験値を超えている場合、ループが続く
            if self.level > initial_level + 1:
                print(f"{self.name}は\nレベル{self.level}にあがった！")
        

    def set_level(self, level):
        while self.level < level:
            self.level_up(initial_setup=True)
        self.calculate_stats()
        self.initialize_moves()

    def level_up(self, initial_setup=False):
        self.level += 1
        if not initial_setup:
            print(f"{self.name}は\nレベル{self.level}にあがった！")
            old_stats = self.stats.copy()
            self.calculate_stats()

            # ステータスの変化を表示
            for stat, new_value in self.stats.items():
                increase = new_value - old_stats[stat]
                if increase > 0:
                    print(f"{self.stat_names[stat]}が{increase}あがった！")
            print("\n")

        # レベルアップで覚えるわざがある場合、覚える
        if self.level in self.level_up_moves:
            for move in self.level_up_moves[self.level]:
                if initial_setup:
                    self.add_move(move)
                else:
                    self.learn_move(move)

    def initialize_moves(self):
        # 現在のレベルまでに覚えた技のリストを作成
        all_moves = []
        for level, moves in self.level_up_moves.items():
            if level <= self.level:
                all_moves.extend(moves)
        
        # 最新の4つ（もしくはそれ以下）の技を選択
        final_moves = all_moves[-4:] if len(all_moves) >= 4 else all_moves

        # 技の詳細情報を設定
        self.moves = []
        for move in final_moves:
            self.add_move(move)

    

    def exp_to_next_level(self):
        if self.exp_growth == "600k":
            return self.__exp__600k()
        elif self.exp_growth == "800k":
            return self.__exp__800k()
        elif self.exp_growth == "1000k":
            return self.__exp__1000k()
        elif self.exp_growth == "1050k":
            return self.__exp__1050k()
        elif self.exp_growth == "1250k":
            return self.__exp__1250k()
        elif self.exp_growth == "1640k":
            return self.__exp__1640k()
        else:
            raise ValueError("Invalid exp growth rate")
    
    def __exp__600k(self):
        lv = self.level + 1
        if 2 <= lv <= 50:
            return math.floor(lv**3 * (100 - lv) / 50)
        elif 50 < lv <= 68:
            return math.floor(lv**3 * (150 - lv) / 100)
        elif 68 < lv <= 98:
            return math.floor(lv**3 * math.floor((637 - 10*lv) / 3) / 500)
        elif lv == 99:
            return math.floor(lv**3 * (160 - lv) / 100)
        else:
            raise ValueError("Invalid level")
    
    def __exp__800k(self):
        lv = self.level + 1
        return math.floor(0.8 * lv**3)
    
    def __exp__1000k(self):
        lv = self.level + 1
        return lv**3
    
    def __exp__1050k(self):
        lv = self.level + 1
        return math.floor(1.2 * lv**3 - 15 * lv**2 + 100 * lv - 140)
    
    def __exp__1250k(self):
        lv = self.level + 1
        return math.floor(1.25 * lv**3)
    
    def __exp__1640k(self):
        lv = self.level + 1
        if 2 <= lv <= 15:
            return math.floor(lv**3 * (24 + math.floor((lv + 1) / 3)) / 50)
        elif 15 < lv <= 36:
            return math.floor(lv**3 * (14 + lv) / 50)
        elif 36 < lv <= 100:
            return math.floor(lv**3 * (32 + math.floor(lv / 2)) / 50)
        else:
            raise ValueError("Invalid level")
        
   
    
    def __str__(self):
        stats_str = '\n'.join([f"{self.stat_names[stat]}: {value}" for stat, value in self.stats.items()])
        move_names = [move['name'] for move in self.moves]
        return (f"{self.name} Lv.{self.level}\n"
                f"タイプ: {', '.join(self.types)}\n"
                f"せいかく: {self.nature.name}\n"
                f"ステータス: {stats_str}\n"
                f"おぼえているわざ : {', '.join(move_names)}")
    
    @staticmethod
    def create_pokemon(name, level=5):
        pokemon_data = load_data('pokemon_data.yml')

        if name not in pokemon_data:
            raise ValueError(f"{name} というポケモンはデータベースにありません。")
        
        data = pokemon_data[name]
        return Pokemon(name, data['type'], data['base_stats'], data['level_up_moves'], data['exp_growth'], level=level)


class Nature:
    def __init__(self, name, increased_stat, decreased_stat):
        self.name = name
        self.increased_stat = increased_stat
        self.decreased_stat = decreased_stat

    def get_multiplier(self, stat):
        if stat == self.increased_stat:
            return 1.1
        elif stat == self.decreased_stat:
            return 0.9
        else:
            return 1.0

# 性格のリストを作成
NATURES = [
    Nature("さみしがり", "attack", "defense"),
    Nature("いじっぱり", "attack", "sp_attack"),
    Nature("やんちゃ", "attack", "sp_defense"),
    Nature("ゆうかん", "attack", "speed"),

    Nature("ずぶとい", "defense", "attack"),
    Nature("わんぱく", "defense", "sp_attack"),
    Nature("のうてんき", "defense", "sp_defense"),
    Nature("のんき", "defense", "speed"),
    
    Nature("ひかえめ", "sp_attack", "attack"),
    Nature("おっとり", "sp_attack", "defense"),
    Nature("うっかりや", "sp_attack", "sp_defense"),
    Nature("れいせい", "sp_attack", "speed"),

    Nature("おだやか", "sp_defense", "attack"),
    Nature("おとなしい", "sp_defense", "defense"),
    Nature("しんちょう", "sp_defense", "sp_attack"),
    Nature("なまいき", "sp_defense", "speed"),
    
    Nature("おくびょう", "speed", "attack"),
    Nature("せっかち", "speed", "defense"),
    Nature("ようき", "speed", "sp_attack"),
    Nature("むじゃき", "speed", "sp_defense"),

    Nature("がんばりや", None, None),
    Nature("すなお", None, None),
    Nature("てれや", None, None),
    Nature("まじめ", None, None),
    Nature("きまぐれ", None, None)
]
