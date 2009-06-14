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

from singleton import Singleton
from scene import Scene

import sys

ESCAPE = '\033'

def init(width = 800, height = 600):
    Display(width, height)

def set_caption(caption):
    glutSetWindowTitle(caption)

def get_size():
    return [glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)]

def mainLoop():
    glutMainLoop()


class Display(Singleton):
    
    def initialize(self, width = 800, height = 600):
        self.__scene = Scene()
        
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        # the window starts at the upper left corner of the screen 
        glutInitWindowPosition(width / 4, height / 4)
        glutCreateWindow("Test")
        
        glutDisplayFunc(self.__DrawGLScene)
        #glutFullScreen()
        glutIdleFunc(self.__DrawGLScene)
        glutReshapeFunc(self.__ReSizeGLScene)
        glutKeyboardFunc(self.__keyPressed)
        
        # Initialize our window. 
        self.__InitGL(width, height)
    
    def __InitGL(self, width, height):
        glEnable(GL_TEXTURE_2D)
        
        # This Will Clear The Background Color To Black
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glClearDepth(1.0)	  # Enables Clearing Of The Depth Buffer
        
        glDepthFunc(GL_LESS)      # The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)   # Enables Depth Testing
        
        glShadeModel(GL_SMOOTH)   # Enables Smooth Color Shading
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA);
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glEnable(GL_BLEND)        # mio
        
        #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        #glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        
        glAlphaFunc(GL_NOTEQUAL, 0.0)
        glEnable(GL_ALPHA_TEST)
        
        #glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()          # Reset The Projection Matrix
        gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    
    def __ReSizeGLScene(self, width, height):
        if height == 0:  # Prevent A Divide By Zero If The Window Is Too Small 
            height = 1
        # Reset The Current Viewport And Perspective Transformation
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def __DrawGLScene(self):
        # Clear The Screen And The Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        for obj in self.__scene.objects:
            obj.draw()
        
        # since this is double buffered, swap the buffers to display 
        # what just got drawn.
        glutSwapBuffers()
    
    def __keyPressed(self, *args):
        if args[0] == ESCAPE:
            sys.exit()
