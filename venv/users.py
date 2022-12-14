import addresses_users
import uuid
import connections
import functions
from functions import make_timestamp
from log_functions import log_add_log_entry

conn = connections.get_connection()

cursor = conn.cursor()


def l_get_user_table_columns():
    query: str = """SELECT 
                        user_id,
                        user_anvil_user,
                        anvil_user_1_int,
                        anvil_user_1_int,
                        temp_user,
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        users 
                    WHERE 
                        user_id=?"""

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
# print(l_get_user_table_columns())

def l_get_active_users():
    query: str = """SELECT 
                        user_id,
                        user_anvil_user,
                        anvil_user_1_int,
                        anvil_user_1_int,  
                        temp_user,                      
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        users 
                    WHERE 
                        admin_active=?"""
    cursor.execute(query,1)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

# print(l_get_active_users())



def l_get_all_users():
    query: str = """SELECT 
                        user_id,
                        user_anvil_user,
                        anvil_user_1_int,
                        anvil_user_1_int,   
                        temp_user,                         
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        users 
                        """
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

# print(l_get_all_users())

def l_get_user_by_id(usr_id):
    cursor.execute("""SELECT 
                        user_id,
                        user_anvil_user,
                        anvil_user_1_int,
                        anvil_user_2_int,
                        temp_user,                    
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        users 
                    where 
                        user_id=?""", usr_id)
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

# a=l_select_user_by_id(100)
# print(a['anvil_user_2_int'])

def l_get_userid_for_anvil_user(anvil_usr_id:str):
    cursor.execute("""SELECT 
                        user_id,
                        user_anvil_user,
                        anvil_user_1_int,
                        anvil_user_2_int, 
                        temp_user,                   
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        users 
                    where 
                        user_anvil_user=?""", anvil_usr_id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = cursor.fetchone()
    if results is None:
        return None
    else:
        res=[]
        res.append(dict(zip(columns, results)))
        # print(results[0])
        return res[0]['user_id']

#print(l_get_userid_for_anvil_user('[344816,524933170]'))


def l_get_userid_for_temp_user_uuid(temp_usr_uuid:str):
    tmp_usr_uuid=uuid.UUID(temp_usr_uuid)
    cursor.execute("""SELECT 
                        user_id,
                        user_anvil_user,
                        anvil_user_1_int,
                        anvil_user_2_int,
                        temp_user,                    
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        users 
                    where 
                        temp_user=?""", temp_usr_uuid)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = cursor.fetchone()
    if results is None:
        return None
    else:
        res=[]
        res.append(dict(zip(columns, results)))
        # print(results[0])
        return res[0]['user_id']

#print(l_get_userid_for_temp_user_uuid('FA12615A-8FFE-11ED-85CC-ACDE48001122'))








def l_get_anvil_user_as_list_from_table(usr_id):
    first_id =  l_get_user_by_id(usr_id)['anvil_user_1_int']
    second_id = l_get_user_by_id(usr_id)['anvil_user_2_int']
    anvil_list=[]
    anvil_list.append(first_id)
    anvil_list.append(second_id)
    return anvil_list

#print (l_get_anvil_user_as_list_from_table(100))

def l_get_anvil_user_components_as_list(anvil_user):
    a=anvil_user
    anv_user_as_list=[]
    anv_user_as_list.append(int(a.replace("[","").replace("]","").split(",")[0]))
    anv_user_as_list.append(int(a.replace("[","").replace("]","").split(",")[1]))
    return anv_user_as_list

#print(l_get_anvil_user_components_as_list("[344816,524933170]")[0])

def add_log_entry(user, current_timestamp, table_name, table_id, payload):
    return log_add_log_entry(user, current_timestamp, table_name, table_id, payload)

def create_admin_user():
    return functions.make_uuid()

def l_add_user  (u_anvil_usr,
                usr_last_name,
                usr_first_name,
                e_mail,
                anvil_user_two_int=True):
    anvil_user_l = l_get_anvil_user_components_as_list(u_anvil_usr)
    usr1=anvil_user_l[0]
    usr2=anvil_user_l[1]
    admin_user = create_admin_user()
    timestamp = make_timestamp()
    tmp_user=create_admin_user()

    query = """insert into 
                     users (
                     user_anvil_user, 
                     anvil_user_1_int, 
                     anvil_user_2_int,
                     temp_user,
                     admin_user, 
                     admin_previous_entry, 
                     admin_active, 
                     admin_timestamp 
                     )
                     values (?,?,?,?,?,?,?,?)"""
    cursor.execute(query,
                   (u_anvil_usr,
                    usr1,
                    usr2,
                    tmp_user,
                    admin_user,
                    0,
                    1,
                    timestamp
                    ))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    addresses_users.add_address(usr_last_name,usr_first_name,e_mail,last_id)
    return tmp_user

#print(l_add_user("[344817,524933171]","Schumacher","Martin","ms@gmail.com"))


def l_get_new_temp_user_id(anvil_usr_to_change):
    usr_id=l_get_userid_for_anvil_user(anvil_usr_to_change)
    if usr_id is None:
        print("get_new_temp_user: no such anvil usr!!")
    else:
        # print('l_get_new_temp_user:',anvil_usr_to_change)
        current_adminuser = l_get_user_by_id(usr_id)['admin_user']
        current_timestamp = make_timestamp()
        current_table_name = 'users'
        current_table_id = usr_id
        current_payload = str(l_get_user_by_id(usr_id))
        # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
        previous_log_entry = add_log_entry(
            current_adminuser,
            current_timestamp,
            current_table_name,
            current_table_id,
            current_payload)
        # print(previous_log_entry)
        cursor3 = conn.cursor()

        temp_usr=create_admin_user()
        # print('get_new_temp user: New temp user is:', temp_usr)
        # print("test of equality:",temp_usr==str(temp_usr),str(temp_usr))
        query = """UPDATE 
                        users
                    SET 
                        temp_user = ?,
                        admin_user=?,
                        admin_previous_entry=?,
                        admin_active=?,
                        admin_timestamp=?
                    WHERE 
                        user_id=?"""
        cursor.execute(query, (temp_usr,
                               current_adminuser,
                               previous_log_entry,
                               1,
                               current_timestamp,
                               usr_id))
        cursor3.commit()
        return str(temp_usr)
    # (id_to_change, "updated")
#l_get_new_temp_user_id('[344816,524933170]')


def l_change_status_user_id(anvil_usr:str, new_status):
    usr_id=l_get_userid_for_anvil_user(anvil_usr)
    current_admin_user = l_get_user_by_id(usr_id)['admin_user']
    current_timestamp = make_timestamp()
    current_table_name = 'users'
    current_table_id = usr_id
    current_payload = str(l_get_user_by_id(usr_id))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry = add_log_entry(
        current_admin_user,
        current_timestamp,
        current_table_name,
        current_table_id,
        current_payload)

    cursor.execute("""  UPDATE 
                            users
                        SET 
                            admin_user=?,
                            admin_timestamp=?,
                            admin_previous_entry=?,
                            admin_active=? 
                        WHERE user_id=?""",
                   (current_admin_user,
                    current_timestamp,
                    previous_log_entry,
                    new_status,
                    usr_id))
    cursor.commit()
# l_change_status_user_id('[344816,524933170]',True)