import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time
from shape import Body
from draw import *

dt = 0.01
p0 = np.zeros(2)
c = 50000
k = 1500
k_fr = 0.3
g = 9.81
F_fr = 0
F_fr_no_reverse_limit = 0

w, h = 0.4, 0.4
inner = Body([[-w, -h], [w, -h], [w, h], [-w, h]], m=50)
w, h = 1.5, 0.5
outer = Body([[-w, -h], [w, -h], [w, h], [-w, h]], m=40)


def calc_forces():
    global F_fr, F_fr_no_reverse_limit
    F = -c * (inner.loc - p0) - k * inner.vel
    inner.force = F
    outer.force = -F

    N = g * (inner.m + outer.m)
    F_fr = k_fr * N * -outer.vel / (np.dot(outer.vel, outer.vel) ** 0.5)
    if np.dot(outer.vel, outer.vel) < 0.01:
        outer.vel = np.zeros_like(outer.vel)
        F_fr = k_fr * N * F / (np.dot(F, F) ** 0.5)
    F_fr_no_reverse_limit = outer.vel * outer.m / dt - outer.force
    F_fr_norm_sq = np.dot(F_fr, F_fr)
    F_fr_lim_norm_sq = np.dot(F_fr_no_reverse_limit, F_fr_no_reverse_limit)
    if np.dot(F_fr, F_fr_no_reverse_limit):
        if F_fr_norm_sq > F_fr_lim_norm_sq:
            F_fr = F_fr_no_reverse_limit
 
    outer.force += F_fr
    print(F_fr[0] * F_fr_no_reverse_limit[0] > 0)
    
    print(F_fr, F_fr_no_reverse_limit, 'v', outer.vel)
    print('vcomp', ((F_fr_no_reverse_limit - F) / outer.m * dt) - outer.vel)
    print(outer.force)


def handle_input():
    global p0, g
    if not hasattr(handle_input, 'prev_pos'):
        handle_input.prev_pos = pygame.mouse.get_pos()
        return
    keys = pygame.key.get_pressed()
    if keys[K_SPACE]: g = 9.81 / 500
    else:             g = 9.81
    print(g)
    pos = pygame.mouse.get_pos()
    p0 = screen_to_world(*pos)
    #p0[1] = 0
    calc_forces()
    inner.update(dt)
    outer.update(dt)
    handle_input.prev_pos = pos


def draw():
    screen = 0, 0, 800, 600
    aspect_ratio = screen[2] / screen[3]
    scale = 6
    world = -scale*aspect_ratio/2, scale/2, scale*aspect_ratio/2, -scale/2

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPointSize(5)

    glBegin(GL_POINTS)
    glVertex2fv(p0)
    glEnd()
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex2fv(outer.loc + [0, 0.03])
    glVertex2fv(outer.loc + F_fr / 100000 + [0, 0.03])
    glVertex2fv(outer.loc + [0, 0.06])
    glVertex2fv(outer.loc + F_fr_no_reverse_limit/ 100000 + [0, 0.06])
    glEnd()
    glColor3f(1, 1, 1)
    inner.draw()
    outer.draw()
    pygame.display.flip()


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
        pygame.time.wait(50)

main()
