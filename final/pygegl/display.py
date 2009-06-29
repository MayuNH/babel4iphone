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
from Image import *
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
    #glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyEvent)
    glutMouseFunc(mouseEvent)
    
    init_gl()

def DrawGLScene():
    begin_draw()
    
    sc = scene.Scene()
    for obj in sc.objects:
        obj.draw()
    
    end_draw()
    
    glutSwapBuffers()

#def ReSizeGLScene(width, height):
#    glViewport(0, 0, width, height)
#    glMatrixMode(GL_PROJECTION)
#    glLoadIdentity()
#    glOrtho(0, width, 0, height, -1, 1)
#    glMatrixMode(GL_MODELVIEW)

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

def keyEvent(*args):
    if args[0] == ESCAPE:
        sys.exit()


from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL.EXT.framebuffer_object import *

glGenFramebuffersEXT = wrapper.wrapper(glGenFramebuffersEXT).setOutput(
    'framebuffers', 
    lambda x: (x,), 
    'n')

glGenRenderbuffersEXT = wrapper.wrapper(glGenRenderbuffersEXT).setOutput(
    'renderbuffers', 
    lambda x: (x,), 
    'n')

def mouseEvent(button, event, x, y):
    import texture
    #data = None
    
    image = open("mike.png")
    # convert to GL texture
    textureID = texture.Texture(image)
    
    # image dimensions
    size = image.size
    
    rboId = glGenRenderbuffersEXT(1)
    glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, int(rboId));
    glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT, GL_DEPTH_COMPONENT,
                             int(size[0]), int(size[1]));
    glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, 0)
    
    fboId = glGenFramebuffersEXT(1)
    glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, int(fboId))
    
    glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT,
                              GL_TEXTURE_2D, textureID, 0)
    
    glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT, GL_DEPTH_ATTACHMENT_EXT,
                                 GL_RENDERBUFFER_EXT, int(rboId))
    
    status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)
    print status == GL_FRAMEBUFFER_COMPLETE_EXT
    glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)
    
    # render
    glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, int(fboId))
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    dl = glGenLists(1)
    glNewList(dl, GL_COMPILE)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glBegin(GL_QUADS)
    glTexCoord2i(0, 0); glVertex3f(-size[0] / 2.0, -size[0] / 2.0, 0)
    glTexCoord2i(1, 0); glVertex3f( size[0] / 2.0, -size[0] / 2.0, 0)
    glTexCoord2i(1, 1); glVertex3f( size[0] / 2.0,  size[0] / 2.0, 0)
    glTexCoord2i(0, 1); glVertex3f(-size[0] / 2.0,  size[0] / 2.0, 0)
    glEnd()
    #glBindTexture(GL_TEXTURE_2D, textureID)
    glEndList()
    
    glPushMatrix()
    glTranslatef(x, 600-y, 0)
    glColor4f(255,255,255,255)
    glRotatef(0, 0, 0, 1)
    glScalef(1, 1, 1)
    glCallList(dl)
    glPopMatrix()
    
    glutSwapBuffers()
    
    glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glGenerateMipmapEXT(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)
    
    data = glReadPixels(x, 600-y, 1, 1, GL_RGBA, GL_UNSIGNED_INT)
    #data = glReadPixelSub(x, 600-y, 1, 1, GL_RGBA, GL_UNSIGNED_INT)
    
    print data

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
