import MySQLdb
import math
from core.db.Conn import MySql
from ConfigParser import ConfigParser
from library.logging.Log import logger

class Select():
    select = []
    query = []
    fetch = ''

    def __init__(self, table, field = '*'):
        try:
            config = ConfigParser()
            config.read('config/api.conf')
                
            pool = MySql(MySQLdb, host=config.get('dbsample','host'), user=config.get('dbsample','username'), passwd=config.get('dbsample','password'), db=config.get('dbsample','database'), port=int(config.get('dbsample','port')), charset='utf8')
            self.conn = pool.connection()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            
            Select.select.append("SELECT {} FROM `{}`".format(field, table))
        except Exception as er:
			logger(str(er))

    def __del__(self):
        Select.select = []
        Select.query = []
        Select.fetch = ''
        self.cursor.close()
        self.conn.close()

    def fetchall(self):
        Select.fetch = 'all'

    def fetchone(self):
        Select.fetch = 'one'

    def get(self):
        build = Select.select + Select.query
        
        try:
            self.cursor.execute(' '.join(build))
            
            if Select.fetch == 'one':
                return self.cursor.fetchone()
            else:
                return self.cursor.fetchall()
        except Exception as er:
            logger(str(er))
            return None
    
    def getpaginate(self, sql, perpage, page):
        data = {}

        try:
            self.cursor.execute(sql)
            lists = self.cursor.fetchall()

            pages = math.ceil(float(len(lists)) / float(perpage))

            next = None
            if page < pages:
                next = page + 1

            prev = None
            if page > 1:
                prev = page - 1

            data = {'total': len(lists), 'perpage': perpage, 'curpage': page, 'next': next, 'prev': prev, 'pages': pages, 'items': None}
            
            return data
        except Exception as er:
            logger(str(er))
            return None

    def raw(self, value):
        Select.query.append("{}".format(value))
    
    def where(self, field, value, operator = '='):
        if len(Select.query) == 0:
            if type(value) is str:
                Select.query.append("WHERE {} {} '{}'".format(field, operator, value))
            else:
                Select.query.append("WHERE {} {} {}".format(field, operator, value))
        else:
            if type(value) is str:
                Select.query.append("AND {} {} '{}'".format(field, operator, value))
            else:
                Select.query.append("AND {} {} {}".format(field, operator, value))

    def orWhere(self, field, value, operator = '='):
        if len(Select.query) == 0:
            if type(value) is str:
                Select.query.append("WHERE {} {} '{}'".format(field, operator, value))
            else:
                Select.query.append("WHERE {} {} {}".format(field, operator, value))
        else:
            if type(value) is str:
                Select.query.append("OR {} {} '{}'".format(field, operator, value))
            else:
                Select.query.append("OR {} {} {}".format(field, operator, value))

    def notWhere(self, field, value):
        if len(Select.query) == 0:
            if type(value) is str:
                Select.query.append("WHERE NOT {} = '{}'".format(field, value))
            else:
                Select.query.append("WHERE NOT {} = {}".format(field, value))
        else:
            if type(value) is str:
                Select.query.append("AND NOT {} = '{}'".format(field, value))
            else:
                Select.query.append("AND NOT {} = {}".format(field, value))

    def Like(self, field, value):
        if len(Select.query) == 0:
            Select.query.append("WHERE {} LIKE '{}'".format(field, value))
        else:
            Select.query.append("AND {} LIKE '{}'".format(field, value))
    
    def inWhere(self, field, value):
        if len(Select.query) == 0:
            Select.query.append("WHERE {} IN ({})".format(field, ','.join(value)))
        else:
            Select.query.append("AND {} IN ({})".format(field, ','.join(value)))

    def between(self, field, value_a, value_b):
        if len(Select.query) == 0:
            Select.query.append("WHERE {} BETWEEN {} AND {}".format(field, value_a, value_b))
        else:
            Select.query.append("AND {} BETWEEN {} AND {}".format(field, value_a, value_b))

    def order_by(self, field_a, field_b = None):
        if field_b:
            Select.query.append("ORDER BY {} {}, {} {}".format(field_a[0], field_a[1], field_b[0], field_b[1]))
        else:
            Select.query.append("ORDER BY {} {}".format(field_a[0], field_a[1]))

    def join(self, join, field, condition):
        Select.query.append("{} JOIN {} ON {}".format(join, field, condition))

    def group_by(self, field, short = 'ASC'):
        Select.query.append("GROUP BY {} {}".format(field, short))
    
    def limit(self, limit, start = 0):
        Select.query.append("LIMIT {},{}".format(start, limit))

    def having(self, field, value, operator = '='):
        if (type(field) is str and type(value) is str):
            Select.query.append("HAVING '{}' {} '{}'".format(field, operator, value))
        else:
            if type(field) is str:
                Select.query.append("HAVING '{}' {} {}".format(field, operator, value))
            elif type(value) is str:
                Select.query.append("HAVING {} {} '{}'".format(field, operator, value))
            else:
                Select.query.append("HAVING {} {} {}".format(field, operator, value))

    def paginate(self, perpage = 10, page = 1):
        start = (page - 1) * perpage
        limit = perpage

        join = Select.select + Select.query
        sql = ' '.join(join)
        paginate = self.getpaginate(sql, perpage, page)

        Select.query.append("LIMIT {},{}".format(int(start), int(limit)))
        Select.fetch = 'all'

        paginate['items'] = self.get()

        return paginate

class Update():
    update = []
    change = []
    query = []

    def __init__(self, table):
        try:
            config = ConfigParser()
            config.read('config/api.conf')
                
            pool = MySql(MySQLdb, host=config.get('dbismaya','host'), user=config.get('dbismaya','username'), passwd=config.get('dbismaya','password'), db=config.get('dbismaya','database'), port=int(config.get('dbismaya','port')), charset='utf8')
            self.conn = pool.connection()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            
            Update.update.append("UPDATE {}".format(table))
        except Exception as er:
			logger(str(er))

    def __del__(self):
        Update.update = []
        Update.change = []
        Update.query = []
        self.cursor.close()
        self.conn.close()

    def get(self):
        build = Update.update + [','.join(Update.change)] + Update.query
        
        try:
            self.cursor.execute(' '.join(build))
            
            return self.cursor.commit()
        except Exception as er:
            logger(str(er))
            self.cursor.rollback()
            return None

    def raw(self, value):
        Update.query.append("{}".format(value))

    def set(self, field, value):
        if len(Update.query) == 0:
            if type(value) is str:
                Update.change.append("SET {} = '{}'".format(field, value))
            else:
                Update.change.append("SET {} = {}".format(field, value))
        else:
            if type(value) is str:
                Update.change.append("{} = '{}'".format(field, value))
            else:
                Update.change.append("{} = {}".format(field, value))

    def where(self, field, value, operator = '='):
        if len(Update.query) == 0:
            if type(value) is str:
                Update.query.append("WHERE {} {} '{}'".format(field, operator, value))
            else:
                Update.query.append("WHERE {} {} {}".format(field, operator, value))
        else:
            if type(value) is str:
                Update.query.append("AND {} {} '{}'".format(field, operator, value))
            else:
                Update.query.append("AND {} {} {}".format(field, operator, value))

    def orWhere(self, field, value, operator = '='):
        if len(Update.query) == 0:
            if type(value) is str:
                Update.query.append("WHERE {} {} '{}'".format(field, operator, value))
            else:
                Update.query.append("WHERE {} {} {}".format(field, operator, value))
        else:
            if type(value) is str:
                Update.query.append("OR {} {} '{}'".format(field, operator, value))
            else:
                Update.query.append("OR {} {} {}".format(field, operator, value))

    def notWhere(self, field, value):
        if len(Update.query) == 0:
            if type(value) is str:
                Update.query.append("WHERE NOT {} = '{}'".format(field, value))
            else:
                Update.query.append("WHERE NOT {} = {}".format(field, value))
        else:
            if type(value) is str:
                Update.query.append("AND NOT {} = '{}'".format(field, value))
            else:
                Update.query.append("AND NOT {} = {}".format(field, value))

class Insert():
    insert = []
    query = []

    def __init__(self, table):
        try:
            config = ConfigParser()
            config.read('config/api.conf')
                
            pool = MySql(MySQLdb, host=config.get('dbismaya','host'), user=config.get('dbismaya','username'), passwd=config.get('dbismaya','password'), db=config.get('dbismaya','database'), port=int(config.get('dbismaya','port')), charset='utf8')
            self.conn = pool.connection()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            
            Insert.insert.append("INSERT INTO {}".format(table))
        except Exception as er:
			logger(str(er))

    def __del__(self):
        Insert.insert = []
        Insert.query = []
        self.cursor.close()
        self.conn.close()

    def get(self):
        build = Insert.insert + Insert.query
        
        try:
            self.cursor.execute(' '.join(build))
        
            return self.cursor.commit()
        except Exception as er:
            logger(str(er))
            self.cursor.rollback()
            return None
        
    def raw(self, value):
        Insert.query.append("{}".format(value))

    def fields(self, field):
        Insert.query.append("({})".format(','.join(field)))

    def values(self, value):
        Insert.query.append("VALUES({})".format(','.join(value)))

class Delete():
    delete = []
    query = []

    def __init__(self, table):
        try:
            config = ConfigParser()
            config.read('config/api.conf')
                
            pool = MySql(MySQLdb, host=config.get('dbismaya','host'), user=config.get('dbismaya','username'), passwd=config.get('dbismaya','password'), db=config.get('dbismaya','database'), port=int(config.get('dbismaya','port')), charset='utf8')
            self.conn = pool.connection()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            
            Delete.delete.append("DELETE FROM {}".format(table))
        except Exception as er:
			logger(str(er))

    def __del__(self):
        Delete.delete = []
        Delete.query = []
        self.cursor.close()
        self.conn.close()

    def get(self):
        build = Delete.delete + Delete.query
        
        try:
            self.cursor.execute(' '.join(build))
        
            return self.cursor.commit()
        except Exception as er:
            logger(str(er))
            self.cursor.rollback()
            return None
        
    def raw(self, value):
        Delete.query.append("{}".format(value))
    
    def where(self, field, value, operator = '='):
        if len(Delete.query) == 0:
            if type(value) is str:
                Delete.query.append("WHERE {} {} '{}'".format(field, operator, value))
            else:
                Delete.query.append("WHERE {} {} {}".format(field, operator, value))
        else:
            if type(value) is str:
                Delete.query.append("AND {} {} '{}'".format(field, operator, value))
            else:
                Delete.query.append("AND {} {} {}".format(field, operator, value))

    def orWhere(self, field, value, operator = '='):
        if len(Delete.query) == 0:
            if type(value) is str:
                Delete.query.append("WHERE {} {} '{}'".format(field, operator, value))
            else:
                Delete.query.append("WHERE {} {} {}".format(field, operator, value))
        else:
            if type(value) is str:
                Delete.query.append("OR {} {} '{}'".format(field, operator, value))
            else:
                Delete.query.append("OR {} {} {}".format(field, operator, value))

    def notWhere(self, field, value):
        if len(Delete.query) == 0:
            if type(value) is str:
                Delete.query.append("WHERE NOT {} = '{}'".format(field, value))
            else:
                Delete.query.append("WHERE NOT {} = {}".format(field, value))
        else:
            if type(value) is str:
                Delete.query.append("AND NOT {} = '{}'".format(field, value))
            else:
                Delete.query.append("AND NOT {} = {}".format(field, value))