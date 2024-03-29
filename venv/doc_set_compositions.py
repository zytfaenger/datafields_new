import doc_set_definition
import field_types
import fields_functions
import functions
import log_functions
import connections
import globals as G


def l_get_active_dsc():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT dsc_id,
                         dsd_reference,
                         field_id_reference, 
                         dsc_sequence, 
                         admin_user, 
                         admin_timestamp, 
                         admin_previous_entry, 
                         admin_active 
                     from 
                       dbo.doc_set_comp 
                     where 
                         admin_active=1 
                      order by 
                        dsd_reference,dsc_sequence"""
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# [print(d) for d in l_get_active_dsc()]

def l_get_all_dsc():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """select 
                            dsc_id, 
                            dsd_reference, 
                            field_id_reference, 
                            dsc_sequence, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active  
                        from 
                            dbo.doc_set_comp 
                        order by 
                            dsc_id,dsc_sequence"""
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
# [print(d) for d in l_get_all_dsc()]

def l_select_dsc_by_dsd(dsd):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                                EasyEL.dbo.doc_set_comp.dsc_id, 
                                EasyEL.dbo.doc_set_comp.dsd_reference, 
                                EasyEL.dbo.doc_set_comp.field_id_reference, 
                                EasyEL.dbo.fields.anvil_component_ref,
                                EasyEL.dbo.doc_set_comp.dsc_sequence, 
                                EasyEL.dbo.doc_set_comp.admin_user, 
                                EasyEL.dbo.doc_set_comp.admin_timestamp, 
                                EasyEL.dbo.doc_set_comp.admin_previous_entry, 
                                EasyEL.dbo.doc_set_comp.admin_active 
                            from 
                                EasyEL.dbo.doc_set_comp
                            JOIN dbo.fields on dbo.fields.field_id = dbo.doc_set_comp.field_id_reference
                            where 
                                dsd_reference=?
                            
                            order by
                                dsc_sequence"""
                            , dsd)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# print("dsc 130:", l_select_dsc_by_dsd(120))
# print('dsd = 130')
# [print(d) for d in l_select_dsc_by_dsd(130)]
# [print(d['dsc_sequence'],d['anvil_component_ref']) for d in l_select_dsc_by_dsd('130')]

def l_get_anvil_field_list_for_dsd_id(dsd_id):
    acl = {}
    for d in l_select_dsc_by_dsd(dsd_id):
        acl[d['anvil_component_ref']]=True
    acl.keys()
    fskeys=list(acl.keys())
    return fskeys

# print(l_get_anvil_field_list_for_dsd_id(130))
# for a in l_get_anvil_field_list_for_dsd_id(130):
#     print(a)
def l_get_anvil_field_list_for_dsd_id_in_sequence(dsd_id):
    acl_ranked =[] #Anvil component list ranked
    [acl_ranked.append((d['dsc_sequence'],d['anvil_component_ref'])) for d in l_select_dsc_by_dsd(dsd_id)]
    return acl_ranked

# a=l_get_anvil_field_list_for_dsd_id_in_sequence(130)
# for c in a:
#     print(c)



def l_select_dsc_to_store_for_case_id(case_id):
    dsd_for_case=doc_set_definition.l_select_dsd_by_case(case_id)
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
            select 
                dsc_id, 
                dsd_reference, 
                field_id_reference, 
                dsc_sequence, 
                admin_user, 
                admin_timestamp, 
                admin_previous_entry, 
                admin_active 
            from 
                doc_set_comp
            where
                dsd_reference=?
            order by 
                dsc_sequence
            """
        cursor.execute(query,dsd_for_case)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        qres=cursor.fetchall()
        results = []
        for row in qres:
            results.append(dict(zip(columns, row)))
        #print(results)
        return results

# print(l_select_dsc_to_store_for_case_id(400))





def l_select_required_form_data(case_dsd,dsc_id, case_language,):   #<--- not working
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("select dsc_id, dsd_reference, field_id_reference, dsc_sequence, admin_user, admin_timestamp, admin_previous_entry, admin_active from dbo.doc_set_comp where dsc_id=?",
                       id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            #print(results[0])
        return results[0]

# print(l_select_dsc_by_id(250))

def l_select_dsc_id_by_case_and_field(case_id,field_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                            EasyEL.dbo.cases.case_id,
                            EasyEL.dbo.doc_set_comp.dsc_id
                           from 
                            EasyEL.dbo.cases
                            join EasyEL.dbo.doc_set_def on EasyEL.dbo.doc_set_def.dsd_id = EasyEL.dbo.cases.dsd_reference
                            join EasyEL.dbo.doc_set_comp on doc_set_comp.dsd_reference = EasyEL.dbo.doc_set_def.dsd_id                                                                
                            where 
                            (cases.case_id=?) AND (field_id_reference = ?)""",
                            (case_id,field_id))
        result=cursor.fetchone()
        # print ("dsc_id ist:", result)
        if result is None:
            current_field_fype_id = fields_functions.l_select_field_by_id(field_id)['field_typ_id'] #get me the field type please
            in_shadow_case = doc_set_definition.l_is_shadow_case(case_id)
            if in_shadow_case==False:
               msg=("select_dsc_id_by_case_and_field: no record in current case for case {}, field: {} -->strange").format(case_id,field_id)
               print(msg)
               return None
            else:
                field_is_Shadow =  field_types.l_select_field_type_by_id(current_field_fype_id)['ft_shadow_store']   #is it shadow?
                if field_is_Shadow is False:
                    msg = ("from select_dsc_id_by_case_and_field --> field_id: {} has field_type: {} where shadow is {}").format(field_id,current_field_fype_id,field_is_Shadow)
                    print(msg)
                else:
                    msg = ("from select_dsc_id_by_case_and_field --> for field_id = {} shadow = true, but record not in store yet  --> if shadow-case,check completeness of shadow!").format(field_id)
                    print(msg)
                return None
        else:
            return result[1]
                #print(results[0]

def l_select_dsc_id_by_case_and_field_modern(anvil_user_id, case_id,field_id):

    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        cursor.execute("""select 
                            EasyEL.dbo.cases.case_id,
                            EasyEL.dbo.doc_set_comp.dsc_id
                           from 
                            EasyEL.dbo.cases
                            join EasyEL.dbo.doc_set_def on EasyEL.dbo.doc_set_def.dsd_id = EasyEL.dbo.cases.dsd_reference
                            join EasyEL.dbo.doc_set_comp on doc_set_comp.dsd_reference = EasyEL.dbo.doc_set_def.dsd_id                                                                
                            where 
                            (cases.case_id=?) AND (field_id_reference = ?)""",
                            (case_id,field_id))
        result=cursor.fetchone()
        # print ("dsc_id ist:", result)
        if result is None:
            current_field_fype_id = fields_functions.l_select_field_by_id(field_id)['field_typ_id'] #get me the field type please
            in_shadow_case = doc_set_definition.l_is_shadow_case(case_id)
            if in_shadow_case==False:
               msg=("select_dsc_id_by_case_and_field: no record in current case for case {}, field: {} -->strange").format(case_id,field_id)
               print(msg)
               return None
            else:
                field_is_Shadow =  field_types.l_select_field_type_by_id(current_field_fype_id)['ft_shadow_store']   #is it shadow?
                if field_is_Shadow is False:
                    msg = ("from select_dsc_id_by_case_and_field --> field_id: {} has field_type: {} where shadow is {}").format(field_id,current_field_fype_id,field_is_Shadow)
                    print(msg)
                else:
                    msg = ("from select_dsc_id_by_case_and_field --> for field_id = {} shadow = true, but record not in store yet  --> if shadow-case,check completeness of shadow!").format(field_id)
                    print(msg)
                return None
        else:
            return result[1]
                #print(results[0]


# print(l_select_dsc_id_by_case_and_field(400,510))


#print(l_select_dsc_id_by_case_and_field(400,110)) # textfeld in formular o.k.
# print(l_select_dsc_id_by_case_and_field(120,160)) # textfeld in formular in shadow nicht enthalten
# print(l_select_dsc_id_by_case_and_field(110,999)) # textfeld in formular nicht enhalten -> sollte nicht sein






def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name,table_id, payload)


def l_add_dsc_entry(dsd_reference,field_id,sequence):
    user=functions.get_user()   #change
    timestamp=functions.make_timestamp()
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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

# l_add_dsc_entry(120,110,99)

def l_update_dsc(id_to_change, reference, field_id,sequence):
    #print('l_updateft:',id_to_change,reference,field_id,sequence)
    current_user=functions.get_user()
    current_timestamp = functions.make_timestamp()
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
    azure = connections.Azure()
    with azure:
        cursor3 = azure.conn.cursor()
        cursor3.execute("""UPDATE 
                                doc_set_comp 
                            SET 
                                dsd_reference=?,
                                field_id_reference=?,
                                dsc_sequence=?,
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=?
                            WHERE 
                                dsc_id=?""",
                                (reference,
                                 field_id,
                                 sequence,
                                 current_user,
                                 current_timestamp,
                                 previous_log_entry,
                                 1,
                                 id_to_change))
        cursor3.commit()


def l_change_status_dsc_by_dsd(dsd_reference,new_status):
    #print(short_name)
    current_user=functions.get_user()    #change
    #print(current_user)
    current_timestamp = functions.make_timestamp()
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
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""UPDATE 
                            doc_set_comp 
                          SET 
                            admin_user=?,
                            admin_timestamp=?,
                            admin_previous_entry=?,
                            admin_active=? 
                          WHERE 
                            dsd_reference=?""",
                            (current_user,
                             current_timestamp,
                             previous_log_entry,
                             new_status,
                             dsd_reference))
        cursor.commit()


def l_change_status_dsc_by_id(id_to_change:int,new_status:int):
    current_user=functions.get_user()
    #print(current_user)
    current_timestamp = functions.make_timestamp()
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

    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""  UPDATE 
                                doc_set_comp 
                            SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE 
                                dsc_id=?""",
                            (current_user,
                            current_timestamp,
                             previous_log_entry,
                             new_status,
                             id_to_change))
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

#print(l_ensure_completeness_of_shadow_dsc (120))



