import pygame
import random


class Tile:
    def __init__(self, img, img_rect, tile_name):
        self.img = img
        self.img_rect = img_rect
        self.tile_name = tile_name


class World:
    def __init__(self):
        self.data = [[random.randint(1, 200) for _ in range(8)] for _ in range(7)]
        self.tiles = []
        self.tile_size = 100
        desert_raw = pygame.image.load('img/desert_tile.jpg').convert_alpha()
        desert = pygame.transform.scale(desert_raw, (100, 100))
        oasis_raw = pygame.image.load('img/oasis_tile.jpg').convert_alpha()
        oasis = pygame.transform.scale(oasis_raw, (100, 100))
        mountain_raw = pygame.image.load('img/mountain_tile.jpg').convert_alpha()
        mountain = pygame.transform.scale(mountain_raw, (100, 100))
        row_count = 0
        for row in self.data:
            col_count = 0
            for tile in row:
                if tile in range(1, 188):
                    img = desert
                    img_rect = img.get_rect()
                    tile = Tile(img, img_rect, 'desert')
                    tile.img_rect.x = col_count * self.tile_size
                    tile.img_rect.y = row_count * self.tile_size
                    self.tiles.append(tile)
                if tile in range(188, 198):
                    img = mountain
                    img_rect = img.get_rect()
                    tile = Tile(img, img_rect, 'mountain')
                    tile.img_rect.x = col_count * self.tile_size
                    tile.img_rect.y = row_count * self.tile_size
                    self.tiles.append(tile)
                if tile in range(198, 201):
                    img = oasis
                    img_rect = img.get_rect()
                    tile = Tile(img, img_rect, 'oasis')
                    tile.img_rect.x = col_count * self.tile_size
                    tile.img_rect.y = row_count * self.tile_size
                    self.tiles.append(tile)
                col_count += 1
            row_count += 1

    def draw(self, s):
        for tile in self.tiles:
            s.blit(tile.img, tile.img_rect)
