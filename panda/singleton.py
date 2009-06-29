#PyCodeAnalizer
#
#Copyright (C) 2008 Domenico Chierico <spaghetty@gmail.com>
#Copyright (C) 2008 Giuseppe Scrivano <gscrivano@gnu.org>
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

class Singleton(object):
    
    def __new__(type, *args, **kwargs):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type, *args, **kwargs)
        return type._the_instance
    
    def __init__(self, *args, **kwargs):
        if not self.__dict__.has_key("_Singleton__inited"):
            self.__inited = True
            try:
                self.initialize(*args, **kwargs)
            except AttributeError, e1:
                pass
            except Exception, e2:
                print e2
