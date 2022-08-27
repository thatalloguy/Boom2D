from boom2d import *


window = Window((1280,720),(600,400))

world = World(window)
player = Player(world,(0,200),(24,24),"images/creature-3.png")
Block(world,1,"images/dirt_tile.png")
Block(world,2,"images/grass_tile.png")
Block(world,3,"images/grass.png")
while True:
    window.handle_loop()
    world.render()
    player.update()

    window.update()
