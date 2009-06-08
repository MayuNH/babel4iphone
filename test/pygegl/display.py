from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import sys, os

def init(screen_size = [800, 600], flags = DOUBLEBUF):
    pygame.init()
    set_caption("pygegl window")
    pygame.display.set_mode(screen_size, flags | OPENGL)
    init_gl()

def set_caption(caption):
    pygame.display.set_caption(caption)

def refresh():
    pygame.display.flip()

def get_size():
    return pygame.display.get_surface().get_size()

def begin_draw():
    screen_size = get_size()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    enable2D((0, screen_size[0], 0, screen_size[1]))

def end_draw():
    disable2D()

def init_gl():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glEnable(GL_TEXTURE_2D)
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_ALPHA_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glAlphaFunc(GL_NOTEQUAL, 0.0)

def enable2D(rect):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(rect[0], rect[0] + rect[1], rect[2], rect[2] + rect[3], -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

def disable2D():
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
