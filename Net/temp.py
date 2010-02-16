#!/usr/bin/python -O

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
import time

## FUNC ##

# da il successione elemento di una lista
def next(l, e):
    return l[(l.index(e) + 1) % len(l)]


## SERVER ##

# il socket riceve solo gli event e li indirizza al factory x attivare i comandi
class ServerProtocol(LineReceiver):
    
    def __init__(self):
        self.uid = None
        self.main_menu = ""
    
    def connectionMade(self):
        pass
    
    def lineReceived(self, data):
        data = data.split("\r\n")
        for msg in data:
            m = msg.split('|')
            if 'U' == m[0]:
                self.factory.addClient(m[1], self)
            elif 'F' == m[0]:
                self.factory.startFight(self.uid, m[1])
            elif 'E' == m[0]:
                print m[1]
            elif 'M' == m[0]:
                self.factory.menu(self, int(m[1]))
            else:
                print "No used: %s" % m
    
    def connectionLost(self , reason):
        self.factory.delClient(self.uid)


class ServerFactory(Factory):
    protocol = ServerProtocol
    
    def __init__(self):
        self.clients = {}
        self.arena = {}
        self.main_menu = "Attack;Defende;Magics;Invocations;Items;Team;Settings"
    
    def addClient(self, uid, client):
        if not self.clients.has_key(uid):
            client.uid = uid
            self.clients[uid] = client
            print "Add user %s." % uid
        else:
            print "User %s exists."
    
    def delClient(self, uid):
        if self.clients.has_key(uid):
            del self.clients[uid]
            print "Delete %s." % uid
    
    def sendAll(self, message, time = 0):
        for uid, client in self.clients.items():
            reactor.callLater(time, client.sendLine, message)
    
    def send(self, uid, message, time = 0):
        if self.clients.has_key(uid):
            reactor.callLater(time, self.clients[uid].sendLine, message)
        else:
            print "No send msg, uid %s not exist." % uid
    
    def mainLoop(self):
        arena_keys = self.arena.keys()
        for k in arena_keys:
            players =  k.split('|')
            t = self.arena[k]["time"]
            if time.time() - t > 20:
                self.arena[k]["turn"] = next(players, self.arena[k]["turn"])
                self.arena[k]["time"] = time.time()
                for uid in players:
                    if self.clients.has_key(uid):
                        if uid == self.arena[k]["turn"]:
                            self.clients[uid].main_menu = ""
                            self.send(uid, "T|%s" % self.getData("name=%s" % self.arena[k]["turn"]))
                            self.send(uid, "M|%s" % self.main_menu, 2)
                        else:
                            self.send(uid, "M|chiudi")
                            self.send(uid, "T|%s" % self.getData("name=%s" % self.arena[k]["turn"]), 0.5)
                    else:
                        del self.arena[k]
                        print "Delete arena %s" % k
                        self.send(next(players, uid), "T|fine")
                        break
        reactor.callLater(1, self.mainLoop)
    
    # simula lettura da db
    def getData(self, query):
        result = ""
        args = query.split('=')
        if "name" == args[0]:
            if len(args[1]) > 10:
                result = "IPhone"
            else:
                result = "Python"
        elif "magics" == args[0]:
            if len(args[1]) > 10:
                result = "Fire:25;Water:25"
            else:
                result = "Fire:25"
        return result
    
    def menu(self, client, i):
        result = ""
        if not client.main_menu:
            items = self.main_menu.split(';')
            client.main_menu = items[i].lower()
            result = self.getData("%s=%s" % (client.main_menu, client.uid))
        else:
            print self.getData("%s=%s" % (client.main_menu, client.uid)).split(';')[i]
            client.main_menu = ""
            result = self.main_menu
        self.send(client.uid, "M|%s" % result, 0.5)
    
    def startFight(self, uid1, uid2):
        key = '%s|%s' % (uid1, uid2)
        if not self.arena.has_key(key):
            print "Create arena %s" % key
            self.arena[key] = {
                "turn": uid2,
                "time": time.time()
                }
            self.send(uid2, "T|%s" % self.getData("name=%s" % uid2))
            self.send(uid2, "M|%s" % self.main_menu, 2)


if __name__=="__main__":
    f = ServerFactory()
    reactor.listenTCP(66666, f)
    reactor.callLater(1, f.mainLoop)
    reactor.run()
