import uuid

import connections
import functions
import relations
import users
import log_functions
import globals as G


def l_get_clients_table_columns():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
                            client_relation_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        FROM 
                            clients
                        WHERE 
                            client_id=?"""

        cursor.execute(query,"")
        i=0
        cset=[]
        for c in cursor.description:
            #print(c)
            type=""
            if c[1]==int:
                type="number"
            elif c[1]==float:
                type="number"
            elif c[1] == bool:
                type="number"
            elif c[1]==str:
                type="text"
            else:
                type=c[1]
            temp=(i,c[0],type)
            cset.append(temp)
            i= i+1
        return cset
# print(l_get_clients_table_columns())

def l_get_active_clients():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
                            client_relation_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        FROM 
                            clients 
                        WHERE 
                            admin_active=?"""
        cursor.execute(query,1)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# [print(r) for r in l_get_active_clients()]



def l_get_all_clients():
    query: str = """SELECT 
                        client_id, 
                        client_user_ref, 
                        client_is_user, 
                        client_name,
                        client_relation_uuid,
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        clients 
                        """
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# print(l_get_all_clients())

def l_get_all_clients_modern_full(anvil_user_id):
    query: str = """SELECT 
                        client_id, 
                        client_user_ref, 
                        client_is_user, 
                        client_name,
                        client_relation_uuid,
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp,
                        client_relation_uuid,
                        doc_store_uuid
                    FROM 
                        clients 
                        """
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# G.l_register_and_setup_user('[344816,583548811]',1)
# clients=l_get_all_clients_modern_full('[344816,583548811]')
# [print(c) for c in clients]




def l_get_client_by_id(client_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
                            client_relation_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        FROM 
                            clients 
                        WHERE 
                            client_id=?""", client_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchone()
        if results is None:
            return None
        else:
            res=[]
            res.append(dict(zip(columns, results)))
            # print(results[0])
            return res[0]


# a=l_get_client_by_id(140)
# print(a['client_relation_uuid'])

def l_get_client_by_id_modern(anvil_user_id, client_id):
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        cursor.execute("""SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
                            client_relation_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        FROM 
                            clients 
                        WHERE 
                            client_id=?""", client_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchone()
        if results is None:
            return None
        else:
            res=[]
            res.append(dict(zip(columns, results)))
            # print(results[0])
            return res[0]

def l_get_client_by_id_modern_full(anvil_user_id, client_id):
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        cursor.execute("""SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
                            client_relation_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp,
                            client_relation_uuid,
                            doc_store_uuid
                        FROM 
                            clients 
                        WHERE 
                            client_id=?""", client_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchone()
        if results is None:
            return None
        else:
            res=[]
            res.append(dict(zip(columns, results)))
            # print(results[0])
            return res[0]

# G.l_register_and_setup_user('[344816,583548811]',1)
# a=l_get_client_by_id_modern('[344816,583548811]',210)
# print(a['client_relation_uuid'])

def l_get_all_clients_of_a_user_id(user_id): #a user can have many clients
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
                            client_relation_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        FROM 
                            clients 
                        WHERE 
                            client_user_ref=?
                        order by 
                            client_is_user""", user_id)

        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if results is None:
            return None
        else:
            res=[]
            for row in results:
                res.append(dict(zip(columns, row)))
            # print(results[0])
            return res

# a=l_get_all_clients_of_a_user_id(100)
# if a is None:
#     print(None)
# elif type(a) is list:
#     for c in a:
#         print(c['client_name'])

def l_get_all_clients_of_a_user_id_modern(anvil_user_id, user_id): #a user can have many clients
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        cursor.execute("""SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
                            client_relation_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        FROM 
                            clients 
                        WHERE 
                            client_user_ref=?
                        order by 
                            client_is_user""", user_id)

        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if results is None:
            return None
        else:
            res=[]
            for row in results:
                res.append(dict(zip(columns, row)))
            # print(results[0])
            return res

# a=l_get_all_clients_of_a_user_id(100)
# if a is None:
#     print(None)
# elif type(a) is list:
#     for c in a:
#         print(c['client_name'])
def l_get_the_client_id_of_a_user_id(user_id): #every user is a client
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
                            client_relation_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        FROM 
                            clients 
                        WHERE 
                            client_user_ref=? and
                            client_is_user=?""", (user_id,1))
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if results == []:
            return None
        else:
            res=[]
            for row in results:
                res.append(dict(zip(columns, row)))
            # print(results[0])
            return res[0]['client_id']

# a=l_get_the_client_id_of_a_user_id(110)
# if a is None:
#     print(None)
# elif type(a) is list:
#     for c in a:
#         print(c['client_name'])
# else:
#     print(a)

def l_get_the_client_id_of_a_user_id_modern(anvil_user_id,user_id): #every user is a client
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        cursor.execute("""SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
                            client_relation_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        FROM 
                            clients 
                        WHERE 
                            client_user_ref=? and
                            client_is_user=?""", (user_id,1))
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if results == []:
            return None
        else:
            res=[]
            for row in results:
                res.append(dict(zip(columns, row)))
            # print(results[0])
            return res[0]['client_id']

def add_log_entry(user, current_timestamp, table_name, table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name, table_id, payload)

def l_add_client_to_clients  (user_ref,client_name="None",client_is_user=False):
    current_admin_user_rec = users.l_get_user_by_id(user_ref)
    client_relation_uuid=functions.make_uuid()
    if current_admin_user_rec is None:
        print('add_client: User given does not exist:', user_ref)
        return None
    else:
        if type(current_admin_user_rec)==dict:
            current_admin_user=current_admin_user_rec['admin_user']
            timestamp = functions.make_timestamp()
            azure = connections.Azure()
            client_relation_uuid=uuid.uuid1()
            doc_store_uuid=uuid.uuid4()
            with azure:
                cursor = azure.conn.cursor()
                query = """insert into 
                             clients (
                                 client_user_ref,
                                 client_is_user,
                                 client_name,
                                 client_relation_uuid,
                                 admin_user, 
                                 admin_previous_entry,
                                 admin_timestamp,
                                 admin_active,
                                 client_relation_uuid,
                                 doc_store_uuid
                             )
                             values (?,?,?,?,?,?,?,?,?,?)"""
                cursor.execute(query,
                               (user_ref,
                                client_is_user,
                                client_name,
                                client_relation_uuid,
                                current_admin_user,
                                0,
                                timestamp,
                                1,
                                client_relation_uuid,
                                doc_store_uuid
                                ))
                cursor.commit()
                cursor.execute("SELECT @@IDENTITY AS ID;")
                last_id = int(cursor.fetchone()[0])
                return last_id
        else:
            print('add_client: current_admin_usershould be dict!:', current_admin_user_rec, type(current_admin_user_rec))
            return None

#l_add_client_to_clients(100,"Tempo zu löschen",client_is_user=True)

def l_add_client_to_clients_modern  (anvil_user_id, user_ref,client_name="None",client_is_user=False):
    current_admin_user_rec = users.l_get_user_by_id(user_ref)
    client_relation_uuid = functions.make_uuid()
    if current_admin_user_rec is None:
        print('add_client: User given does not exist:', user_ref)
        return None
    else:
        if type(current_admin_user_rec)==dict:
            current_admin_user=current_admin_user_rec['admin_user']
            timestamp = functions.make_timestamp()
            azure = G.cached.conn_get(anvil_user_id)
            client_relation_uuid=uuid.uuid1()
            doc_store_uuid=uuid.uuid4()
            with azure:
                cursor = azure.cursor()
                query = """insert into 
                                             clients (
                                                 client_user_ref,
                                                 client_is_user,
                                                 client_name,
                                                 client_relation_uuid,
                                                 admin_user, 
                                                 admin_previous_entry,
                                                 admin_timestamp,
                                                 admin_active,
                                                 client_relation_uuid,
                                                 doc_store_uuid
                                             )
                                             values (?,?,?,?,?,?,?,?,?,?)"""
                cursor.execute(query,
                               (user_ref,
                                client_is_user,
                                client_name,
                                client_relation_uuid,
                                current_admin_user,
                                0,
                                timestamp,
                                1,
                                client_relation_uuid,
                                doc_store_uuid
                                ))
                cursor.commit()
                cursor.execute("SELECT @@IDENTITY AS ID;")
                last_id = int(cursor.fetchone()[0])
                return last_id
        else:
            print('add_client: current_admin_user should be dict!:', current_admin_user_rec, type(current_admin_user_rec))
            return None



def l_ensure_link_code_client_modern(anvil_user_id, client_id):
    client_record=l_get_client_by_id_modern(anvil_user_id,client_id)
    existing_client_relation_uuid=client_record['client_relation_uuid']
    if existing_client_relation_uuid is None:
        new_client_uuid= functions.make_uuid()
        azure = G.cached.conn_get(anvil_user_id)
        with azure:
            cursor = azure.cursor()
            query = """update clients 
                        set client_relation_uuid=?
                        where
                            client_id=?
                        """
            cursor.execute(query,(new_client_uuid,
                                  client_id)
                           )
            cursor.commit()
            return new_client_uuid
    else:
        return existing_client_relation_uuid

# G.l_register_and_setup_user('[344816,583548811]',1)
# print(l_ensure_link_code_client_modern('[344816,583548811]',130))


# l_add_client_to_clients(100,"Tempo zu löschen",client_is_user=True)




def l_update_client(client_id_to_change, user_ref, client_is_user,  name):  #update uuid is another function below!!
    current_admin_user_rec = users.l_get_user_by_id(user_ref)
    if current_admin_user_rec is None:
        print('update_client: User given does not exist:', user_ref)
        return None
    else:
        if type(current_admin_user_rec) != dict:
            print('add_client: current_admin_user should be dict!:', current_admin_user_rec,
                  type(current_admin_user_rec))
            return None
        else:
            current_admin_user = current_admin_user_rec['admin_user']
            current_timestamp = functions.make_timestamp()
            current_table_name = 'clients'
            current_table_id=client_id_to_change
            current_payload=str(l_get_client_by_id(client_id_to_change))
            #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
            previous_log_entry=add_log_entry(current_admin_user,
                                             current_timestamp,
                                             current_table_name,
                                             current_table_id,
                                             current_payload)
            #print(previous_log_entry)
            azure = connections.Azure()
            with azure:
                cursor3 = azure.conn.cursor()
                query="""   UPDATE 
                                clients 
                            SET 
                                client_user_ref=?,
                                client_is_user=?,
                                client_name=?,
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=?
                            WHERE 
                                EasyEL.dbo.clients.client_id=?"""
                cursor3.execute(query, (user_ref,client_is_user,name,current_admin_user, current_timestamp, previous_log_entry, 1, client_id_to_change))
                cursor3.commit()


# l_update_client(190, 160,False,"Roger Rabbit")

def l_update_client_modern(anvil_user_id, client_id_to_change, user_ref, client_is_user,  name):  #update uuid is another function below!!
    current_admin_user_rec =users.l_get_user_by_id_modern(anvil_user_id,user_ref)
    if current_admin_user_rec is None:
        print('update_client: User given does not exist:', user_ref)
        return None
    else:
        if type(current_admin_user_rec) != dict:
            print('add_client: current_admin_user should be dict!:', current_admin_user_rec,
                  type(current_admin_user_rec))
            return None
        else:
            current_admin_user = current_admin_user_rec['admin_user']
            current_timestamp = functions.make_timestamp()
            current_table_name = 'clients'
            current_table_id=client_id_to_change
            current_payload=str(l_get_client_by_id_modern_full(anvil_user_id, client_id_to_change))
            #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
            previous_log_entry=add_log_entry(current_admin_user,
                                             current_timestamp,
                                             current_table_name,
                                             current_table_id,
                                             current_payload)
            #print(previous_log_entry)
            azure = connections.Azure()
            with azure:
                cursor3 = azure.conn.cursor()
                query="""   UPDATE 
                                clients 
                            SET 
                                client_user_ref=?,
                                client_is_user=?,
                                client_name=?,
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=?
                            WHERE 
                                EasyEL.dbo.clients.client_id=?"""
                cursor3.execute(query, (user_ref,client_is_user,name,current_admin_user, current_timestamp, previous_log_entry, 1, client_id_to_change))
                cursor3.commit()


# l_update_client(190, 160,False,"Roger Rabbit")




def l_change_status_client(client_id, user_id, new_status):
    current_admin_user = users.l_get_admin_user_by_id(user_id)
    current_timestamp = functions.make_timestamp()
    current_table_name = 'cases'
    current_table_id = client_id
    current_payload = str(l_get_client_by_id(client_id))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry = add_log_entry(
        current_admin_user,
        current_timestamp,
        current_table_name,
        current_table_id,
        current_payload)
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""  UPDATE 
                                clients
                            SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE client_id=?""",
                       (current_admin_user,
                        current_timestamp,
                        previous_log_entry,
                        new_status,
                        client_id))
        cursor.commit()
# l_change_status_client(150,100,True)

def l_change_client_relation_uuid_modern(anvil_user_id, client_id, user_id):
    current_admin_user = users.l_get_admin_user_by_id(user_id)
    current_timestamp = functions.make_timestamp()
    current_table_name = 'cases - update client_relation_uuid'
    current_table_id = client_id
    current_payload = str(l_get_client_by_id(client_id))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry = add_log_entry(
        current_admin_user,
        current_timestamp,
        current_table_name,
        current_table_id,
        current_payload)

    # get existing relation uuid
    existing_client_relation_uuid = l_get_client_by_id_modern(anvil_user_id,client_id)['client_relation_uuid']
    print(existing_client_relation_uuid,'existing uuid')
    #generate new relation uuid
    new_client_relation_uuid = functions.make_uuid()
    print(new_client_relation_uuid,'new uuid')
    #generate new relation uuid

    #change the relationsship-table
    relations.l_change_existing_relationsship_uuid_modern(anvil_user_id,current_admin_user,existing_client_relation_uuid,new_client_relation_uuid)


    #now the client_entry

    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        cursor.execute("""  UPDATE 
                                clients
                            SET 
                                client_relation_uuid=?,
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE client_id=?""",
                        (new_client_relation_uuid,
                        current_admin_user,
                        current_timestamp,
                        previous_log_entry,
                        1,
                        client_id))
        cursor.commit()
    return str(new_client_relation_uuid)
#l_change_client_relation_uuid('[344816,524933170]', 210, 100)

def l_get_client_string_from_client_id(link_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """select 
                            cdm.payload_text,
                            f1.field_id
                            from client_data_main as cdm
                            join doc_set_comp as dsc on dsc.dsc_id = cdm.dsc_reference
                            join doc_set_def as dsd on dsd.dsd_id=dsc.dsd_reference
                            join fields as f1 on f1.field_id=dsc.field_id_reference
                            join EasyEL.dbo.cases as ca on ca.case_id = cdm.case_id_reference
                            join clients on client_id = ca.client_id_ref
                        where 
                                dsd.dsd_id=? and 
                                (f1.field_id=? or f1.field_id=? or f1.field_id=? or f1.field_id=? or f1.field_id=?) 
                                and clients.client_relation_uuid=?"""

        cursor.execute(query, (130,  #dsd für Address
                               110,  # Name
                               120,  # Vorname
                               140,  # Strasse
                               130,  # PLZ
                               170,  # Town
                                link_id) )

        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if results == []:
            return None
        else:
            res = []
            for row in results:
                res.append(dict(zip(columns, row)))
            info={}
            for r in res:
                info[r['field_id']]=r['payload_text']
        address = ("{}, {}, {}, {}, {},").format(info[110], info[120], info[140],info[130],info[170])
        return address

#print(l_get_client_string_from_client_id('BE979A7A-A6C2-11ED-8FF5-ACDE48001122'))

def l_ensure_doc_store_uuid(anvil_user_id):
    clients = l_get_all_clients_modern_full(anvil_user_id)
    for c in clients:
        if c['doc_store_uuid'] is None:
            current_client_id = c['client_id']
            new_doc_store_uuid=uuid.uuid4()
            azure = G.cached.conn_get(anvil_user_id)
            with azure:
                cursor = azure.cursor()
                cursor.execute("""  UPDATE 
                                          clients
                                      SET 
                                          doc_store_uuid=?
                                      WHERE 
                                        client_id=?""",
                                       (new_doc_store_uuid,
                                        current_client_id))
                cursor.commit()
            print('Client {}, doc_store_uuid_set to: {}'.format(current_client_id,new_doc_store_uuid))
        else:
            print('Client {} already set!'.format(c['client_id']))


# G.l_register_and_setup_user('[344816,583548811]',1)
# l_ensure_doc_store_uuid('[344816,583548811]')
def l_get_doc_store_uuid_for_a_client(anvil_user_id, client_id):
    azure=G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query="""
        select 
          doc_store_uuid
        from clients
        where client_id=?
        """
        cursor.execute(query,client_id)
        result=cursor.fetchone()
        if result is None:
            cursor2 = azure.cursor()
            new_doc_store_id=str(uuid.uuid4())
            query = """UPDATE 
                         clients 
                       SET 
                         doc_store_uuid=?
                       WHERE 
                         EasyEL.dbo.clients.client_id=?"""
            cursor2.execute(query,new_doc_store_id,client_id)
            return new_doc_store_id
        else:
            return result[0]

        # print(columns)
# G.l_register_and_setup_user('[344816,583548811]',1)
# print(l_get_doc_store_uuid_for_a_client('[344816,583548811]',210))