import pyodbc
from functions import regenerate_password


def get_connection():
    driver = "ODBC Driver 18 for SQL Server"
    server = 'tcp:msfp.database.windows.net,1433'
    database = 'EasyEL'
    encrypt = 'yes'
    username = 'fschumacher'
    password = regenerate_password()
    connectstring='DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT='+encrypt+';UID='+username+';PWD='+password
    print("connections")
    conn = pyodbc.connect(connectstring)
    return conn
