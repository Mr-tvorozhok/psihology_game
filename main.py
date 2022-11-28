import os

import pygame

from cat_file.begin_space_act import main

pygame.init()

infoObject = pygame.display.Info()
height = infoObject.current_h
# height = 1080
widht = infoObject.current_w
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


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

main()