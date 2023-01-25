import connections


def log_add_log_entry(user, current_timestamp, table_name,table_id, payload):
    azure = connections.Azure()
    with azure:
        cursor=azure.conn.cursor()
        cursor.execute("insert into dbo.log (editing_user,timestamp, table_name, reference_to_table_id, payload)"
                       "values (?,?,?,?,?)",
                       (user, current_timestamp, table_name, table_id, payload))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return last_id
