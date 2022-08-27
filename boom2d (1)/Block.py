import random
import pygame, sys
from pygame.locals import *

class Block:
    def __init__(self,world,block_id,image,phyisical=True):
        self.world = world
        self.image = pygame.transform.scale(pygame.image.load(image),(self.world.TILE_SIZE,self.world.TILE_SIZE))
        self.physisical = phyisical
        if block_id not in self.world.tile_index:
            self.block_id = block_id
            self.world.tile_index[self.block_id] = self.image
            if self.physisical:
                self.world.tile_rects_index.append(self.block_id)
        else:
            Exception("Id already in use")