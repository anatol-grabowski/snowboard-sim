import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Player():
    def __init__(self):
        self.m = 100
        self.p = np.zeros(2)
        self.f = 0.0
        self.w = 0.3
        self.l = 0.8
        self.r = np.zeros(2)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.p[0], self.p[1], 0)
        glRotatef(np.rad2deg(self.f), 0, 0, 1)
        glPolygonMode(GL_FRONT, GL_LINE)
        glRectf(-self.l/2, -self.w/2, self.l/2, self.w/2)
        man_scale = 3
        glTranslatef(self.r[0], self.r[1], 0)
        glRectf(-self.l/2/man_scale, -self.w/2/man_scale, self.l/2/man_scale, self.w/2/man_scale)
        glPopMatrix()
        

def draw():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    # glEnable(GL_POINT_SMOOTH)
    # glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPointSize(5)

    glBegin(GL_LINE_LOOP)
    glVertex3fv((1, 1, 0))
    glVertex3fv((-1, 1, 0))
    glVertex3fv((-1, -1, 0))
    glVertex3fv((1, -1, 0))
    glEnd()
    player.draw()
    pygame.display.flip()

def handle_kb():
    pressed = pygame.key.get_pressed()
    speed = 0.01
    if pressed[pygame.K_LSHIFT]: speed *= 3
    if pressed[pygame.K_w]: player.r[1] += speed
    if pressed[pygame.K_s]: player.r[1] -= speed
    if pressed[pygame.K_a]: player.r[0] -= speed
    if pressed[pygame.K_d]: player.r[0] += speed
    board = np.array([player.l, player.w])
    player.r = np.clip(player.r, -board/2, board/2)

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    h = 3
    w = display[0] / display[1] * h
    gluOrtho2D(-w/2, w/2, -h/2, h/2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        handle_kb()
        draw()
        pygame.time.wait(10)

player = Player()
player.f = 0.3
player.p = [0.5, 0.2]
player.r = [0.4, 0.15]

main()
