import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time
from shape import Polygon

class Player():
    def __init__(self):
        self.m = 100
        self.friction_l = 0.01
        self.loc = np.zeros(2)
        self.vel = np.zeros(2)
        self.acc = np.zeros(2)
        self.board = Polygon([[-1, -0.3],
                            [1, -0.3],
                            [1, 0.3],
                            [-1, 0.3]])
        self.m_board = 20

    def draw(self):
        glBegin(GL_LINE_LOOP)
        for p in self.board.points:
            glVertex2fv(p)
        glEnd()
        glPushMatrix()
        # glTranslatef(*self.board.loc, 0)
        glBegin(GL_POINTS)
        glVertex2fv(self.loc)
        glEnd()
        glPopMatrix()

    def update(self):
        dt = 0.01
        self.board.update()
        
        

def draw():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    # glEnable(GL_POINT_SMOOTH)
    # glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPointSize(10)

    glBegin(GL_LINE_LOOP)
    glVertex3fv((1, 1, 0))
    glVertex3fv((-1, 1, 0))
    glVertex3fv((-1, -1, 0))
    glVertex3fv((1, -1, 0))
    glEnd()
    player.draw()
    pygame.display.flip()

def handle_input():
    x, y = pygame.mouse.get_pos()
    print(x, y)
    pos = screen_to_world(x, y)
    if player.board.contains(pos):
        player.loc = pos
    player.update()


def map_xy(x, y, src=(0, 0, 800, 600), trg=(-4/3, -1, 4/3, 1)):
    sx = (world[2] - world[0]) / (screen[2] - screen[0])
    sy = (world[3] - world[1]) / (screen[3] - screen[1])
    scale = sx, sy
    x = trg[0] + (x - src[0]) * scale[0]
    y = trg[1] + (y - src[1]) * scale[1]
    return x, y

screen = 0, 0, 800, 600
world = -4, 3, 4, -3
def screen_to_world(x, y): return map_xy(x, y, screen, world)
def world_to_screen(x, y): return map_xy(x, y, world, screen)



def main():
    pygame.init()
    pygame.display.set_mode(screen[2:], DOUBLEBUF|OPENGL)

    gluOrtho2D(world[0], world[2], world[3], world[1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        handle_input()
        draw()
        pygame.time.wait(5)

player = Player()
player.board.rot = -0.3
player.board.loc = [1, 1]

main()
