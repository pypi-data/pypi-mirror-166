"""
    AWS Manager (using boto3)
    
    Author: 
        Asyraf Nur
    
    Path: 
        pypetl.core.aws

    Description:
        ----
        
    Dependency:
        - boto3
        - json
        - pypetl.core.file
        - pypetl.core.log
        - pypetl.core.preference
"""
import boto3
import json

from pypetl.core import log

# Global Variable
enabled = False
started = False
secret = {}
session = boto3.session.Session()

def getSecret(secret_id:str=""):
    fname = 'aws.getSecret'
    data = session.client('secretsmanager').get_secret_value(SecretId=secret_id)['SecretString']
    log.append(function_name = fname, identifier="ID: %s"%(secret_id), show = True)
    return json.loads(data)  

