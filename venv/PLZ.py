import connections

def l_select_plz_info_by_plz(PLZ):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
            select  
                PLZ_ID,
                Post_Code,
                Town,
                Kanton,
                Kanton_short  
            from 
                PLZ
            where
                Post_Code=?
            """
        cursor.execute(query,PLZ)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            entry=row[2]
            lentry=(entry,row[0])
            results.append(lentry)
        return results

# print(l_select_plz_info_by_plz(6005))

def l_select_plz_info_by_id(plz_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
        select  
            PLZ_ID,
            Post_Code,
            Town,
            Kanton,
            Kanton_short  
        from 
            PLZ
        where
            PLZ_ID=?
        """
        cursor.execute(query,plz_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            entry=row[0],row[1],row[2]
            results.append(entry)
        return results[0]

# res=(l_select_plz_info_by_id(2635))[0]
# print(res)
# print(l_select_plz_info_by_plz(6005))