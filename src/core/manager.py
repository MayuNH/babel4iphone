from singleton import Singleton
import MySQLdb
import time

class Manager(Singleton):
    
    def login(self, u, p):
        sql = "SELECT * FROM account WHERE"
        sql += " username='%s' and passwd='%s'" % (u, p)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
