from math import gcd
import threading
import json


class PointGenerator(threading.Thread):
    def load(self):
        try:
            self.found = json.load(open('steinhaus.json'))
        except FileNotFoundError:
            self.found = []

    def __init__(self):
        super().__init__()
        self.bot = 1
        self.top = 100
        self.found = []
        self.callback = lambda x: print('Callback: ', x)

    def run(self):
        # self.load()
        for i in self.found:
            self.callback(tuple(i))
        for a in range(self.bot, self.top):
            for b in range(self.bot, self.top):
                for c in range(self.bot, self.top):
                    for l in range(self.bot, self.top):
                        asq = a * a
                        bsq = b * b
                        csq = c * c
                        lsq = l * l
                        if asq * asq + bsq * bsq + csq * csq + lsq * lsq == asq * bsq + asq * csq + asq * lsq + bsq * csq + bsq * lsq + csq * lsq:
                            if sorted([a, b, c, l]) not in self.found and gcd(a, gcd(b, gcd(c, l))) != 1:
                                self.found += [sorted([a, b, c, l])]
                                self.callback(tuple(sorted((a, b, c, l))))
                                json.dump(self.found, open('steinhaus.json', 'w'))
