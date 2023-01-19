import uuid
import connections
import functions
import log_functions

conn = connections.get_connection()

cursor = conn.cursor()


def l_get_client_uuid_columns():
    query: str = """SELECT 
                        client_uuid_id,
                        client_id,
                        client_uuid,
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        client_uuid 
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
# print(l_get_client_uuid_columns())

def l_get_active_client_uuids():
    query: str = """SELECT 
                       client_uuid_id,
                        client_id,
                        client_uuid,
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        client_uuid 
                    WHERE 
                        admin_active=?"""
    cursor.execute(query,1)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = cursor.fetchall()
    if results == []:
        return None
    else:
        res = []
        for row in results:
            res.append(dict(zip(columns, row)))
        return res

# print(l_get_active_client_uuids())



def l_get_all_client_uuids():
    query: str = """SELECT 
                           client_uuid_id,
                            client_id,
                            client_uuid,
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        FROM 
                            client_uuid """
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = cursor.fetchall()
    if not results:
        return None
    else:
        res = []
        for row in results:
            res.append(dict(zip(columns, row)))
        return res

# print(l_get_all_client_uuids())


def l_get_client_id_by_client_uuid_id(client_uuid_id):

    cursor.execute("""SELECT 
                        client_uuid_id,
                        client_id,
                        client_uuid,
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        client_uuid 
                    WHERE 
                        client_uuid_id=?""", client_uuid_id)
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

# print(l_get_client_id_by_client_uuid_id(3))


def l_get_client_id_by_client_id(client_id):

    cursor.execute("""SELECT 
                        client_uuid_id,
                        client_id,
                        client_uuid,
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        client_uuid 
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

# print(l_get_client_id_by_client_id(350))


def l_get_client_id_by_client_uuid(client_uuid):
    cursor.execute("""SELECT 
                        client_uuid_id,
                        client_id,
                        client_uuid,
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        client_uuid 
                    WHERE 
                        client_uuid=?""", client_uuid)
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

#print(l_get_client_id_by_client_uuid('6F87BF98-978E-11ED-9B62-ACDE48001122'))


#print(l_get_anvil_user_components_as_list("[344816,524933170]")[0])

def add_log_entry(user, current_timestamp, table_name, table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name, table_id, payload)

def create_admin_user():
    return functions.make_uuid()


def l_add_client_uuid(admin_user_id, client_id):
    new_client_uuid = functions.make_uuid()
    admin_user = admin_user_id
    timestamp = functions.make_timestamp()

    query = """insert into client_uuid (
                     client_id,
                     client_uuid,
                     admin_user, 
                     admin_previous_entry, 
                     admin_active, 
                     admin_timestamp 
                     )
                     values (?,?,?,?,?,?)"""
    cursor.execute(query,
                   (client_id,
                    new_client_uuid,
                    admin_user,
                    0,
                    1,
                    timestamp
                    ))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    return last_id

#print(l_add_client_uuid('1399C078-6C0F-11ED-B0BC-ACDE48001122',370))

def l_upate_client_uuid():
   print("Careful: any updating has to be done in accordance with client_entry and relations")

def l_change_status_user_id():
    print("Careful: not applicable")