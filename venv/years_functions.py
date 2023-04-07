import globals as G
def l_select_years_for_dropdown(anvil_user_id):
    # G.l_register_and_setup_user('[344816,583548811]',1)
     try:
        azure = G.cached.conn_get(anvil_user_id)
     except:
        G.l_register_and_setup_user('[344816,583548811]',1)
        azure = G.cached.conn_get(anvil_user_id)
     with azure:
        cursor = azure.cursor()
        cursor.execute("""SELECT 
                                year_text,
                                year
                            FROM 
                                years
                            order by year_sort,year
                                """)
        columns = [column[0] for column in cursor.description]

        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            # results.append(dict(zip(columns, row)))
            results.append((row[0],row[1]))
        return results


#print(l_select_years_for_dropdown('[344816,583548811]'))