from singleton import Singleton
from db.models import *

class Manager(Singleton):

    def initialize(self):
        self.logged = {}
    
    def login(self, u, p):
        try:
            u = Session.query(Account).filter(and_(Account.username == u, 
                                                   Account.passwd == p)).one()
            acc = Session.query(Account).filter(Account.id==u.id).one()
            self.logged[u.id] = acc.dna
        except Exception, e:
            print e
            return 0
        return 1
    
    def logout(self, id):
        try:
            del self.logged[id]
        except Exception, e:
            print e
            return 0
        return 1
