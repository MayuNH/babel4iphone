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

import pygame
from pygame.locals import *

import surface

class gobj(object):
    
    def __init__(self, file_name, pos):
        self.image = surface.load(file_name)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.is_picked = False
        self.is_movable = False
        self.is_showed = True
        
        # auto aggiunta dell'oggetto alla scena
        #from scene import scene
        #self.scene = scene()
        #self.scene.objects.append(self)
    
    #def get_distance(self, pos):
    #    rect = self.image.get_rect()
    #    p = rect.center
    #    return round(math.sqrt((p[0] - pos[0])**2 + (p[1] - pos[1])**2))
    
    def is_hit(self, pos):
        if self.is_showed and self.rect.collidepoint(pos):
            x = pos[0] - self.rect.left
            y = pos[1] - self.rect.top
            col = self.image.get_at((int(x), int(y)))
            #print col
            if len(col) == 4 and col[3] < 255:
                return False
            else:
                return True
        return False
    
    def MouseMove(self, rel):
        if self.is_showed and self.is_movable:
            self.rect.x += rel[0]
            self.rect.y += rel[1]
