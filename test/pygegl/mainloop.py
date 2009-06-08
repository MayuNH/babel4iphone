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

from twisted.internet import reactor

import singleton

def start(time, scene):
    twistedLoop(time, scene)


class twistedLoop(singleton.Singleton):
    
    def initialize(self, time, scene):
        self.time = time
        self.scene = scene
        
        self.update()
        reactor.run()
    
    def update(self):
        self.scene.iterate()
        
        if self.scene.want_quit:
            self.scene.quit()
            reactor.stop()
        else:
            reactor.callLater(self.time, self.update)
