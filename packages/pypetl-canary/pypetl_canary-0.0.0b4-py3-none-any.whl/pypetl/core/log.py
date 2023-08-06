"""
    Log Manager
    
    Author: 
        Asyraf Nur
        
    Path: 
        pypetl.core.log
    
    Description:
        -
        
    Dependency:
        - datetime.datetime
        - datetime.timedelta
        - datetime.date
        - datetime.time
        
""" 
import os
import inspect
from datetime import datetime, timedelta, date, time

# Global Variable
report = []
show = False,
message_library = {
    "aws.getSecret": "Retrieve data from secret manager!",
    "db.start": "Start database session!"
}

def append(function_name="", message="", identifier="", show=False):
    show = True
    if function_name in message_library.keys():
        message = message_library[function_name]
    if identifier != "":
        message = "%s (%s)"%(message, identifier)
    log = ((datetime.utcnow() + timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S'), function_name, message)
    report.append(log)
    if show == True:
        time, function_name, message = log
        print('%s -->  %s: %s'%(time, function_name, message))


def show():
    """
        Show / Print All Recorded Log
        
        Author: 
            Asyraf Nur
            
        Path: 
            pypetl.core.log.show()
        
        Description:
            -
            
        Dependency:
            - pypetl.core.log.format()
            
    """ 
    for log in report:
        print(log)
