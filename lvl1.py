import pygame
import os

pygame.init()
Progr = pygame.sprite.Group()
Walls_prog = pygame.sprite.Group()
Object_prog = pygame.sprite.Group()
infoObject = pygame.display.Info()
height = infoObject.current_h
razn = 100
widht = infoObject.current_w
screen = pygame.display.set_mode((widht, height))


def load_image(name, color_key=None):
    fullname = os.path.join('data\\img', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Osmotr_Object(pygame.sprite.Sprite):
    def __init__(self, x, y, item, peremen):
        super().__init__(Object_prog)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.image = load_image('32.png')
        item1 = []
        for i in item:
            if i == '+':
                item1.append(' ')
            else:
                item1.append(i)
        self.item = ''.join(item1)
        self.peremen = peremen

    def pp(self):
        try:
            return self.peremen.pp()
        except BaseException:
            pass


###################
#
#
# 1
Walls_prog1 = pygame.sprite.Group()
Progr1 = pygame.sprite.Group()


class H1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # computer test
        super().__init__(Walls_prog1)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.image = load_image('432.png')
        self.walls = False
        self.floor = False
        self.osm = [1, 1, 1, 1]
        self.osm1 = []
        self.ob = 9
        self.x, self.y = 0, 0

    def smena(self, x, y):
        print(1)
        self.rect = self.rect.move(x, y)
        self.x, self.y = x, y
        if self.osm[0] == 1:
            self.osm1.append(Osmotr_Object(x, y - razn, "пр", self))

        if self.osm[1] == 1:
            self.osm1.append(Osmotr_Object(x, y + razn, "пр", self))

        if self.osm[2] == 1:
            self.osm1.append(Osmotr_Object(x - razn, y, "пр", self))

        if self.osm[3] == 1:
            self.osm1.append(Osmotr_Object(x + razn, y, "пр", self))

    def proverka(self):
        print('Обьект найден, команда дошла')

    def hits_act(self):
        return {"mess": ['Зачем ты врезался сюда?']}

    def pp(self):
        return {"mess": ['Это компьютер', 'Хз на чем он работает', 'Но он превратился в квадрат',
                         'И да, он отличается от других обьектов']}

    def despawn(self, razn):
        for i in self.osm1:
            i.kill()
        self.rect = self.rect.move(-self.x - razn, -self.y - razn)
        return self.ob


Parametrs1 = {'H': H1(-100, -100)}
#
# Parametrs1 = {}
# 2

Walls_prog2 = pygame.sprite.Group()
Progr2 = pygame.sprite.Group()


class u1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # computer test
        super().__init__(Progr2)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.image = load_image('432.png')
        self.walls = False
        self.floor = False
        self.osm = [1, 1, 1, 1]
        self.osm1 = []

        self.x, self.y = 0, 0

    def smena(self, x, y):
        print(1)
        self.rect = self.rect.move(x, y)
        self.x, self.y = x, y
        if self.osm[0] == 1:
            self.osm1.append(Osmotr_Object(x, y - razn, "пр", self))

        if self.osm[1] == 1:
            self.osm1.append(Osmotr_Object(x, y + razn, "пр", self))

        if self.osm[2] == 1:
            self.osm1.append(Osmotr_Object(x - razn, y, "пр", self))

        if self.osm[3] == 1:
            self.osm1.append(Osmotr_Object(x + razn, y, "пр", self))

    def proverka(self):
        print('Обьект найден, команда дошла')

    def hits_act(self):
        return {"mess": ['Зачем ты врезался сюда?']}

    def pp(self):
        return {"mess": ['Это компьютер', 'Хз на чем он работает', 'Но он превратился в квадрат'],
                'hp': -10, 'inv': {'add': ['что то']}}

    def despawn(self):
        for i in self.osm1:
            i.kill()
        self.rect = self.rect.move(-self.x, -self.y)
        return self.ob


Parametrs2 = {'u': u1(0, 0)}

Walls_prog3 = pygame.sprite.Group()
Progr3 = pygame.sprite.Group()


# 3
class T3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # computer test
        super().__init__(Progr3)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.image = load_image('4313.png')
        self.walls = False
        self.floor = False
        self.osm = [1, 1, 1, 1]
        self.osm1 = []
        self.x, self.y = 0, 0

    def smena(self, x, y):
        print(1)
        x = int(x)
        y = int(y)
        self.rect = self.rect.move(x, y)
        self.x, self.y = x, y
        if self.osm[0] == 1:
            self.osm1.append(Osmotr_Object(x, y - razn, "пр", self))

        if self.osm[1] == 1:
            self.osm1.append(Osmotr_Object(x, y + razn, "пр", self))

        if self.osm[2] == 1:
            self.osm1.append(Osmotr_Object(x - razn, y, "пр", self))

        if self.osm[3] == 1:
            self.osm1.append(Osmotr_Object(x + razn, y, "пр", self))

    def proverka(self):
        print('Обьект найден, команда дошла')

    def hits_act(self):
        return {}

    def pp(self):
        return {"mess": ['Я умею кусаться', "ахахаахахах", "Вы получили 15 урона"],
                'hp': -15, }

    def despawn(self):
        for i in self.osm1:
            i.kill()
        self.rect = self.rect.move(-self.x, -self.y)


Parametrs3 = {"T": T3(0, 0)}

Walls_prog4 = pygame.sprite.Group()
Progr4 = pygame.sprite.Group()
Walls_prog5 = pygame.sprite.Group()
Progr5 = pygame.sprite.Group()
param = {1: Parametrs1, 2: Parametrs2, 3: Parametrs3, 4: [], 5: []}
param_group = {1: [Walls_prog1, Progr1], 2: [Walls_prog2, Progr2], 3: [Walls_prog3, Progr3], 4: [Walls_prog4, Progr4],
               5: [Walls_prog5, Progr5]}
