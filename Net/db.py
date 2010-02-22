# This file is part of babel4iphone.

# Copyright (C) 2009 Giovanni Amati <amatig@gmail.com>

# babel4iphone is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# babel4iphone is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with babel4iphone.  If not, see <http://www.gnu.org/licenses/>.


import sys, sqlite3
#import sys, MySQLdb

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
    
    fname = "../Babel/gameDB.sqlite"
    try:
        os.remove(fname)
        print "Rimosso il vecchio database client."
    except:
        print "Il database client non esiste."
    
    s = Database()
    d = Database(fname)
    print "Creato nuovo database client."
    
    sql = 'CREATE TABLE "character" ("id" INTEGER PRIMARY KEY  NOT NULL ,"name" VARCHAR(25) NOT NULL ,"race_id" VARCHAR(25) NOT NULL ,"job_id" VARCHAR(25))'
    if d.execute(sql):
        print "Creata tabella character."
        
        check = False
        for r in s.select("*", "character"):
            r["name"] = "'%s'" % r["name"]
            r["race_id"] = "'%s'" % r["race_id"]
            r["job_id"] = "'%s'" % r["job_id"].replace("None", "")
            if not d.insert("character", r):
                check = True
        
        print "Database client popolato con le entry..."
        for r in d.select("*", "character"):
            print r
        if check:
            print "ERRORE: Alcuni character possono non essere stati inseriti!!!"
    else:
        print "Impossibile creare tabella character."
    
    sql = 'CREATE TABLE "type" ("id" VARCHAR(25) PRIMARY KEY  NOT NULL ,"hp" CHAR,"mp" CHAR,"str" CHAR,"dex" CHAR,"vit" CHAR,"agi" CHAR,"int" CHAR,"mnd" CHAR)'
    if d.execute(sql):
        print "Creata tabella type."
        
        check = False
        for r in s.select("*", "type"):
            for k in r.keys():
                r[k] = "'%s'" % r[k]
            if not d.insert("type", r):
                check = True
        
        print "Database client popolato con le entry..."
        for r in d.select("*", "type"):
            print r
        if check:
            print "ERRORE: Alcuni type possono non essere stati inseriti!!!"
    else:
        print "Impossibile creare tabella type."
    
    sql = 'CREATE TABLE "scale" ("id" CHAR PRIMARY KEY  NOT NULL ,"scaleHP" REAL DEFAULT 0 ,"baseHP" REAL DEFAULT 0 ,"scaleMP" REAL DEFAULT 0 ,"baseMP" REAL DEFAULT 0 ,"scaleSTATS" REAL DEFAULT 0 ,"baseSTATS" REAL DEFAULT 0 )'    
    if d.execute(sql):
        print "Creata tabella scale."
        
        check = False
        for r in s.select("*", "scale"):
            r["id"] = "'%s'" % r["id"]
            if not d.insert("scale", r):
                check = True
        
        print "Database client popolato con le entry..."
        for r in d.select("*", "scale"):
            print r
        if check:
            print "ERRORE: Alcuni scale possono non essere stati inseriti!!!"
    else:
        print "Impossibile creare tabella scale."
