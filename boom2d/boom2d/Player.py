import random
import pygame, sys
from pygame.locals import *







class Player:
    def __init__(self,world,position,size,image,use_preset_movement=True):
        self.world = world
        self.x = position[0]
        self.y = position[1]
        self.width = size[0]
        self.height = size[1]
        self.image = pygame.transform.scale(pygame.image.load(image), (self.width,self.height))
        self.world.player_image = self.image
        self.world.player_rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.movementer_use = use_preset_movement
        self.moving_right = False
        self.moving_left = False

        self.player_y_momentum = 0
        self.air_timer = 0

    def update(self):
        self.player_movement = [0, 0]

        self.events = self.world.window.events
        if self.moving_right:
            self.player_movement[0] += 4

        if self.moving_left:
            self.player_movement[0] -= 4
        self.player_movement[1] += self.player_y_momentum
        self.player_y_momentum += 0.2
        if self.player_y_momentum > 3:
            self.player_y_momentum = 3

        if self.player_movement[0] > 0:
            self.world.player_flip = False

        if self.player_movement[0] < 0:
            self.world.player_flip = True

        self.world.player_rect, collisions = self.move(self.world.player_rect, self.player_movement,
                                                       self.world.tile_rects)

        if collisions['bottom']:
            self.player_y_momentum = 0
            self.air_timer = 0
            # landed = False
        else:
            self.air_timer += 1


    def collision_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, rect, movement, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types