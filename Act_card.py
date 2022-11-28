import os
from card_act import Card
import pygame

pygame.init()

infoObject = pygame.display.Info()
height = infoObject.current_h

widht = infoObject.current_w
#height = 1080
#height = 1000
#widht = 1000
#screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
screen = pygame.display.set_mode((widht, height))
#screen_menu = pygame.display.set_mode((widht, height))
clock = pygame.time.Clock()
hits = False
all_sprites = pygame.sprite.Group()
Walls = pygame.sprite.Group()
Floors = pygame.sprite.Group()
decor = pygame.sprite.Group()
osmotr = pygame.sprite.Group()
Item_dop = pygame.sprite.Group()
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
def messages(messages):
    global message_act, messages1
    message_act = True
    messages1 = messages
def message(screen1, message, x = 50, y = height - 100):
    font = pygame.font.Font(None, 72)
    text = font.render(message, True, (255, 255, 255))
    place = text.get_rect(center=(0, 0))
    screen1.blit(text, (x, y))
def message_next():
    global message_countt, message_count, message_time
    message_countt += 1
    message_count = 0
    message_time = 0
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

def restart_menu():
    count_item = 0
        
        

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
        print(self.item.split("&"))
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
        self.item = item
        self.osm =[]

        if list_osmotr[0] == '1':
            self.osm.append(Osmotr_Object(x, y - razn, "",  peremen))


        if list_osmotr[1] == '1':
            self.osm.append(Osmotr_Object(x, y + razn, "",  peremen))

        if list_osmotr[2] == '1':
            self.osm.append(Osmotr_Object(x - razn, y, "",  peremen))

        if list_osmotr[3] == '1':
            self.osm.append(Osmotr_Object(x + razn, y, "",  peremen))
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

class Decorathion(pygame.sprite.Sprite):
    def __init__(self, im, x, y, columns, rows, list_osmotr, peremen, osmotr=None, wall = False):
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
            Osmotr_Object(x, y - razn, osmotr,  peremen)

        if list_osmotr[1] == '1':
            Osmotr_Object(x, y + razn, osmotr,  peremen)

        if list_osmotr[2] == '1':
            Osmotr_Object(x - razn, y, osmotr,  peremen)

        if list_osmotr[3] == '1':
            Osmotr_Object(x + razn, y, osmotr,  peremen)
                    
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

    def __init__(self, x, y,im):
        super().__init__(Walls)
        self.image = load_image(im)
        self.rect = pygame.Rect(0, 0, 99, 99)
        self.rect = self.rect.move(x, y)


x, y = 0, 0
a = Card(1)
act_list = a.act_list()
for i in a.pp():

    for g in i:
        if g in act_list:
            act_spawn = act_list[g]
            print(act_spawn, g)
            if act_spawn[1] == "Dec":
                if act_spawn[0]:
                    Wall(x, y+1, "space.png")
                act[g] = Decorathion(act_spawn[4], x, y+1, act_spawn[2], act_spawn[3], act_spawn[5:9], g, act_spawn[9])
            elif act_spawn[1] == "Item":
                print(8248612)
                act[g] = Item(x, y+1, act_spawn[2], act_spawn[-1], act_spawn[3:7], g)
                
                    
        elif g == "#":
            Wall( x, y,'213.png')
        elif g == "@":
            play = Player(load_image("Player.png"), 1, 1, x, y)
            Floor('1233.png', x, y)
        elif g == "&":
            Wall( x, y,'432.png')
        elif g == ".":
            Floor('1233.png', x, y)

        x += razn
    x = 0
    y += razn
running = True
print(act)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                play.u(False)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                play.dow(False)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                play.le(False)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                play.ri(False)
            if event.key == pygame.K_z:
                if message_act:
                    message_next()
                else:
                    if hits_osm:
                        hits_osm[0].pp()
            if event.key == pygame.K_x:
                menu_act = not menu_act
                menu_act1 = False
                screen.fill(pygame.Color("black"))
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
    if not menu_act:
        Floors.draw(screen)
        all_sprites.draw(screen)
        Walls.draw(screen)
        decor.draw(screen)
        all_sprites.update()
        Item_dop.draw(screen)
        hits = pygame.sprite.spritecollide(play, Walls, False)
        hits_osm = pygame.sprite.spritecollide(play, osmotr, False)
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
    else:
        count_item = 0
        screen.fill(pygame.Color("black"))
        restart_menu()
        if len(inventar) !=0:
            for i in inventar:
                print(count_item)
                count_item += 50
                message(screen, f'{str(i)} {str(inventar[i])}', 50, count_item)

        else:

            message(screen, "Ивентарь пуст", 50, 50)

    pygame.display.flip()