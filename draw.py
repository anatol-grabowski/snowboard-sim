from OpenGL.GL import *
from shape import Body

def map_xy(x, y, src, trg):
    sx = (world[2] - world[0]) / (screen[2] - screen[0])
    sy = (world[3] - world[1]) / (screen[3] - screen[1])
    scale = sx, sy
    x = trg[0] + (x - src[0]) * scale[0]
    y = trg[1] + (y - src[1]) * scale[1]
    return [x, y]

screen = 0, 0, 800, 600
aspect_ratio = screen[2] / screen[3]
scale = 6
world = -scale*aspect_ratio/2, scale/2, scale*aspect_ratio/2, -scale/2
def screen_to_world(x, y): return map_xy(x, y, screen, world)
def world_to_screen(x, y): return map_xy(x, y, world, screen)

def draw_body(body):
    glBegin(GL_LINE_LOOP)
    for p in body.points:
        glVertex2fv(p)
    glEnd()
    glBegin(GL_LINES)
    glVertex2fv(body.loc)
    glVertex2fv(body.loc + body.force/100000)
    glEnd()
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2fv(body.loc)
    glEnd()

Body.draw = draw_body
