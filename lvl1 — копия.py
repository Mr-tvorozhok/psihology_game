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
    fullname = os.path.join('data\img', name)
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


# 1
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
        
    



class H1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # computer test
        super().__init__(Walls_prog)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.image = load_image('432.png')
        self.walls = True
        self.osm = [1, 1, 1, 1]
        self.osm1 = []

    def smena(self, x, y):
        print(1)
        self.rect = self.rect.move(x, y)
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

    def pp(self):
        return {"mess": ['Это компьютер', 'Хз на чем он работает', 'Но он превратился в квадрат'],
                'hp': -10, 'inv': { 'add': ['что то']}}
    
    def killing(self):
        for i in self.osm1:
            i.kill()
        self.kill


Parametrs1 = {'H': H1(0, 0)}
# 2
param = {1: Parametrs1}
