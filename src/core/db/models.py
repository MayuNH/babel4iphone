from sqlalchemy import *
from sqlalchemy.orm import relation, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import time

Engine = create_engine("mysql://root@localhost/genoma")
Session = scoped_session(sessionmaker(autocommit=False, 
                                      autoflush=False, 
                                      bind=Engine))
Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), nullable=False, unique=True)
    passwd = Column(String(25), nullable=False)
    email = Column(String(60), nullable=False)
    dna = relation("Dna", backref="account")
    
    def __repr__(self):
        return "Account(%s)" % self.username
    
class Dna(Base):
    __tablename__ = 'dna'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    creation_date = Column(String(10), nullable=False)
    cur_timestamp = Column(String(10), nullable=False)
    decaying_time = Column(String(10), nullable=False)
    genes = Column(String(500), nullable=False)
    
    def update(self):
        self.cur_timestamp = int(time.time())
        self.decaying_time = int(self.decaying_time) - 1
    
    def __repr__(self):
        return "Dna(%s %s)" % (self.account.username, self.id)


if __name__=="__main__":
    pass
