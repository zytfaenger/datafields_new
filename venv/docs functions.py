from functions import make_timestamp, get_user
from log_functions import log_add_log_entry
from connections import get_connection

conn = get_connection()

cursor = conn.cursor()

def l_get_active_docs():
    query: str = """SELECT 
                        doc_id, 
                        case_id_reference, 
                        field_id_reference, 
                        doc_desc_short, 
                        doc_desc_long, 
                        doc_version, 
                        doc_date, 
                        doc_file, 
                        doc_pending, 
                        doc_valid, 
                        doc_next_version, 
                        doc_previous_version,
                        admin_user, 
                        admin_timestamp, 
                        admin_previous_entry, 
                        admin_active
                    FROM 
                        docs
                    WHERE 
                        admin_active=1 
                    ORDER BY case_id_reference,field_id_reference"""

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_get_all_docs():
    query: str = """SELECT 
                            doc_id, 
                            case_id_reference, 
                            field_id_reference, 
                            doc_desc_short, 
                            doc_desc_long, 
                            doc_version, 
                            doc_date, 
                            doc_file, 
                            doc_pending, 
                            doc_valid, 
                            doc_next_version, 
                            doc_previous_version,
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active
                        FROM 
                            docs
                        ORDER BY case_id_reference,field_id_reference"""

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_select_doc_by_id(id):
    cursor.execute("""select 
                           doc_id, 
                            case_id_reference, 
                            field_id_reference, 
                            doc_desc_short, 
                            doc_desc_long, 
                            doc_version, 
                            doc_date, 
                            doc_file, 
                            doc_pending, 
                            doc_valid, 
                            doc_next_version, 
                            doc_previous_version,
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active
                        from 
                            docs 
                        where doc_id=?""", id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
        #print(results[0])
    return results[0]

#print(l_select_case_by_id(110))



def l_get_docs_for_case_id(ca_id):
    query="""
        select 
                doc_id, 
                case_id_reference, 
                field_id_reference, 
                doc_desc_short, 
                doc_desc_long, 
                doc_version, 
                doc_date, 
                doc_file, 
                doc_pending, 
                doc_valid, 
                doc_next_version, 
                doc_previous_version,
                admin_user, 
                admin_timestamp, 
                admin_previous_entry, 
                admin_active
        from
         docs
        where
         case_id_reference=?   
    """
    cursor.execute(query,ca_id)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
        # print(results[0])
    if results == []:
        return None
    else:
        return results[0]


# print(l_get_docs_for_case_id(100))

def l_get_docs_for_a_field_by_case(field_id, ca_id):
    print("Not defined yet")

def l_get_case_id_client_id_for_doc_id(d_id):
    query="""
        select 
         case_id_reference,
         cases.client_id_ref
        from
         docs
            inner join EasyEL.dbo.cases on case_id = EasyEL.dbo.docs.case_id_reference
        where
         doc_id=?   
    """
    cursor.execute(query,d_id)
    result = cursor.fetchone()
    rlist=[]
    for r in result:
        rlist.append(r)

    print(rlist)
    return rlist  # case_id first, then client_id

# print(l_get_case_id_client_id_for_doc_id(1))

def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_add_log_entry(user, current_timestamp, table_name,table_id, payload)



def l_add_doc(client_id,dsd_reference,language_ref,user_id):
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