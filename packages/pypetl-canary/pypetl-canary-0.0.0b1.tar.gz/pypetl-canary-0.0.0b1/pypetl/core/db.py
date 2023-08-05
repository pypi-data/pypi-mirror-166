"""
    Connection Manager
    
    Author: 
        Asyraf Nur
        
    Path: 
        pypetl.core.connection
    
    Description:
        -
        
    Dependency:
        - io
        - paramiko
        - psycopg2 / psycopg2-binary
        - redshift_connector / redshift-connector 
        - sshtunnel.SSHTunnelForwarder
        - operator.itemgetter
        - pypetl.core.aws
        - pypetl.core.log
        - pypetl.core preference
        
""" 
import paramiko
import redshift_connector as rc
import psycopg2 as pg
from operator import itemgetter

from pypetl.core import log

# Global Variable
session = {}

def start(alias, engine, host, port, username, password, database):
    fname = 'db.start'
    log.append(function_name = fname, identifier="Alias: %s, Engine: %s"%(alias, engine), show = True)
    if engine=='postgres':
        result = pg.connect(
            host = host,
            port = port,
            database = database,
            user = username,
            password = password
        )
    elif engine=='redshift':
        result = rc.connect(
            host = host,
            port = port,
            database = database,
            user = username,
            password = password
        )
    session[alias] = result
    return result


def stop(alias):
    fname = 'db.stop'
    log.append(function_name = fname, identifier="Alias: %s"%(alias), show = True)
    session[alias].close()

def stopAll():
    fname = 'db.stopAll'
    log.append(function_name = fname, show = True)
    for alias in session.keys():
        stop(alias)
