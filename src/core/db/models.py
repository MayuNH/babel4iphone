from sqlalchemy import *
from sqlalchemy.orm import relation, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://root@localhost/genoma")
Session = scoped_session(sessionmaker(autocommit=False, 
                                      autoflush=False, 
                                      bind=engine))
Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), nullable=False, unique=True)
    passwd = Column(String(25), nullable=False)
    email = Column(String(60), nullable=False)
    dna = relation("Dna", backref="account")
    
    #def __repr__(self):
    #    return "%s %s %s %s %s" % (self.id,
    #                               self.username,
    #                               self.passwd,
    #                               self.email,
    #                               self.dna)

class Dna(Base):
    __tablename__ = 'dna'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    creation_date = Column(String(10), nullable=False)
    cur_timestamp = Column(String(10), nullable=False)
    decaying_time = Column(String(10), nullable=False)
    genes = Column(String(500), nullable=False)
    
    #def __repr__(self):
    #    return "%s" % (self.id)

        
if __name__=="__main__":
    q = (Session.query(Account).filter(Account.id==1))
    print q.all()
