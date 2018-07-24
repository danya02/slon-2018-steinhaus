#!/usr/bin/python3
import pygame
import math
import itertools
import generator
import os


class Visualiser:
    def __init__(self):
        self.screen: pygame.Surface = None

        self.scroll = [-392, -294]
        self.zoom = [50, 50]
        self.width = 800
        self.height = 600
        self.dirty = True
        self.clock = pygame.time.Clock()

        self.shape = [(0, 0), (1, 0), (0.5, math.sqrt(3) / 2)]
        self.targets = {}
        self.colliders = []

        self.axis_color = pygame.Color('black')
        self.shape_color = pygame.Color('blue')
        self.pos_slope_color = pygame.Color('red')
        self.neg_slope_color = pygame.Color('blue')
        self.line_color = pygame.Color('green')
        self.circle_color = self.line_color
        self.point_color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (0, 0, 0)]
        self.point_color = [pygame.Color(*i) for i in self.point_color]
        self.file = 'steinhaus-input'
        self.generator = None

    def load_from_file(self):
        print(f'Loading tuples from {self.file}...')
        try:
            with open(self.file) as o:
                for i in o:
                    i = i.strip()
                    for j in self.generator.data['found']:
                        if j == i:
                            print(f'Tuple ({i}) already loaded!')
                            break
                    else:
                        print(f'Adding tuple ({i})...')
                        self.add_tuple(i)

        except FileNotFoundError:
            print(f'But file {self.file} wasn\'t found.')

    def run(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.generator = generator.PointGenerator(self)
        self.generator.callback = self.add_tuple
#        self.generator.start()
        self.load_from_file()
        while 1:
            self.draw()
            self.input()

    def real_to_screen(self, coord: (float, float)) -> (int, int):
        x, y = coord
        y = -y
        x *= self.zoom[0]
        y *= self.zoom[1]
        x += ((self.width // 2) + self.scroll[0]) * self.zoom[0]
        y += ((self.height // 2) + self.scroll[1]) * self.zoom[1]
        return int(x), int(y)

    def screen_to_real(self, coord: (int, int)) -> (float, float):
        x, y = coord
        x -= ((self.width // 2) + self.scroll[0]) * self.zoom[0]
        y -= ((self.height // 2) + self.scroll[1]) * self.zoom[1]
        x /= self.zoom[0]
        y /= self.zoom[1]
        y = -y

        return x, y


    def draw(self):
        if self.dirty:
            line = pygame.draw.line
            self.screen.fill(pygame.Color(*[127] * 4))
            line(self.screen, self.axis_color, (int(((self.width // 2) + self.scroll[0]) * self.zoom[0]), 0),
                 (int(((self.width // 2) + self.scroll[0]) * self.zoom[0]), self.height))
            line(self.screen, self.axis_color, (0, int(((self.height // 2) + self.scroll[1]) * self.zoom[1])),
                 (self.width, int(((self.height // 2) + self.scroll[1]) * self.zoom[1])))
            for i in range(len(self.shape) - 1):
                line(self.screen, self.shape_color, self.real_to_screen(self.shape[i]),
                     self.real_to_screen(self.shape[i + 1]))
            line(self.screen, self.shape_color, self.real_to_screen(self.shape[0]), self.real_to_screen(self.shape[-1]))
            ci = (100/self.zoom[0])*1000 # current infinity
            start_line = (-ci,0)
            end_line = (ci,0)
            start_pos = (-ci, -ci*math.sqrt(3))
            end_pos = (ci, ci*math.sqrt(3))
            start_neg = (-ci, math.sqrt(3)*ci+math.sqrt(3))
            end_neg = (ci, -math.sqrt(3)*ci+math.sqrt(3))
            start_pos = self.real_to_screen(start_pos)
            end_pos = self.real_to_screen(end_pos)
            start_neg = self.real_to_screen(start_neg)
            end_neg = self.real_to_screen(end_neg)
            line(self.screen,self.axis_color,start_line,end_line)
            line(self.screen,self.pos_slope_color,start_pos,end_pos)
            line(self.screen,self.neg_slope_color,start_neg,end_neg)
            try:
                pygame.draw.circle(self.screen, self.circle_color, self.real_to_screen((0.5, math.sqrt(3)/6)),int((math.sqrt(3)/3)*self.zoom[0]), 1)
            except ValueError:
                pass
            self.colliders = []
            for i in self.generator.data['found']:
                for j in self.generator.data['found'][i]:
                    pygame.draw.circle(self.screen, self.point_color[j[2]], self.real_to_screen((j[0], j[1])), 3)
                    cpoint = self.real_to_screen((j[0], j[1]))
                    target = (i, j)
                    self.colliders.append((cpoint, target))
            pygame.display.flip()
            self.clock.tick(60)
            self.dirty = False

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.dirty = True
                if event.button == 4:  # up self.scroll wheel
                    self.zoom = [i * 1.25 for i in self.zoom]
                elif event.button == 5:  # down self.scroll wheel
                    self.zoom = [i / 1.25 for i in self.zoom]
                elif event.button == 1:  # left click
                    for i in self.colliders:
                        crect = pygame.Rect(0, 0, 5, 5)
                        crect.center = i[0]
                        if crect.collidepoint(*event.pos):
                            target = self.generator.data['found'][i[1][0]]
                            target[target.index(i[1][1])][2] += 1
                            if target[target.index(i[1][1])][2] >= len(self.point_color):
                                target[target.index(i[1][1])][2] = 0
                            self.generator.save()
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[2]:
                    self.dirty = True
                    self.scroll[0] += event.rel[0] / self.zoom[0]
                    self.scroll[1] += event.rel[1] / self.zoom[1]

    def add_tuple(self, new_val):
        print(new_val)
        val = new_val.split(' ')
        val = [int(i) for i in val]
        values = []
        for i in itertools.permutations(val):
            a, b, c, l = i
            a /= l
            b /= l
            c /= l
            l = 1
            x = -((b * b) - (a * a) - (l * l)) / (2 * l)
            y = ((a * a) + (l * l) + (b * b) - (2 * c * c)) / (2 * math.sqrt(3) * l)
            values.append([x, y, 0])
        self.generator.data['found'].update({new_val: values})

        self.dirty = True


if __name__ == '__main__':
    v = Visualiser()
    v.run()
