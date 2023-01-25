import clients
import connections
import functions
import users
import log_functions

def l_get_active_cases():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            case_id, 
                            client_id_ref, 
                            dsd_reference, 
                            language_ref, 
                            user_id,
                            shadow_case_id,
                            shadow_case_indicator,
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
# [print(r) for r in l_get_active_cases()]

def l_get_all_cases():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            case_id, 
                            client_id_ref, 
                            dsd_reference, 
                            language_ref, 
                            user_id,
                            shadow_case_id,
                            shadow_case_indicator,
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
# [print(r) for r in l_get_all_cases()]
def l_get_cases_for_userid(anvil_usr_id):
    usr_id=users.l_get_userid_for_anvil_user(anvil_usr_id)
    if usr_id is None:
        print("no such user Id")
    else:
        azure = connections.Azure()
        with azure:
            cursor = azure.conn.cursor()
            query: str = """SELECT 
                                case_id, 
                                client_id_ref, 
                                dsd_reference, 
                                language_ref, 
                                user_id,
                                shadow_case_id,
                                shadow_case_indicator,
                                admin_user, 
                                admin_timestamp, 
                                admin_previous_entry, 
                                admin_active  
                            FROM 
                                EasyEL.dbo.cases
                            WHERE
                                user_id=? """

            cursor.execute(query,usr_id)

            columns = [column[0] for column in cursor.description]
        # print(columns)
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results

# [print(r) for r in l_get_cases_for_userid('[344816,524933170]')]

def l_get_cases_for_a_client_id(client_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            EasyEL.dbo.cases.case_id, 
                            EasyEL.dbo.cases.client_id_ref, 
                            EasyEL.dbo.cases.dsd_reference, 
                            EasyEL.dbo.doc_set_def.dsd_name,
                            EasyEL.dbo.doc_set_def.dsd_domain,
                            EasyEL.dbo.doc_set_def.dsd_year,
                            EasyEL.dbo.cases.language_ref, 
                            EasyEL.dbo.cases.user_id,
                            EasyEL.dbo.cases.shadow_case_id,
                            EasyEL.dbo.cases.shadow_case_indicator,
                            EasyEL.dbo.cases.admin_user, 
                            EasyEL.dbo.cases.admin_timestamp, 
                            EasyEL.dbo.cases.admin_previous_entry, 
                            EasyEL.dbo.cases.admin_active  
                        FROM 
                            EasyEL.dbo.cases
                        left outer join 
                            doc_set_def on dbo.doc_set_def.dsd_id = EasyEL.dbo.cases.dsd_reference
                        WHERE
                            client_id_ref=? """

        cursor.execute(query,client_id)

        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if results == []:
            return [None]
        else:
            res=[]
            for row in results:
                res.append(dict(zip(columns, row)))
            return res
# a=l_get_cases_for_a_client_id(210)
# for i in range(0,len(a)):
#     print(a[i])


def l_check_certain_case_exists_for_anvil_userid(anvil_usr_id,dsd_id):      #check of case 130 = Address is here
    usr_id=users.l_get_userid_for_anvil_user(anvil_usr_id)
    client_id=clients.l_get_the_client_id_of_a_user_id(usr_id)
    if usr_id is None:
        print("no such user Id")
    else:
        azure = connections.Azure()
        with azure:
            cursor = azure.conn.cursor()
            query: str = """SELECT 
                                case_id, 
                                client_id_ref, 
                                dsd_reference, 
                                language_ref, 
                                user_id,
                                shadow_case_id,
                                shadow_case_indicator,
                                admin_user, 
                                admin_timestamp, 
                                admin_previous_entry, 
                                admin_active  
                            FROM 
                                EasyEL.dbo.cases
                            WHERE
                                client_id_ref=? and dsd_reference=?"""

            cursor.execute(query,(client_id,dsd_id))

            columns = [column[0] for column in cursor.description]
            # print(columns)
            res = cursor.fetchall()

            if res == []:
                print('Check Case exists: Case does not exist!')
                return (0,False)
            else:
                results = []
                if len(res) == 1:
                    for row in res:
                        results.append(dict(zip(columns, row)))
                    if results[0]['dsd_reference']==dsd_id:
                        print('Check Case exists: Case does exists!')
                        return (results[0]['case_id'],True)

# print(l_check_certain_case_exists_for_anvil_userid('[344816,524933170]',120))


def l_check_certain_case_exists_for_client_id(client_id, dsd_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            case_id, 
                            client_id_ref, 
                            dsd_reference, 
                            language_ref, 
                            user_id,
                            shadow_case_id,
                            shadow_case_indicator,
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active  
                        FROM 
                            EasyEL.dbo.cases
                        WHERE
                            client_id_ref=? and dsd_reference=?"""
        cursor.execute(query,(client_id,dsd_id))

        columns = [column[0] for column in cursor.description]
        # print(columns)
        res = cursor.fetchall()

        if res == []:
            print('Check Case exists: Case does not exist!')
            return (0,False)
        else:
            results = []
            if len(res) == 1:
                for row in res:
                    results.append(dict(zip(columns, row)))
                if results[0]['dsd_reference']==dsd_id:
                    print('Check Case exists: Case does exists!')
                    return (results[0]['case_id'],True)

# print(l_check_certain_case_exists_for_client_id(140,120))



def l_get_cases_for_temp_user_id(temp_user_uuid_string):
    usr_id=users.l_get_userid_for_temp_user_uuid(temp_user_uuid_string)
    if usr_id is None:
        print("no such user Id")
    else:
        azure = connections.Azure()
        with azure:
            cursor = azure.conn.cursor()
            query: str = """SELECT 
                                case_id, 
                                client_id_ref, 
                                dsd_reference, 
                                language_ref, 
                                user_id,
                                shadow_case_id,
                                shadow_case_indicator,
                                admin_user, 
                                admin_timestamp, 
                                admin_previous_entry, 
                                admin_active  
                            FROM 
                                EasyEL.dbo.cases
                            WHERE
                                user_id=? """

            cursor.execute(query,usr_id)

            columns = [column[0] for column in cursor.description]
            # print(columns)
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results

# [print(r) for r in l_get_cases_for_temp_user_id('142452F6-9685-11ED-B4C0-ACDE48001122')]
def l_get_cases_for_temp_user_id_and_DSD(temp_user_uuid_string,dsd_id):
    usr_id=users.l_get_userid_for_temp_user_uuid(temp_user_uuid_string)
    if usr_id is None:
        print("no such user Id")
        return None
    else:
        azure = connections.Azure()
        with azure:
            cursor = azure.conn.cursor()
            query: str = """SELECT 
                                case_id, 
                                client_id_ref, 
                                dsd_reference, 
                                language_ref, 
                                user_id,
                                shadow_case_id,
                                shadow_case_indicator,
                                admin_user, 
                                admin_timestamp, 
                                admin_previous_entry, 
                                admin_active  
                            FROM 
                                EasyEL.dbo.cases
                            WHERE
                                user_id=? AND dsd_reference=? """

            cursor.execute(query,(usr_id,dsd_id))

            columns = [column[0] for column in cursor.description]
            # print(columns)
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results

# print(l_get_cases_for_temp_user_id_and_DSD('142452F6-9685-11ED-B4C0-ACDE48001122',120)[0]['case_id'])



def l_select_case_by_id(id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                                case_id, 
                                client_id_ref, 
                                dsd_reference, 
                                language_ref, 
                                user_id, 
                                shadow_case_id,
                                shadow_case_indicator,
                                admin_user, 
                                admin_timestamp, 
                                admin_previous_entry, 
                                admin_active 
                            from 
                                EasyEL.dbo.cases 
                            where case_id=?""", id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if results == []:
            return None
        else:
            res = []
            for row in results:
                res.append(dict(zip(columns, row)))
                #print(results[0])
            return res[0]

# print(l_select_case_by_id(110))



def l_get_dsd_reference_for_case_id(ca_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
            select dsd_reference 
            from
             EasyEL.dbo.cases
            where
             case_id=?   
        """
        cursor.execute(query,ca_id)
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            for r in result:
                dsd=r
        # print('l_get_dsd_reference_for_case_id',dsd)
        # print('l_get_dsd_reference_for_case_id:',ca_id, " ist: dsd:",dsd)
            return dsd

# print(l_get_dsd_reference_for_case_id(100))

def l_get_user_id_for_case_id(ca_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
            select user_id 
            from
             EasyEL.dbo.cases
            where
             case_id=?   
        """
        cursor.execute(query,ca_id)
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

# print(l_get_user_id_for_case_id(170))

def l_get_client_id_for_case_id(ca_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
            select client_id_ref 
            from
             EasyEL.dbo.cases
            where
             case_id=?   
        """
        cursor.execute(query,ca_id)
        result = cursor.fetchone()
        client_id=None
        for r in result:
            client_id=r
        #print(dsd)
        #print(ca_id, " ist: dsd:",dsd)
        return client_id

# print(l_get_client_id_for_case_id(170))

def l_get_shadow_case_id_for_case_id(ca_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query= """
            select shadow_case_id 
            from
             EasyEL.dbo.cases
            where
             case_id=?   
        """

        cursor.execute(query,ca_id)
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            shadow_case_id = None
            for r in result:
                shadow_case_id=r
            return shadow_case_id

# print(l_get_shadow_case_id_for_case_id(200))

def l_get_shadow_case_id_for_client_id(client_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query= """
            select case_id
            from
             EasyEL.dbo.cases
            where
             client_id_ref=?  and shadow_case_indicator=?
        """
        cursor.execute(query,(client_id,True))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            shadow_case_id = None
            for r in result:
                shadow_case_id=r
            return shadow_case_id

# print(l_get_shadow_case_id_for_client_id(110))




def l_get_shadow_case_indicator_for_case_id(ca_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query= """
            select shadow_case_indicator
            from
             EasyEL.dbo.cases
            where
             case_id=?   
        """
        cursor.execute(query,ca_id)
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            shadow_case_ind = None
            for r in result:
                shadow_case_ind=r
            return shadow_case_ind

# print(l_get_shadow_case_id_for_case_id(170))
# print(l_get_shadow_case_indicator_for_case_id(170))
# print(l_get_shadow_case_id_for_case_id(100))
# print(l_get_shadow_case_indicator_for_case_id(100))

def l_select_language_short_by_case_id(case_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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

# print(l_get_dsd_reference_for_case_id(110))


def l_select_language_id_from_case_id(case_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                            cases.language_ref
                            from
                                EasyEL.dbo.cases
                            where 
                                cases.case_id=?""",
                           case_id)
        res=cursor.fetchone()
        if res is None:
            return None
        else:
            return res[0]

# print(l_select_language_id_from_case_id(100))



def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name,table_id, payload)

def l_add_case(client_id, dsd_reference, language_ref, user_id, shadow_case_id=0, shdw_case_ind=False ):
    admin_user=users.l_get_admin_user_by_id(user_id)
    timestamp=functions.make_timestamp()
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query= """insert into 
                         EasyEL.dbo.cases (client_id_ref, 
                                            dsd_reference, 
                                            language_ref, 
                                            user_id,
                                            shadow_case_id,
                                            shadow_case_indicator,
                                            admin_user, 
                                            admin_timestamp, 
                                            admin_previous_entry, 
                                            admin_active)
                                           values (?,?,?,?,?,?,?,?,?,?)"""
        cursor.execute(query,(client_id,dsd_reference,language_ref,user_id, 0,shdw_case_ind, admin_user, timestamp,0,1))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return last_id

# l_add_case(110,100,1,100,0)


def l_add_shadow_case(client_id,language_ref,user_id,dsd_reference=120,shdw_case_ind=True):
    return l_add_case(client_id,dsd_reference,language_ref,user_id,shadow_case_id=1,shdw_case_ind=True)

def l_update_cases_shadow_case_id(client_id,shdw_case_id):
    user_id=l_get_user_id_for_case_id(client_id)
    user_record=users.l_get_user_by_id(user_id)
    current_user = user_record['admin_user']
    current_timestamp = functions.make_timestamp()
    current_table_name = 'cases'
    current_table_id = client_id
    current_payload = str(l_select_case_by_id(shdw_case_id))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry = add_log_entry(current_user,
                                       current_timestamp,
                                       current_table_name,
                                       current_table_id,
                                       current_payload)
    # print(previous_log_entry)
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""  UPDATE 
                                   EasyEL.dbo.cases 
                               SET 
                                   shadow_case_id=?
                               WHERE 
                               client_id_ref = ? and case_id <> ? """,
                       (shdw_case_id, client_id, shdw_case_id))
        cursor.commit()

# l_update_cases_shadow_case_id(740,730)

def l_update_shadow_case_id_for_a_given_case_id(client_id,case_id, shdw_case_id):
    user_id=clients.l_get_client_by_id(client_id)['client_user_ref']
    user_record=users.l_get_user_by_id(user_id)
    current_user = user_record['admin_user']
    current_timestamp = functions.make_timestamp()
    current_table_name = 'cases'
    current_table_id = client_id
    current_payload = str(l_select_case_by_id(shdw_case_id))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry = add_log_entry(current_user,
                                       current_timestamp,
                                       current_table_name,
                                       current_table_id,
                                       current_payload)
    # print(previous_log_entry)
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""  UPDATE 
                                   EasyEL.dbo.cases 
                               SET 
                                   shadow_case_id=?
                               WHERE 
                               case_id= ?""",
                       (shdw_case_id, case_id))
        cursor.commit()


# l_update_cases_shadow_case_id(110,170)


def l_update_cases(id_to_change, client_id_ref, dsd_reference, language_ref, user_id):
    #print('l_updateft:',id_to_change,type,description,sequence)
    current_adminuser=users.l_get_admin_user_by_id(user_id)
    current_timestamp = functions.make_timestamp()
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
    azure = connections.Azure()
    with azure:
        cursor3 = azure.conn.cursor()
        query="""   UPDATE 
                        cases 
                    SET 
                        client_id_ref=?,
                        dsd_reference=?,
                        language_ref=?,
                        user_id=?,
                        shadow_case_id=?,
                        admin_user=?,
                        admin_timestamp=?,
                        admin_previous_entry=?,
                        admin_active=?
                    WHERE 
                        EasyEL.dbo.cases.case_id=?"""
        cursor3.execute(query, (client_id_ref, dsd_reference, language_ref, user_id, 0, current_adminuser, current_timestamp, previous_log_entry,1, id_to_change))
        cursor3.commit()


# l_update_cases(160, 110,100,1,100)



def l_change_status_case_by_id(ca_to_change:int,new_status:int):
    current_user=users.l_get_admin_user_by_id(ca_to_change)
    #print(current_user)
    current_timestamp = functions.make_timestamp()
    current_table_name = 'cases'
    current_table_id=ca_to_change
    current_payload=str(l_select_case_by_id(ca_to_change))
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
                                EasyEL.dbo.cases 
                            SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE case_id=?""",
                           (current_user,current_timestamp,previous_log_entry,new_status,ca_to_change))
        cursor.commit()