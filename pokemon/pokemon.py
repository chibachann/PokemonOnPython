import random
from typing import Dict, List, Union
from .nature import Nature
from .move import Move
from .exp_strategy import ExpStrategy, Exp600k, Exp800k, Exp1000k, Exp1050k, Exp1250k, Exp1640k
from .config import Config


# ポケモン
class Pokemon:
    def __init__(self, name: str, types: Union[str, List[str]], base_stats: Dict[str, int], 
                 level_up_moves: Dict[int, List[str]], exp_strategy: ExpStrategy, level: int = 1):
        self.name = name
        self.nature = Nature(**random.choice(Config.NATURES))
        self.types = types if isinstance(types, list) else [types]
        self.base_stats = base_stats
        self.stat_names = {
            'hp': 'HP', 'attack': 'こうげき', 'defense': 'ぼうぎょ',
            'sp_attack': 'とくこう', 'sp_defense': 'とくぼう', 'speed': 'すばやさ'
        }
        self.level = level
        self.ivs = {stat: random.randint(0, 31) for stat in base_stats}
        self.evs = {stat: 0 for stat in base_stats}
        self.stats = {stat: 0 for stat in base_stats}
        self.moves: List[Move] = []
        self.level_up_moves = level_up_moves
        self.exp_strategy = exp_strategy
        self.exp = 0
        
        self.set_level(level)
        self.calculate_stats()

    def set_ivs(self, ivs: Dict[str, int]) -> None:
        self.ivs.update(ivs)
        self.calculate_stats()

    def set_evs(self, evs: Dict[str, int]) -> None:
        self.evs.update(evs)
        self.calculate_stats()

    def set_level(self, level: int) -> None:
        while self.level < level:
            self.level_up(initial_setup=True)
        self.calculate_stats()
        self.initialize_moves()

    def calculate_stats(self) -> None:
        for stat, base in self.base_stats.items():
            if stat == 'hp':
                self.stats[stat] = self._calculate_hp(base)
            else:
                self.stats[stat] = self._calculate_other_stat(stat, base)

    def _calculate_hp(self, base: int) -> int:
        return int((2 * base + self.ivs['hp'] + self.evs['hp'] // 4) * self.level / 100) + self.level + 10

    def _calculate_other_stat(self, stat: str, base: int) -> int:
        value = int(((2 * base + self.ivs[stat] + self.evs[stat] // 4) * self.level / 100) + 5)
        return int(value * self.nature.get_multiplier(stat))

    def learn_move(self, new_move_name: str) -> None:
        if len(self.moves) < 4:
            self._add_move(new_move_name)
            print(f"{self.name}は{new_move_name}をおぼえた!")
        else:
            self._handle_move_learning(new_move_name)

    def _add_move(self, move_name: str) -> None:
        move_data = Config.MOVES_DATA[move_name]
        new_move = Move(
            name=move_name,
            type=move_data['type'],
            power=move_data['power'],
            accuracy=move_data['accuracy'],
            pp=move_data['pp'],
            max_pp=move_data['pp'], 
            category=move_data['category']
        )
        if len(self.moves) < 4:
            self.moves.append(new_move)

    def _handle_move_learning(self, new_move_name: str) -> None:
        print(f"{self.name}は新しく{new_move_name}を覚えようとしている！")
        print(f"{self.name}はすでに４つのわざをおぼえています。わすれさせるわざを選んでください。")
        for i, move in enumerate(self.moves):
            print(f"{i+1}: {move.name}")
        print(f"5: {new_move_name}をおぼえるのをやめる")
        print("\n")

        print("どのわざをわすれさせますか？")
        try:
            choice = int(input("わすれさせるわざのばんごうをえらんでください。"))
        except ValueError:
            print("ばんごうがまちがっています。わざをおぼえなかった")
            return

        if 1 <= choice <= 4:
            forgotten_move = self.moves[choice-1].name
            self.moves[choice-1] = Move(name=new_move_name, **Config.MOVES_DATA[new_move_name])
            print(f"{self.name}は{forgotten_move}をわすれて{new_move_name}をおぼえました!")
        elif choice == 5:
            print(f"{self.name}は{new_move_name}をおぼえなかった")
        else:
            print("ばんごうがまちがっています。わざをおぼえなかった")

    def gain_exp(self, amount: int) -> None:
        self.exp += amount
        print(f"{self.name}は{amount}のけいけんちをもらった！")
        
        while self.exp >= self.exp_to_next_level():
            initial_level = self.level
            self.level_up()
            if self.level > initial_level + 1:
                print(f"{self.name}は\nレベル{self.level}にあがった！")

    def level_up(self, initial_setup: bool = False) -> None:
        self.level += 1
        if not initial_setup:
            self._display_level_up_info()
        self._learn_new_moves(initial_setup)

    def _display_level_up_info(self) -> None:
        print(f"{self.name}は\nレベル{self.level}にあがった！")
        old_stats = self.stats.copy()
        self.calculate_stats()
        for stat, new_value in self.stats.items():
            increase = new_value - old_stats[stat]
            if increase > 0:
                print(f"{self.stat_names[stat]}が{increase}あがった！")
        print("\n")

    def _learn_new_moves(self, initial_setup: bool) -> None:
        if self.level in self.level_up_moves:
            for move in self.level_up_moves[self.level]:
                if initial_setup:
                    self._add_move(move)
                else:
                    self.learn_move(move)

    def initialize_moves(self) -> None:
        all_moves = [move for level, moves in self.level_up_moves.items() 
                     for move in moves if level <= self.level]
        final_moves = all_moves[-4:] if len(all_moves) >= 4 else all_moves
        self.moves = []
        for move in final_moves:
            self._add_move(move)

    def exp_to_next_level(self) -> int:
        return self.exp_strategy.calculate_exp(self.level + 1)

    def __str__(self) -> str:
        stats_str = '\n'.join([f"{self.stat_names[stat]}: {value}" for stat, value in self.stats.items()])
        move_names = [move.name for move in self.moves]
        return (f"{self.name} Lv.{self.level}\n"
                f"タイプ: {', '.join(self.types)}\n"
                f"せいかく: {self.nature.name}\n"
                f"ステータス: {stats_str}\n"
                f"おぼえているわざ : {', '.join(move_names)}")

    @staticmethod
    def create_pokemon(name: str, level: int = 5) -> 'Pokemon':
        if name not in Config.POKEMON_DATA:
            raise ValueError(f"{name} というポケモンはデータベースにありません。")
        
        data = Config.POKEMON_DATA[name]
        exp_growth = data["exp_growth"]
        exp_strategy: ExpStrategy

        if exp_growth == '600k':
            exp_strategy = Exp600k()
        elif exp_growth == '800k':
            exp_strategy = Exp800k()
        elif exp_growth == '1000k':
            exp_strategy = Exp1000k()
        elif exp_growth == '1050k':
            exp_strategy = Exp1050k()
        elif exp_growth == '1250k':
            exp_strategy = Exp1250k()
        elif exp_growth == '1640k':
            exp_strategy = Exp1640k()
        else:
            raise ValueError(f"不正な経験値成長率です: {exp_growth}")
        
        return Pokemon(name, data['type'], data['base_stats'], data['level_up_moves'], exp_strategy, level=level)
