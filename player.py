import pygame
import random


class Player:
    def __init__(self, debug=False):
        self.dbg = debug
        if self.dbg:
            self.water_sources = 0
            self.water = 1000
            self.wood = 1000
            self.food = 1000
            self.minerals = 1000
            self.population = 0
            self.farms = 0
            self.mines = 0
            self.huts = 0
        else:
            self.water_sources = 1
            self.water = 10
            self.wood = 5
            self.food = 10
            self.minerals = 8
            self.population = 0
            self.farms = 1
            self.mines = 0
            self.huts = 0
