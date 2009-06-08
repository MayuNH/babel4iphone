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

import pygame
from pygame.locals import *

import singleton, display, mainloop, event, time

def create(caption, screen_size, flags = DOUBLEBUF):
    return Scene(caption, screen_size, flags)


class Scene(singleton.Singleton):
    
    def initialize(self, caption, screen_size, flags = DOUBLEBUF):
        """Initialize"""
        self.objects = []
        self.events = []
        self.click_time = 0
        self.want_quit = False
        
        """Initialize GL"""
        display.init(screen_size, flags)
        display.set_caption(caption)
    
    def iterate(self):
        for e in event.get():
            if e.type == QUIT:
                self.want_quit = True
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                self.want_quit = True
            else:
                self.__event_proxy(e)
        self.__draw()
    
    def mainloop(self, time):
        mainloop.start(time, self)
    
    def __draw(self):
        display.begin_draw()
        
        #size = display.get_size()
        #draw.rect([0, 0, size[0], size[1]], [255, 255, 255])        
        for obj in self.objects:
            obj.draw()
        
        display.end_draw()
        
        display.refresh()
    
    def quit(self):
        pygame.quit()
    
    def addEvent(self, event):
        self.events.append(event)
    
    def addObject(self, obj):
        self.objects.append(obj)
    
    def __get_collide(self, pos):
        size = self.objects.__len__()
        for i in xrange(size):
            o = self.objects[size - i - 1]
            if o.is_hit(pos):
                return o
        return None
    
    def __event_proxy(self, event):
        obj = None
        try:
            obj = self.__get_collide(event.pos)
            # print obj
        except Exception, e:
            pass
        
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.__check_time():
                    self.events.append([obj, 'MouseDoubleLeft', event.pos])
                else:
                    self.events.append([obj, 'MouseDownLeft', event.pos])
            elif event.button == 3:
                self.events.append([obj, 'MouseDownRight', event.pos])
        elif event.type == MOUSEMOTION:
            self.events.append([obj, 'MouseMove', event.rel])
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.events.append([obj, 'MouseUpLeft', event.pos])
            elif event.button == 3:
                self.events.append([obj, 'MouseUpRight', event.pos])
        
        while self.events.__len__() > 0:
            e = self.events.pop(0)
            try:
                print e
                getattr(e[0], e[1])(*e[2:])
            except Exception, ex:
                # print ex
                pass
    
    def __check_time(self):
        t = time.time()
        diff = t - self.click_time
        self.click_time = t
        ret = diff < 0.25
        if ret:
            self.click_time = 0
        return ret
