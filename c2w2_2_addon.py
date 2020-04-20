# В этом задании вам необходимо сделать рефакторинг уже реализованной программы - заставки для скринсейвера.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Polyline(object):
    

    def __init__(self, points=None, speeds=None):
        self.points = points or []
        self.speeds = speeds or []

    def append(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p].x = - self.speeds[p].x
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p].y = -self.speeds[p].y

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color,
                                (int(self.points[p_n].x), int(self.points[p_n].y)),
                                (int(self.points[p_n + 1].x), int(self.points[p_n + 1].y)), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color,
                                (int(p.x), int(p.y)), width)

    def delete_point(self):
        if len(self.points) > 0:
            self.points.pop(-1)
            self.speeds.pop(-1)

    def speed_up(self, k=1.1):
        if k == 0:
            k = 1
        self.speeds = [x*k for x in self.speeds]
    
    def speed_down(self, k=1.1):
        if k == 0:
            k = 1
        self.speeds = [x*(1/k) for x in self.speeds]


class Vec2d(object):
    
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)
    
    def __mul__(self, k):
        return Vec2d(self.x * k, self.y * k)
    
    def len(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def int_pair(self):
        return(self.x, self.y)


class Knot(Polyline):

    def __init__(self, points=None, count=0):
        self.points = points or []
        self.count = count

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return ((points[deg] * alpha) + (self.get_point(points, alpha, deg - 1)*(1 - alpha)))

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append(((self.points[i] + self.points[i + 1]) * 0.5))
            ptn.append(self.points[i + 1])
            ptn.append(((self.points[i + 1] + self.points[i + 2]) * 0.5))

            res.extend(self.get_points(ptn))
        return res

# =======================================================================================
# Отрисовка меню
# =======================================================================================

def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["D", "Delete points"])
    data.append(["UP", "Increase speed"])
    data.append(["DOWN", "Decrease speed"])
    data.append(["A", "Append new curve"])
    data.append(["RIGHT", "Next curve"])
    data.append(["LEFT", "Previous curve"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))
# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True

    # инициализация
    polyline_list = []
    polyline_list.append(Polyline())
    line_number = 0
    current_line_number = 0

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                        polyline_list = []
                        polyline_list.append(Polyline())
                        line_number = 0
                        current_line_number = 0
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_EQUALS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_MINUS:
                    steps -= 1 if steps > 1 else 0
                # удалить точку
                if event.key == pygame.K_d:
                    polyline_list[current_line_number].delete_point()
                # увкеличить скорость
                if event.key == pygame.K_UP:
                    polyline_list[current_line_number].speed_up()
                # уменьшить скорость
                if event.key == pygame.K_DOWN:
                    polyline_list[current_line_number].speed_down()
                # добавить кривую
                if event.key == pygame.K_a:
                    polyline_list.append(Polyline())
                    line_number += 1
                    current_line_number = len(polyline_list) - 1
                # переключение между кривыми
                if event.key == pygame.K_RIGHT:
                    if current_line_number < line_number:
                        current_line_number += 1
                if event.key == pygame.K_LEFT:
                    if current_line_number > 0:
                        current_line_number -= 1
            # добавить точку в активную кривую
            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline_list[current_line_number].append(Vec2d(event.pos[0], event.pos[1]),
                                Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        
        for polyline in polyline_list:
            # отрисовка опорных точек
            polyline.draw_points()   
            # инициализация
            knot = Knot(polyline.points, steps)
            # расчет точек кривой
            curve_points = knot.get_knot()
            Polyline(curve_points).draw_points("line", 3, color)
        
            if not pause:
                # переместить точки
                polyline.set_points()

        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
