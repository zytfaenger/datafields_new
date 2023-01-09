from functions import make_timestamp, get_user
from log_functions import log_add_log_entry
from connections import get_connection

conn = get_connection()

cursor = conn.cursor()


def l_get_fields_table_columns():
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
                        field_id=? 
                    ORDER BY field_sequence"""

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
# print(l_get_fields_table_columns())

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
                        admin_active=?
                    ORDER BY field_sequence"""
    cursor.execute(query,1)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

print(l_get_active_fields())


def l_get_active_fields_for_shadow_dsd():
    active=True
    shd_store=True
    query: str = """SELECT 
                        field_id, 
                        field_sequence,
                        field_typ_id,
                        field_types.ft_shadow_store
                    FROM 
                        fields
                        inner join field_types on fields.field_typ_id = field_types.ft_id
                    WHERE 
                        fields.admin_active=? and field_types.ft_shadow_store=?
                    ORDER BY field_sequence"""
    cursor.execute(query,(active,shd_store))
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

# print(l_get_active_fields_for_shadow_dsd())


def l_get_active_fields_for_dd(filter="%"):
    query: str = """SELECT 
                        field_name,
                        field_id
                    FROM 
                        fields 
                    WHERE 
                        admin_active=? and field_name like ?
                    ORDER BY field_sequence"""

    cursor.execute(query,1,filter)
    columns = [column[0] for column in cursor.description]
    # print(columns)
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

# print(l_get_active_fields_for_dd(filter="%La%"))

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
# print(l_get_all_fields())

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
    results = cursor.fetchone()
    if results is None:
        return None
    else:
        res=[]
        res.append(dict(zip(columns, results)))
        # print(results[0])
        return res[0]


#print(l_select_field_by_id(160)['field_typ_id'])


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
    # print('l_get_field_sub_group_for_id', sub_group)
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
                   fd_group,
                   fd_group_order,
                   fd_sub_group,
                   fd_sub_group_value):
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
    # (id_to_change, "updated")


# Zuerst entsprechendes Feld erzeugen!
# l_update_field(290, 100,"Test2","das ist ein Testfeld2",2)
#l_update_field(160, 170, "Haupttitel 1", None, 1, "Case", 1, "aaaaa")

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
