import random
import pygame, sys
from pygame.locals import *
pygame.init() #bri'ish

class Window:
    def __init__(self,
                 WINDOW_SIZE,
                 RESOLUTION,
                 title="A Boom2D Window",
                 icon="boom2d/images/bugger.png",
                 bg=(146,244,255),
                 fps_cap=60):

        # Window
        self.window_size= WINDOW_SIZE
        self.resolution = RESOLUTION
        self.title = title
        self.icon = icon
        self.bg = bg
        self.fps_cap = fps_cap
        self.screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
        self.display = pygame.Surface(self.resolution)
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(pygame.image.load(self.icon))
        self.clock = pygame.time.Clock()

    def handle_loop(self):
        self.display.fill(self.bg)
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    def update(self):
        surf = pygame.transform.scale(self.display, self.window_size)
        self.screen.blit(surf, (0, 0))
        pygame.display.update()  # update display
        self.clock.tick(self.fps_cap)  # maintain 60 fps
