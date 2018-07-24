from math import gcd
import threading
import json


class PointGenerator(threading.Thread):
    def load(self):
        try:
            self.data = json.load(open('steinhaus.json'))
        except FileNotFoundError:
            self.data = {'found': {}}

    def __init__(self, vis):
        super().__init__()
        self.bot = 1
        self.top = 100
        self.data = {'found': {}}
        self.vis = vis

    def save(self):
        json.dump(self.data, open('steinhaus.json', 'w'))

    def run(self):
        self.load()
        delta = self.top - self.bot
        for a in range(self.bot, self.top):
            apercent = ((a-self.bot) / delta) * 100
            #print(apercent)
            for b in range(self.bot, self.top):
                bpercent = ((b-self.bot) / delta) * 100
                for c in range(self.bot, self.top):
                    cpercent = ((c-self.bot) / delta) * 100
                    print(f'a={apercent}% b={bpercent}% c={cpercent}%   ')
                    for l in range(self.bot, self.top):
                        asq = a * a
                        bsq = b * b
                        csq = c * c
                        lsq = l * l
                        if asq * asq + bsq * bsq + csq * csq + lsq * lsq == asq * bsq + asq * csq + asq * lsq + bsq * csq + bsq * lsq + csq * lsq:
                            newval = ' '.join([str(i) for i in sorted([a, b, c, l])])
                            if newval not in self.data['found'] and gcd(a, gcd(b, gcd(c, l))) != 1:
                                self.vis.add_tuple(newval)
                                self.save()
