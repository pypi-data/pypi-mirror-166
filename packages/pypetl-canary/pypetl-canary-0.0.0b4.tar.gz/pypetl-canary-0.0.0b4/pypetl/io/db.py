from tkinter.tix import INTEGER
import petl

from pypetl import config
from pypetl.core import db, log
from pypetl.transform import table2str

def fromDBSecret(alias, query, cache=False):
    fname = 'fromDBSecret'
    if len(query) >= 100:
        query_log = query[0:97]+'...'
    else:
        query_log = query
    session = db.session[alias]
    session.commit()
    result = petl.fromdb(session, query)
    session.commit()
    if cache:
        result = result.cache()
    return result

def executeDBSecret(alias, query):
    fname = 'executeDBSecret'
    if len(query) >= 100:
        query_log = query[0:97]+'...'
    else:
        query_log = query
    session = db.session[alias]
    cursor = session.cursor()
    session.commit()
    cursor.execute(query)
    session.commit()

def toDBSecretDelete(alias, table, location_table, condition='id'):
    fname = 'toDBSecretDelete'
    source = table2str(table)
    if source.nrows() != 0:
        delete_value = ', '.join( repr(v) for v in source.todataframe()[condition].values.tolist()).replace("'","")
        delete_query = 'DELETE FROM %s WHERE %s in ( %s );'%(
            location_table,
            condition,
            delete_value
        )
        executeDBSecret(alias, delete_query)

def toDBSecretUpdate(alias, table, location_table, condition='id'):
    fname = 'toDBSecretUpdate'
    source = table2str(table)
    if source.nrows() != 0:
        delete_value = ', '.join( repr(v) for v in source.todataframe()[condition].values.tolist()).replace("'","")
        delete_query = 'DELETE FROM %s WHERE %s in ( %s );'%(
            location_table,
            condition,
            delete_value
        )
        executeDBSecret(alias, delete_query)
        table_field = ', '.join( repr(v) for v in list(source.fieldnames())).replace("'","")
        table_value = ', '.join( repr(v) for v in list(source.data())).replace("[", "(").replace("]", ")").replace("None", "null").replace("'null'", "null")
        table_query = 'INSERT INTO %s ( %s ) VALUES %s ;'%(
            location_table,
            table_field,
            table_value
        )
        executeDBSecret(alias, table_query)

def toDBSecretInsert(alias, table, location_table):
    fname = 'toDBSecretUpdate'
    source = table2str(table)
    if source.nrows() != 0:
        table_field = ', '.join( repr(v) for v in list(source.fieldnames())).replace("'","")
        table_value = ', '.join( repr(v) for v in list(source.data())).replace("[", "(").replace("]", ")").replace("None", "null").replace("'null'", "null")
        table_query = 'INSERT INTO %s ( %s ) VALUES %s ;'%(
            location_table,
            table_field,
            table_value
        )
        executeDBSecret(alias, table_query)

def _get_field_type_(typestring):
    if typestring == 'bigint':
        return 'BIGINT'
    elif typestring == 'integer':
        return 'INTEGER'
    elif typestring == 'decimal':
        return 'DECIMAL'
    elif typestring == 'varchar':
        return 'VARCHAR(256)'
    elif typestring == 'text':
        return 'VARCHAR(65000)'
    elif typestring == 'boolean':
        return 'BOOLEAN'
    elif typestring == 'timestmap':
        return 'TIMESTAMP'

def _get_field_null_(nullstring):
    if nullstring == 'not null':
        return 'NOT NULL'
    elif nullstring == 'null':
        return 'NULL'


def _get_field_increment_(incrementint:int):
    return 'identity(1,%s)'%(incrementint)

def createDBTable(alias, tablename:str, primarykey:tuple=('id', 'bigint', 'not null', 0)):
    fname, ftype, fnull, fincrement = primarykey
    if config.database[alias] in ['postgres']:
        query = 'CREATE TABLE IF NOT EXISTS %s ( %s %s %s %s );'%(tablename, fname, _get_field_type_(ftype), _get_field_null_(fnull), _get_field_increment_(fincrement))
    executeDBSecret(alias, query)

def addDBTable(alias, tablename:str, field:tuple=('id', 'bigint', 'not null')):
    fname, ftype, fnull = field
    if config.database[alias] in ['postgres']:
        query = 'ALTER TABLE %s ADD COLUMN %s %s %s );'%(tablename, fname, _get_field_type_(ftype), _get_field_null_(fnull))
    executeDBSecret(alias, query)

def truncateDBTable(alias, tablename:str):
    if config.database[alias] in ['redshift']:
        query = 'TRUNCATE TABLE %s;'%(tablename)
    executeDBSecret(alias, query)