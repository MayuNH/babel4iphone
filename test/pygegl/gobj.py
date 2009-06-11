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
        self.surface = surface.load(file_name, pos)
        self.__rect = self.surface.get_rect() # ref to rect image
        
        self.is_picked = False
        self.is_movable = False
        self.is_showed = True
        
    #def get_distance(self, pos):
    #    p = self.__rect.center
    #    return round(math.sqrt((p[0] - pos[0])**2 + (p[1] - pos[1])**2))
    
    def is_hit(self, pos):
        if self.is_showed and self.__rect.collidepoint(pos):
            x = pos[0] - self.__rect.x
            y = pos[1] - self.__rect.y
            #col = self.surface.get_at((int(x), int(y)))
            #print col
            #if len(col) == 4 and col[3] < 255:
            #    return False
            #else:
            return True
        return False
    
#     def MouseMove(self, rel):
#         if self.is_showed and self.is_movable:
#             self.__rect.x += rel[0] da mettere move_ip
#             self.__rect.y += rel[1]
