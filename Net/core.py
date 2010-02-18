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


from db import Database
from client import Client
from utils import *
import time

class Core(object):
    
    def __init__(self, server):
        self.__server = server
        self.__db = Database()
        self.__c = {}
        self.__a = {}
        self.__an = 0
    
    def getSockets(self):
        return [c.socket for c in self.__c.values()]
    
    def setClientMap(self, u, c):
        self.__c[u] = c
    
    def getClient(self, u):
        if self.__c.has_key(u):
            return self.__c[u]
        return None
    
    def getClientBySocket(self, s):
        for c in self.__c.values():
            if c.socket == s:
                return c
        return None
    
    def delClientMap(self, u):
        if self.__c.has_key(u):
            del self.__c[u]
        
    # Main Function Server
    
    def addClient(self, uid, s):
        c = None
        try:
            name = self.__db.getNameByUid(uid)
            if name:
                c = Client(s, uid, name)
        except Exception, e:
            print e
        
        if self.getClient(uid): # nel caso nn sia staro ripulito il vecchio socket x quella uid (login/out veloci)
            self.__server.sendLine(s, "E|You are already logged")
        elif c:
            self.setClientMap(uid, c)
            print "Add client uid %s" % uid
        else:
            self.__server.sendLine(s, "E|You don't have registration")
    
    def delClientBySocket(self, s):
        c = self.getClientBySocket(s)
        if c:
            c.socket.close()
            self.delClientMap(c.uid)
            print "Del client uid %s" % c.uid
        else:
            s.close()
    
    def mainLoop(self):
        arena = self.__getAllArena()
        #print arena
        for a in arena:
            t = a["time"]
            if t != 0 and time.time() - t > 20: # change turn
                mode = 0
                uids = [a["user_id1"], a["user_id2"]]
                clients = [self.getClient(u) for u in uids]
                other = clients[0]
                
                if not clients[0]:
                    mode += 1
                    other = clients[1]
                if not clients[1]:
                    mode += 2
                
                if mode < 3:
                    if mode > 0:
                        self.__server.sendLine(other.socket, "T|end")
                        self.delArena(a)
                        return
                else:
                    self.delArena(a)
                    return
                
                uids.extend(["__fight__"])
                a["turn"] = next(uids, a["turn"])
                
                if "__fight__" == a["turn"]:
                    a["turn_name"] = "__fight__"
                    a["time"] = time.time() + 10 # tempo animazione
                    
                    for c in clients:
                        self.__server.sendLine(c.socket, "A|dati animazione")
                else:
                    a["turn_name"] = self.getClient(a["turn"]).name
                    a["time"] = time.time()
                    
                    for c in clients:
                        if c.uid == a["turn"]:
                            self.__server.sendLine(c.socket, "T|you")
                        else:
                            self.__server.sendLine(c.socket, 
                                                   "T|%s" % a["turn_name"])
    
    def __getArenaByUid(self, u):
        if self.__a.has_key(u):
            return self.__a[u]
        return None
    
    def __getAllArena(self):
        tmp = {}
        for a in self.__a.values():
            if not tmp.has_key(a["id"]):
                tmp[a["id"]] = a
        return tmp.values()
    
    def delArena(self, a):
        del self.__a[a["user_id1"]]
        del self.__a[a["user_id2"]]
        print "Del arena id %s|%s" % (a["user_id1"], a["user_id2"])
    
    def __createArena(self, u1, u2, turn, time):
        arena = {"id":self.__an, 
                 "user_id1":u1, 
                 "user_id2":u2, 
                 "turn":turn, 
                 "turn_name": self.getClient(turn).name,
                 "time":time}
        self.__an += 1
        self.__a[u1] = arena
        self.__a[u2] = arena
    
    def createArena(self, s, uid2):
        c1 = self.getClientBySocket(s)
        
        tmp1 = self.__getArenaByUid(c1.uid)
        if tmp1 and uid2 != tmp1["user_id1"] and uid2 != tmp1["user_id2"]:
            self.__server.sendLine(c1.socket, "E|You are in another arena")
            return
        
        tmp2 = self.__getArenaByUid(uid2)
        if tmp2 and c1.uid != tmp2["user_id1"] and c1.uid != tmp2["user_id2"]:
            self.__server.sendLine(c1.socket, "E|Player busy")
            return
        
        c2 = self.getClient(uid2)
        if not c2 and not tmp2:
            self.__server.sendLine(c1.socket, "E|Player off-line")
            return
        
        if not tmp1:
            self.__createArena(c1.uid, uid2, c1.uid, 0)
            # invio dati team
            self.__sendParty(c1.uid, uid2, c1.socket, c2.socket) # 1 manda i dati dei team a tutti e 2 i client
            self.__server.sendLine(c1.socket, "T|you")
            self.__server.sendLine(c2.socket, "T|%s" % self.__a[c1.uid]["turn_name"])
            self.__a[c1.uid]["time"] = time.time()  # mettere il time solo dopo aver inviato i dati ai client
            print "Create arena %s|%s" % (c1.uid, uid2)
        else:
            # invio dati team solo a c1 se cade (a chi rientra appunto)
            self.__sendParty(c1.uid, uid2, c1.socket, None)
            msgs = None
            if c1.uid == tmp1["turn"]:
                msgs = "T|you"
            elif "__fight__" == tmp1["turn"]:
                msgs = "A|dati animazione"
            else:
                msgs = "T|%s" % tmp1["turn_name"]
            self.__server.sendLine(c1.socket, msgs)
            print "Client re-enter in arena %s|%s" % (c1.uid, uid2)
    
    def __sendParty(self, u1, u2, s1, s2):
        d1 = ["%s,%s,%s,%s,%s" % \
                  (x["id"], x["char_id"], x["level"], x["hp"], x["mp"]) for x in self.__db.getParty(u1)]
        d2 = ["%s,%s,%s,%s,%s" % \
                  (x["id"], x["char_id"], x["level"], x["hp"], x["mp"]) for x in self.__db.getParty(u2)]
        t1 = ';'.join(d1)
        t2 = ';'.join(d2)
        msgs = ["P1|%s" % t1, "P2|%s" % t2]
        
        self.__server.sendLine(s1, msgs)
        if s2:
            msgs = ["P1|%s" % t2, "P2|%s" % t1]
            self.__server.sendLine(s2, msgs)
