#!/usr/bin/env python3

import pygame

from pygame import Rect, gfxdraw, draw
from pygame.locals import MOUSEBUTTONUP
from random import randint

from src.helpers import draw_rect_border
from src.point import Point
from src.quadtree import QuadTree

RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Point Quadtree")

        self._clock = pygame.time.Clock()
        self._fps = 30
        self._rect = Rect(0, 0, 1200, 800)
        self._running = True
        self._screen = pygame.display.set_mode([self._rect.w, self._rect.h])
        self._points = []
        self._qtree = QuadTree(self._rect, 4)

        for i in range(200):
            point = Point(randint(0, self._rect.w), randint(0, self._rect.h))
            self._points.append(point)
            self._qtree.insert(point)

    def draw(self) -> None:
        self._screen.fill((0, 0, 0))
        for p in self._points:
            gfxdraw.pixel(self._screen, p.x, p.y, RED)

        (mX, mY) = pygame.mouse.get_pos()
        search_area = Rect(mX - 100, mY - 100, 200, 200)
        found = self._qtree.query(search_area)
        draw_rect_border(self._screen, search_area, GREEN)

        for point in found:
            draw.circle(self._screen, GREEN, (point.x, point.y), 3)

        self._qtree.draw(self._screen)

        pygame.display.update()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                (mX, mY) = pygame.mouse.get_pos()
                point = Point(mX, mY)
                self._points.append(point)
                self._qtree.insert(point)

    def loop(self) -> None:
        while self._running:
            self.event_loop()
            self.draw()
            self._clock.tick(self._fps)
        pygame.quit()


Game().loop()
pygame.quit()
