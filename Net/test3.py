from twisted.internet import reactor
#from twisted.internet.threads import deferToThread
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
#from gui import *
import random

class ClientProtocol(LineReceiver):
    
    def __init__(self):
        self.username = "U55555"
    
    def connectionMade(self):
        self.factory.client = self
        self.sendLine("U|" + self.username)
    
    def lineReceived(self, data):
        data = data.split("\r\n")
        for msg in data:
            if msg:
                m = msg.split('|')
                if m:
                    try:
                        if 'N' == m[0]:
                            #cocos.director.director.scene.get("interface").setName(m[1])
                            print "Mio nome %s" % m[1]
                        elif 'E' == m[0]:
                            print "Echo: %s" % m[1]
                            #cocos.director.director.scene.get("interface").update_label(m[1])
                        elif 'M' == m[0]:
                            print "Menu: %s" % m[1]
                            #cocos.director.director.scene.get("interface").initMenu(m[1].split(';'))
                        elif 'T' == m[0]:
                            print "E' il turno di %s" % m[1]
                            #cocos.director.director.scene.get("interface").setTurn(m[1])
                        else:
                            print "Comando non implementato: %s" % m
                    except:
                        pass
        
    def connectionLost(self , reason):
        if reactor.running:
            print "Server down."
            reactor.stop()


class ClientFactory(Factory):
    protocol = ClientProtocol
    
    def __init__(self):
        self.client = None
    
    def startedConnecting(self, connector):
        pass
    
    def clientConnectionFailed(self, connector, reason):
        pass
    
    def clientConnectionLost(self, connector, reason):
        pass
    
    def send(self, message):
        if self.client:
            self.client.sendLine(message)


def loop(f):
    f.send("F|%s" % "U66666")
    #f.send("E|%s" % random.randint(0, 100))
    #reactor.callLater(0, loop, f)


if __name__=="__main__":
    #deferToThread(initGUI)
    f = ClientFactory()
    reactor.connectTCP('localhost', 66666, f)
    reactor.callLater(1, loop, f)
    reactor.run()
