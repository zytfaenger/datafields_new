import connections
import functions
import log_functions


def l_get_active_dsd():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            dsd_id, 
                            dsd_name, 
                            dsd_domain, 
                            dsd_year, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry,
                            admin_active 
                        from 
                            dbo.doc_set_def 
                        where 
                            admin_active=1 
                        order by 
                            dsd_year,dsd_domain,dsd_name """
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# print(l_get_active_dsd())

def l_get_all_dsd():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """select 
                            dsd_id, 
                            dsd_name, 
                            dsd_domain, 
                            dsd_year, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry,
                            admin_active  
                        from 
                            dbo.doc_set_def 
                        order by 
                            dsd_year,dsd_domain,dsd_name"""
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# [print(r) for r in l_get_all_dsd()]
def l_select_dsd_by_id(id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                                dsd_id, 
                                dsd_name, 
                                dsd_domain, 
                                dsd_year, 
                                admin_user, 
                                admin_timestamp, 
                                admin_previous_entry,
                                admin_active 
                            from 
                                dbo.doc_set_def 
                            where 
                                dsd_id=?""",
                                            id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            #print(results[0])
        return results[0]

# print(l_select_dsd_by_id(120))

def l_select_dsd_by_case(case_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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
# print(l_select_dsd_by_case(170))

def l_select_dsd_by_dsd_name(dsd_name:str):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                            dsd_id, 
                            dsd_name, 
                            dsd_domain, 
                            dsd_year, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active
                        from 
                            doc_set_def
                        where 
                            dsd_name=?""",
                       dsd_name)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

    #print("Number of records",len(results))
        if len(results)==0:
            return None
        elif len(results)==1:
            return results
        else:
            if results[0]['dsd_domain']=='unique':
                print("there should be only one record for:", dsd_name)
                raise "Data inconsistency"
            else:
                return results

# a=l_select_dsd_by_dsd_name("Address")
# for d in a:
#     print(d['dsd_id'])

def l_select_the_dsd_by_dsd_name_domain_year(dsd_name:str,dsd_domain,dsd_year):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                            dsd_id
                        from 
                            doc_set_def
                        where 
                            dsd_name=? and
                            dsd_domain=? and
                            dsd_year=?""",
                       (dsd_name,dsd_domain,dsd_year))
        result=cursor.fetchone()
        if result is None:
            return None
        else:
            return result[0]

# print(l_select_the_dsd_by_dsd_name_domain_year("Address","unique",9999))


def l_select_dsd_id_by_dsd_name(dsd_name:str):
    res=l_select_dsd_by_dsd_name(dsd_name)
    if res is None:
        return None
    elif len(res)==1:
        return res[0]['dsd_id']
    else:
        dsds=[]
        for dsd in res:
            dsds.append(dsd['dsd_id'])
        return dsds

def l_select_the_dsd_id_by_dsd_name_domain_year(dsd_name:str, dsd_domain:str,dsd_year):
    res=l_select_dsd_by_dsd_name(dsd_name)
    if res is None:
        return None
    elif len(res)==1:
        return res[0]['dsd_id']
    else:
        dsds=[]
        for dsd in res:
            dsds.append(dsd['dsd_id'])
        return  dsds




# print(l_select_dsd_id_by_dsd_name('Address'))



def l_is_shadow_case(case_id):
    current_dsd_id=l_select_dsd_by_case(case_id)
    current_dsd_record=l_select_dsd_by_id(current_dsd_id)
    if current_dsd_record['dsd_name']=="Shadowset":
        return True
    else:
        return False

#print(l_is_shadow_case(110))

def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name,table_id, payload)


def l_add_dsd_entry(name, domain, year):
    user=functions.get_user()       #change
    timestamp=functions.make_timestamp()
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("insert into dbo.doc_set_def (dsd_name,dsd_domain,dsd_year, admin_user, admin_timestamp, admin_previous_entry, admin_active) "
                       "values (?,?,?,?,?,?,?)",
                       (name, domain, year, user, timestamp,0,1))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return last_id

# l_add_dsd_entry('EL','SO',2023)
def l_update_dsd(id_to_change, name, domain, year):
    #print('l_updateft:',id_to_change,reference,field_id,sequence)
    current_user=functions.get_user()
    current_timestamp = functions.make_timestamp()
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
    azure = connections.Azure()
    with azure:
        cursor3 = azure.conn.cursor()
        cursor3.execute(""" UPDATE 
                                doc_set_def 
                            SET 
                                dsd_name=?,
                                dsd_domain=?,
                                dsd_year=?,
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE 
                                dsd_id=?""",
                        (name, domain, year, current_user, current_timestamp, previous_log_entry, 1, id_to_change))
        cursor3.commit()


def l_change_status_dsd_by_id(id_to_change:int,new_status:int):
    current_user=functions.get_user()   #change
    #print(current_user)
    current_timestamp = functions.make_timestamp()
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

    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""  UPDATE 
                                doc_set_def
                            SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE 
                                dsd_id=?""",(current_user,
                                             current_timestamp,
                                             previous_log_entry,
                                             new_status,
                                             id_to_change))
        cursor.commit()

