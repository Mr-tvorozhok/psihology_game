import os
from card_act import Card
import pygame
from lvl1 import param, Progr, Walls_prog, Object_prog
import time

infoObject = pygame.display.Info()
height = infoObject.current_h
FPS = 180
widht = infoObject.current_w
# height = 1080
# height = 1000
# widht = 1000
# screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
screen = pygame.display.set_mode((widht, height))
# screen_menu = pygame.display.set_mode((widht, height))
clock = pygame.time.Clock()
hits = False
all_sprites = pygame.sprite.Group()
Walls = pygame.sprite.Group()
Floors = pygame.sprite.Group()
decor = pygame.sprite.Group()
prohod = pygame.sprite.Group()
osmotr = pygame.sprite.Group()
Item_dop = pygame.sprite.Group()
Chests = pygame.sprite.Group()
Walls_dm = pygame.sprite.Group()
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
                      'inv': {'rem': 'Баллон с воздухом'}})
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
    global prohod_end, play, all_sprites, Walls, Floors, decor, prohod, osmotr, Item_dop, Chests, Walls_dm
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
    run_card(lvl)
    prohod_end = False


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


class inventar_act:
    def __init__(self):
        self.act = False
        self.act_chests = False
        self.count = 0
        self.count_act = 0

    def update_param(self, napr):
        if napr == 'ri':
            if chests_act:
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
                if self.count_act == 1:
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
        self.image = load_image('space.png')
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
            act[self.peremen].act()
        except IndexError:
            pass
        if self.item != "":
            messages(self.item.split("&"))


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, im, item, list_osmotr, peremen):
        super().__init__(Item_dop)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
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
            self.osm.append(Osmotr_Object(x, y - razn, "", peremen))

        if list_osmotr[1] == '1':
            self.osm.append(Osmotr_Object(x, y + razn, "", peremen))

        if list_osmotr[2] == '1':
            self.osm.append(Osmotr_Object(x - razn, y, "", peremen))

        if list_osmotr[3] == '1':
            self.osm.append(Osmotr_Object(x + razn, y, "", peremen))

    def act(self):
        global inventar
        if self.item in inventar:
            inventar[self.item] += 1
        else:
            inventar[self.item] = 1
        messages(f"Вы подобрали {self.item}".split("&"))
        Floor('1233.png', self.x, self.y)
        for i in self.osm:
            i.kill()
        self.kill()


class Prohod(pygame.sprite.Sprite):
    def __init__(self, x, y, im, lvl):
        super().__init__(prohod)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.lvl = lvl
        self.image = load_image(im)

    def pp(self):
        global prohod_end, prohodlvl
        prohod_end = True
        prohodlvl = self.lvl


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, im, item, list_osmotr, peremen):
        super().__init__(Chests)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.image = load_image(im)
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
            self.osm.append(Osmotr_Object(x, y - razn, "", peremen))

        if list_osmotr[1] == '1':
            self.osm.append(Osmotr_Object(x, y + razn, "", peremen))

        if list_osmotr[2] == '1':
            self.osm.append(Osmotr_Object(x - razn, y, "", peremen))

        if list_osmotr[3] == '1':
            self.osm.append(Osmotr_Object(x + razn, y, "", peremen))

    def act(self):
        global chests_act
        chests_act = True
        chests_act1(self)

    def list_return(self):
        return self.item

    def drop(self, intt):
        self.item.pop(intt)


class Decorathion(pygame.sprite.Sprite):
    def __init__(self, im, x, y, columns, rows, list_osmotr, peremen, osmotr=None, wall=False):
        super().__init__(decor)
        self.frames = []
        self.cut_sheet(load_image(im), int(columns), int(rows))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.a = 0
        if list_osmotr[0] == '1':
            Osmotr_Object(x, y - razn, osmotr, peremen)

        if list_osmotr[1] == '1':
            Osmotr_Object(x, y + razn, osmotr, peremen)

        if list_osmotr[2] == '1':
            Osmotr_Object(x - razn, y, osmotr, peremen)

        if list_osmotr[3] == '1':
            Osmotr_Object(x + razn, y, osmotr, peremen)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def despawn(self):
        self.kill()

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def act(self):
        print(1)


class Floor(pygame.sprite.Sprite):

    def __init__(self, im, x, y):
        super().__init__(Floors)
        self.image = load_image(im)
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect = self.rect.move(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.left = False
        self.ridht = False
        self.up = False
        self.down = False
        self.wall = False
        self.button = False
        self.button1 = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        # Реакция на стену(сделано с божьей помощью)
        if hits:
            self.wall = True
        else:
            self.wall = False
        if hits:
            if self.x % 5 != 0:
                if self.button == "ri":
                    self.rect = self.rect.move(-1, 0)
                    self.x -= 1
                else:
                    self.rect = self.rect.move(1, 0)
                    self.x += 1
            if self.y % 5 != 0:
                if self.button1 == "dow":
                    self.rect = self.rect.move(0, -1)
                    self.y += 1
                else:
                    self.y -= 1
                    self.rect = self.rect.move(0, 1)
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

        # print(self.x, self.y, self.wall, hits, self.button, self.button1, self.x % 5 != 0, self.y % 5 != 0)
        # print("do", self.down, "up", self.up, "le", self.left, "ri", self.ridht)
        # Конец реакций со стенойy

    def ri(self, off):
        if not self.left and not off:
            self.button = "ri"
            self.ridht = True
        if off:
            self.ridht = False

    def u(self, off):
        if not self.down and not off:
            self.button1 = "u"
            self.up = True
        if off:
            self.up = False

    def le(self, off):
        if not self.ridht and not off:
            self.button = "le"
            self.left = True
        if off:
            self.left = False

    def dow(self, off):
        if not self.up and not off:
            self.down = True
            self.button1 = "dow"
        if off:
            self.down = False


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, im):
        super().__init__(Walls)
        self.image = load_image(im)
        self.rect = pygame.Rect(0, 0, 99, 99)
        self.rect = self.rect.move(x, y)

    def pp_heats(self):
        pass


class Wall_damage(pygame.sprite.Sprite):

    def __init__(self, x, y, im, damage):
        super().__init__(Walls_dm)
        self.image = load_image(im)
        self.rect = pygame.Rect(0, 0, 99, 99)
        self.rect = self.rect.move(x, y)
        self.damage = int(damage)

    def pp_heats(self):
        act_prog({'mess': ['Вы наткнулись на колючку и получили 30 урона'], 'hp': self.damage * -1})


def run_card(lvl):
    global act, play, param
    x, y = 0, 0
    a = Card(lvl)
    act_list = a.act_list()
    for i in a.pp():

        for g in i:
            if g == "#":
                Wall(x, y, act_list[g][1])
            elif g == "@":
                Floor(act_list['.'][1], x, y)
                play = Player(load_image("Player.png"), 1, 1, x, y)

            elif g == "&":
                Wall(x, y, '432.png')
            elif g == ".":
                Floor(act_list[g][1], x, y)
            if g in act_list:
                act_spawn = act_list[g]
                if act_spawn[1] == "Dec":
                    if act_spawn[0]:
                        Wall(x, y + 1, "space.png")
                    act[g] = Decorathion(act_spawn[4], x, y + 1, act_spawn[2], act_spawn[3], act_spawn[5:9], g,
                                         act_spawn[9])
                elif act_spawn[1] == "Item":
                    act[g] = Item(x, y + 1, act_spawn[2], act_spawn[-1], act_spawn[3:7], g)
                elif act_spawn[1] == "Che":
                    if act_spawn[0]:
                        Wall(x, y + 1, "space.png")
                    act[g] = Chest(x, y + 1, act_spawn[2], act_spawn[-1], act_spawn[3:7], g)
                elif act_spawn[1] == 'Pro':
                    act[g] = Prohod(x, y, act_spawn[2], act_spawn[3])
                elif act_spawn[1] == 'Obl':
                    act[g] = Wall_damage(x, y, act_spawn[2], act_spawn[3])
            if lvl in param:
                if g in param[lvl]:
                    param[lvl][g].smena(x, y)
                    if param[lvl][g].walls:
                        Wall(x, y + 1, "space.png")
            '''     
            elif g == "#":
                Wall( x, y,'213.png')
            elif g == "@":
                play = Player(load_image("Player.png"), 1, 1, x, y)
                Floor('1233.png', x, y)
            elif g == "&":
                Wall( x, y,'432.png')
            elif g == ".":
                Floor('1233.png', x, y)
                '''

            x += razn
        x = 0
        y += razn


def main_card():
    global chests_act, menu_act, menu_act1, play, message_count, message_countt, message_time, message1, messages1, act, message_act, hits, prohod_end, prohod_lvl, clock_ballons, clock_ballons1
    running = True
    inventar_a = inventar_act()
    FPS_act = False
    FPS_cons = False
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
                if event.key == pygame.K_f:
                    FPS_act = not FPS_act
                if event.key == pygame.K_l:
                    FPS_cons = not FPS_cons
                if event.key == pygame.K_z:
                    if menu_act or chests_act:
                        inventar_a.drop()
                    if message_act:
                        message_next()
                    else:
                        if not menu_act:
                            if hits_osm:
                                hits_osm[0].pp()
                            if hits_osm_prog:
                                print(11234124)
                                act_prog(hits_osm_prog[0].pp())
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

                    message(screen, f'{str(i)}'
                            , 750, count_item)
            else:
                message(screen, "Сундук пуст", 750, 50)

        elif not menu_act:
            Floors.draw(screen)
            all_sprites.draw(screen)
            message(screen, str(hp_player), 1000, 1000)
            Walls.draw(screen)
            decor.draw(screen)
            all_sprites.update()
            Item_dop.draw(screen)
            Walls_dm.draw(screen)
            hits = pygame.sprite.spritecollide(play, Walls, False)
            hits_osm = pygame.sprite.spritecollide(play, osmotr, False)
            Chests.draw(screen)
            Progr.draw(screen)
            Walls_prog.draw(screen)
            hits_osm_prog = (pygame.sprite.spritecollide(play, Object_prog, False))
            hits_prog = pygame.sprite.spritecollide(play, Walls_prog, False)
            hits_proh = pygame.sprite.spritecollide(play, prohod, False)
            hits_Obl = pygame.sprite.spritecollide(play, Walls_dm, False)
            if hits_Obl:
                hits = True
                hits_Obl[0].pp_heats()
            if hits_proh:
                hits_proh[0].pp()
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

            osmotr.draw(screen)
            if not message_act:
                clock_ballons1 += 1
                if clock_ballons1 == 100:
                    clock_ballons -= 1
                    clock_ballons1 = 0
            if hits_prog:
                hits = True
                act_prog(hits_prog[0].hits_act())
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
        pygame.display.flip()


def act_main_card():
    main_card()
    reload(prohodlvl)
    return 1


if __name__ == '__main__':
    run_card(1)
    ran = 1
    while ran == 1:
        ran = act_main_card()
