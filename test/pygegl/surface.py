#PyGL2D - A 2D library for PyGame and PyOpenGL
#Copyright (C) 2008 - PyMike

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import rect, display, texture

def load(elem, pos = [0, 0], filters = ["filter"]):
    return Surface(elem, pos, filters)


class Surface(object):

    def __init__(self, elem, pos = [0, 0], filters = ["filter"]):
        if type(elem) is str:
            self.__surface = pygame.image.load(elem)
        else:
            # is a pygame.Surface
            self.__surface = elem
        
        # texturize GL
        self.__texture = texture.Texture(self.__surface, filters)
        
        # image dimensions. fixed value
        [self.__w, self.__h] = self.__surface.get_size()
        self.__win_size = display.get_size()
        
        # rect
        self.rect = rect.Rect(0, 0, self.__w, self.__h)
        self.rect.center = pos
        
        # image mods
        self.rotation = 0
        self.scalar = 1.0
        self.color = [1.0, 1.0, 1.0, 1.0]
        
        # setting GL
        self.__dl = glGenLists(1)
        glNewList(self.__dl, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.__texture)
        glBegin(GL_QUADS)
        glTexCoord2i(0, 0); glVertex3f(-self.__w / 2.0, -self.__h / 2.0, 0)
        glTexCoord2i(1, 0); glVertex3f( self.__w / 2.0, -self.__h / 2.0, 0)
        glTexCoord2i(1, 1); glVertex3f( self.__w / 2.0,  self.__h / 2.0, 0)
        glTexCoord2i(0, 1); glVertex3f(-self.__w / 2.0,  self.__h / 2.0, 0)
        glEnd()
        glEndList()
    
    #def get_at(self, pos):
    #    return self.__surface.get_at(pos) # ???
    
    def delete(self):
        glRemoveTextures([self.__texture])
        del self
    
    def scale(self, scale):
        new_w = self.__w * scale
        new_h = self.__h * scale
        
        # important!! this exec first resize rect
        self.rect.x = self.rect.centerx - new_w / 2
        self.rect.y = self.rect.centery - new_h / 2
        # rect scale
        self.rect.w = new_w
        self.rect.h = new_h
        
        # value for draw gl scale
        self.scalar = scale
    
    def rotate(self, rotation):
        self.rotation = rotation
    
    def colorize(self, R, G, B, A):
        self.color = [R / 255.0, G / 255.0, B / 255.0, A / 255.0]
    
    def get_width(self):
        return self.__w * self.scalar
    
    def get_height(self):
        return self.__h * self.scalar
    
    def get_rect(self):
        return self.rect
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.rect.x + self.rect.w / 2, 
                     self.__win_size[1] - self.rect.y - self.rect.h / 2,
                     0)
        glColor4f(*self.color)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.scalar, self.scalar, 1)
        glCallList(self.__dl)
        glPopMatrix()
