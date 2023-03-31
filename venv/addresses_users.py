import functions
import log_functions
import users
import connections

conn = connections.get_connection()

cursor = conn.cursor()



def add_address(last,first,email,usr_id):
    admin_user = users.l_get_admin_user_by_id(usr_id)
    timestamp = functions.make_timestamp()
    query = """insert into 
                     addresses (
                     address_LastName,
                     address_FirstName,
                     anvil_user_id_E_Mail,
                     user_id_reference, 
                     admin_user, 
                     admin_previous_entry, 
                     admin_active, 
                     admin_timestamp)
                     values (?,?,?,?,?,?,?,?)"""
    cursor.execute(query,
                   (last,
                    first,
                    email,
                    usr_id,
                    admin_user,
                    0,
                    1,
                    timestamp))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    return last_id

def l_get_address_for_userid(user_id_reference):
    cursor.execute("""SELECT 
                        address_id,
                        address_LastName,
                        address_FirstName,
                        anvil_user_id_E_Mail, 
                        user_id_reference,                
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        addresses
                    where 
                        user_id_reference=?""", user_id_reference)
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


def l_update_address(user_id_reference_to_change, admin_user, last, first, email):
    # print('l_updateft:',id_to_change,type,description,sequence)
    current_admin_user = admin_user
    current_timestamp = functions.make_timestamp()
    current_table_name = 'addresses'
    current_table_id = l_get_address_for_userid(user_id_reference_to_change)['address_id']
    current_payload = str(l_get_address_for_userid(user_id_reference_to_change))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry = log_functions.log_add_log_entry(
        current_admin_user,
        current_timestamp,
        current_table_name,
        current_table_id,
        current_payload)
    # print(previous_log_entry)
    cursor3 = conn.cursor()
    query = """   UPDATE 
                    addresses 
                SET 
                    address_LastName=?,
                    address_FirstName=?,
                    anvil_user_id_E_Mail=?,
                    user_id_reference=?,
                    admin_user=?,
                    admin_previous_entry=?,
                    admin_active=?,
                    admin_timestamp=?
                WHERE 
                    address_id=?"""
    cursor.execute(query, (last,
                           first,
                           email,
                           user_id_reference_to_change,
                           current_admin_user,
                           previous_log_entry,
                           1,
                           current_timestamp,
                           current_table_id))
    cursor3.commit()
    # (id_to_change, "updated")

#l_update_address(110, 'BAED397C-8F46-11ED-91CE-ACDE48001122', 'Schumacher', 'Martin Karl', 'ms@gmail.com')
