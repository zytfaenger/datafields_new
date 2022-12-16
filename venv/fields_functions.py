from functions import make_timestamp, get_user
from log_functions import log_add_log_entry
from connections import get_connection

conn = get_connection()

cursor = conn.cursor()


def l_get_active_fields():
    query: str = """SELECT 
                        field_id, 
                        field_typ_id, 
                        field_name, 
                        field_description, 
                        field_sequence, 
                        field_group, 
                        field_group_order, 
                        field_sub_group, 
                        field_sub_group_value, 
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        fields 
                    WHERE 
                        admin_active=1 
                    ORDER BY field_sequence"""

    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_get_all_fields():
    query: str = """SELECT 
                        field_id, 
                        field_typ_id, 
                        field_name, 
                        field_description, 
                        field_sequence, 
                        field_group, 
                        field_group_order, 
                        field_sub_group, 
                        field_sub_group_value, 
                        admin_user, 
                        admin_previous_entry, 
                        admin_active, 
                        admin_timestamp
                    FROM 
                        fields 
                    ORDER BY field_sequence"""
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results


def l_select_field_by_id(f_id):
    cursor.execute("""select 
                            field_id, 
                            field_typ_id, 
                            field_name, 
                            field_description, 
                            field_sequence, 
                            field_group, 
                            field_group_order, 
                            field_sub_group, 
                            field_sub_group_value, 
                            admin_user, 
                            admin_previous_entry, 
                            admin_active, 
                            admin_timestamp
                        from 
                            fields
                        where field_id=?""", f_id)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
        # print(results[0])
    return results[0]


# print(l_select_field_by_id(110))


def l_get_field_sub_group_value_for_id(f_id):
    query = """
        select  
            field_sub_group_value
        from
         fields
        where
         field_id=?   
    """
    cursor.execute(query, f_id)
    result = cursor.fetchone()
    for r in result:
        sub_group_value = r
        print('l_get_field_sub_group_value_for_id', sub_group_value)
        return sub_group_value

# print(l_get_field_sub_group_value_for_id(230))
def l_get_field_sub_group_for_id(f_id):
    query = """
        select  
            field_sub_group
        from
         fields
        where
         field_id=?   
    """
    cursor.execute(query, f_id)
    result = cursor.fetchone()
    sub_group = ""
    for r in result:
        sub_group = r
    print('l_get_field_sub_group_for_id', sub_group)
    return sub_group


def add_log_entry(user, current_timestamp, table_name, table_id, payload):
    return log_add_log_entry(user, current_timestamp, table_name, table_id, payload)


def l_add_field(fd_typ_id,
                fd_name,
                fd_description,
                fd_sequence,
                ft_field_group="Case",
                ft_group_order=1,
                ft_subgroup=None,
                ft_sub_group_value=None):
    admin_user = get_user()
    timestamp = make_timestamp()
    query = """insert into 
                     fields (
                     field_typ_id,
                     field_name,
                     field_description,
                     field_sequence,
                     field_group,
                     field_group_order,
                     field_sub_group,
                     field_sub_group_value,
                     admin_user,
                     admin_previous_entry,
                     admin_active,
                     admin_timestamp)
                     values (?,?,?,?,?,?,?,?,?,?,?,?)"""
    cursor.execute(query,
                   (fd_typ_id,
                    fd_name,
                    fd_description,
                    fd_sequence,
                    ft_field_group,
                    ft_group_order,
                    ft_subgroup,
                    ft_sub_group_value,
                    admin_user,
                    0,
                    1,
                    timestamp))
    cursor.commit()
    cursor.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor.fetchone()[0])
    return last_id


# l_add_field(100,"test","das ist ein Testfeld",2)


def l_update_field(id_to_change,
                   fd_typ_id,
                   fd_name,
                   fd_description,
                   fd_sequence,
                   fd_group="Case",
                   fd_group_order=1,
                   fd_sub_group=None,
                   fd_sub_group_value=None):
    # print('l_updateft:',id_to_change,type,description,sequence)
    current_adminuser = get_user()
    current_timestamp = make_timestamp()
    current_table_name = 'fields'
    current_table_id = id_to_change
    current_payload = str(l_select_field_by_id(id_to_change))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry = add_log_entry(
        current_adminuser,
        current_timestamp,
        current_table_name,
        current_table_id,
        current_payload)
    # print(previous_log_entry)
    cursor3 = conn.cursor()
    query = """   UPDATE 
                    fields 
                SET 
                    field_typ_id=?,
                    field_name=?,
                    field_description=?,
                    field_sequence=?,
                    field_group=?,
                    field_group_order=?,
                    field_sub_group=?,
                    field_sub_group_value=?,
                    admin_user=?,
                    admin_previous_entry=?,
                    admin_active=?,
                    admin_timestamp=?
                WHERE 
                    field_id=?"""
    cursor.execute(query, (fd_typ_id,
                           fd_name,
                           fd_description,
                           fd_sequence,
                           fd_group,
                           fd_group_order,
                           fd_sub_group,
                           fd_sub_group_value,
                           current_adminuser,
                           previous_log_entry,
                           1,
                           current_timestamp,
                           id_to_change))
    cursor3.commit()


# Zuerst entsprechendes Feld erzeugen!
# l_update_field(290, 100,"Test2","das ist ein Testfeld2",2)


def l_change_status_field_id(id_to_change, new_status):
    current_user = get_user()
    # print(current_user)
    current_timestamp = make_timestamp()
    current_table_name = 'cases'
    current_table_id = id_to_change
    current_payload = str(l_select_field_by_id(id_to_change))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry = add_log_entry(
        current_user,
        current_timestamp,
        current_table_name,
        current_table_id,
        current_payload)

    cursor.execute("""  UPDATE 
                            fields
                        SET 
                            admin_user=?,
                            admin_timestamp=?,
                            admin_previous_entry=?,
                            admin_active=? 
                        WHERE field_id=?""",
                   (current_user,
                    current_timestamp,
                    previous_log_entry,
                    new_status, id_to_change))
    cursor.commit()
