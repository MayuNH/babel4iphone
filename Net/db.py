#import sys, MySQLdb
import sys, sqlite3

class Database(object):
    
    #def __init__(self, h = "localhost", u = "root", p = "", db = "gameDB"):
    def __init__(self, db = "gameDB.sqlite"):
        self.conn = None
        try:
            #self.conn = MySQLdb.connect(h, u, p, db)
            self.conn = sqlite3.connect(db)
            self.conn.row_factory = sqlite3.Row
        except Exception, e:
            print e
            self.close()
            sys.exit(1)
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def execute(self, sql):
        result = True
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            print e
            result = False
            self.conn.rollback()
        return result
    
    def select(self, select, table, where = "'1'"):
        #cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor = self.conn.cursor()
        sql = "SELECT %s FROM %s WHERE %s;" % (select, table, where)
        c = cursor.execute(sql)
        tmp = cursor.fetchall()
        
        # x sqlite return dict
        result = []
        for r in tmp:
            i = 0
            row = {}
            
            col = []
            try:
                col = cursor.keys()
            except:
                col = [c[0] for c in cursor.description]
            
            for k in col:
                row.update({k: str(r[i])})
                i += 1
            result.append(row)
        return result
    
    def insert(self, table, fields):
        result = True
        try:
            cursor = self.conn.cursor()
            keys = fields.keys()
            values = fields.values()
            sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, ','.join(keys), ','.join(values))
            cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            print e
            result = False
            self.conn.rollback()
        return result
    
    def update(self, table, fields, where):
        result = True
        try:
            cursor = self.conn.cursor()
            values = ["%s=%s" % (k, v) for k, v in fields.items()]
            sql = "UPDATE %s SET %s WHERE %s;" % (table, ','.join(values), where)
            cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            print e
            result = False
            self.conn.rollback()
        return result
    
    def delete(self, table, where = '1'):
        result = True
        try:
            cursor = self.conn.cursor()
            sql = "DELETE FROM %s WHERE %s;" % (table, where)
            cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            print e
            result = False
            self.conn.rollback()
        return result
    
    # High Functions Database
    
    def getNameByUid(self, uid):
        r = self.select("name", "user", "id='%s'" % uid)
        if r:
            r = r[0]["name"]
        return r
    
    def getParty(self, uid):
        r = self.select("id, char_id, level, hp, mp", 
                        "collection", 
                        "user_id='%s' and party=1" % uid)
        if r:
            r = r
        return r


if __name__ == "__main__":
    # questo codice permette di creare un db solo delle info dei character per il client
    import os
    
    fname = "../Babel/Resources/gameDB.sqlite"
    try:
        os.remove(fname)
        print "Rimosso il vecchio database client."
    except:
        print "Il database client non esiste."
    
    s = Database()
    d = Database(fname)
    
    sql = 'CREATE TABLE "character" ("id" INTEGER PRIMARY KEY  NOT NULL ,"name" VARCHAR(50) NOT NULL ,"race" VARCHAR(50) NOT NULL ,"atk" INTEGER DEFAULT 0 ,"def" INTEGER DEFAULT 0 ,"matk" INTEGER DEFAULT 0 ,"mdef" INTEGER DEFAULT 0 )'
    
    if d.execute(sql):
        print "Creato nuovo database client."
        
        check = False
        for r in s.select("*", "character"):
            r["race"] = "'%s'" % r["race"]
            r["name"] = "'%s'" % r["name"]
            if not d.insert("character", r):
                check = True
        
        # stampa del nuovo db
        print "Database client popolato con le entry..."
        for r in d.select("*", "character"):
            print r
        if check:
            print "ERRORE: Alcuni character possono non essere stati inseriti!!!"
    else:
        print "Impossibile creare nuovo database client."
