from connections import get_connection

# Dieses Script fügt Daten in eine Azure-Datenbank ein!


conn = get_connection()
cursor = conn.cursor()

def log_add_log_entry(user, current_timestamp, table_name,table_id, payload):
    cursor2=conn.cursor()
    cursor2.execute("insert into dbo.log (editing_user,timestamp, table_name, reference_to_table_id, payload)"
                   "values (?,?,?,?,?)",
                   (user, current_timestamp, table_name, table_id, payload))
    cursor2.commit()
    cursor2.execute("SELECT @@IDENTITY AS ID;")
    last_id = int(cursor2.fetchone()[0])
    cursor2.close
    return last_id
