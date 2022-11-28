import os

import pygame

from cat_file.generate_star_xy import get_star_coords

pygame.init()

FPS = 80
dragon1 = 1
infoObject = pygame.display.Info()
height = infoObject.current_h
# height = 1080
widht = infoObject.current_w
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
screen_space = []
star_coord = get_star_coords(widht, height)
# screen = pygame.display.set_mode((1080, 1080))
clock = pygame.time.Clock()
message_time = -100
message_count = 0
message_countt = 0
message_act = False
message_max = 3
messages3 = False
mess = False
act_2 = False
messages = []
all_sprites = pygame.sprite.Group()
Fone_sprites = pygame.sprite.Group()
aster_bum = False
aster1 = False


# Исправить баг с капсулой когда скипаешь сообщение

def restart_messages(messagess, messages_time1):
    global messages, message_act, message_count, message_countt, message_time, message_max
    message_time = messages_time1
    message_count = 0
    message_countt = 0
    message_max = len(messagess)
    message_act = False
    messages = messagess


def message(message):
    font = pygame.font.Font(None, 72)
    text = font.render(message, True, (255, 255, 255))
    place = text.get_rect(center=(0, 0))
    screen.blit(text, (50, height - 100))


def load_image(name, color_key=None):
    fullname = os.path.join('data\img', name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    return image


class AnimatedFoneSpace(pygame.sprite.Sprite):
    def __init__(self, image, x_run, y_run, x, y):
        super().__init__(Fone_sprites)
        self.frames = []
        self.run = (x_run, y_run)
        self.image_name = image
        self.image = load_image(image)
        self.image_x_y = [self.image.get_width(), self.image.get_height()]
        self.rect = pygame.Rect(0, 0, self.image.get_width(),
                                self.image.get_height())
        self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.yx = [-x, -y]
        self.a = 0

    def update(self):
        if self.run[0]:
            self.yx[0] += 1
            self.rect = self.rect.move(self.x - self.x - 1, self.y - self.y)
            if self.yx[0] + widht == int(self.image_x_y[0]):
                AnimatedFoneSpace(self.image_name, 1, 1, widht, 0)
            if self.yx[0] == int(self.image_x_y[0]):
                self.kill()

    def despawn(self):
        self.kill()


class Ship_bum(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.a = 0
        self.conti = False
        self.image1 = 0
        self.r = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.a += 1
        if self.a == 5 and self.image1 < 8:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.a = 0
            self.image1 += 1
        if message_count == 1 and self.r and mess:
            a = kapsula(load_image("caps.png"), 1050, (height / 3) + 50)
            self.r = False


class AnimatedSpriteold(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.a = 0

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


class Aster(pygame.sprite.Sprite):
    def __init__(self, aster, x, y):
        super().__init__(all_sprites)
        self.image = aster
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect = self.rect.move(x, y)

    def despawn(self):
        self.kill()


class kapsula(pygame.sprite.Sprite):
    def __init__(self, kaps, x, y):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect = self.rect.move(x, y)
        self.image = kaps
        self.a = 0
        self.b = 0
        self.x = x
        self.y = y

    def despawn(self):
        self.kill()

    def update(self):
        self.a += 1
        if self.a == 3:
            self.rect = self.rect.move((self.x - self.x) + 1, (self.y - self.y) + 1)
            self.b += 1
            self.a = 0
        if self.b == 50:
            self.kill()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, cat):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(0, y)
        self.x = 0
        self.y = y
        self.x1 = x
        self.a = 0
        self.conti = False
        self.act = True
        self.cat = cat
        self.conti1 = False

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
        self.a += 1
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.a == 2 and (self.act or self.x < self.x1):
            if self.cat:
                self.rect = self.rect.move((self.x - self.x) + 4, self.y - self.y)
                self.a = 0
                self.x += 4
            else:
                self.rect = self.rect.move((self.x - self.x) + 2, self.y - self.y)
                self.a = 0
                self.x += 2
        if message_count >= message_max and not self.cat:
            self.x += 2
            self.rect = self.rect.move((self.x - self.x) + 2, self.y - self.y)
        '''        if self.x >= self.x1:
            global mess
            mess = True'''

        if self.x >= self.x1 and self.cat:
            global aster_bum
            aster_bum = True
        if self.x >= widht:
            self.conti = True
        if message_count == 1 and self.cat:
            a = kapsula(load_image("caps.png"), 1050, (height / 3) + 50)


def main():
    global message_count, message_countt, message_time, act_2, ship, aster_bum, dragon1, mess, aster
    restart_messages(["Давным давно", "Летел экипаж на марс", "Они перевозят с собой семена", "Ближе к подлету марса"],
                     -100)
    dragon = AnimatedFoneSpace("небо.png", 1, 1, 0, 0)
    ship = AnimatedSprite(load_image("ship.png"), 3, 1, 600, height / 3, False)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    message_count += 1
                    message_countt = 0
                    message_time = 0

        message_time += 1

        if ship.conti:
            ship.conti = False

            act_2 = True
            dragon.despawn()
            ship.despawn()

            ship = AnimatedSprite(load_image("ship.png"), 3, 1, 1000, height / 3, True)
            restart_messages(
                ['Они неожиданно врезались в астероид', 'И Вы приняли решение спастись в спасательной шлюпке'], -200)
            aster = Aster(load_image("aster.png"), 1050, height / 3)
            dragon1 = AnimatedFoneSpace(("марс.png"), False, 1, 0, 0)
        if act_2:
            screen.fill(pygame.Color("black"))

            for g in star_coord:
                pygame.draw.circle(screen, (255, 255, 255), (g[0], g[1]), g[2])
            ship.update()
            dragon1.update()

            if aster_bum:
                ship.despawn()
                aster.despawn()
                ship = Ship_bum(load_image("123 (1).png"), 9, 1, 1000, height / 3)
                mess = True

                aster_bum = False

        Fone_sprites.draw(screen)

        all_sprites.draw(screen)
        if message_time > 0:
            if message_count < message_max:
                if 60 // len(messages[message_count]) == message_time:
                    message_countt += 1
                    message_time = 0
                message(messages[message_count][0:message_countt])
        pygame.display.flip()
        Fone_sprites.update()
        all_sprites.update()
        clock.tick(FPS)

    pygame.quit()
