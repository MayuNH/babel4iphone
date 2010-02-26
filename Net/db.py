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

def list_factory(cursor, row):
    return [str(c) for c in row]


class Database(object):
    
    def __init__(self, db = "gameDB.sqlite"):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db)
            #self.conn.row_factory = sqlite3.Row # for dict
            self.conn.row_factory = list_factory
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
        cursor = self.conn.cursor()
        sql = "SELECT %s FROM %s WHERE %s;" % (select, table, where)
        c = cursor.execute(sql)
        return cursor.fetchall()
    
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
            r = r[0][0]
        return r
    
    def getCharacter(self, uid):
        r = self.select("char_id, name, race_id, job_id, supjob_id", 
                        "collection, character", 
                        "collection.char_id = character.id and user_id='%s' and party=1" % uid)
        return r
    
    def getJob(self, cid, job):
        r = self.select("level, exp, hp, mp, time", 
                        "job", 
                        "char_id=%s and type_id='%s'" % (cid, job))
        if r:
            r = r[0]
        return r


if __name__ == "__main__":
    d = Database()
    print d.getNameByUid("U55555")
    
    p1 = []
    for c in d.getCharacter("U66666"):
        j = d.getJob(c[0], c[3])
        c.extend(j)
        if j:
            s = d.getJob(c[0], c[4])
            c.extend(s)
        p1.append(','.join(c))
    
    print ';'.join(p1)
