import cases_functions
import doc_set_compositions
import functions
import users
import log_functions
import connections
import field_descriptions
import globals as G
import cache


def l_get_all_active_cdm_entries():
    # cdm = Client Data Main
    azure = connections.Azure()
    with azure:
        cursor=azure.conn.cursor()
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
                        WHERE admin_active=? 
                        """
        cursor.execute(query,True)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# print(l_get_all_active_cdm_entries())

def l_get_all_cdm_entries():
    azure = connections.Azure()
    with azure:
        cursor=azure.conn.cursor()
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

# print(l_get_all_cdm_entries())
def l_get_active_cdm_entries_by_case_id_and_dsc_id(case_id, dsc_id_ref):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            cdm_id, 
                            user_id_reference, 
                            case_id_reference,
                            EasyEL.dbo.cases.client_id_ref,
                            dsc_reference, 
                            payload_text, 
                            payload_number, 
                            payload_boolean, 
                            client_data_main.admin_user, 
                            client_data_main.admin_timestamp, 
                            client_data_main.admin_previous_entry, 
                            client_data_main.admin_active 
                        FROM client_data_main
                        join EasyEL.dbo.cases on EasyEL.dbo.cases.case_id = client_data_main.case_id_reference
                        WHERE case_id_reference=? AND dsc_reference=? and client_data_main.admin_active=?
                        """
        cursor.execute(query,(case_id,dsc_id_ref,True))
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if results==[]:
            return None
        else:
            res=[]
        for row in results:
            res.append(dict(zip(columns, row)))
        return res
#print(l_get_active_cdm_entries_by_case_id_and_dsc_id(720,1960))

def l_get_all_cdm_entries_by_case_id_and_dsc_id(case_id, dsc_id_ref):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            cdm_id, 
                            user_id_reference, 
                            case_id_reference,
                            EasyEL.dbo.cases.client_id_ref,
                            dsc_reference, 
                            payload_text, 
                            payload_number, 
                            payload_boolean, 
                            client_data_main.admin_user, 
                            client_data_main.admin_timestamp, 
                            client_data_main.admin_previous_entry, 
                            client_data_main.admin_active 
                        FROM client_data_main
                        join EasyEL.dbo.cases on EasyEL.dbo.cases.case_id = client_data_main.case_id_reference
                        WHERE case_id_reference=? AND dsc_reference=?
                        """
        cursor.execute(query,(case_id,dsc_id_ref))
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

#print(l_get_all_cdm_entries_by_case_id_and_dsc_id(100, 210))

def l_get_active_cdm_entries_by_client_id(client_id):
    azure = connections.Azure()
    with azure:
        cursor=azure.conn.cursor()
        query: str = """SELECT 
                            cdm_id, 
                            user_id_reference, 
                            case_id_reference,
                            EasyEL.dbo.cases.client_id_ref,
                            dsc_reference, 
                            payload_text, 
                            payload_number, 
                            payload_boolean, 
                            client_data_main.admin_user, 
                            client_data_main.admin_timestamp, 
                            client_data_main.admin_previous_entry, 
                            client_data_main.admin_active 
                        FROM client_data_main
                        join EasyEL.dbo.cases on EasyEL.dbo.cases.case_id = client_data_main.case_id_reference
                        join EasyEL.dbo.doc_set_comp on EasyEL.dbo.doc_set_comp.dsc_id = client_data_main.dsc_reference
                        WHERE EasyEL.dbo.cases.client_id_ref=? and client_data_main.admin_active=?
                        order by 
                        dbo.doc_set_comp.dsc_sequence
                        """
        cursor.execute(query,(client_id, True))
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

#[print(r) for r in l_get_active_cdm_entries_by_client_id(230)]

#test
#
# res=l_get_active_cdm_entries_by_client_id(client_id=110)
# if res is None:
#     print(None)
# else:
#     print("Anzahl Records",len(res))
#     if type(res) is list:
#         for e in res:
#             print(e)
#     else:
#         print("Other type of return")


def l_get_active_cdm_entries_by_case_id(case_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            cdm_id, 
                            user_id_reference, 
                            case_id_reference,
                            EasyEL.dbo.cases.client_id_ref,
                            dsc_reference, 
                            payload_text, 
                            payload_number, 
                            payload_boolean, 
                            client_data_main.admin_user, 
                            client_data_main.admin_timestamp, 
                            client_data_main.admin_previous_entry, 
                            client_data_main.admin_active 
                        FROM client_data_main
                        join EasyEL.dbo.cases on EasyEL.dbo.cases.case_id = client_data_main.case_id_reference
                        join EasyEL.dbo.doc_set_comp on EasyEL.dbo.doc_set_comp.dsc_id = client_data_main.dsc_reference
                        WHERE case_id_reference=? and client_data_main.admin_active=?
                        order by 
                        dbo.doc_set_comp.dsc_sequence
                        """
        cursor.execute(query,(case_id, True))
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

#[print(r) for r in l_get_active_cdm_entries_by_case_id(170)]

#test
#
# res=l_get_active_cdm_entries_by_case_id(case_id=170)
# if res is None:
#     print(None)
# else:
#     print("Anzahl Records",len(res))
#     if type(res) is list:
#         for e in res:
#             print(e)
#     else:
#         print("Other type of return")



def l_select_cdm_by_id(id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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

#print(l_select_cdm_by_id(1050))

def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name,table_id, payload)


def l_add_cdm_entry(user_id, case_id, dsc_id,pl_text=None,pl_number=None,pl_boolean=None):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        admin_user=users.l_get_admin_user_by_id(user_id)
        timestamp=functions.make_timestamp()
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

#print(l_add_cdm_entry(100,100,410,"AzureConnTest",88888,False))  #remove after test!!!

def l_get_cdm_entry_ID(case_id, dsc_id_ref):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        usr_from_case=cases_functions.l_get_user_id_for_case_id(case_id)
        if usr_from_case is None:
            print('Case', case_id,'does not exist, aborting!')
            print("cdm_get_cdm_entry - userid, caseId, dsc-id", usr_from_case, case_id, dsc_id_ref)
            return None
        else:
            print("cdm_get_cdm_entry - userid, caseId, dsc-id", usr_from_case, case_id, dsc_id_ref)
            query: str = """SELECT
                                cdm_id
                            FROM
                                client_data_main
                            WHERE case_id_reference=? AND dsc_reference=?
                            """
            cursor.execute(query,(case_id,dsc_id_ref))
            result = cursor.fetchall()

            if result == []:
                print("l_get_cdm_entry_ID no record für case_id/dsc_id",case_id,dsc_id_ref)
                print('generating new record')
                entry = l_add_cdm_entry(usr_from_case, case_id, dsc_id_ref, pl_text="None",pl_number=99999,pl_boolean=0)
                print ("cdm_entry line 108",entry)
                return entry #Id des neuen Eintrags
            else:
                if type(result) is list:
                    return result[0][0]
                elif type(result) is int:
                    return result
                else:
                  print('get_cdm_entry: multiple results but there should be only one')
                  return None

#print(l_get_cdm_entry_ID(case_id=170,dsc_id_ref=1170))

def l_update_cdm_entry(user_id, case_id, field_id,pl_text,pl_number,pl_boolean):  #just dummy as a reminder to make functions complete
    l_set_fd(user_id, case_id, field_id,pl_text,pl_number,pl_boolean)


# def l_change_status_cdm_by_id(id_to_change:int,new_status:int):
#     azure = connections.Azure()
#     with azure:
#         cursor = azure.conn.cursor()
#         current_user=functions.get_user()    #change
#         #print(current_user)
#         current_timestamp = functions.make_timestamp()
#         current_table_name = 'client_data_main'
#         current_table_id=id_to_change
#         current_payload=str(l_select_cdm_by_id(id_to_change))
#         #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
#         previous_log_entry=add_log_entry(current_user,
#                                          current_timestamp,
#                                          current_table_name,
#                                          current_table_id,
#                                          current_payload)
#         #print(previous_log_entry)
#
#
#         cursor.execute("""UPDATE doc_set_def SET admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? WHERE dsd_id=?""",(current_user,current_timestamp,previous_log_entry,new_status,id_to_change))
#         cursor.commit()

def l_ensure_completeness_of_store_for_case(case_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        current_user=cases_functions.l_get_user_id_for_case_id(case_id)
        # current_dsd_id = l_select_dsd_by_case(case_id)
        current_docsets = doc_set_compositions.l_select_dsc_to_store_for_case_id(case_id)
        counter=0
        for ds in current_docsets:
            print(counter)
            print(ds)
            counter +=1
            # print(ds['ft_stores_state'])
            # print(ds['ft_stores_data'])
            current_dsc_id=ds['dsc_id']
            existing_cdm=l_get_active_cdm_entries_by_case_id_and_dsc_id(case_id=case_id,dsc_id_ref=current_dsc_id)
            if existing_cdm==[] or existing_cdm==None:
                l_add_cdm_entry(current_user,case_id,current_dsc_id,'None',99999,False) #if there is none

                print (current_dsc_id, "added")
            elif type(existing_cdm) ==list:
                if len(existing_cdm)==1:
                  print(current_dsc_id, " exists!")
                else:
                    print("Multiple Entries")
                    print(current_dsc_id, " exists!")
            else:
                print('Return type strange!!!!!')

# +l_ensure_completeness_of_store_for_case(190)

def l_get_fd_shadow(anvil_user_id, case_id, field_id):
    print("l_get_shadow, parameters:",case_id, field_id)
    # current_lang=cases_functions.l_select_language_short_by_case_id(case_id)
    #current_dsc=doc_set_compositions.l_select_dsc_id_by_case_and_field(case_id,field_id)
    #current_userID=cases_functions.l_get_user_id_for_case_id(case_id)
    current_lang= G.cached.get_language_id(anvil_user_id)
    current_dsc = doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id,case_id, field_id)
    current_userID=cases_functions.l_get_user_id_for_case_id_modern(anvil_user_id, case_id)
    print("zwischenstand l_get_fd: ", case_id, field_id,current_lang, current_dsc, current_userID)
    azure = G.cached.conn_get()
    with azure:
        cursor = azure.conn.cursor()
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
            azure2 = G.cached.conn_get()
            with azure2:
                cursor2=azure2.conn.cursor()
                cursor2.execute(query,(current_dsc,case_id))
                payload=cursor2.fetchone()
                print('New payload:',payload)

        print(payload)
        result['payload_text']=payload[0]
        result['payload_number']=payload[1]
        result['payload_boolean'] = payload[2]
        print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc, payload)
        print(field_descriptions.l_get_label(current_lang, field_id))
        # result['label']=l_get_label(current_lang,field_id)  # not necessary, because no labels are created in shadow
        # result['prompt']=l_get_prompt(current_lang,field_id) # not necessary, because no labels are created in shadow
        print(result)
        return result

# print(l_get_fd_shadow(170,210))



def l_get_fd(anvil_user_id, case_id, field_id):
    print("l_get_fd, parameters:",case_id, field_id)
    #current_lang=cases_functions.l_select_language_short_by_case_id(case_id)
    #current_dsc=doc_set_compositions.l_select_dsc_id_by_case_and_field(case_id,field_id)
    current_lang = G.cached.get_language_id(anvil_user_id)
    current_dsc=doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id, case_id,field_id)
    if current_dsc==None:  ##DSC nicht eröffnet, abort
        text=("DSC not set!! Cannot create cdm record for case {}, field {}!").format(case_id,field_id)
    else:
        #current_userID=cases_functions.l_get_user_id_for_case_id(case_id)
        #shadow_case_id = cases_functions.l_get_shadow_case_id_for_case_id(case_id) #is not = shadow  DSD!!!
        current_userID = cases_functions.l_get_user_id_for_case_id_modern(anvil_user_id,case_id)
        shadow_case_id = cases_functions.l_get_shadow_case_id_for_case_id_modern(anvil_user_id,case_id) #is not = shadow  DSD!!!
        if shadow_case_id==0: #make sure it is really a shadow case direct
            #if cases_functions.l_get_shadow_case_indicator_for_case_id(case_id) is True:
            if cases_functions.l_get_shadow_case_indicator_for_case_id_modern(anvil_user_id,case_id) is True:
                shadow_case_id=case_id
                print('get_fd:',case_id," is Shadow Case!")
            else:
                print("l_get_fd_case: Shadow_Case not defined for Case:", case_id)
        print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc,current_userID)
        #azure = connections.Azure()
        azure=G.cached.conn_get()
        with azure:
            cursor = azure.conn.cursor()
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
                result = l_get_fd_shadow(anvil_user_id,shadow_case_id,field_id)  # if the record is not there, get it from the shadow
                                                            # the shadow ensures that there is at least an empty record
                                                            # now use the copy of the results either filled or new

                new_record = l_add_cdm_entry(current_userID,
                                case_id,
                                current_dsc,
                                pl_text=result['payload_text'],
                                pl_number=result['payload_number'],
                                pl_boolean=result['payload_boolean'])

                azure2=G.cached.conn_get()
                with azure2:
                    cursor2 = azure2.conn.cursor()
                    cursor2.execute(query,(current_dsc,case_id))
                    payload=cursor2.fetchone()
                    print('New payload:',payload)

            print(payload)
            result['payload_text']=payload[0]
            result['payload_number'] = payload[1]
            result['payload_boolean'] = payload[2]
            print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc, payload)
            print(field_descriptions.l_get_label(current_lang, field_id))
            result['label']=field_descriptions.l_get_label(current_lang,field_id)
            result['prompt']=field_descriptions.l_get_prompt(current_lang,field_id)
            #  print(result)
            return result

#print(l_get_fd(case_id=400,field_id=510))

# print(l_get_fd(case_id=110,field_id=160)) #test is ein Textfeld und muss behandelt werden!

def l_get_fd_cached(anvil_user_id, case_id, field_id):
    print("l_get_fd, parameters:",anvil_user_id, case_id, field_id)
    current_lang=cases_functions.l_select_language_short_by_case_id(case_id)
    current_dsc=doc_set_compositions.l_select_dsc_id_by_case_and_field(case_id,field_id)
    if current_dsc==None:  ##DSC nicht eröffnet, abort
        text=("DSC not set!! Cannot create cdm record for case {}, field {}!").format(case_id,field_id)
    else:
        current_userID=cases_functions.l_get_user_id_for_case_id(case_id)
        shadow_case_id = cases_functions.l_get_shadow_case_id_for_case_id(case_id) #is not = shadow  DSD!!!
        if shadow_case_id==0: #make sure it is really a shadow case direct
            if cases_functions.l_get_shadow_case_indicator_for_case_id(case_id) is True:
                shadow_case_id=case_id
                print('get_fd:',case_id," is Shadow Case!")
            else:
                print("l_get_fd_case: Shadow_Case not defined for Case:", case_id)
        print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc,current_userID)
        azure = connections.Azure()
        with azure:
            cursor = azure.conn.cursor()
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
                result = l_get_fd_shadow(anvil_user_id, shadow_case_id, field_id)  # if the record is not there, get it from the shadow
                                                            # the shadow ensures that there is at least an empty record
                                                            # now use the copy of the results either filled or new

                new_record = l_add_cdm_entry(current_userID,
                                case_id,
                                current_dsc,
                                pl_text=result['payload_text'],
                                pl_number=result['payload_number'],
                                pl_boolean=result['payload_boolean'])

                azure2=connections.Azure()
                with azure2:
                    cursor2 = azure2.conn.cursor()
                    cursor2.execute(query,(current_dsc,case_id))
                    payload=cursor2.fetchone()
                    print('New payload:',payload)

            print(payload)
            result['payload_text']=payload[0]
            result['payload_number'] = payload[1]
            result['payload_boolean'] = payload[2]
            print("zwischenstand l_get_fd: ", case_id, field_id, current_lang, current_dsc, payload)
            print(field_descriptions.l_get_label(current_lang, field_id))
            result['label']=field_descriptions.l_get_label(current_lang,field_id)
            result['prompt']=field_descriptions.l_get_prompt(current_lang,field_id)
            #  print(result)
            return result

#print(l_get_fd(anvil_user_id='[344816,583548811]',case_id=400,field_id=510))

# print(l_get_fd(case_id=110,field_id=160)) #test is ein Textfeld und muss behandelt werden!








def l_set_fd(anvil_user_id, case_id, field_id,pl_text,pl_number,pl_boolean):
    user_id=users.l_get_userid_for_anvil_user(anvil_user_id)
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
        existing_payload = l_get_fd(anvil_user_id,case_id,field_id)
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
        print("Update läuft mit folgenden Paras:", anvil_user_id,case_id,field_id,pl_new_text,pl_new_number,pl_new_boolean)
        # shadow_case_id=cases_functions.l_get_shadow_case_id_for_case_id(case_id)
        shadow_case_id = cases_functions.l_get_shadow_case_id_for_case_id_modern(anvil_user_id, case_id)

        if shadow_case_id==0: #hey we may have a shadow-case in direct mode, let's make sure
            # is_shadow = cases_functions.l_get_shadow_case_indicator_for_case_id(case_id)
            is_shadow = cases_functions.l_get_shadow_case_indicator_for_case_id_modern(anvil_user_id,case_id)
            if is_shadow is False:
                msg = ("Set_fd: Bei case id {} ist die Shadow_id nicht gesetzt!").format(case_id)
                return msg
        else:
            # shadow_case_id = case_id  # stellt case auf sich selbst ein
            #dsc_id=doc_set_compositions.l_select_dsc_id_by_case_and_field(case_id,field_id)
            dsc_id = doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id, case_id, field_id)
            #shadow_dsc_id=doc_set_compositions.l_select_dsc_id_by_case_and_field(shadow_case_id,field_id)
            shadow_dsc_id = doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id, shadow_case_id, field_id)

            #update normal  Record should exist -:)
            print("set_fd: dsc_id", dsc_id)
            id_to_change=l_get_cdm_entry_ID(case_id, dsc_id)
            current_admin_user=functions.get_user()
            current_timestamp = functions.make_timestamp()
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
            azure = G.cached.conn_get()
            with azure:
                cursor3 = azure.conn.cursor()
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
                id_to_change=l_get_cdm_entry_ID(shadow_case_id, shadow_dsc_id)
                current_admin_user=functions.get_user()
                current_timestamp = functions.make_timestamp()
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
                    azure = G.cached.conn_get()
                    with azure:
                        cursor4 = azure.conn.cursor()
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