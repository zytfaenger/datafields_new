from functions import make_timestamp, get_user
from log_functions import log_add_log_entry
from connections import get_connection

conn = get_connection()

cursor = conn.cursor()
def l_get_active_field_types():
    query: str = "SELECT ft_id, ft_type, ft_description, ft_sequence,  ft_shadow_store, admin_user, admin_previous_entry, admin_active,admin_timestamp  from dbo.field_types where admin_active=1 order by ft_sequence"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

def l_get_active_field_types_for_dd():
    query: str = """SELECT  
                        ft_type,
                        ft_description,
                        ft_id
                    from 
                        dbo.field_types 
                    where 
                        admin_active=1 order by ft_sequence"""
    cursor.execute(query)
    # print(columns)
    results = []
    for row in cursor.fetchall():
        entry = row[0]+": "+row[1]
        list=(entry,row[2])
        results.append(list)
    return results

#print(l_get_active_field_types_for_dd())

def l_get_all_field_types():
    query: str = "select ft_id, ft_type, ft_description, ft_sequence, ft_shadow_store, admin_user, admin_previous_entry, admin_active, admin_timestamp  from dbo.field_types order by ft_sequence"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_select_field_types_by_shortname(type):
    cursor.execute("""select
                        ft_id,
                        ft_type, 
                        ft_description, 
                        ft_sequence, 
                        ft_shadow_store, 
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp 
                    from 
                        dbo.field_types 
                    where ft_type=?""",
                   type)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results



def l_select_field_type_by_id(id):
    cursor.execute("""select 
                            ft_id, 
                            ft_type, 
                            ft_description, 
                            ft_sequence, 
                            ft_shadow_store
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp 
                        from 
                            dbo.field_types 
                        where 
                            ft_id=?""",
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


def l_add_field_type(type,description,sequence,shadow):
    user=get_user()
    timestamp=make_timestamp()
    cursor.execute("insert into dbo.field_types (ft_type, ft_description, ft_sequence, ft_shadow_store, admin_user, admin_timestamp, admin_previous_entry, admin_active) "
                   "values (?,?,?,?,?,?,?,?)",
                   (type, description, sequence, shadow, user, timestamp,0,1))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    return last_id


def l_update_field_type(id_to_change, type, description,sequence, shadow):
    #print('l_updateft:',id_to_change,type,description,sequence)
    current_user=get_user()
    current_timestamp = make_timestamp()
    current_table_name = 'field_types'
    current_table_id=id_to_change
    current_payload=str(l_select_field_type_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)
    cursor3=conn.cursor()
    cursor3.execute("""UPDATE 
                            field_types 
                        SET 
                            ft_type=?,
                            ft_description=?,
                            ft_sequence=?,
                            ft_shadow_store=?, 
                            admin_user=?,
                            admin_timestamp=?,
                            admin_previous_entry=?,
                            admin_active=?
                        WHERE 
                            ft_id=?""",
                    (type, description, sequence, shadow, current_user, current_timestamp, previous_log_entry,1, id_to_change))
    cursor3.commit()


def l_change_status_field_type_by_short_name(type,new_status:int):
    #print(short_name)
    current_user=get_user()
    #print(current_user)
    current_timestamp = make_timestamp()
    current_table_name = 'field_types'
    id_to_change=l_select_field_types_by_shortname(type)['ft_id']
    current_table_id = id_to_change
    current_payload=str(l_select_field_type_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    cursor.execute("UPDATE field_types SET admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? WHERE ft_type=?",(current_user,current_timestamp,previous_log_entry,new_status,type))
    cursor.commit()


def l_change_status_field_type_by_id(id_to_change:int,new_status:int):
    current_user=get_user()
    #print(current_user)
    current_timestamp = make_timestamp()
    current_table_name = 'field_types'
    current_table_id=id_to_change
    current_payload=str(l_select_field_type_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)


    cursor.execute("UPDATE field_types SET admin_user=?,admin_timestamp=?,admin_previous_entry=?,admin_active=? WHERE ft_id=?",(current_user,current_timestamp,previous_log_entry,new_status,id_to_change))
    cursor.commit()