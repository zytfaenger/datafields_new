import functions
import connections
import log_functions

def l_get_active_languages():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """select 
                            lang_id, 
                            lang_short, 
                            lang_german, 
                            lang_local, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry,
                            admin_active 
                        from 
                            dbo.Languages 
                        where 
                            admin_active=1"""
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


def l_get_all_languages():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """select 
                            lang_id, 
                            lang_short, 
                            lang_german, 
                            lang_local, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry,
                            admin_active 
                        from 
                            dbo.Languages"""
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


def l_select_language_by_shortname(short_name):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                                lang_id, 
                                lang_short, 
                                lang_german, 
                                lang_local 
                            from 
                                dbo.languages 
                            where 
                                lang_short=?""",
                                                short_name)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results



def l_select_language_by_id(lang_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                                lang_id, 
                                lang_short, 
                                lang_german, 
                                lang_local, 
                                admin_user, 
                                admin_timestamp,
                                admin_previous_entry,
                                admin_active 
                            from 
                                dbo.languages 
                            where 
                                lang_id=?""",
                                        lang_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results[0]


def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    azure = connections.Azure()
    with azure:
        cursor2 = azure.conn.cursor()
        cursor2.execute("""insert into 
                                dbo.log 
                                    (editing_user,
                                    timestamp, 
                                    table_name, 
                                    reference_to_table_id, 
                                    payload)
                                values 
                                (?,?,?,?,?)""",
                                (user, current_timestamp, table_name, table_id, payload))
        cursor2.commit()
        cursor2.execute("SELECT @@IDENTITY AS ID;")
        cursor2.close
        last_id = int(cursor2.fetchone()[0])
        return last_id


def l_add_language(short_name, german_name, local_name):
    user=functions.get_user()
    timestamp=functions.make_timestamp()
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""insert into 
                                dbo.languages 
                                    (lang_short, 
                                    lang_german, 
                                    lang_local,
                                    admin_user,
                                    admin_timestamp,
                                    admin_previous_entry,
                                    admin_active) 
                                (values (?,?,?,?,?,?,?)""",
                                        (short_name, german_name, local_name, user, timestamp,0,1))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return last_id


def l_update_language(id_to_change, short_name, german_name, local_name):
    current_user=functions.get_user()
    current_timestamp = functions.make_timestamp()
    current_table_name = 'languages'
    current_table_id=id_to_change
    current_payload=str(l_select_language_by_id(id_to_change))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
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
                                languages 
                            SET 
                                lang_short=?,
                                lang_german=?,
                                lang_local=?,
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE 
                                lang_id=?""",
                                      (short_name,
                                       german_name,
                                       local_name,
                                       current_user,
                                       current_timestamp,
                                       previous_log_entry,
                                       1,
                                       id_to_change))
        cursor3.commit()


def l_change_status_language_by_short_name(short_name,new_status:int):
    #print(short_name)
    current_user=functions.get_user()
    #print(current_user)
    current_timestamp = functions.make_timestamp()
    current_table_name = 'languages'
    id_to_change=l_select_language_by_shortname(short_name)['lang_id']
    current_table_id = id_to_change
    current_payload=str(l_select_language_by_id(id_to_change))
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
                                languages 
                            SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE 
                                lang_short=?""",
                       (current_user,current_timestamp,previous_log_entry,new_status,short_name))
        cursor.commit()


def l_change_status_language_by_id(id_to_change:int,new_status:int):
    current_user=functions.get_user()
    #print(current_user)
    current_timestamp = functions.make_timestamp()
    current_table_name = 'languages'
    current_table_id=id_to_change
    current_payload=str(l_select_language_by_id(id_to_change))
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
                                languages 
                            SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE 
                            lang_id=?""",
                                (current_user,current_timestamp,previous_log_entry,new_status,id_to_change))
        cursor.commit()