import os
from card_act import Card
import pygame
from lvl1 import param, Progr, Walls_prog, Object_prog, param_group
import logging

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a")
log = False
log_act = False
infoObject = pygame.display.Info()
height = infoObject.current_h
FPS = 180
g = ''
widht = infoObject.current_w
# height = 1080
# height = 1000
# widht = 1000
# screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
screen = pygame.display.set_mode((widht, height))
# screen_menu = pygame.display.set_mode((widht, height))
clock = pygame.time.Clock()
hits = []
all_sprites = pygame.sprite.Group()
Walls = pygame.sprite.Group()
Floors = pygame.sprite.Group()
decor = pygame.sprite.Group()
prohod = pygame.sprite.Group()
osmotr = pygame.sprite.Group()
Item_dop = pygame.sprite.Group()
Chests = pygame.sprite.Group()
Walls_dm = pygame.sprite.Group()
prov = pygame.sprite.Group()
act = {}
razn = 100
message_time = 0
message_count = 0
message_countt = 0
message_act = False
messages1 = []
clock = pygame.time.Clock()
# Блок меню инвентаря, переменые константы
inventar = {}
menu_act = False
count_item = 0
menu_act1 = False
chests_act = False
chests_invent = []
act_object = []
prohod_end = False
prohodlvl = ''
play = ''
hp_player = 100
ballons = 100
clock_ballons = 100
clock_ballons1 = 0
lvl = 0
prohod_lvl = None
hits = []
hits_osm = False
hits_osm_prog = False
hits_prog = False
hits_proh = False
hits_prog1 = False
hits_Obl = False
despawn_list = []


def item_act(item):
    global hp_player, ballons, inventar, clock_ballons
    if item == 'Еда':
        if hp_player + 30 > 100:
            hp_player = 100
        else:

            hp_player += 30

        act_prog({'inv': {'rem': ['Еда']}, 'mess': ['', "ВЫ поели", "Восстановлено 30 здоровья"]})
    elif item == 'Баллон c воздухом':
        if clock_ballons > 20:
            act_prog({'mess': ['', 'Вы поменяли баллон',
                               "Но баллон не весь был израскходован",
                               "ВЫ положили не доконца израсходованый баллон обратно"],
                      'inv': {'add': ['Неполный баллон с воздухом'], 'rem': ['Баллон c воздухом']}})
        else:
            act_prog({'mess': ['', 'Вы поменяли баллон', "Баллон полностью израсходовался", "Вы его выбросили"],
                      'inv': {'rem': ['Баллон c воздухом']}})
        clock_ballons = 100
    elif item == 'Походная Аптечка':
        if hp_player + 50 > 100:
            hp_player = 100
        else:

            hp_player += 50

        act_prog({'rem': ['Походная Аптечка'],
                  'mess': ["", "Вы использовали Походную аптечку", "Восстановлено 50 здоровья"]})
    elif item == 'Бинт':
        if hp_player + 40 > 100:
            hp_player = 100
        else:

            hp_player += 40

        act_prog({'rem': ['Бинт'], 'mess': ["", "Вы намотали бинт на рану", "Восстановлено 40 здоровья"]})


def check_item(item):
    if item == 'Еда':
        act_prog({'mess': ['', 'Это консерва с едой', "Не особо она приятна на вкус", "Но довольно питательно"]})
    elif item == 'Походная Аптечка':
        act_prog({'mess': ['', 'Это Походная аптечка', "В ней важные медицинские препараты", "Только аскорбинок нету"]})
    elif item == 'Баллон c воздухом':
        act_prog(
            {'mess': ['', 'Это Баллон с воздухом', "Он полон кислородом", "Полностью соместим с вашим скафандром"]})
    elif item == 'Неполный баллон с воздухом':
        act_prog({'mess': ['', 'Это баллон с воздухом', "Его показатель кислорода не полон",
                           "Наверное можно обединить оставшийся кислород", "В приборе",
                           "Правда надо несколько таких баллонов"]})
    elif item == 'Бинт':
        act_prog({'mess': ['', 'Это Бинт', "Способна лечить рану", "Даже через скафандр"]})


def act_prog(retur):
    global inventar, hp_player
    if 'inv' in retur:
        if 'rem' in retur['inv']:
            for i in retur['inv']['rem']:
                if i in inventar:
                    if inventar[i] != 1:
                        inventar[i] -= 1
                    else:
                        inventar.pop(i)
        if 'add' in retur['inv']:

            for i in retur['inv']['add']:
                if i in inventar:
                    inventar[i] += 1
                else:
                    inventar[i] = 1

    if 'hp' in retur:
        hp_player += retur['hp']
    if 'mess' in retur:
        messages(retur['mess'])
    if 'que' in retur:
        pass


def chests_act1(object1):
    global act_object
    act_object = object1


def messages(messages):
    global message_act, messages1
    message_act = True
    messages1 = messages


def message(screen1, message, x=50, y=height - 100):
    font = pygame.font.Font(None, 72)
    text = font.render(message, True, (255, 255, 255))
    place = text.get_rect(center=(0, 0))
    screen1.blit(text, (x, y))


def message_next():
    global message_countt, message_count, message_time
    message_countt += 1
    message_count = 0
    message_time = 0


def reload(lvl):
    global prohod_end, play, all_sprites, Walls, Floors, decor, prohod, osmotr, Item_dop, Chests, Walls_dm, log_act
    # restart sprites
    all_sprites = pygame.sprite.Group()
    Walls = pygame.sprite.Group()
    Floors = pygame.sprite.Group()
    decor = pygame.sprite.Group()
    prohod = pygame.sprite.Group()
    osmotr = pygame.sprite.Group()
    Item_dop = pygame.sprite.Group()
    Chests = pygame.sprite.Group()
    Walls_dm = pygame.sprite.Group()
    play.kill()
    # end restard sprites
    log_act = False
    run_card(lvl)
    prohod_end = False


def load_image(name, color_key=None):
    fullname = os.path.join('data\\img', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image.set_colorkey((255, 255, 255))
    '''
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    '''
    return image


class inventar_act:
    def __init__(self):
        self.act = False
        self.act_chests = False
        self.count = 0
        self.count_act = 0

    def update_param(self, napr):
        print(inventar)
        if napr == 'ri':
            if chests_act:
                print('сундук', act_object.item)
                if not self.act_chests:
                    if len(act_object.item) != 0:
                        self.act_chests = True
                        if self.count >= len(act_object.item):
                            self.count = len(act_object.item) - 1
            elif self.act:
                if self.count_act < 1:
                    self.count_act += 1

        elif napr == 'le':
            if chests_act:
                if self.act_chests:
                    self.act_chests = False
                    if self.count >= len(inventar):
                        self.count = len(inventar) - 1
                        if len(inventar) == 0:
                            self.count = 0
            elif self.act:
                if self.count_act != 0:
                    self.count_act -= 1
        elif napr == 'dow':
            if chests_act:
                if self.act_chests:
                    if self.count != len(act_object.item) - 1 and len(act_object.item) != 0:
                        self.count += 1
                else:
                    if self.count != len(inventar) - 1 and len(inventar) != 0:
                        self.count += 1
            else:

                if self.count != len(inventar) - 1 and len(inventar) != 0:
                    self.count += 1
        else:
            if self.count != 0:
                self.count -= 1

    def restart(self):
        self.count = 0
        self.act_chests = False
        self.act = False
        self.count_act = 0

    def update(self):
        if self.act_chests:
            pygame.draw.circle(screen, pygame.Color('Red'), (700, 50 * (self.count + 1) + 20), 25)
        elif self.act:
            pygame.draw.circle(screen, pygame.Color('Red'), (65 + 450 * self.count_act, height - 80), 25)
        else:
            pygame.draw.circle(screen, pygame.Color('Red'), (40, 50 * (self.count + 1) + 20), 25)
        if self.act:
            message(screen, 'Исользовать', 100, height - 100)
            message(screen, 'Изучить', 550, height - 100)

    def drop(self):
        global inventar, menu_act
        if self.act_chests:
            if len(act_object.item) != 0:
                print(act_object.item, act_object.item != 0)
                if act_object.item[self.count] in inventar:
                    inventar[act_object.item[self.count]] += 1
                else:
                    inventar[act_object.item[self.count]] = 1
                act_object.drop(self.count)
                if self.count == len(act_object.item) and len(act_object.item) != 0:
                    self.count = len(act_object.item) - 1

        if menu_act:
            if self.act:
                if self.count_act == 0:
                    inventar_temp = []
                    for i in inventar:
                        inventar_temp.append(i)
                    menu_act = False
                    item_act(inventar_temp[self.count])
                    self.restart()
                elif self.count_act == 1:
                    inventar_temp = []
                    for i in inventar:
                        inventar_temp.append(i)
                    menu_act = False
                    check_item(inventar_temp[self.count])
                    self.restart()
            else:
                if len(inventar) != 0:
                    self.act = True


class Osmotr_Object(pygame.sprite.Sprite):
    def __init__(self, x, y, item, peremen):
        super().__init__(osmotr)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.image = load_image('4313.png')
        item1 = []
        for i in item:
            if i == '+':
                item1.append(' ')
            else:
                item1.append(i)
        self.item = ''.join(item1)
        self.peremen = peremen

    def osmotr_act(self):
        try:
            act[self.peremen].act()
        except IndexError:
            pass
        if self.item != "":
            messages(self.item.split("&"))


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, im, item, list_osmotr, peremen, ob):
        super().__init__(Item_dop)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.ob = ob
        self.x = x
        self.y = y
        self.image = load_image(im)
        item1 = []
        for i in item:
            if i == '+':
                item1.append(' ')
            else:
                item1.append(i)
        self.item = ''.join(item1)
        self.osm = []

        if list_osmotr[0] == '1':
            self.osm.append(Osmotr_Object(x, y - (razn / 2), "", peremen))

        if list_osmotr[1] == '1':
            self.osm.append(Osmotr_Object(x, y + (razn / 2), "", peremen))

        if list_osmotr[2] == '1':
            self.osm.append(Osmotr_Object(x - (razn / 2), y, "", peremen))

        if list_osmotr[3] == '1':
            self.osm.append(Osmotr_Object(x + (razn / 2), y, "", peremen))

    def act(self):
        global inventar, despawn_list
        if self.item in inventar:
            inventar[self.item] += 1
        else:
            inventar[self.item] = 1
        messages(f"Вы подобрали {self.item}".split("&"))
        Floor('1233.png', self.x, self.y)
        for i in self.osm:
            i.kill()
        despawn_list.append(self.ob)
        self.kill()


class Prohod(pygame.sprite.Sprite):
    def __init__(self, x, y, im, lvl, ob):
        super().__init__(prohod)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.lvl = lvl
        self.image = load_image(im)
        self.ob = ob
        # self.param = param

    def osmotr_act(self):
        global prohod_end, prohodlvl, despawn_list
        despawn_list.append(self.ob)

        prohod_end = True
        prohodlvl = self.lvl


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, im, item, list_osmotr, peremen, ob):
        super().__init__(Chests)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.image = load_image(im)
        self.ob = ob
        item1 = []
        item2 = ''
        for i in item:
            if i == '+':
                item2 += ' '

            elif i == '&':
                item1.append(item2)
                item2 = ''
            else:
                item2 += i
        item1.append(item2)
        self.item = item1
        self.osm = []

        if list_osmotr[0] == '1':
            self.osm.append(Osmotr_Object(x, y - (razn / 2), "", peremen))

        if list_osmotr[1] == '1':
            self.osm.append(Osmotr_Object(x, y + (razn / 2), "", peremen))

        if list_osmotr[2] == '1':
            self.osm.append(Osmotr_Object(x - (razn / 2), y, "", peremen))

        if list_osmotr[3] == '1':
            self.osm.append(Osmotr_Object(x + (razn / 2), y, "", peremen))

    def act(self):
        global chests_act
        chests_act = True
        chests_act1(self)

    def list_return(self):
        return self.item

    def drop(self, intt):
        self.item.pop(intt)

    def despawn(self):
        global despawn_list
        despawn_list.append(self.ob)


class Decorathion(pygame.sprite.Sprite):
    def __init__(self, im, x, y, columns, rows, list_osmotr, peremen, ob, osmotr=None, wall=False):
        super().__init__(decor)
        self.frames = []
        self.cut_sheet(load_image(im), int(columns), int(rows))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.a = 0
        self.ob = ob
        if list_osmotr[0] == '1':
            Osmotr_Object(x, y - (razn / 2), osmotr, peremen)

        if list_osmotr[1] == '1':
            Osmotr_Object(x, y + (razn / 2), osmotr, peremen)

        if list_osmotr[2] == '1':
            Osmotr_Object(x - (razn / 2), y, osmotr, peremen)

        if list_osmotr[3] == '1':
            Osmotr_Object(x + (razn / 2), y, osmotr, peremen)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def despawn(self):
        global despawn_list
        despawn_list.append(self.ob)
        self.kill()

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def act(self):
        pass


class Floor(pygame.sprite.Sprite):

    def __init__(self, im, x, y):
        super().__init__(Floors)
        self.image = load_image(im)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.x = x
        self.y = y
        sheet = load_image('player_down.png')
        self.rect = pygame.Rect(0, 0, sheet.get_width() // 4,
                                sheet.get_height() // 1)
        self.cut_sheet(load_image('player_down.png'), 4, 1)

        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.rect = self.rect.move(x, y)
        # self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.left = False
        self.ridht = False
        self.up = False
        self.down = False
        self.wall = False
        self.button = False
        self.button1 = False
        self.button2 = False
        self.button3 = 'dow'
        self.button_old = 'dow'
        self.animation = 0

    def restart_image(self, param):
        self.frames = []
        # WARNING
        # Спрайты персонажа должны быть одинакового размера
        if param == 'dow':
            self.cut_sheet(load_image('player_down.png'), 4, 1)
        elif param == 'u':
            self.cut_sheet(load_image('player_up.png'), 4, 1)
        elif param == 'le':
            self.cut_sheet(load_image('player_left.png'), 4, 1)
        elif param == 'ri':
            self.cut_sheet(load_image('player_right.png'), 4, 1)
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        '''
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
                                '''
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                a = pygame.Rect(frame_location, self.rect.size)
                self.frames.append(sheet.subsurface(a))
        # self.rect.move_ip(-self.x, -self.y)

    def update(self):
        global hits
        # Анимация спрайта
        if not self.button2:
            if self.ridht:
                if not (self.up or self.down):
                    self.button3 = 'ri'
                    self.button_old = 'dow'
            if self.left:
                if not (self.up or self.down):
                    self.button3 = 'le'
                    self.button_old = 'dow'
        else:
            if self.up:
                if not (self.left or self.ridht):
                    self.button3 = 'u'
                    self.button_old = 'le'
            if self.down:
                if not (self.left or self.ridht):
                    self.button3 = 'dow'
                    self.button_old = 'le'
        if self.button3 == 'dow':
            if self.button_old != 'dow':
                self.button_old = 'dow'
                self.restart_image('dow')
                '''
            if self.down:
                self.animation += 1
            else:
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]'''
        if self.button3 == 'u':
            if self.button_old != 'u':
                self.button_old = 'u'
                self.restart_image('u')
                '''
            if self.up:
                self.animation += 1
            else:
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]'''
        if self.button3 == 'le':
            if self.button_old != 'le':
                self.button_old = 'le'
                self.restart_image('le')
                '''
                if self.left:
                self.animation += 1
            
            else:
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]'''
        if self.button3 == 'ri':
            if self.button_old != 'ri':
                self.button_old = 'ri'
                self.restart_image('ri')
                '''
            if self.ridht:
                self.animation += 1
            else:
                self.cur_frame = 0
                self.image = self.frames[self.cur_frame]'''
        if self.left or self.ridht or self.down or self.up:
                self.animation += 1
        else:
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
        if self.animation >= 30:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.animation = 0

        # конец обработчика информаций

        # Реакция на стену(сделано с божьей помощью)
        if hits:
            self.wall = True
        else:
            self.wall = False
        if hits:
            if True:
                if self.button2:
                    if self.button == "ri":
                        self.rect = self.rect.move(-1, 0)
                        self.x -= 1
                    elif self.button == 'le':
                        self.rect = self.rect.move(1, 0)
                        self.x += 1
                else:
                    if self.button1 == "dow":
                        self.rect = self.rect.move(0, -1)
                        self.y += 1
                    elif self.button1 == 'u':
                        self.y -= 1
                        self.rect = self.rect.move(0, 1)
                hits = pygame.sprite.spritecollide(play, Walls, False)

                hits = hits + pygame.sprite.spritecollide(play, param_group[lvl][0], False) + \
                       pygame.sprite.spritecollide(play, Walls_dm, False)
                if hits:
                    if self.button2:
                        if self.button1 == "dow":
                            self.rect = self.rect.move(0, -1)
                            self.y += 1
                        elif self.button1 == 'u':
                            self.y -= 1
                            self.rect = self.rect.move(0, 1)
                    else:
                        if self.button == "ri":
                            self.rect = self.rect.move(-1, 0)
                            self.x -= 1
                        elif self.button == 'le':
                            self.rect = self.rect.move(1, 0)
                            self.x += 1
        if not message_act:
            if self.down:
                if hits:
                    self.rect = self.rect.move(0, -1)
                    self.y -= -1
                self.rect = self.rect.move(0, 1)
                self.y -= 1
            if self.ridht:
                if hits:
                    self.rect = self.rect.move(-1, 0)
                    self.x -= 1

                self.x += 1

                self.rect = self.rect.move(1, 0)
            if self.up:
                if hits:
                    self.y -= 1
                    self.rect = self.rect.move(0, 1)
                self.y += 1

                self.rect = self.rect.move(0, -1)
            if self.left:
                if hits:
                    self.x += 1
                    self.rect = self.rect.move(1, 0)
                self.x -= 1
                self.rect = self.rect.move(-1, 0)
        if hits:
            self.ridht = False
            self.up = False
            self.left = False
            self.down = False
        # print(self.x, self.y, self.wall, hits, self.button, self.button1, self.x % 5 != 0, self.y % 5 != 0)
        # print("do", self.down, "up", self.up, "le", self.left, "ri", self.ridht)
        # Конец реакций со стеной

    def ri(self, off):

        if not self.left and not off and not hits:
            self.button = "ri"
            self.ridht = True
            self.button2 = True
            self.button3 = 'ri'
        if off:
            self.ridht = False

    def u(self, off):
        if not self.down and not off and not hits:
            self.button1 = "u"
            self.up = True
            self.button2 = False
            self.button3 = 'u'
        if off:
            self.up = False

    def le(self, off):
        if not self.ridht and not off and not hits:
            self.button = "le"
            self.left = True
            self.button2 = True
            self.button3 = "le"
        if off:
            self.left = False

    def dow(self, off):
        if not self.up and not off and not hits:
            self.down = True
            self.button1 = "dow"
            self.button3 = "dow"
            self.button2 = False
        if off:
            self.down = False

    def coords(self):
        return self.x, self.y


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, im):
        super().__init__(Walls)
        self.image = load_image(im)
        self.rect = pygame.Rect(0, 0, 99, 99)
        self.rect = self.rect.move(x, y)

    def pp_heats(self):
        pass


class Wall_damage(pygame.sprite.Sprite):

    def __init__(self, x, y, im, damage, ob):
        super().__init__(Walls_dm)
        self.image = load_image(im)
        self.rect = pygame.Rect(0, 0, 99, 99)
        self.rect = self.rect.move(x, y)
        self.damage = int(damage)
        self.ob = ob

    def pp_heats(self):
        act_prog({'mess': [f'Вы наткнулись на колючку и получили {self.damage} урона'], 'hp': self.damage * -1})

    def despawn(self):
        global despawn_list
        despawn_list.append(self.ob)


def run_card(lvl1):
    global act, play, param, lvl, g
    x, y = 0, 0
    lvl = int(lvl1)
    a = Card(lvl)
    act_list = a.act_list()
    image_floor = ''
    image_wall = ''
    for i in a.pp():
        for g in i:
            if g == "#":
                Wall(x, y, act_list[g][1])
                image_wall = act_list[g][1]
            elif g == "@":
                Floor(act_list['.'][1], x, y)
                play = Player(x, y)

            elif g == "&":
                Wall(x, y, '432.png')
            elif g == ".":
                image_floor = act_list[g][1]
                Floor(act_list[g][1], x, y)
            if g in act_list:
                act_spawn = act_list[g]
                if act_spawn[-1] in despawn_list:
                    Floor(image_floor, x, y)
                    x += razn
                    continue
                if act_spawn[1] == "Dec":
                    if act_spawn[0]:
                        Wall(x, y, "space.png")
                    act[g] = Decorathion(act_spawn[4], x, y + 1, act_spawn[2], act_spawn[3], act_spawn[5:9], g,
                                         act_spawn[10], osmotr=act_spawn[9])
                elif act_spawn[1] == "Item":
                    act[g] = Item(x, y, act_spawn[2], act_spawn[7], act_spawn[3:7], g, act_spawn[-1])
                elif act_spawn[1] == "Che":
                    if act_spawn[0]:
                        Wall(x, y + 1, "space.png")
                    act[g] = Chest(x, y, act_spawn[2], act_spawn[7], act_spawn[3:7], g, act_spawn[-1])
                elif act_spawn[1] == 'Pro':
                    Floor(image_floor, x, y)
                    act[g] = Prohod(x, y, act_spawn[2], act_spawn[3], act_spawn[-1])
                elif act_spawn[1] == 'Obl':
                    act[g] = Wall_damage(x, y, act_spawn[2], act_spawn[3], act_spawn[-1])
            if lvl in param:
                if g in param[lvl]:
                    a = param[lvl]
                    a = a[g]
                    if a.ob in despawn_list:
                        Floor(image_floor, x, y)
                        x += razn

                        continue
                    a.smena(x + razn, y + razn)
                    if param[lvl][g].floor:
                        Floor(image_floor, x, y)
            x += razn
        x = 0
        y += razn


def main_card():
    global chests_act, menu_act, menu_act1, play, message_count, \
        message_countt, message_time, messages1, act, message_act, hits, \
        prohod_end, prohod_lvl, clock_ballons, clock_ballons1, hits_osm, \
        hits_osm_prog, hits_prog, hits_proh, hits_prog1, hits_Obl, log_act, despawn_list
    log_act = True
    running = True
    inventar_a = inventar_act()
    FPS_act = False
    FPS_cons = False
    hits_ignore = False
    player_coords = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if menu_act or chests_act:
                        inventar_a.update_param('up')
                    play.u(False)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if menu_act or chests_act:
                        inventar_a.update_param('dow')
                    play.dow(False)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if menu_act or chests_act:
                        inventar_a.update_param('le')
                    play.le(False)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if menu_act or chests_act:
                        inventar_a.update_param('ri')
                    play.ri(False)

                if event.key == pygame.K_z:
                    if menu_act or chests_act:
                        inventar_a.drop()
                    if message_act:
                        message_next()
                    else:
                        if not menu_act:
                            if hits_osm:
                                hits_osm[0].osmotr_act()
                            if hits_osm_prog:
                                act_prog(hits_osm_prog[0].osmotr_act())
                if event.key == pygame.K_x:
                    if inventar_a.act:
                        inventar_a.count_act = 0
                        inventar_a.act = False
                    else:
                        if not message_act:
                            if chests_act:
                                chests_act = False
                            else:
                                menu_act = not menu_act
                                menu_act1 = False
                                screen.fill(pygame.Color("black"))
                        inventar_a.restart()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_h:
                    hits_ignore = not hits_ignore
                if event.key == pygame.K_f:
                    FPS_act = not FPS_act
                if event.key == pygame.K_l:
                    FPS_cons = not FPS_cons
                if event.key == pygame.K_p:
                    player_coords = not player_coords
                if event.key == pygame.K_r:
                    despawn_list = []
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    play.u(True)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    play.dow(True)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    play.le(True)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    play.ri(True)

        screen.fill(pygame.Color("black"))
        if prohod_end:
            for i in param[lvl]:
                bye = param[lvl][i].despawn(razn)
                if bye:
                    despawn_list.append(bye)
            for i in Chests:
                i.despawn()

            return 0
        elif chests_act:
            count_item = 0
            screen.fill(pygame.Color("black"))
            inventar_a.update()
            if len(inventar) != 0:
                for i in inventar:
                    count_item += 50
                    message(screen, f'{str(i)} {str(inventar[i])}', 100, count_item)

            else:

                message(screen, "Ивентарь пуст", 100, 50)
            count_item = 0
            if len(act_object.item) != 0:
                for i in act_object.list_return():
                    count_item += 50

                    message(screen, f'{str(i)}',
                            750, count_item)
            else:
                message(screen, "Сундук пуст", 750, 50)

        elif not menu_act:
            Floors.draw(screen)
            all_sprites.draw(screen)
            Walls.draw(screen)
            decor.draw(screen)
            all_sprites.update()
            Item_dop.draw(screen)
            Walls_dm.draw(screen)

            Chests.draw(screen)
            Progr.draw(screen)
            Walls_prog.draw(screen)

            param_group[lvl][0].draw(screen)
            param_group[lvl][1].draw(screen)
            hits = []
            hits_prog = False

            if not hits_ignore:
                hits = pygame.sprite.spritecollide(play, Walls, False)
                hits_osm = pygame.sprite.spritecollide(play, osmotr, False)
                hits_osm_prog = (pygame.sprite.spritecollide(play, Object_prog, False))
                hits_prog = pygame.sprite.spritecollide(play, param_group[lvl][0], False)
                hits_proh = pygame.sprite.spritecollide(play, prohod, False)
                hits_prog1 = pygame.sprite.spritecollide(play, param_group[lvl][1], False)
                hits_Obl = pygame.sprite.spritecollide(play, Walls_dm, False)
                hits = hits + hits_prog + hits_Obl
            else:
                message(screen, 'Включен чит', widht - 400, height - 300)
            if player_coords:
                message(screen, f'x = {str(play.coords()[0])} y = {str(play.coords()[1])}', widht - 400, height - 200)

            if hits_Obl:
                hits = [1]
                hits_Obl[0].pp_heats()
            if hits_proh:
                hits_proh[0].osmotr_act()
            if message_countt >= len(messages1):
                message_act = False
                message_countt = 0
            if message_act:
                message_time += 1

                if 60 // len(messages1[message_countt]) == message_time:
                    if message_count <= len(messages1[message_countt]):
                        message_count += 1
                        message_time = 0
                message(screen, messages1[message_countt][0:message_count])
            # osmotr.draw(screen)
            if not message_act:
                clock_ballons1 += 1
                if clock_ballons1 == 10:
                    clock_ballons -= 1
                    clock_ballons1 = 0
            if hits_prog:
                hits = [1]
                act_prog(hits_prog[0].hits_act())
            if hits_prog1:
                act_prog(hits_prog1[0].hits_act())

        else:
            count_item = 0
            screen.fill(pygame.Color("black"))
            pygame.draw.rect(screen, (pygame.Color("red")), (900, 30, 300, 55))
            pygame.draw.rect(screen, (pygame.Color("green")), (900, 30, 300 * (hp_player / 100), 55))
            message(screen, 'Здоровье', 650, 35)
            message(screen, 'Кислород', 650, 105)
            pygame.draw.rect(screen, (pygame.Color("Blue")), (900, 100, 300, 55))
            pygame.draw.rect(screen, (pygame.Color("Aqua")), (900, 100, 300 * (clock_ballons / 100), 55))
            inventar_a.update()
            if len(inventar) != 0:
                for i in inventar:
                    count_item += 50
                    message(screen, f'{str(i)} {str(inventar[i])}', 100, count_item)

            else:

                message(screen, "Ивентарь пуст", 100, 50)
        # print(hits)
        clock.tick(FPS)
        if FPS_act:
            message(screen, f'FPS {round(clock.get_fps())}', widht - 250, height - 100)
        if FPS_cons:
            print(round(clock.get_fps()))
        message(screen, str(play.button) + ' ' + str(play.button1) + ' ' + str(len(hits)), 700, 600)
        pygame.display.flip()


def act_main_card():
    main_card()
    reload(prohodlvl)
    return 1


if __name__ == '__main__':
    if log:
        try:
            run_card(1)
            ran = 1
            while ran == 1:
                ran = act_main_card()
        except BaseException as err:
            if log:
                if log_act:
                    if str(err) != 'display Surface quit':
                        logging.critical(err)

                        logging.error(
                            f'Переменные main_act {chests_act, menu_act, menu_act1, play, message_count}'
                            f' {message_countt, message_time, messages1, act, message_act, hits}'
                            f' {prohod_end, prohod_lvl, clock_ballons, clock_ballons1}'
                            f' Хиты {hits, hits_osm, hits_osm_prog, hits_prog, hits_proh, hits_prog1, hits_Obl}')
                else:
                    logging.critical(err)
                    logging.error(f"Переменные lvl {lvl}, g{g}, act{act}")
        exit()
    else:
        run_card(1)
        ran = 1
        while ran == 1:
            ran = act_main_card()
