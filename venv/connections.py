import pyodbc
from functions import regenerate_password


def get_connection():
    driver = "ODBC Driver 18 for SQL Server"
    server = 'tcp:msfp.database.windows.net,1433'
    database = 'EasyEL'
    encrypt = 'yes'
    autocommit='True'
    username = 'fschumacher'
    password = regenerate_password()
    connectstring='DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT='+encrypt+';UID='+username+';PWD='+password+';AUTOCOMMIT='+autocommit
    print("connections")
    conn = pyodbc.connect(connectstring)
    return conn

class Azure:
    def __init__(self):
        self.conn = None

        self.driver = "ODBC Driver 18 for SQL Server"
        self.server = 'tcp:msfp.database.windows.net,1433'
        self.database = 'EasyEL'
        self.encrypt = 'yes'
        self.autocommit = 'True'
        self.username = 'fschumacher'
        self.password = 'L~Q6Y#z@91<n' #regenerate_password()
        self.connect_string = 'DRIVER=' + self.driver + ';SERVER=' + self.server + ';DATABASE=' + self.database + ';ENCRYPT=' + self.encrypt + ';UID=' + self.username + ';PWD=' + self.password  # + ';AUTOCOMMIT=' + autocommit

    def __enter__(self):

        self.conn=pyodbc.connect(self.connect_string)
        self.conn.autocommit=True
        #print('Azure geöffnet')
    def __exit__(self, *args):
        if self.conn:
            self.conn.close()
            self.conn = None
            #print('Azure zu')