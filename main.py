from pokemon.pokemon import Pokemon

def main():
    # ピカチュウの作成例
    pikachu = Pokemon.create_pokemon('ピカチュウ', 10)
    print(pikachu)

if __name__ == '__main__':
    main()
