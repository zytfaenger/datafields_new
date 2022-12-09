from connections import get_connection
conn = get_connection()

cursor = conn.cursor()

def l_select_plz_info_by_PLZ(PLZ):
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
        results.append(dict(zip(columns, row)))
    return results
    print(demo)

print(l_select_plz_info_by_PLZ(6005))