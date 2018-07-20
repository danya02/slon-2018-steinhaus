#!/usr/bin/python3
import pygame
import math
import itertools
import generator


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

        self.axis_color = pygame.Color('black')
        self.shape_color = pygame.Color('blue')
        self.line_color = pygame.Color('green')
        self.point_color = pygame.Color('red')
        self.generator = None

    def run(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.generator = generator.PointGenerator()
        self.generator.callback = self.add_tuple
        self.generator.start()
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
            for i in self.targets:
                for j in self.shape:
                    for k in self.targets[i]:
                        line(self.screen, self.line_color, self.real_to_screen(j), self.real_to_screen(k))
            for j in self.targets:
                for i in self.targets[j]:
                    pygame.draw.circle(self.screen, self.point_color, self.real_to_screen(i), 3)
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
                    pass  # TODO: select node.
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[2]:
                    self.dirty = True
                    self.scroll[0] += event.rel[0] / self.zoom[0]
                    self.scroll[1] += event.rel[1] / self.zoom[1]

    def add_tuple(self, new_val):
        print(new_val)
        values = []
        for i in itertools.permutations(new_val):
            a, b, c, l = i
            a /= l
            b /= l
            c /= l
            l = 1
            x = -((b * b) - (a * a) - (l * l)) / (2 * l)
            y = ((a * a) + (l * l) + (b * b) - (2 * c * c)) / (2 * math.sqrt(3) * l)
            values.append([x, y])
        self.targets.update({new_val: values})

        self.dirty = True


if __name__ == '__main__':
    v = Visualiser()
    v.run()
