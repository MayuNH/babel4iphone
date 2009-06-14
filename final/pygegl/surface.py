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
from Image import *

import texture, display

def load(filename):
    return Surface(filename)


class Surface(object):
    
    def __init__(self, filename):
        image = open(filename)
        # convert to GL texture
        self.texture = texture.Texture(image)
        
        # image dimensions
        self.size = image.size
        self.width = self.w = self.size[0]
        self.height = self.h = self.size[1]
        self.win_size = display.get_size()
        
        # image mods
        self.rotation = 0
        self.scalar = 1.0
        self.color = [1.0, 1.0, 1.0, 1.0]
        self.cx, self.cy = self.w / 2, self.h / 2
        
        # setting GL
        self.dl = glGenLists(1)
        glNewList(self.dl, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        
        glBegin(GL_QUADS)
        glTexCoord2i(0, 0); glVertex3f(-self.w / 2.0, -self.h / 2.0, 0)
        glTexCoord2i(1, 0); glVertex3f( self.w / 2.0, -self.h / 2.0, 0)
        glTexCoord2i(1, 1); glVertex3f( self.w / 2.0,  self.h / 2.0, 0)
        glTexCoord2i(0, 1); glVertex3f(-self.w / 2.0,  self.h / 2.0, 0)
        glEnd()
        
        glEndList()
    
    def delete(self):
        glRemoveTextures([self.texture])
        del self
   
    def scale(self, scale):
        self.scalar = scale
    
    def rotate(self, rotation):
        self.rotation = rotation
    
    def colorize(self, R, G, B, A):
        self.color = (R / 255.0, G / 255.0, B / 255.0, A / 255.0)
    
    def get_width(self):
        return self.w * self.scalar
    
    def get_height(self):
        return self.h * self.scalar
    
    def draw(self, pos):
        glPushMatrix()
        
        glTranslatef(pos[0] + self.cx, self.win_size[1] - pos[1] - self.cy, 0)
        glColor4f(*self.color)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.scalar, self.scalar, 1)
        
        glCallList(self.dl)
        glPopMatrix()
