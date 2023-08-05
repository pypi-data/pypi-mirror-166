import paramiko
from io import StringIO
from sshtunnel import SSHTunnelForwarder

from pypetl.core import log


session = {}
remote_address = {}
local_bind_address = {}

def generateRSAKey(password):
    fname = 'tunnel.generateRSAKey'
    content = "-----BEGIN RSA PRIVATE KEY-----\n%s\n-----END RSA PRIVATE KEY-----"%(password.replace(" ", "\n"))
    result = paramiko.RSAKey.from_private_key(StringIO(content))
    log.append(function_name = fname, show = True)
    return result

def generateTunnelForwarder(rsa, host, port, username, password, remote_address):
    fname = 'tunnel.generateTunnelForwarder'
    if rsa == True:
        pkey = generateRSAKey(password)
        result = SSHTunnelForwarder(
            (
                host, 
                port
            )
            , ssh_username = username
            , ssh_pkey = pkey
            , remote_bind_addresses = remote_address
        )
    else:
        result = SSHTunnelForwarder(
            (
                host, 
                port
            )
            , ssh_username = username
            , ssh_password = password
            , remote_bind_addresses = remote_address
        )
    log.append(function_name = fname, identifier = "Username: %s"%(username), show = True)
    return result

def start(alias, rsa, host, port, username, password, remote_addresses):
    fname = 'tunnel.start'
    global session, remote_address, local_bind_address
    result = generateTunnelForwarder(rsa, host, port, username, password, remote_addresses)
    log.append(function_name = fname, identifier = "Alias: %s, RSA: %s"%(alias, rsa), show = True)
    result.start()
    session[alias] = result
    remote_address[alias] = remote_addresses
    local_bind_address[alias] = result.local_bind_addresses
    return (session[alias], remote_address[alias], local_bind_address[alias])

def stop(alias):
    fname = 'tunnel.stop'
    log.append(function_name = fname, identifier = "Alias: %s"%(alias), show = True)
    session[alias].stop()

def stopAll():
    fname = 'tunnel.stopAll'
    log.append(function_name = fname, show = True)
    for alias in session.keys():
        stop(alias)
    