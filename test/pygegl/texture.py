#PyGL2D - A 2D library for PyGame and PyOpenGL
#Copyright (C) 2008 - PyMike

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

def Texture(surface, filters):
    texture = glGenTextures(1)
    Data = pygame.image.tostring(surface, "RGBA", 1)
    
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 
                 0, 
                 GL_RGBA,
                 surface.get_width(), 
                 surface.get_height(),
                 0,
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 Data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    
    if filters == None:
        return texture
    
    for f in filters:
        if f == "filter":
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        elif f == "wrap":
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        elif f == "mipmap":
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            gluBuild2DMipmaps(GL_TEXTURE_2D,
                              3,
                              surface.get_width(),
                              surface.get_height(),
                              GL_RGB,
                              GL_UNSIGNED_BYTE,
                              Data)
            if "filter" in filters:
                glTexParameterf(GL_TEXTURE_2D, 
                                GL_TEXTURE_MIN_FILTER, 
                                GL_LINEAR_MIPMAP_LINEAR)
                glTexParameterf(GL_TEXTURE_2D, 
                                GL_TEXTURE_MAG_FILTER, 
                                GL_LINEAR)
            else:
                glTexParameterf(GL_TEXTURE_2D, 
                                GL_TEXTURE_MIN_FILTER, 
                                GL_LINEAR_MIPMAP_NEAREST)
                glTexParameterf(GL_TEXTURE_2D, 
                                GL_TEXTURE_MAG_FILTER, 
                                GL_NEAREST)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    return texture
