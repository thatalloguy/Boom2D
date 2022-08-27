import random

import pygame, sys
from pydualsense import *
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())
# get dualsense instance
dualsense = pydualsense()
dualsense.init()
dualsense.light.setColorI(255,0,0)



dualsense.audio.setMicrophoneState(True)
clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('boom 2D Test')
icon = pygame.image.load('images/bugger.png')
pygame.display.set_icon(icon)
WINDOW_SIZE = (1280,720)

screen = pygame.display.set_mode(WINDOW_SIZE)#,pygame.FULLSCREEN)
RESOLUTION = (600,400)
display = pygame.Surface(RESOLUTION)


grass_image = pygame.image.load('images/dirt_tile.png')
TILE_SIZE = grass_image.get_width()

dirt_image = pygame.image.load('images/grass_tile.png')
grass_grass_image = pygame.image.load('images/grass.png')
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
walk_sound = pygame.mixer.Sound('sounds/walk.wav')
land_sound = pygame.mixer.Sound('sounds/land.wav')

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

true_scroll = [0,0]

tile_index = {1:grass_image,2:dirt_image,3:grass_grass_image}

def load_map(path):
    f = open(path + ".txt")
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

CHUNK_SIZE = 8

def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0
            if target_y  > 10:
                tile_type = 2 # grass
            elif target_y == 10:
                tile_type = 1 # dirt
            elif target_y == 9:
                if random.randint(1,5) == 1:
                    tile_type = 3 # plant

            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])

    return chunk_data




global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

animation_database = {}

animation_database['run'] = load_animation('images/walk',[7,7,7,7])
animation_database['idle'] = load_animation('images/walk',[1])

game_map = {}

player_action = 'run'
player_frame = 0
player_flip = False

screenshake = 0

landed = True

player_rect = pygame.Rect(100,100,50,50)
motion = [0,0]
test_rect = pygame.Rect(100,100,100,50)
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
while True: #  game loop

    display.fill((146,244,255))

    true_scroll[0] += (player_rect.x - true_scroll[0]-RESOLUTION[0] / 2)/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - RESOLUTION[1] / 2)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(204, 0, 255),obj_rect)
        else:
            pygame.draw.rect(display, (102, 0, 102), obj_rect)
    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*TILE_SIZE)))
            target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * TILE_SIZE)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x,target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]],(tile[0][0]*TILE_SIZE-scroll[0],tile[0][1]*TILE_SIZE-scroll[1]))
                if tile[1] in [1,2]:
                    tile_rects.append(pygame.Rect(tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))

    player_movement = [0, 0]

    if moving_right:
        player_movement[0] += 4

    if moving_left:
        player_movement[0] -= 4
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_movement[0] > 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = False

        dualsense.setLeftMotor(5)


    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')

    if player_movement[0] < 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = True
        dualsense.setRightMotor(5)

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
        #landed = False
        if not landed:
            land_sound.play()
            dualsense.setLeftMotor(100)
            dualsense.setRightMotor(100)
            screenshake = 60
            landed = True
    else:

        air_timer += 1


    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    #print(animation_frames)
    player_img_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_img_id]
    display.blit(pygame.transform.scale(pygame.transform.flip(player_image,player_flip,False),(150,150)), (player_rect.x-scroll[0], player_rect.y-scroll[1]))
    player_rect.width = pygame.transform.scale(pygame.transform.flip(player_image,player_flip,False),(150,150)).get_width()
    player_rect.height = pygame.transform.scale(pygame.transform.flip(player_image,player_flip,False),(150,150)).get_height()
    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            dualsense.close()
            pygame.quit() # stop pygame
            sys.exit() # stop script
            exit()
            quit()

        if event.type == pygame.JOYAXISMOTION:
            if event.axis < 2:
                motion[event.axis] = event.value


        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                if air_timer < 6:
                    jump_sound.play()
                    landed = False
                    player_y_momentum = -6

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    landed = False
                    player_y_momentum = -6

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

        if motion[0] >= 1:
            moving_right = True
        else:
            moving_right = False


        if motion[0] < 0:
            moving_left = True
        else:
            moving_left = False





    if screenshake > 0:
        screenshake -= 1
    else:
        dualsense.setLeftMotor(0)
        dualsense.setRightMotor(0)
    render_offset = [0,0]
    screenshake_intensity = 20
    if screenshake:
        render_offset[0] = random.randint(0, screenshake_intensity) - 4
        render_offset[1] = random.randint(0, screenshake_intensity) - 4

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, render_offset)
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps

