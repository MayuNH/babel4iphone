#!/usr/bin/python -O

# This file is part of babel4iphone.

# Copyright (C) 2009 Giovanni Amati <amatig@gmail.com>

# babel4iphone is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# babel4iphone is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with babel4iphone.  If not, see <http://www.gnu.org/licenses/>.


from core import Core
from reactor import *
from types import StringType
import select, socket, sys, signal

SHOST = "localhost"
SPORT = 66666
BUFSIZ = 1024
DELIMETER = "\r\n"

class Server(object):
    
    def __init__(self, host = SHOST, port = SPORT, backlog = 5):        
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((host, port))
            self.server.listen(backlog)
            print "Server up [%s:%s]" % (host, port)
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Server error: %s" % message
            sys.exit(1)
        
        signal.signal(signal.SIGINT, self.sighandler) # ctrl-c
        self.__core = Core(self)
        self.__start()
    
    def sighandler(self, signum, frame):
        print "Shutting down server..."
        for s in self.__core.getSockets():
            s.close()
        self.server.close()
    
    def sendLine(self, s, msg, t = 0):
        if type(msg) is StringType:
            msg = [msg]
        msg = DELIMETER.join(msg)
        reactor.callLater(t, s.send, msg + DELIMETER)
    
    def __start(self):
        running = 1
        while running:
            try:
                inputs = [self.server, sys.stdin]
                scks = self.__core.getSockets()
                inputs.extend(scks)
                inputready, outputready, exceptready = select.select(inputs, [], [], 1)
            except select.error, e:
                break
            except socket.error, e:
                break
            
            for s in inputready:
                if s == self.server:
                    c_sck, address = self.server.accept()
                    self.__dispatch(c_sck)
                elif s == sys.stdin:
                    junk = sys.stdin.readline()
                    running = 0
                else:
                    try:
                        self.__dispatch(s)
                    except socket.error, e:
                        self.__core.delClientBySocket(s)
            self.__core.mainLoop()
            reactor.step()
            #time.sleep(1) # necessario altrim. scoppia CPU e DB :D
        self.server.close()
    
    def __dispatch(self, s):
        data = None
        try:
            data = s.recv(BUFSIZ).split(DELIMETER)[:-1]
        except:
            pass
        if not data:
            self.__core.delClientBySocket(s)
        else:
            for msg in data:
                if msg:
                    m = msg.split('|')
                    if m:
                        if 'U' == m[0]:
                            self.__core.addClient(m[1], s)
                        elif 'F' == m[0]:
                            self.__core.createArena(s, m[1])
                        elif 'E' == m[0]:
                            print "Echo server: %s" % m[1]
                        elif 'M' == m[0]:
                            print "Menu: %s" % m[1]
                        else:
                            print "Not implemented: %s" % m


if __name__ == "__main__":
    Server()
