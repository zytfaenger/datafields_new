import pyodbc
import uplink as uplink
import anvil.server
import re
from functions import regenerate_password

#Dieses Script fügt Daten in eine Azure-Datenbank ein!



driver="ODBC Driver 18 for SQL Server";
server = 'tcp:msfp.database.windows.net,1433'
database = 'Go3'
encrypt = 'yes'
username = 'fschumacher'
password = regenerate_password()
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
connectstring='DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT='+encrypt+';UID='+username+';PWD='+password
#connectstring='jdbc:sqlserver://msfp.database.windows.net:1433;database=EasyEL;user=fschumacher@msfp;password=password;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;'
conn = pyodbc.connect(connectstring)

cursor = conn.cursor()
#Sample select query
anvil.server.connect('GE4DCZUVVOJIINUGUTZSK3KB-ODQMODGOZ2DXHHG4')




@anvil.server.callable
def say_hello(name):
  print("Hello from the uplink, %s!" % name)


@anvil.server.callable
def get_DocSet(PDocSetID):
    cols = cursor.columns(table='DokSetQ')
    colnames = []
    for c in cols:
        colnames.append(c[3])
        #print(c[3]) #die Spalten
    #print(colnames)
    query= "SELECT DokSetEntryID, DokSetID, Component, CopID, Name, StoreName, Sequence,Text, Position, Tags, Properties, Parameters, Init_Handlers, other_handlers, TagValues FROM dbo.DokSetQ where DokSetID=? order by Sequence"
    cursor.execute(query,PDocSetID)

    items = cursor.fetchall()
    arr_of_fl=[]
    for rows in items:
        counter=0
        FL={}
        for i in rows:
            FL[colnames[counter]]=rows[counter]
            #print(colnames[counter],":",rows[counter])
            counter+=1
        #print("-------")
        arr_of_fl.append(FL)
    print(counter,arr_of_fl)
    return(arr_of_fl)





@anvil.server.callable
def get_items():
    cursor.execute("SELECT * FROM dbo.Names order by Name, Firstname, Place")
    items=cursor.fetchall()
    return [
        {'NameID':item[0],'Name':item[1],'Firstname':item[2],'Place':item[3]}
        for item in items
    ]
@anvil.server.callable
def insert_item(Name,Firstname,Place):
    cursor.execute("INSERT INTO Names (Name, Firstname, Place) VALUES (?,?,?)", (Name,Firstname,Place))
    print(Name,Firstname,Place)
    cursor.commit()

@anvil.server.callable
def update_item(NameId,Name,Firstname,Place):
    cursor.execute("UPDATE Names Set Name=?,Firstname=?,Place=? WHERE NameID=?",(Name,Firstname,Place,NameId))
    cursor.commit()


@anvil.server.callable
def delete_item(NameId):
    cursor.execute("DELETE from Names WHERE NameID=?", (NameId))
    print(NameId)
    cursor.commit()

#Hier die Cases

@anvil.server.callable()
def get_cases_for_userID(user_ID):
    cursor.execute("select * from Cases where Case_UserID=?",(user_ID))
    items=cursor.fetchall()
    return [
        {'Case_ID':item[0],'Case_UserID':item[1],'Case_LastName':item[2],'Case_FirstName':item[3],'Case_AHV':item[4],'Case_Canton':item[5],'Case_Year':item[6],'Case_Status':item[7]}
        for item in items
    ]
@anvil.server.callable()
def get_items_AB0_1(CaseID):
    print("es ist auf dem Server:",CaseID)
    cursor.execute("select * from Abschnitt0_1 where AB0_1_Case_ID=?",(CaseID))
    item = cursor.fetchone()
    if item==None: #case does not exist, let's give notice, then create one
        print("No record! - Create a record")
        add_case_AB0_1(CaseID)
        cursor.execute("select * from Abschnitt0_1 where AB0_1_Case_ID=?",(CaseID))
        item = cursor.fetchone()

    print("es sind so viele items:",item)
    return  {   'AB0_1_Case_ID':item[0],
            'AB0_FormType':item[1],
            'AB1_FamilyName':item[2],
            'AB1_FirstName':item[3],
            'AB1_AHV':item[4],
            'AB1_Birthdate':item[5],
            'AB1_Salutation':item[6],
            'AB1_Official_Address':item[7],
            'AB1_Official_PostCode':item[8],
            'AB1_Official_City':item[9],
            'AB1_Official_Country':item[10],
            'AB1_TelefoneFix':item[11],
            'AB1_TelefonPortable':item[12],
            'AB1_EMail_main':item[13],
            'AB1_EMail_second':item[14],
            'AB1_Current_Address':item[15],
            'AB1_Current_PostCode':item[16],
            'AB1_Current_City':item[17],
            'AB1_Current_Country':item[18],
            'AB1_Nationality':item[19],
            'AB1_Date_of_Domicil':item[20],
            'AB1_Date_of_Citizenship':item[21],
            'AB1_Typ_of_Permit_to_stay':item[22],
            'AB1_Issuedate_of_Permit':item[23],
            'AB1_DOK_Permit_to_Stay':item[24],
            'AB1_Civil_Status ':item[25],
            'AB1_Civil_Status_Date ':item[26],
            'AB1_DOK_LastCivil_Status':item[27],
            'AB1_Salutation_State':item[28]
            }

@anvil.server.callable()
def add_case_AB0_1(CaseID):
    cursor.execute("Insert into dbo.Abschnitt0_1 (AB0_1_Case_ID, AB0_FormType) values (?,?)",(CaseID,1))
    cursor.commit()

@anvil.server.callable()
def update_case_content(case_id,table_name,field_name,value,value_type):

    if value_type=="number":
        fsupdatestring="update {} set {} = {} where {}={}".format(table_name,field_name,value,'AB0_1_Case_ID',case_id)
        print(fsupdatestring)
        cursor.execute(fsupdatestring)
        cursor.commit()
    elif value_type=="text":
        fsupdatestring="update {} set {} = '{}' where {}={}".format(table_name,field_name,value,'AB0_1_Case_ID',case_id)
        print(fsupdatestring)
        cursor.execute(fsupdatestring)
        cursor.commit()

@anvil.server.callable()
def ahv_check(avh_string): # checks for validity of number, returns boolean
    AHV_Muster=re.compile('\A756.\d\d\d\d.\d\d\d\d.\d\d\Z')
    return(EAN13_check(avh_string,AHV_Muster))

def EAN13_check(string_to_check:str,pattern):
    if pattern.fullmatch(string_to_check):
        ahv_str=string_to_check[0:-1]
        regex=re.compile('[.]')
        ahv_clean_str=(regex.sub('',ahv_str))
        #print(ahv_clean_str)
        counter=0
        ahv_summe=0
        for s in ahv_clean_str:
            counter+=1
            #print(counter)
            nbr=int(s)

            if counter%2 == 0: # gerade
                #print("Die Zahl ist:", nbr,nbr*3)
                ahv_summe+=nbr*3
            else: #ungerade
                #print("Die Zahl ist:", nbr, nbr)
                ahv_summe+=nbr
            #print(ahv_summe)
        #print("AHV-Summe total", ahv_summe)
        prüfziffer=(10-ahv_summe%10)
        #print("PZ",prüfziffer)
        return(int(string_to_check[-1])==prüfziffer)

    else:
        return(False)

#print(ahv_check('755.9217.0769.85'))
@anvil.server.callable()
def add_new_case(user_id,LastName,FirstName,AHV,Canton,Year):
    if ahv_check(AHV):
        querystring = "insert into dbo.Cases (Case_UserID,Case_LastName,Case_FirstName,Case_AHV,Case_Canton,Case_Year," \
                      "Case_Status) VALUES (?,?,?,?,?,?,?) "
        query_values = (user_id,LastName,FirstName,AHV,Canton,Year,1)
        cursor.execute(querystring,query_values)
        print(querystring,query_values)
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        new_case_id=int(cursor.fetchone()[0])
        print("new Case ID:",new_case_id)
        return new_case_id
    else:
        print("AHV incorrect")
        return False

#print(add_new_case("[313649,524933170]","Schumacher","Franz II",'756.4853.9280.87',"LU",2020 ))

print(get_DocSet(1))
anvil.server.wait_forever()

