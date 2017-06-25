import pygame
import math
blocks = []

__author__ = "adam_mcdaniel"

import pygame,sys,os,random,time,glob,math
from pygame.locals import *

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
cyan = (0,255,255)
grey = (90,90,90)
slate = (47,89,89)
silver = (200,200,200)
bblue = (0, 109, 160)

width = 800
height = 600
WIN_WIDTH = width
WIN_HEIGHT = height
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 1000

pygame.init()
"""

[1,1,1]
[ , , ]
[ ,R, ]

"""

screen = pygame.display.set_mode(DISPLAY,FLAGS, DEPTH)

class Block():
    def __init__(self,x,y,width=32,depth=32,height=32,color=(220,150,150)):
        global blocks
        blocks.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.depth = depth
        self.height = height
        self.color = color


class Camera():
    def __init__(self,x,y,angle,screen):
        self.angle = angle
        self.angle_change = 0
        self.velocity = 0
        self.x = x
        self.y = y
        self.draw_list = []
        self.screen = screen

    def detect(self):
        self.draw_list = []
        for ray_angle in range(-20,20):
            ray_angle*=2
            ray_angle+=self.angle
            if ray_angle > 360:
                ray_angle += -360
            if ray_angle < 0:
                ray_angle += 360
            r = Ray(ray_angle, self.x, self.y)
            self.draw_list.append(r.return_distance())
            

    def draw(self):
        self.screen.fill((0,0,0))
        pygame.draw.rect(screen,pygame.Color("#EEEEEE"),(0,300,800,600))
        pygame.draw.rect(screen,pygame.Color("#999999"),(0,0,800,300))
        y = 0
        for x in self.draw_list:
            draw_size = 24
            y += draw_size
            if type(x[0])==int:
                pygame.draw.line(self.screen,x[2],(y,(500-x[0])),(y,(50+x[0])),draw_size)
            else:
                pass
            
    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                self.angle_change = -8
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                self.angle_change = 8
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                self.angle_change = 0
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                self.angle_change = 0
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                self.velocity = -6
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                self.velocity = 6
            if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                self.velocity = 0
            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                self.velocity = 0
                
        self.x+=self.velocity*math.cos(math.radians(abs(self.angle)))
        self.y+=self.velocity*math.sin(math.radians(abs(self.angle)))
        self.angle += self.angle_change

        if self.angle > 360:
            self.angle += -360
        if self.angle < 0:
            self.angle += 360
            
        self.detect()
        self.draw()




class Ray():
    def __init__(self, angle, x, y):
        self.angle = angle
        self.x = x
        self.y = y
        self.distance = self.return_distance()

    def return_distance(self):
        list_of_distances = []
        block_type = None
        block_height = 0
        block_color = ()
        for block in blocks:
            # print(self.x+distance*math.sin(math.radians(abs(self.angle))))
            # print(self.y+distance*math.cos(math.radians(abs(self.angle))))
            for distance in range(180):
                if self.x+distance*math.cos(math.radians(abs(self.angle))) >= block.x and self.x+distance*math.cos(math.radians(abs(self.angle))) <= (block.x + block.width):
                    if self.y+distance*math.sin(math.radians(abs(self.angle))) >= block.y and self.y+distance*math.sin(math.radians(abs(self.angle))) <= (block.y + block.depth):
                        list_of_distances.append(distance)
                        block_type = type(block)
                        block_height = block.height
                        block_color = block.color
                        break
                    
        if len(list_of_distances)>0:
            list_of_distances.sort()
            return (list_of_distances[0],block_height,block_color)
        else:
            return (None,None)
        
def build():
    game_map = [[2,0,0,0,3,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [1,0,0,0,2,0],
                [0,0,0,0,0,0]]

    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            # print(item)
            if game_map[y][x]== 1:
                # print("x:"+str(x*64)+" y:"+str(y*64))
                b = Block(x*32,y*32,32,32,32,(220,150,150))
            if game_map[y][x]== 2:
                # print("x:"+str(x*64)+" y:"+str(y*64))
                b = Block(x*32,y*32,32,32,32,(150,150,220))
            if game_map[y][x]== 3:
                # print("x:"+str(x*64)+" y:"+str(y*64))
                b = Block(x*32,y*32,32,32,32,(220,220,150))

def main():
    global blocks,screen
    camera = Camera(72,72,270,screen)
    pygame.display.set_caption("3D Attempt")
    build()
    timer = pygame.time.Clock()
    timer.tick(60)
    while True:
        start = time.time()
        
        pygame.draw.rect(screen,(200,200,200),(0,300,800,600))
        camera.update()
        pygame.display.update()
        
        time_taken = time.time() - start
        fps = 1. / time_taken
        pygame.display.set_caption(str(fps))

if __name__ == "__main__":
    main()
