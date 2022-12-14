from functions import make_timestamp, get_user, get_user_id
from log_functions import log_add_log_entry
from connections import get_connection
from doc_set_definition import l_select_dsd_by_case, l_select_dsd_by_id
from doc_set_compositions import l_select_dsc_to_store_for_dsd,l_select_dsc_id_by_case_and_field
from cases_functions import l_get_dsd_reference_for_case_id,l_select_language_by_case_id, l_get_user_id_for_case_id
from field_descriptions import l_get_label, l_get_prompt
conn = get_connection()

cursor = conn.cursor()





def l_get_cdm_entries(case_id, dsc_id_ref):
    # cdm = Client Data Main
    query: str = """SELECT 
                        cdm_id, 
                        user_id_reference, 
                        case_id_reference, 
                        dsc_reference, 
                        payload_text, 
                        payload_number, 
                        payload_boolean, 
                        admin_user, 
                        admin_timestamp, 
                        admin_previous_entry, 
                        admin_active 
                    FROM client_data_main 
                    WHERE case_id_reference=? AND dsc_reference=? AND admin_active=? 
                    """
    cursor.execute(query,(case_id,dsc_id_ref,True))
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results





def l_get_all_cdm_entries():
    #cdm = Client Data Main
    query: str = """select  cdm_id, 
                            user_id_reference, 
                            case_id_reference, 
                            dsc_reference, 
                            payload_text, 
                            payload_number, 
                            payload_boolean, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active
                    from client_data_main
                    order by case_id_reference,dsc_reference"""
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_get_active_cdm_entries(case_id, dsc_id_ref):
    # cdm = Client Data Main
    query: str = """SELECT 
                        cdm_id, 
                        user_id_reference, 
                        case_id_reference, 
                        dsc_reference, 
                        payload_text, 
                        payload_number, 
                        payload_boolean, 
                        admin_user, 
                        admin_timestamp, 
                        admin_previous_entry, 
                        admin_active 
                    FROM client_data_main 
                    WHERE case_id_reference=? AND dsc_reference=? 
                    """
    cursor.execute(query,(case_id,dsc_id_ref))
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_get_cdm_entry_ID(case_id, dsc_id_ref):
    # cdm = Client Data Main
    query: str = """SELECT 
                        cdm_id 
                        FROM client_data_main 
                    WHERE case_id_reference=? AND dsc_reference=? 
                    """
    cursor.execute(query,(case_id,dsc_id_ref))
    result = cursor.fetchone()
    for row in result:
        a=row
        print(row)
    #print(a)
        return a



def l_select_cdm_by_id(id):
    cursor.execute("""select 
                        cdm_id, 
                        user_id_reference, 
                        case_id_reference, 
                        dsc_reference, 
                        payload_text, 
                        payload_number, 
                        payload_boolean, 
                        admin_user, 
                        admin_timestamp, 
                        admin_previous_entry, 
                        admin_active from dbo.client_data_main 
                      where cdm_id=?""",
                        id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
        #print(results[0])
    return results[0]


def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_add_log_entry(user, current_timestamp, table_name,table_id, payload)


def l_add_cdm_entry(user_id, case_id, dsc_id,pl_text=None,pl_number=None,pl_boolean=None):
    admin_user=get_user()
    timestamp=make_timestamp()
    cursor.execute("""insert into dbo.client_data_main 
                    (user_id_reference, 
                     case_id_reference,
                     dsc_reference,
                     payload_text,
                     payload_number,
                     payload_boolean, 
                     admin_user, 
                     admin_timestamp, 
                     admin_previous_entry,
                     admin_active) """
                   "values (?,?,?,?,?,?,?,?,?,?)",
                   (user_id, case_id, dsc_id, pl_text, pl_number, pl_boolean,admin_user, timestamp,0,1))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    return last_id


def l_update_cdm_entry(user_id, case_id, field_id,pl_text,pl_number,pl_boolean):
    print("Update läuft mit folgenden Paras:", user_id,case_id,field_id,pl_text,pl_number,pl_boolean)
    dsc_id=l_select_dsc_id_by_case_and_field(case_id,field_id)
    id_to_change=l_get_cdm_entry_ID(case_id, dsc_id)
    current_admin_user=get_user()
    current_timestamp = make_timestamp()
    current_table_name = 'client_data_main'
    current_table_id=id_to_change
    current_payload=str(l_select_cdm_by_id(id_to_change))
    print("------>",current_admin_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_admin_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)
    cursor3=conn.cursor()
    cursor3.execute("""UPDATE 
                            client_data_main 
                       SET 
                            user_id_reference=?,
                            case_id_reference=?,
                            dsc_reference=?,
                            payload_text=?,
                            payload_number=?,
                            payload_boolean=?,
                            admin_user=?,
                            admin_timestamp=?,
                            admin_previous_entry=?,
                            admin_active=?
                        WHERE 
                            cdm_id=?""",
                    (user_id, case_id, dsc_id, pl_text, pl_number, pl_boolean, current_admin_user, current_timestamp, previous_log_entry, 1, id_to_change))
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

def l_ensure_completeness_of_stores(case_id):
    current_user=get_user_id()
    current_dsd_id = l_select_dsd_by_case(case_id)
    current_language_short=l_select_language_by_case_id(case_id)
    current_docsets = l_select_dsc_to_store_for_dsd(current_dsd_id, current_language_short)
    counter=0
    for ds in current_docsets:
        print(counter)
        print(ds)
        counter +=1
        print(ds['ft_stores_state'])
        print(ds['ft_stores_data'])
        current_dsc_id=ds['dsc_id']
        if l_get_cdm_entries(current_dsd_id,current_dsc_id)==[]:
            l_add_cdm_entry(current_user,current_dsd_id,current_dsc_id,'Test - delete',99999,False)
            print (current_dsc_id, "added")
        else:
            print(current_dsc_id, " exists!")

def l_get_fd(case_id, field_id):
    print("l_get_fd, parameters:",case_id, field_id)
    current_dsd=l_get_dsd_reference_for_case_id(case_id)
    current_lang=l_select_language_by_case_id(case_id)
    current_dsc=l_select_dsc_id_by_case_and_field(case_id,field_id)
    current_userID=l_get_user_id_for_case_id(case_id)
    print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc,current_userID)
    result= {}
    query= """select 
                payload_text
              from 
                client_data_main
              where
                dsc_reference=?
            """
    cursor.execute(query,current_dsc)
    payload= cursor.fetchone()
    print("Payload", payload)

    print('get_fd payload',payload)
    if payload == None:
        print("No record found")
        l_add_cdm_entry(current_userID, case_id, current_dsc, pl_text="Empty", pl_number=0, pl_boolean=1)
        print('missing cdm record added:!')
        cursor.execute(query,current_dsc)
        payload=cursor.fetchone()
        print('New payload:',payload)
    result['payload']=payload[0]
    print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc, payload)
    print(l_get_label(current_lang, field_id))
    result['label']=l_get_label(current_lang,field_id)
    result['prompt']=l_get_prompt(current_lang,field_id)
    print(result)
    return result

#print(l_get_fd(case_id=100,field_id=160))




#l_ensure_completeness_of_stores(100)
#print(l_get_cdm_entries(100,200))
#print(l_select_cdm_by_id(190))
# print(l_add_cdm_entry(100, 100, 150,pl_text="Hirtenhofweg 11",pl_number=31415,pl_boolean=1))
#l_update_cdm_entry(100, 110, 150,'Benziwil 27',6020,False)