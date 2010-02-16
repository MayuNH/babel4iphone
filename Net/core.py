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
        
        # menu principale fisso unico
        self.__mmenu = "Attack;Defende;Magics;Invocations;Items"
    
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
        
        if self.getClient(uid): # lo sleep potrebbe aspettare a ripulire il vecchio socket in caso di rilogin
            self.__server.sendLine(s, "E|Wait 2 seconds for re-login")
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
                
                a["turn"] = next(uids, a["turn"])
                a["time"] = time.time()
                
                for c in clients:
                    if c.uid == a["turn"]:
                        self.__server.sendLine(c.socket, 
                                               ["T|you", 
                                                "M|%s" % self.__mmenu])
                    else:
                        self.__server.sendLine(c.socket, 
                                               "T|%s" % self.getClient(a["turn"]).name)
    
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
        arena = {"id":self.__an, "user_id1":u1, "user_id2":u2, "turn":turn, "time":time}
        self.__an += 1
        self.__a[u1] = arena
        self.__a[u2] = arena
    
    def createArena(self, c1, c2):
        if not c2:
            self.__server.sendLine(c1.socket, "E|Player off-line")
            return
        
        mode = 0
        tmp = self.__getArenaByUid(c1.uid)
        if tmp and c2.uid != tmp["user_id1"] and c2.uid != tmp["user_id2"]:
            self.__server.sendLine(c1.socket, "E|You are in another arena")
            return
        else:
            mode += 1
        tmp = self.__getArenaByUid(c2.uid)
        if tmp and c1.uid != tmp["user_id1"] and c1.uid != tmp["user_id2"]:
            self.__server.sendLine(c1.socket, "E|Player busy")
            return
        else:
            mode += 2
        
        arena = self.__getArenaByUid(c1.uid)
        if not arena:
            self.__createArena(c1.uid, c2.uid, c1.uid, 0)
            # invio dati team
            self.__sendParty(c1, c2, 1) # 1 manda i dati dei team a tutti e 2 i client
            
            self.__server.sendLine(c1.socket, ["T|you", "M|%s" % self.__mmenu])
            self.__server.sendLine(c2.socket, "T|%s" % c1.name)
            
            self.__a[c1.uid]["time"] = time.time()  # mettere il time solo dopo aver inviato i dati ai client
            print "Create arena %s|%s" % (c1.uid, c2.uid)
        elif mode >= 3:
            # invio dati team solo a c1 se cade (a chi rientra appunto)
            self.__sendParty(c1, c2)
            
            msgs = None
            if c1.uid == arena["turn"]:
                msgs = ["T|you", "M|%s" % self.__mmenu]
            else:
                msgs = ["T|%s" % self.getClient(arena["turn"]).name]
            self.__server.sendLine(c1.socket, msgs)
            print "Client re-enter in arena %s|%s" % (c1.uid, c2.uid)
    
    def __sendParty(self, c1, c2, flag = 0):
        d1 = ["%s,%s,%s,%s,%s" % \
                  (x["id"], x["char_id"], x["level"], x["hp"], x["mp"]) for x in self.__db.getParty(c1.uid)]
        d2 = ["%s,%s,%s,%s,%s" % \
                  (x["id"], x["char_id"], x["level"], x["hp"], x["mp"]) for x in self.__db.getParty(c2.uid)]
        t1 = ';'.join(d1)
        t2 = ';'.join(d2)
        msgs = ["P1|%s" % t1, "P2|%s" % t2]
        
        self.__server.sendLine(c1.socket, msgs)
        if flag:
            msgs = ["P1|%s" % t2, "P2|%s" % t1]
            self.__server.sendLine(c2.socket, msgs)
