import cases_functions
import doc_set_definition
import fields_functions
import functions
from functions import make_timestamp, get_user
from log_functions import log_add_log_entry
from connections import get_connection

conn = get_connection()

cursor = conn.cursor()
def l_get_active_dsc():
    query: str = "SELECT dsc_id, dsd_reference, field_id_reference, dsc_sequence, admin_user, admin_timestamp, admin_previous_entry, admin_active " \
                 "from dbo.doc_set_comp where admin_active=1 " \
                 "order by dsc_id,dsc_sequence"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

def l_get_all_dsc():
    query: str = "select dsc_id, dsd_reference, field_id_reference, dsc_sequence, admin_user, admin_timestamp, admin_previous_entry, admin_active  from dbo.doc_set_comp order by dsc_id,dsc_sequence"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_select_dsc_by_dsd(dsd):
    cursor.execute("""select 
                            dsc_id, dsd_reference, 
                            field_id_reference, 
                            dsc_sequence, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active 
                        from 
                            dbo.doc_set_comp 
                        where 
                            dsd_reference=?"""
                        , dsd)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

#print("dsc 120:", l_select_dsc_by_dsd(120))


def l_select_dsc_to_store_for_dsd(case_dsd, case_language):
    query="""
    SELECT
        doc_set_comp.dsc_sequence,
        doc_set_comp.dsc_id,
        doc_set_def.dsd_name,
        fields.field_id,
        fields.field_name,
        dbo.languages.lang_short,
        dbo.field_types.ft_stores_state,
        dbo.field_types.ft_stores_data
    FROM
        dbo.doc_set_comp
            INNER JOIN dbo.doc_set_def ON dbo.doc_set_comp.dsd_reference = dbo.doc_set_def.dsd_id
            INNER JOIN dbo.fields ON dbo.doc_set_comp.field_id_reference = dbo.fields.field_id
            INNER JOIN dbo.field_types ON dbo.fields.field_typ_id = dbo.field_types.ft_id
            INNER JOIN dbo.field_descriptions ON dbo.fields.field_id = dbo.field_descriptions.field_id_reference
            INNER JOIN dbo.languages ON dbo.field_descriptions.language_id_reference = dbo.languages.lang_id
    WHERE
    (dsd_id = ?) AND (languages.lang_short = ?) AND ((field_types.ft_stores_data=1) OR (field_types.ft_stores_state=1))
    ORDER BY
    dbo.doc_set_comp.dsc_sequence """
    cursor.execute(query,(case_dsd,case_language))
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    #print(results)
    return results

#unregistered yet

def l_select_required_form_data(case_dsd,dsc_id, case_language,):   #<--- not working
    query="""
    SELECT
        doc_set_comp.dsc_sequence,
        doc_set_comp.dsc_id,
        doc_set_def.dsd_name,
        fields.field_id,
        fields.field_name,
        dbo.languages.lang_short,
        dbo.field_types.ft_stores_state,
        dbo.field_types.ft_stores_data
    FROM
        dbo.doc_set_comp
            INNER JOIN dbo.doc_set_def ON dbo.doc_set_comp.dsd_reference = dbo.doc_set_def.dsd_id
            INNER JOIN dbo.fields ON dbo.doc_set_comp.field_id_reference = dbo.fields.field_id
            INNER JOIN dbo.field_types ON dbo.fields.field_typ_id = dbo.field_types.ft_id
            INNER JOIN dbo.field_descriptions ON dbo.fields.field_id = dbo.field_descriptions.field_id_reference
            INNER JOIN dbo.languages ON dbo.field_descriptions.language_id_reference = dbo.languages.lang_id
    WHERE
    (dsd_id = ?) AND (dsc_id = ?) And (languages.lang_short = ?)
    ORDER BY
    dbo.doc_set_comp.dsc_sequence """
    cursor.execute(query,(case_dsd,dsc_id,case_language))
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    #print(results)
    return results



def l_select_dsc_by_id(id):
    cursor.execute("select dsc_id, dsd_reference, field_id_reference, dsc_sequence, admin_user, admin_timestamp, admin_previous_entry, admin_active from dbo.doc_set_comp where dsc_id=?",
                   id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
        #print(results[0])
    return results[0]

def l_select_dsc_id_by_case_and_field(case_id,field_id):
    cursor.execute("""select 
                        dsc_id
                       from 
                        dbo.doc_set_comp
                            inner join doc_set_def on  doc_set_comp.dsd_reference = doc_set_def.dsd_id
                            inner join EasyEL.dbo.cases on cases.dsd_reference=doc_set_def.dsd_id
                        where 
                        (cases.case_id=?) AND (field_id_reference = ?)""",
                        (case_id,field_id))
    result=cursor.fetchone()
    # print ("dsc_id ist:", result)
    if result is None:
        return None
    else:
        return result[0]
            #print(results[0]

#print(l_select_dsc_id_by_case_and_field(100,300))





def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_add_log_entry(user, current_timestamp, table_name,table_id, payload)


def l_add_dsc_entry(dsd_reference,field_id,sequence):
    user=get_user()
    timestamp=make_timestamp()
    cursor.execute("""insert into 
                            dbo.doc_set_comp (
                                dsd_reference, 
                                field_id_reference, 
                                dsc_sequence, 
                                admin_user, 
                                admin_timestamp, 
                                admin_previous_entry, 
                                admin_active) """
                   "values (?,?,?,?,?,?,?)""",
                   (dsd_reference, field_id, sequence, user, timestamp,0,1))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    return last_id

#l_add_dsc_entry(120,110,99)

def l_update_dsc(id_to_change, reference, field_id,sequence):
    #print('l_updateft:',id_to_change,reference,field_id,sequence)
    current_user=get_user()
    current_timestamp = make_timestamp()
    current_table_name = 'doc_set_comp'
    current_table_id=id_to_change
    current_payload=str(l_select_dsc_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)
    cursor3=conn.cursor()
    cursor3.execute("UPDATE doc_set_comp SET dsd_reference=?,field_id_reference=?,dsc_sequence=?,admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? "
                    "WHERE dsc_id=?",
                    (reference, field_id,sequence, current_user, current_timestamp, previous_log_entry,1, id_to_change))
    cursor3.commit()


def l_change_status_dsc_by_dsd(dsd_reference,new_status):
    #print(short_name)
    current_user=get_user()
    #print(current_user)
    current_timestamp = make_timestamp()
    current_table_name = 'doc_set_comp'
    id_to_change=l_select_dsc_by_dsd(dsd_reference)['dsc_id']
    current_table_id = id_to_change
    current_payload=str(l_select_dsc_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    cursor.execute("UPDATE doc_set_comp SET admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? WHERE dsd_reference=?",(current_user,current_timestamp,previous_log_entry,new_status,dsd_reference))
    cursor.commit()


def l_change_status_dsc_by_id(id_to_change:int,new_status:int):
    current_user=get_user()
    #print(current_user)
    current_timestamp = make_timestamp()
    current_table_name = 'doc_set_comp'
    current_table_id=id_to_change
    current_payload=str(l_select_dsc_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)


    cursor.execute("UPDATE doc_set_comp SET admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? WHERE dsc_id=?",(current_user,current_timestamp,previous_log_entry,new_status,id_to_change))
    cursor.commit()

def l_ensure_completeness_of_shadow_dsc(dsd_id=120):
    current_user=functions.get_user_id()
    current_dsd_id = dsd_id
    counter=0
    soll_dsc=fields_functions.l_get_active_fields_for_shadow_dsd()
    current_content= l_select_dsc_by_dsd(dsd_id)
    if current_content==[]:
        for f in soll_dsc:

            dsc_new= l_add_dsc_entry(current_dsd_id, f['field_id'], f['field_sequence'])
            print(f," added with Id: ", dsc_new)
    else:
        current_dsc_ids=[]
        for c in current_content:
            current_dsc_ids.append(c['field_id_reference'])

        for f in soll_dsc:
            if f['field_id'] in current_dsc_ids:
                pass
            else:
                dsc_new = l_add_dsc_entry(current_dsd_id, f['field_id'], f['field_sequence'])
                print(f, " added with Id: ", dsc_new)

print(l_ensure_completeness_of_shadow_dsc (120))

     #

