from twisted.internet import reactor
from core.manager import Manager
from core.db.models import *

class Server(object):
    
    def __init__(self):
        self.manager = Manager()
    
    def mainloop(self):
        for id, p in self.manager.logged.items():
            tmp = ""
            for dna in p:
                dna.update()
                tmp += "\n\t%s %s %s" % (dna.creation_date, 
                                         dna.cur_timestamp, 
                                         dna.decaying_time)
            tmp = "Account %s%s" % (id, tmp)
            print tmp
        reactor.callLater(1.0, self.mainloop)


if __name__=="__main__":
    s = Server()
    
    s.manager.login('amati', 'amati')
    s.manager.login('vito', 'vito')
    
    s.mainloop()
    reactor.run()
