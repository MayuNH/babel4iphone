from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
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
            print msg
    
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
    f.send("F|6397D24E-299F-594E-BEE1-C1BBEA6C0B9E")
    #f.send("E|%s" % random.randint(0, 100))
    #reactor.callLater(0, loop, f)


if __name__=="__main__":
    f = ClientFactory()
    reactor.connectTCP('localhost', 66666, f)
    reactor.callLater(1, loop, f)
    reactor.run()
