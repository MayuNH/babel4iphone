from twisted.internet import reactor
from core.manager import Manager
from core.db.models import Session

class Server(object):
    
    def __init__(self):
        self.manager = Manager()
    
    def mainloop(self):
        for id, p in self.manager.logged.items():
            tmp = "%s %s %s" % (p.id, 
                                p.username, 
                                p.passwd)
            for dna in p.dna:
                tmp += "\n\t%s %s %s" % (dna.creation_date, 
                                         dna.cur_timestamp, 
                                         dna.decaying_time)
                dna.update()
            print tmp
        Session.commit()
        reactor.callLater(1.0, self.mainloop)


if __name__=="__main__":
    s = Server()
    
    s.manager.login('amati', 'amati')
    s.manager.login('vito', 'vito')
    
    s.mainloop()
    reactor.run()
