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

import time

class Event(object):
    
    def __init__(self, scene):
        """Initialize"""
        self.events = []
        self.click_time = 0  # for implement doubleclick
        
        self.scene = scene
    
    def get(self):
        return pygame.event.get()
    
    def addEvent(self, event):
        self.events.append(event)
    
    def manage(self):
        for e in self.get():
            if e.type == QUIT:
                self.scene.want_quit = True
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                self.scene.want_quit = True
            else:
                self.__event_proxy(e)
    
    def __event_proxy(self, event):
        obj = None
        try:
            obj = self.__get_collide(event.pos)
            print obj
        except Exception, e:
            print e
        
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
                #print e
                getattr(e[0], e[1])(*e[2:])
            except Exception, ex:
                #print ex
                pass
    
    def __get_collide(self, pos):
        size = self.scene.objects.__len__()
        for i in xrange(size):
            o = self.scene.objects[size - i - 1]
            if o.is_hit(pos):
                return o
        return None
    
    def __check_time(self):
        t = time.time()
        diff = t - self.click_time
        self.click_time = t
        ret = diff < 0.25
        if ret:
            self.click_time = 0
        return ret
