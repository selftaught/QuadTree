#!/usr/bin/env python3

import pygame
import random

from src.helpers import drawRectBorder
from src.point import Point
from src.quadtree import QuadTree
from pygame import Rect, gfxdraw
from pygame.locals import MOUSEBUTTONUP


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("QuadTree")

        self._clock = pygame.time.Clock()
        self._fps = 30
        self._rect = Rect(0, 0, 1200, 800)
        self._running = True
        self._screen = pygame.display.set_mode([self._rect.w, self._rect.h])
        self._points = []
        self._quadtree = QuadTree(self._rect, 4)

        for i in range(20):
            point = Point(
                random.randrange(0, self._rect.w),
                random.randrange(0, self._rect.h),
            )
            self._points.append(point)
            self._quadtree.insert(point)

    def draw(self) -> None:
        self._screen.fill((0, 0, 0))
        for p in self._points:
            gfxdraw.pixel(self._screen, p.x, p.y, (255, 255, 255))

        (mX, mY) = pygame.mouse.get_pos()
        searchArea = Rect(mX - 100, mY - 100, 200, 200)
        found = self._quadtree.query(searchArea)
        drawRectBorder(self._screen, searchArea, (0, 255, 0))
        print(len(found))

        self._quadtree.draw(self._screen)

        pygame.display.update()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                (mX, mY) = pygame.mouse.get_pos()
                point = Point(mX, mY)
                self._points.append(point)
                self._quadtree.insert(point)

    def loop(self) -> None:
        while self._running:
            self.event_loop()
            self.update()
            self.draw()
            self._clock.tick(self._fps)
        pygame.quit()

    def update(self) -> None:
        pass


Game().loop()
pygame.quit()
