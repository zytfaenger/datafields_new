from functions import make_timestamp, get_user
from log_functions import log_add_log_entry
from connections import get_connection

conn = get_connection()

cursor = conn.cursor()
def l_get_active_dsd():
    query: str = "SELECT dsd_id, dsd_name, dsd_domain, dsd_year, admin_user, admin_timestamp, admin_previous_entry, " \
                 "admin_active from dbo.doc_set_def where admin_active=1 order by dsd_year,dsd_domain,dsd_name "
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

def l_get_all_dsd():
    query: str = "select dsd_id, dsd_name, dsd_domain, dsd_year, admin_user, admin_timestamp, admin_previous_entry, " \
                 "admin_active  from dbo.doc_set_def order by dsd_year,dsd_domain,dsd_name"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_select_dsd_by_id(id):
    cursor.execute("select dsd_id, dsd_name, dsd_domain, dsd_year, admin_user, admin_timestamp, admin_previous_entry, "
                   "admin_active from dbo.doc_set_def where dsd_id=?",
                   id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
        #print(results[0])
    return results[0]


def l_select_dsd_by_case(case_id):
    cursor.execute("""select 
                        cases.Case_ID,
                        cases.dsd_reference
                    from 
                        EasyEL.dbo.cases
                    where 
                        case_id=?""",
                   case_id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    #print(results[0])
    return results[0]['dsd_reference']



def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_add_log_entry(user, current_timestamp, table_name,table_id, payload)


def l_add_dsd_entry(name, domain, year):
    user=get_user()
    timestamp=make_timestamp()
    cursor.execute("insert into dbo.doc_set_def (dsd_name,dsd_domain,dsd_year, admin_user, admin_timestamp, admin_previous_entry, admin_active) "
                   "values (?,?,?,?,?,?,?)",
                   (name, domain, year, user, timestamp,0,1))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    return last_id


def l_update_dsd(id_to_change, name, domain, year):
    #print('l_updateft:',id_to_change,reference,field_id,sequence)
    current_user=get_user()
    current_timestamp = make_timestamp()
    current_table_name = 'doc_set_def'
    current_table_id=id_to_change
    current_payload=str(l_select_dsd_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)
    cursor3=conn.cursor()
    cursor3.execute("UPDATE doc_set_def SET dsd_name=?,dsd_domain=?,dsd_year=?,admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? "
                    "WHERE dsd_id=?",
                    (name, domain, year, current_user, current_timestamp, previous_log_entry, 1, id_to_change))
    cursor3.commit()


def l_change_status_dsd_by_id(id_to_change:int,new_status:int):
    current_user=get_user()
    #print(current_user)
    current_timestamp = make_timestamp()
    current_table_name = 'doc_set_def'
    current_table_id=id_to_change
    current_payload=str(l_select_dsd_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)


    cursor.execute("UPDATE doc_set_def SET admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? WHERE dsd_id=?",(current_user,current_timestamp,previous_log_entry,new_status,id_to_change))
    cursor.commit()

