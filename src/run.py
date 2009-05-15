from twisted.internet import reactor
from core.manager import Manager
from core.db.models import *

class Server(object):
    
    def __init__(self):
        self.manager = Manager()
        self.logged = {}
    
    def logon(self, u, p):
        record = self.manager.login(u, p)
        cid = record[0][0]
        self.logged[cid] = Session.query(Account).get(cid)
    
    def logoff(self, id):
        del self.logged[id]
    
    def mainloop(self):
        for id, p in self.logged.items():
            print "%s %s %s" % (p.id,
                                p.username,
                                p.email)
                                #p.dna.creation_date, 
                                #p.dna.cur_timestamp, 
                                #p.dna.decaying_time)
        reactor.callLater(1.0, self.mainloop)


if __name__=="__main__":
    s = Server()
    
    s.logon('amati', 'amati')
    s.logon('vito', 'vito')
    
    s.mainloop()
    reactor.run()
