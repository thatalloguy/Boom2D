import random
import pygame, sys
from pygame.locals import *


class World:
    def __init__(self,window,AIR_SPACE=10,GRASS_LAYER=1):
        self.childs = []
        self.window = window
        self.display = window.display
        self.game_map = {}
        self.animation_database = {}
        self.CHUNK_SIZE = 8
        self.tile_index = {}
        self.tile_rects = []
        self.tile_rects_index = []
        self.TILE_SIZE = 32
        self.AIR_SPACE = AIR_SPACE
        self.GRASS_LAYER = GRASS_LAYER
        self.true_scroll = [0,0]
        self.player_rect = pygame.Rect(100,100,50,50)
        self.player_image = None
        self.player_flip = False

    def render(self):
        if self.player_image != None:
            self.true_scroll[0] += (self.player_rect.x - self.true_scroll[0] - self.window.resolution[0] / 2) / 20
            self.true_scroll[1] += (self.player_rect.y - self.true_scroll[1] - self.window.resolution[1] / 2) / 20
            scroll = self.true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            self.display.blit(pygame.transform.scale(pygame.transform.flip(self.player_image, self.player_flip, False), (24, 24)),
                         (self.player_rect.x - scroll[0], self.player_rect.y - scroll[1]))

            # World generation
            tile_rects = []
            for y in range(3):
                for x in range(4):
                    target_x = x - 1 + int(round(scroll[0] / (self.CHUNK_SIZE * self.TILE_SIZE)))
                    target_y = y - 1 + int(round(scroll[1] / (self.CHUNK_SIZE * self.TILE_SIZE)))
                    target_chunk = str(target_x) + ';' + str(target_y)
                    if target_chunk not in self.game_map:
                        self.game_map[target_chunk] = self.generate_chunk(target_x, target_y)
                    for tile in self.game_map[target_chunk]:
                        self.display.blit(self.tile_index[tile[1]],
                                     (tile[0][0] * self.TILE_SIZE - scroll[0], tile[0][1] * self.TILE_SIZE - scroll[1]))
                        if tile[1] in [1, 2]:
                            tile_rects.append(
                                pygame.Rect(tile[0][0] * self.TILE_SIZE, tile[0][1] * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))


        else:
            Exception("You Need an Player")
            sys.exit()

    def generate_chunk(self,x, y):
        chunk_data = []
        for y_pos in range(self.CHUNK_SIZE):
            for x_pos in range(self.CHUNK_SIZE):
                target_x = x * self.CHUNK_SIZE + x_pos
                target_y = y * self.CHUNK_SIZE + y_pos
                tile_type = 0
                if target_y > 10:
                    tile_type = 2  # grass
                elif target_y == 10:
                    tile_type = 1  # dirt
                elif target_y == 9:
                    if random.randint(1, 5) == 1:
                        tile_type = 3  # plant

                if tile_type != 0:
                    chunk_data.append([[target_x, target_y], tile_type])

        return chunk_data