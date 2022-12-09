import pyodbc
import uplink as uplink
import anvil.server
import re
from functions import regenerate_password, make_timestamp, get_user
from language_functions import *
from log import *

# Dieses Script fügt Daten in eine Azure-Datenbank ein!

driver = "ODBC Driver 18 for SQL Server"
server = 'tcp:msfp.database.windows.net,1433'
database = 'EasyEL'
encrypt = 'yes'
username = 'fschumacher'
password = regenerate_password()
connectstring='DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';ENCRYPT='+encrypt+';UID='+username+';PWD='+password


# connectstring = 'jdbc:sqlserver://msfp.database.windows.net:1433;database=EasyEL;
# user=fschumacher@msfp;password=password;encrypt=true;trustServerCertificate=false;
# hostNameInCertificate=*.database.windows.net;loginTimeout=30;'
print(connectstring)
conn = pyodbc.connect(connectstring)

cursor = conn.cursor()

anvil.server.connect('server_PJMM2F27IXZFCGTC4LUMFXPN-OZFH7FH3ARG7HIGO')

@anvil.server.callable
def get_active_languages():
    return l_get_active_languages()


@anvil.server.callable
def get_all_languages():
    return l_get_all_languages()


@anvil.server.callable()
def select_language_by_shortname(short_name):
    cursor.execute("select lang_id, lang_short, lang_german, lang_local from dbo.languages where lang_short=?",
                   short_name)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


@anvil.server.callable()
def select_language_by_id(lang_id):
    cursor.execute("select lang_id, lang_short, lang_german, lang_local, admin_user, admin_timestamp,admin_previous_entry,admin_active "
                   "from dbo.languages "
                   "where lang_id=?",
                   lang_id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results[0]


def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    cursor2=conn.cursor()
    cursor2.execute("insert into dbo.log (editing_user,timestamp, table_name, reference_to_table_id, payload)"
                   "values (?,?,?,?,?)",
                   (user, current_timestamp, table_name, table_id, payload))
    cursor2.commit()
    cursor2.execute("SELECT @@IDENTITY AS ID;")
    cursor2.close
    last_id = int(cursor2.fetchone()[0])
    return last_id





@anvil.server.callable
def add_language(short_name, german_name, local_name):
    user=get_user()
    timestamp=make_timestamp()
    cursor.execute("insert into dbo.languages (lang_short, lang_german, lang_local,admin_user,admin_timestamp,admin_previous_entry,admin_active) "
                   "values (?,?,?,?,?,?,?)",
                   (short_name, german_name, local_name, user, timestamp,0,1))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    return last_id


@anvil.server.callable
def update_language(id_to_change, short_name, german_name, local_name):
    current_user=get_user()
    current_timestamp = make_timestamp()
    current_table_name = 'languages'
    current_table_id=id_to_change
    current_payload=str(select_language_by_id(id_to_change))
    print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                    current_table_name,
                                     current_table_id,
                                     current_payload)
    print(previous_log_entry)
    cursor3=conn.cursor()
    cursor3.execute("UPDATE languages SET lang_short=?,lang_german=?,lang_local=?,admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? "
                    "WHERE lang_id=?",
                    (short_name, german_name, local_name, current_user, current_timestamp, previous_log_entry,1, id_to_change))
    cursor3.commit()




@anvil.server.callable
def change_status_language_by_short_name(short_name,new_status:int):
    #print(short_name)
    current_user=get_user()
    #print(current_user)
    current_timestamp = make_timestamp()
    current_table_name = 'languages'
    current_table_id=id_to_change
    current_payload=str(select_language_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    cursor.execute("UPDATE languages SET admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? WHERE lang_short=?",(current_user,current_timestamp,previous_log_entry,new_status,short_name))
    cursor.commit()


@anvil.server.callable
def change_status_language_by_id(id_to_change:int,new_status:int):
    current_user=get_user()
    #print(current_user)
    current_timestamp = make_timestamp()
    current_table_name = 'languages'
    current_table_id=id_to_change
    current_payload=str(select_language_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)


    cursor.execute("UPDATE languages SET admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? WHERE lang_id=?",(current_user,current_timestamp,previous_log_entry,new_status,id_to_change))
    cursor.commit()

# print(get_languages())
# last_lang = add_language('en-uk2',
#                          'English - Vereinigtes Königreich',
#                          'British English',
#                          '1399c078-6c0f-11ed-b0bc-acde48001122',
#                          make_timestamp())
# print(last_lang)
print(get_all_languages())
print(get_active_languages())
# delete_language_by_short_name('en-uk')
#
# result = get_all_languages()
# print(result)
# result = get_active_languages()
# print(result)
#
# delete_language_by_id(52)
#
# result = get_all_languages()
# print(result)
# result = get_active_languages()
# print(result)

# UUID = ('1399c078-6c0f-11ed-b0bc-acde48001122')
# ts=make_timestamp()
# print(UUID,ts)
# print(8, 'EN-UK', result['lang_german'], result['lang_local'], UUID, ts)
# update_language(last_lang, 'EN-UK995', 'Englisch', 'English', UUID, ts)
# print(get_languages())
anvil.server.wait_forever()
