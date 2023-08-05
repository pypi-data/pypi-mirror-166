import os
import sys

try:
    from .core import log, aws, tunnel, db
except ImportError:
    from core import log, aws, tunnel, db

try:
    from . import config
except ImportError:
    import config

env = os.environ.get("AWS_EXECUTION_ENV")
name = 'engine'

def get_secret(configuration):
    result = {}
    for alias_aws, content in configuration.items():
        secret_id = content['secret_id']
        result[alias_aws] = {}
        result[alias_aws]['secret_id'] = secret_id
        result[alias_aws]['secret_string'] = aws.getSecret(secret_id)
    return result

def get_credential(configuration):
    result_db = config.database['credential']
    result_tunnel = config.tunnel['credential']
    for alias_aws, secret_content in configuration.items():
        if secret_content['secret_string']['engine'] in ['postgres', 'redshift']:
            result_db[alias_aws] = {}
            for key in ['engine', 'host', 'port', 'username', 'password', 'database']:
                result_db[alias_aws][key] = secret_content['secret_string'][key]
        elif secret_content['secret_string']['engine'] in ['ssh']:
            result_tunnel[alias_aws] = {}
            for key in ['host', 'port', 'username', 'password', 'rsa', 'remote_address']:
                result_tunnel[alias_aws][key] = secret_content['secret_string'][key]
    return (result_db, result_tunnel)

def transform_remote_address(configuration):
    result = []
    for host, port in configuration.items():
        result.append((host, port))
    return result

def run_tunnel(alias_ssh, config_ssh):
    session_ssh, remote_address, local_bind_address = tunnel.start(
        alias = alias_ssh,
        rsa = config_ssh['rsa'], 
        host = config_ssh['host'], 
        port = config_ssh['port'], 
        username = config_ssh['username'], 
        password = config_ssh['password'], 
        remote_addresses = transform_remote_address(config_ssh['remote_address'])
    )
    return (remote_address, local_bind_address)

def start():
    config_aws = config.aws
    config_tunnel = config.tunnel
    config_database = config.database
    if config_aws['enabled']:
        config_aws['secret'] = get_secret(config_aws['secret'])    
        config_database['credential'], config_tunnel['credential'] = get_credential(config_aws['secret'])
    if (config_tunnel['enabled']) and (env == None):
        for alias_ssh, config_ssh in config_tunnel['credential'].items():
            remote_address, local_bind_address = run_tunnel(alias_ssh, config_ssh)
            for content in remote_address:
                index = remote_address.index(content)
                host, port = content
                for alias_db, value in config_database['credential'].items():
                    if (value['host'] == host) and (value['port'] == port):
                        new_host, new_port = local_bind_address[index]
                        config_database['credential'][alias_db]['host'] = new_host
                        config_database['credential'][alias_db]['port'] = new_port
    if config_database['credential'] != {}:
        for alias_db, config_db in config_database['credential'].items():
            db.start(
                alias = alias_db,
                engine = config_db['engine'], 
                host = config_db['host'], 
                port = config_db['port'], 
                username = config_db['username'], 
                password = config_db['password'], 
                database = config_db['database'] 
            )
        
def stop():
    db.stopAll()
    tunnel.stopAll()

