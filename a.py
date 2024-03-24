import random
import numpy as np


class Animal:
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __init__(self, x, y, name, gender, footage, radar=None):
        self.name = name
        self.gender = gender
        self.x = x
        self.y = y
        self.footage = footage
        self.radar = radar


def place_objects(matrix, num_objects, object) -> None:
    for _ in range(num_objects):
        x = random.randint(0, 499)
        y = random.randint(0, 499)
        while matrix[x, y] is not None:
            x = random.randint(0, 499)
            y = random.randint(0, 499)
        matrix[x, y] = object
        object.x = x
        object.y = y
        add_to_list(object)


def print_animals(matrix):
    for row in matrix:
        for element in row:
            if element is not None:
                print(element.x)
                print(element.y)
                print(element.name)
                print(element.gender)
                print("**************")


def move_object(obje: Animal):
    global game_board

    directions = [0, 1, 2, 3]

    while directions:
        direction = random.choice(directions)

        # up
        if direction == 0:
            if obje.x - obje.footage >= 0 and game_board[obje.x - obje.footage][obje.y] == None:
                obje.x -= obje.footage
                directions.remove(0)
                return

        # right
        elif direction == 1:
            if obje.y + obje.footage < 499 and game_board[obje.x][obje.y + obje.footage] == None:
                obje.y += obje.footage
                directions.remove(1)
                return

        # down
        elif direction == 2:
            if obje.x + obje.footage < 499 and game_board[obje.x + obje.footage][obje.y] == None:
                obje.x += obje.footage
                directions.remove(2)
                return

        # left
        elif direction == 3:
            if obje.y - obje.footage >= 0 and game_board[obje.x][obje.y - obje.footage] == None:
                obje.y -= obje.footage
                directions.remove(3)
                return
    return


def eat_if_possible(avci: Animal, av: Animal):
    global game_board

    if abs(avci.x - av.x) <= avci.radar and abs(avci.y - av.y) <= avci.radar:
        game_board[av.x][av.y] = None
        if av.name == "koyun":
            animals[0] = [x for x in animals[0] if x.x == av.x and x.y == av.y]
        elif av.name == "inek":
            print(abs(avci.x - av.x) <= avci.radar)
            print("inek öldü")
            print(avci.x, " - ", avci.y)
            print(av.x, " - ", av.y)
            print(animals[2])
            a = [x for x in animals[2] if x.x == av.x and x.y == av.y]
            print(a)
        elif av.name == "tavuk":
            animals[3] = [x for x in animals[3] if x.x == av.x and x.y == av.y]


def eat():
    global game_board, animals
    for kurt in animals[1]:

        for koyun in animals[0]:
            eat_if_possible(kurt, koyun)

        for tavuk in animals[3]:
            eat_if_possible(kurt, tavuk)
    for aslan in animals[4]:
        for koyun in animals[0]:
            eat_if_possible(aslan, koyun)

        for inek in animals[3]:
            eat_if_possible(aslan, inek)

    for avcı in animals[5]:
        for animal_list in animals[0:-1]:
            for animal in animal_list:
                eat_if_possible(avcı, animal)


def add_to_list(obje: Animal):
    if obje.name == "koyun":
        animals[0].append(obje)
    elif obje.name == "kurt":
        animals[1].append(obje)
    elif obje.name == "inek":
        animals[2].append(obje)
    elif obje.name == "tavuk":
        animals[3].append(obje)
    elif obje.name == "aslan":
        animals[4].append(obje)
    elif obje.name == "avcı":
        animals[5].append(obje)


def main():
    global game_board, animals

    game_board = np.full((500, 500), None)
    koyunlar = []
    avcı = []
    kurtlar = []
    inekler = []
    tavuklar = []
    aslanlar = []
    animals = [koyunlar, kurtlar, inekler, tavuklar, aslanlar, avcı]

    place_objects(game_board, 15, Animal(None, None, "koyun", True, 2)),
    place_objects(game_board, 5, Animal(None, None, "kurt", True, 3, 4)),
    place_objects(game_board, 5, Animal(None, None, "inek", True, 2)),
    place_objects(game_board, 5, Animal(None, None, "tavuk", True, 1)),
    place_objects(game_board, 4, Animal(None, None, "aslan", True, 4, 5)),
    place_objects(game_board, 15, Animal(None, None, "koyun", False, 2)),
    place_objects(game_board, 5, Animal(None, None, "kurt", False, 3, 4)),
    place_objects(game_board, 5, Animal(None, None, "inek", False, 2)),
    place_objects(game_board, 5, Animal(None, None, "tavuk", False, 1)),
    place_objects(game_board, 4, Animal(None, None, "aslan", False, 4, 5)),
    place_objects(game_board, 1, Animal(None, None, "avcı", None, 1, 8)),
    for _ in range(10000):
        eat()
        for list in animals:
            for animal in list:
                move_object(animal)

    for animal in animals:
        print(animal)


if __name__ == "__main__":
    main()

""" 
Hayvanat Bahçesi Projesi
500'e 500'lük bir alanda yaşayan 30 koyun (15 erkek,15 dişi), 10 inek (5 erkek,5 dişi),
10 tavuk,10 kurt (5 dişi,5 erkek) 10 horoz, 8 aslan (4 erkek, 4 dişi) ve 1 avcı
bulunmaktadır.
Hayvanlardan;
koyun 2 birim,
kurt 3 birim,
inek 2 birim,
tavuk 1 birim,
horoz 1 birim,
aslan 4 birim,
avcı 1 birim rasgele şekilde hareket etmektedir ancak alanın dışına çıkamamaktadır.
kurt kendisine 4 birim yakınındaki koyun, tavuk, horoz'u avlayabiliyor.
aslan kendisine 5 birim yakınlıktaki inek, koyun'u avlayabiliyor.
avcı da kendisine 8 birim yakınlıktaki hayvanlardan herhangi birisini avlayabiliyor.
aynı cins farklı cinsiyetteki hayvanlar birbirine 3 birim yakınlaştığı zaman random
cinsiyetli ve aynı cins bir hayvan meydana gelmektedir.
1000 birim hareket sonunda hayvanların sayısının bulunduğu bir console application
yazılması beklenmektedir. """
