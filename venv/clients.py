import connections
import functions
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

def l_get_client_by_id(client_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
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


# a=l_get_client_by_id(110)
# print(a['client_name'])

def l_get_all_clients_of_a_user_id(user_id): #a user can have many clients
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""SELECT 
                            client_id, 
                            client_user_ref, 
                            client_is_user, 
                            client_name,
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
    if current_admin_user_rec is None:
        print('add_client: User given does not exist:', user_ref)
        return None
    else:
        if type(current_admin_user_rec)==dict:
            current_admin_user=current_admin_user_rec['admin_user']
            timestamp = functions.make_timestamp()
            azure = connections.Azure()
            with azure:
                cursor = azure.conn.cursor()
                query = """insert into 
                             clients (
                                 client_user_ref,
                                 client_is_user,
                                 client_name,
                                 admin_user, 
                                 admin_previous_entry,
                                 admin_timestamp,
                                 admin_active
                             )
                             values (?,?,?,?,?,?,?)"""
                cursor.execute(query,
                               (user_ref,
                                client_is_user,
                                client_name,
                                current_admin_user,
                                0,
                                timestamp,
                                1
                                ))
                cursor.commit()
                cursor.execute("SELECT @@IDENTITY AS ID;")
                last_id = int(cursor.fetchone()[0])
                return last_id
        else:
            print('add_client: current_admin_usershould be dict!:', current_admin_user_rec, type(current_admin_user_rec))
            return None

# l_add_client_to_clients(100,"Tempo zu löschen",client_is_user=True)

def l_add_client_to_clients_modern  (anvil_user_id, user_ref,client_name="None",client_is_user=False):
    current_admin_user_rec = users.l_get_user_by_id(user_ref)
    if current_admin_user_rec is None:
        print('add_client: User given does not exist:', user_ref)
        return None
    else:
        if type(current_admin_user_rec)==dict:
            current_admin_user=current_admin_user_rec['admin_user']
            timestamp = functions.make_timestamp()
            azure = G.cached.conn_get(anvil_user_id)
            with azure:
                cursor = azure.cursor()
                query = """insert into 
                             clients (
                                 client_user_ref,
                                 client_is_user,
                                 client_name,
                                 admin_user, 
                                 admin_previous_entry,
                                 admin_timestamp,
                                 admin_active
                             )
                             values (?,?,?,?,?,?,?)"""
                cursor.execute(query,
                               (user_ref,
                                client_is_user,
                                client_name,
                                current_admin_user,
                                0,
                                timestamp,
                                1
                                ))
                cursor.commit()
                cursor.execute("SELECT @@IDENTITY AS ID;")
                last_id = int(cursor.fetchone()[0])
                return last_id
        else:
            print('add_client: current_admin_user should be dict!:', current_admin_user_rec, type(current_admin_user_rec))
            return None

# l_add_client_to_clients(100,"Tempo zu löschen",client_is_user=True)




def l_update_client(client_id_to_change, user_ref, client_is_user,  name):
    current_admin_user_rec = users.l_get_user_by_id(user_ref)
    if current_admin_user_rec is None:
        print('update_client: User given does not exist:', user_ref)
        return None
    else:
        if type(current_admin_user_rec) != dict:
            print('add_client: current_admin_usershould be dict!:', current_admin_user_rec,
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

