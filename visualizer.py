#!/usr/bin/python3
import pygame
import math

screen: pygame.Surface = None

scroll = [-392, -294]
zoom = [50, 50]
width = 800
height = 600
dirty = True
clock = pygame.time.Clock()

shape = [(0, 0), (1, 0), (0.5, math.sqrt(3) / 2)]
points = [(3, 3),(1,1),(2,2)]

axis_color = pygame.Color('black')
shape_color = pygame.Color('blue')
line_color = pygame.Color('green')
point_color = pygame.Color('red')


def init():
    global screen
    screen = pygame.display.set_mode((width, height))


def real_to_screen(coord: (float, float)) -> (int, int):
    x, y = coord
    y = -y
    x *= zoom[0]
    y *= zoom[1]
    x += ((width // 2) + scroll[0]) * zoom[0]
    y += ((height // 2) + scroll[1]) * zoom[1]
    return int(x), int(y)


def screen_to_real(coord: (int, int)) -> (float, float):
    x, y = coord
    x -= ((width // 2) + scroll[0]) * zoom[0]
    y -= ((height // 2) + scroll[1]) * zoom[1]
    x /= zoom[0]
    y /= zoom[1]
    y = -y
    return x, y


def draw():
    global dirty
    if dirty:
        line = pygame.draw.line
        screen.fill(pygame.Color(*[127] * 4))
        line(screen, axis_color, (int(((width // 2) + scroll[0]) * zoom[0]), 0),
             (int(((width // 2) + scroll[0]) * zoom[0]), height))
        line(screen, axis_color, (0, int(((height // 2) + scroll[1]) * zoom[1])),
             (width, int(((height // 2) + scroll[1]) * zoom[1])))
        for i in range(len(shape) - 1):
            line(screen, shape_color, real_to_screen(shape[i]), real_to_screen(shape[i + 1]))
        line(screen, shape_color, real_to_screen(shape[0]), real_to_screen(shape[-1]))
        for i in points:
            for j in shape:
                line(screen, line_color, real_to_screen(j), real_to_screen(i))
            pygame.draw.circle(screen, point_color, real_to_screen(i), 3)
        pygame.display.flip()
        clock.tick(60)
        dirty = False


def input():
    global zoom
    global dirty
    dirty = True
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            dirty = True
            if event.button == 4:  # up scroll wheel
                zoom = [i * 1.25 for i in zoom]
            elif event.button == 5:  # down scroll wheel
                zoom = [i / 1.25 for i in zoom]
            elif event.button == 1:  # left click
                pass # TODO: select node.
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[2]:
                dirty = True
                scroll[0] += event.rel[0] / zoom[0]
                scroll[1] += event.rel[1] / zoom[1]
                print(scroll, zoom)


if __name__ == '__main__':
    init()
    while 1:
        draw()
        input()
