from functions import make_timestamp, get_user
from log_functions import log_add_log_entry
from connections import get_connection

conn = get_connection()

cursor = conn.cursor()
def l_get_active_cases():
    query: str = """SELECT 
                        case_id, 
                        client_id_ref, 
                        dsd_reference, 
                        language_ref, 
                        user_id, 
                        admin_user, 
                        admin_timestamp, 
                        admin_previous_entry, 
                        admin_active  
                    FROM 
                        EasyEL.dbo.cases 
                    WHERE 
                        admin_active=1 
                    ORDER BY user_id"""

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_get_all_cases():
    query: str = """SELECT 
                        case_id, 
                        client_id_ref, 
                        dsd_reference, 
                        language_ref, 
                        user_id, 
                        admin_user, 
                        admin_timestamp, 
                        admin_previous_entry, 
                        admin_active  
                    FROM 
                        EasyEL.dbo.cases 
                    ORDER BY user_id"""

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_select_case_by_id(id):
    cursor.execute("""select 
                            case_id, 
                            client_id_ref, 
                            dsd_reference, 
                            language_ref, 
                            user_id, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active 
                        from 
                            EasyEL.dbo.cases 
                        where case_id=?""", id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
        #print(results[0])
    return results[0]

#print(l_select_case_by_id(110))



def l_get_dsd_reference_for_case_id(ca_id):
    query="""
        select dsd_reference 
        from
         EasyEL.dbo.cases
        where
         case_id=?   
    """
    cursor.execute(query,ca_id)
    result = cursor.fetchone()
    for r in result:
        dsd=r
    print('l_get_dsd_reference_for_case_id',dsd)
    print('l_get_dsd_reference_for_case_id:',ca_id, " ist: dsd:",dsd)
    return dsd

#print(l_get_dsd_reference_for_case_id(100))

def l_get_user_id_for_case_id(ca_id):
    query="""
        select user_id 
        from
         EasyEL.dbo.cases
        where
         case_id=?   
    """
    cursor.execute(query,ca_id)
    result = cursor.fetchone()
    for r in result:
        user_id=r
    #print(dsd)
    #print(ca_id, " ist: dsd:",dsd)
    return user_id

def l_get_client_id_for_case_id(ca_id):
    query="""
        select client_id_ref 
        from
         EasyEL.dbo.cases
        where
         case_id=?   
    """
    cursor.execute(query,ca_id)
    result = cursor.fetchone()
    for r in result:
        client_id=r
    #print(dsd)
    #print(ca_id, " ist: dsd:",dsd)
    return client_id

def l_select_language_by_case_id(case_id):
    cursor.execute("""select 
                        cases.Case_ID,
                        cases.language_ref,
                        dbo.languages.lang_short
                       from 
                            EasyEL.dbo.cases
                                inner join dbo.languages on languages.lang_id = EasyEL.dbo.cases.language_ref
                        where 
                            cases.case_id=?""",
                       case_id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    # print(results[0])
    return results[0]['lang_short']

#print(l_get_dsd_reference_for_case_id(110))


def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_add_log_entry(user, current_timestamp, table_name,table_id, payload)



def l_add_case(client_id,dsd_reference,language_ref,user_id):
    admin_user=get_user()
    timestamp=make_timestamp()
    query= """insert into 
                     EasyEL.dbo.cases (client_id_ref, 
                                        dsd_reference, 
                                        language_ref, 
                                        user_id, 
                                        admin_user, 
                                        admin_timestamp, 
                                        admin_previous_entry, 
                                        admin_active)
                                       values (?,?,?,?,?,?,?,?)"""
    cursor.execute(query,(client_id,dsd_reference,language_ref,user_id, admin_user, timestamp,0,1))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    return last_id

#l_add_case(110,100,1,100)

def l_update_cases(id_to_change, client_id_ref,dsd_reference,language_ref,user_id):
    #print('l_updateft:',id_to_change,type,description,sequence)
    current_adminuser=get_user()
    current_timestamp = make_timestamp()
    current_table_name = 'cases'
    current_table_id=id_to_change
    current_payload=str(l_select_case_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_adminuser,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)
    cursor3=conn.cursor()
    query="""   UPDATE 
                    cases 
                SET 
                    client_id_ref=?,
                    dsd_reference=?,
                    language_ref=?,
                    user_id=?,
                    admin_user=?,
                    admin_timestamp=?,
                    admin_previous_entry=?,
                    admin_active=?
                WHERE 
                    EasyEL.dbo.cases.case_id=?"""
    cursor.execute(query, (client_id_ref, dsd_reference, language_ref, user_id, current_adminuser, current_timestamp, previous_log_entry,1, id_to_change))
    cursor3.commit()


#l_update_cases(160, 110,100,1,100)



def l_change_status_case_by_id(id_to_change:int,new_status:int):
    current_user=get_user()
    #print(current_user)
    current_timestamp = make_timestamp()
    current_table_name = 'cases'
    current_table_id=id_to_change
    current_payload=str(l_select_case_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)


    cursor.execute("""  UPDATE 
                            EasyEL.dbo.cases 
                        SET 
                            admin_user=?,
                            admin_timestamp=?,
                            admin_previous_entry=?,
                            admin_active=? 
                        WHERE case_id=?""",
                       (current_user,current_timestamp,previous_log_entry,new_status,id_to_change))
    cursor.commit()