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

import singleton, display, mainloop, event

def create(caption, screen_size, flags = DOUBLEBUF):
    return Scene(caption, screen_size, flags)


class Scene(singleton.Singleton):
    
    def initialize(self, caption, screen_size, flags = DOUBLEBUF):
        """Initialize"""
        self.objects = []
        self.want_quit = False  # for stop twisted reactor
        
        """Initialize EventManger"""
        self.eventManager = event.Event(self)
        
        """Initialize GL"""
        display.init(screen_size, flags)
        display.set_caption(caption)
    
    def addObject(self, obj):
        self.objects.append(obj)
    
    def delObject(self, obj):
        self.objects.remove(obj)
    
    def iterate(self):
        self.eventManager.manage()
        self.__draw_scene()
    
    def __draw_scene(self):
        display.begin_draw()
        
        for obj in self.objects:
            obj.draw()
        
        display.end_draw()
        
        display.refresh()
    
    def mainloop(self, time):
        mainloop.start(time, self)
    
    def quit(self):
        # insert here another thing yo clear :|
        pygame.quit()
