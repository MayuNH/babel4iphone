# pygegl
#
# Copyright (C) 2009 Giovanni Amati <amatig@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import scene, sys

SCREEN_SIZE = [800, 600]
ESCAPE = '\033'

def init(width, height):
    global SCREEN_SIZE
    SCREEN_SIZE = [width, height]
    
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    
    glutInitWindowPosition(width / 4, height / 4)
    glutCreateWindow("Example")
    
    glutDisplayFunc(DrawGLScene)
    #glutFullScreen()
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    
    init_gl()

def DrawGLScene():
    begin_draw()
    
    sc = scene.Scene()
    for obj in sc.objects:
        obj.draw()
    
    end_draw()
    
    glutSwapBuffers()

def ReSizeGLScene(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def begin_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    enable2D([0, SCREEN_SIZE[0], 0, SCREEN_SIZE[1]])

def end_draw():
    disable2D()

def get_window_size():
    return [glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)]

def get_size():
    return SCREEN_SIZE

def set_caption(caption):
    glutSetWindowTitle(caption)

def mainLoop():
    glutMainLoop()

def keyPressed(*args):
    if args[0] == ESCAPE:
        sys.exit()


# Internal from pygl2d

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
