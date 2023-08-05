aws = {
    "enabled": False,
    "secret": {}
}

tunnel = {
    "enabled": False,
    "credential": {}
}

database = {
    "credential": {}
}

def aws_enable():
    global aws
    aws['enabled'] = True

def aws_disable():
    global aws
    aws['enabled'] = False

def tunnel_enable():
    global tunnel
    tunnel['enabled'] = True

def set_tunnel_credential(alias:str, host:str, port:int, username:str, password:str, rsa:bool, remote_address):
    global tunnel
    tunnel['credential'][alias] = {}
    tunnel['credential'][alias]['host'] = host
    tunnel['credential'][alias]['port'] = port
    tunnel['credential'][alias]['username'] = username
    tunnel['credential'][alias]['password'] = password
    tunnel['credential'][alias]['rsa'] = rsa
    tunnel['credential'][alias]['remote_address'] = remote_address

def set_database_credential(alias:str, engine:str, host:str, port:int, username:str, password:str, dbname:str):
    global database
    database['credential'][alias] = {}
    database['credential'][alias]['engine'] = engine
    database['credential'][alias]['host'] = host
    database['credential'][alias]['port'] = port
    database['credential'][alias]['username'] = username
    database['credential'][alias]['password'] = password
    database['credential'][alias]['dbname'] = dbname

def tunnel_disable():
    global tunnel
    tunnel['enabled'] = False

def set_aws_secret(alias, secret_id:str):
    global aws
    aws['secret'][alias] = {}
    aws['secret'][alias]['secret_id'] = secret_id
