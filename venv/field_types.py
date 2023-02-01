import functions
import log_functions
import connections

def l_get_active_field_types():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            ft_id, 
                            ft_type, 
                            ft_description, 
                            ft_sequence,  
                            ft_shadow_store, 
                            admin_user, 
                            admin_previous_entry, 
                            admin_active,admin_timestamp  from dbo.field_types where admin_active=1 order by ft_sequence"""
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

def l_get_active_field_types_for_dd():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """select 
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
                        order by 
                            ft_sequence"""
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


def l_select_field_types_by_shortname(type):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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

# print(l_select_field_type_by_id(170)['ft_shadow_store'])
# print(l_select_field_type_by_id(170))

def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name,table_id, payload)


def l_add_field_type(type,description,sequence,shadow):
    user=functions.get_user()
    timestamp=functions.make_timestamp()
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("insert into dbo.field_types (ft_type, ft_description, ft_sequence, ft_shadow_store, admin_user, admin_timestamp, admin_previous_entry, admin_active) "
                       "values (?,?,?,?,?,?,?,?)",
                       (type, description, sequence, shadow, user, timestamp,0,1))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return last_id


def l_update_field_type(id_to_change, type, description,sequence, shadow):
    #print('l_updateft:',id_to_change,type,description,sequence)
    current_user=functions.get_user()
    current_timestamp = functions.make_timestamp()
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
    azure = connections.Azure()
    with azure:
        cursor3 = azure.conn.cursor()
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
    current_user=functions.get_user()
    #print(current_user)
    current_timestamp = functions.make_timestamp()
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
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""  UPDATE 
                                field_types 
                            SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE 
                                ft_type=?""",(current_user,current_timestamp,previous_log_entry,new_status,type))
        cursor.commit()


def l_change_status_field_type_by_id(id_to_change:int,new_status:int):
    current_user=functions.get_user()
    #print(current_user)
    current_timestamp = functions.make_timestamp()
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

    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""    UPDATE 
                                field_types 
                              SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                              WHERE 
                                 ft_id=?""",(current_user,
                                             current_timestamp,
                                             previous_log_entry,
                                             new_status,
                                             id_to_change))
        cursor.commit()