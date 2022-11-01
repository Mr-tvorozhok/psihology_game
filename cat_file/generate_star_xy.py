from random import randrange, choice
# 740 120 1660 940
def get_star_coords(widht, height):
    a = 0
    star = []
    star_temp = []
    while a != 40:
        x = randrange(0, widht)
        y = randrange(0, height)
        star_temp = [x, y, choice([5, 3])]
        star.append(star_temp)
        a += 1
    return star

