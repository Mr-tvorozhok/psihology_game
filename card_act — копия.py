class Card:
    def __init__(self, lvl):
        self.lvl = lvl
        a = open(f'data/level/txt/lvl{lvl}.txt', "r", encoding= "utf-8").readlines()
        self.card = []
        b = a[0]
        c = 1
        self.act_item = {}
        while b != "~\n":
            self.card.append(b[:-1])
            b = a[c]
            c += 1
        b = a[c][:-1]

        while b != "":
            d = b.split()
            self.act_item[d[0]] = d[1:]
            c += 1
            try:
                b = a[c][:-1]
            except IndexError:
                b = ''

    def pr(self):
        print(self.card)
        print(self.act_item)

    def pp(self):
        return self.card
    
    def act_list(self):
        return self.act_item
print(Card(1).act_list())