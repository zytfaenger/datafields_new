import cases_functions
import doc_set_compositions
from functions import make_timestamp, get_user, get_user_id
from log_functions import log_add_log_entry
from connections import get_connection
from doc_set_definition import l_select_dsd_by_case, l_select_dsd_by_id
from cases_functions import l_get_dsd_reference_for_case_id,l_select_language_short_by_case_id, l_get_user_id_for_case_id
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


def l_get_cdm_entry_ID(user_id, case_id, dsc_id_ref):
    # cdm = Client Data Main
    print("cdm97 - userid, caseId, dsc-id", user_id, case_id, dsc_id_ref)
    query: str = """SELECT 
                        cdm_id 
                    FROM 
                        client_data_main 
                    WHERE case_id_reference=? AND dsc_reference=? 
                    """
    cursor.execute(query,(case_id,dsc_id_ref))
    result = cursor.fetchone()
    if result == None:
        print("l_get_cdm_entry_ID no record (cdm 105)")
        entry = l_add_cdm_entry(user_id, case_id, dsc_id_ref, pl_text="None",pl_number=99999,pl_boolean=0)
        print ("cdm_entry line 108",entry)
        return entry
    for row in result:
        a=row
        # print(row)
        # print(a)
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

def l_ensure_completeness_of_store_for_case(case_id):
    current_user=get_user_id()
    current_dsd_id = l_select_dsd_by_case(case_id)
    current_language_short=l_select_language_short_by_case_id(case_id)
    current_docsets = doc_set_compositions.l_select_dsc_to_store_for_case_id(case_id)
    counter=0
    for ds in current_docsets:
        print(counter)
        print(ds)
        counter +=1
        # print(ds['ft_stores_state'])
        # print(ds['ft_stores_data'])
        current_dsc_id=ds['dsc_id']
        if l_get_cdm_entries(current_dsd_id,current_dsc_id)==[]:
            l_add_cdm_entry(current_user,case_id,current_dsc_id,'None',99999,False)
            print (current_dsc_id, "added")
        else:
            print(current_dsc_id, " exists!")

#l_ensure_completeness_of_store_for_case(180)

def l_get_fd_shadow(case_id, field_id):
    print("l_get_shadow, parameters:",case_id, field_id)
    current_dsd=l_get_dsd_reference_for_case_id(case_id)
    current_lang=l_select_language_short_by_case_id(case_id)
    current_dsc=doc_set_compositions.l_select_dsc_id_by_case_and_field(case_id,field_id)
    current_userID=l_get_user_id_for_case_id(case_id)
    print("zwischenstand l_get_fd: ", case_id, field_id,current_lang, current_dsc, current_userID)
    result= {}
    query= """select 
                payload_text,
                payload_number,
                payload_boolean
              from 
                client_data_main
              where
                dsc_reference=? and case_id_reference=?
            """
    cursor.execute(query,(current_dsc,case_id))
    payload= cursor.fetchone()
    print('get_fd_all payload',payload)

    if payload == None:  #do a detour and create the shadow record first
        print("No shadow record found")
        l_add_cdm_entry(current_userID, case_id, current_dsc, 'None',99999,False)
        print('get_fd_shadow: missing cdm shadow record added!')
        cursor2=conn.cursor()
        cursor2.execute(query,(current_dsc,case_id))
        payload=cursor2.fetchone()
        print('New payload:',payload)

    print(payload)
    result['payload_text']=payload[0]
    result['payload_number']=payload[1]
    result['payload_boolean'] = payload[2]
    print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc, payload)
    print(l_get_label(current_lang, field_id))
    # result['label']=l_get_label(current_lang,field_id)  # not necessary, because no labels are created in shadow
    # result['prompt']=l_get_prompt(current_lang,field_id) # not necessary, because no labels are created in shadow
    print(result)
    return result





def l_get_fd(case_id, field_id):
    print("l_get_fd, parameters:",case_id, field_id)
    current_dsd=l_get_dsd_reference_for_case_id(case_id)
    current_lang=l_select_language_short_by_case_id(case_id)
    current_dsc=doc_set_compositions.l_select_dsc_id_by_case_and_field(case_id,field_id)
    if current_dsc==None:  ##DSC nicht er??ffnet, abort
        text=("DSC not set!! Cannot create cdm record for case {}, field {}!").format(case_id,field_id)
    else:
        current_userID=l_get_user_id_for_case_id(case_id)
        shadow_case_id = cases_functions.l_get_shadow_case_id_for_case_id(case_id) #is not = shadow  DSD!!!
        if shadow_case_id==0: #make sure it is really a shadow case direct
            if cases_functions.l_get_shadow_case_indicator_for_case_id(case_id) is True:
                shadow_case_id=case_id
                print('get_fd:',case_id," is Shadow Case!")
            else:
                print("l_get_fd_case: Shadow_Case not defined for Case:", case_id)
        print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc,current_userID)
        result= {}
        query= """select 
                    payload_text,
                    payload_number,
                    payload_boolean
                  from 
                    client_data_main
                  where
                    dsc_reference=? and case_id_reference=?
                """
        cursor.execute(query,(current_dsc,case_id))
        payload= cursor.fetchone()
        # print("Payload", payload)

        print('get_fd payload',payload)
        if payload is None:
            print("No record found in current data")
            result = l_get_fd_shadow(shadow_case_id,field_id)  # if the record is not there, get it from the shadow
                                                        # the shadow ensures that there is at least an empty record
                                                        # now use the copy of the results either filled or new

            new_record = l_add_cdm_entry(current_userID,
                            case_id,
                            current_dsc,
                            pl_text=result['payload_text'],
                            pl_number=result['payload_number'],
                            pl_boolean=result['payload_boolean'])

            cursor2=conn.cursor()
            cursor2.execute(query,(current_dsc,case_id))
            payload=cursor2.fetchone()
            print('New payload:',payload)

        print(payload)
        result['payload_text']=payload[0]
        result['payload_number'] = payload[1]
        result['payload_boolean'] = payload[2]
        print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc, payload)
        print(l_get_label(current_lang, field_id))
        result['label']=l_get_label(current_lang,field_id)
        result['prompt']=l_get_prompt(current_lang,field_id)
        #  print(result)
        return result

# print(l_get_fd(case_id=110,field_id=170))

# print(l_get_fd(case_id=110,field_id=160)) #test is ein Textfeld und muss behandelt werden!

def l_set_fd(user_id, case_id, field_id,pl_text,pl_number,pl_boolean):
    if pl_text=='=':
        update_text=False
    else:
        update_text=True

    if pl_number == '=':
        update_number = False
    else:
        update_number = True

    if pl_boolean == '=':
        update_boolean = False
    else:
        update_boolean = True

    if update_text==False and update_number==False and update_boolean==False:
        print ("set FD: nothing to update")
    else:  #we need to define the values to be updated
        existing_payload = l_get_fd(case_id,field_id)
        if update_text==True:
            pl_new_text=pl_text
        else:
           pl_new_text=existing_payload['payload_text']

        if update_number==True:
            pl_new_number=pl_number
        else:
            pl_new_number=existing_payload['payload_number']

        if update_boolean == True:
            pl_new_boolean = pl_boolean
        else:
            pl_new_boolean = existing_payload['payload_boolean']
    # ok, we have them
        print("Update l??uft mit folgenden Paras:", user_id,case_id,field_id,pl_new_text,pl_new_number,pl_new_boolean)
        shadow_case_id=cases_functions.l_get_shadow_case_id_for_case_id(case_id)

        if shadow_case_id==0: #hey we may have a shadow-case in direct mode, let's make sure
            is_shadow = cases_functions.l_get_shadow_case_indicator_for_case_id(case_id)
            if is_shadow is False:
                msg = ("Set_fd: Bei case id {} ist die Shadow_id nicht gesetzt!").format(case_id)
                return msg
        else:
            shadow_case_id = case_id  # stellt case auf sich selbst ein
            dsc_id=doc_set_compositions.l_select_dsc_id_by_case_and_field(case_id,field_id)
            shadow_dsc_id=doc_set_compositions.l_select_dsc_id_by_case_and_field(shadow_case_id,field_id)

            #update normal  Record should exist -:)
            print("set_fd: dsc_id", dsc_id)
            id_to_change=l_get_cdm_entry_ID(user_id, case_id, dsc_id)
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
            # print(previous_log_entry)
            cursor3 = conn.cursor()
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
                            (
                            user_id, case_id, dsc_id, pl_new_text, pl_new_number, pl_new_boolean, current_admin_user, current_timestamp,
                            previous_log_entry, 1, id_to_change))
            cursor3.commit()

            # shadow Record does not necessarily exist!
            print("set fd: shadow_dsc_id", shadow_dsc_id)
            id_to_change=l_get_cdm_entry_ID(user_id, shadow_case_id, shadow_dsc_id)
            current_admin_user=get_user()
            current_timestamp = make_timestamp()
            current_table_name = 'shadow_client_data_main'
            current_table_id=id_to_change
            if id_to_change is None:
                current_payload="No Record existed yet --> is added as copy"
            else:
                current_payload=str(l_select_cdm_by_id(id_to_change))
            print("------>",current_admin_user,current_timestamp,current_table_name,current_table_id,current_payload)
            previous_log_entry=add_log_entry(current_admin_user,
                                             current_timestamp,
                                             current_table_name,
                                             current_table_id,
                                             current_payload)

            if id_to_change is None:
                l_add_cdm_entry(user_id,shadow_case_id,shadow_dsc_id,pl_new_text,pl_new_number,pl_new_boolean)
            else:
                cursor4 = conn.cursor()
                cursor4.execute("""UPDATE 
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
                                (
                                user_id, shadow_case_id, shadow_dsc_id, pl_new_text, pl_new_number, pl_new_boolean, current_admin_user, current_timestamp,
                                previous_log_entry, 1, id_to_change))
                cursor4.commit()

#l_set_fd(100, 100, 170,'Carouge',1200,'=')




#l_ensure_completeness_of_stores(100)
#print(l_get_cdm_entries(100,200))
#print(l_select_cdm_by_id(190))
# print(l_add_cdm_entry(100, 100, 150,pl_text="Hirtenhofweg 11",pl_number=31415,pl_boolean=1))
#l_update_cdm_entry(100, 110, 150,'Benziwil 27',6020,False)