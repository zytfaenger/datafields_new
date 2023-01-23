import connections
import functions
import users
import log_functions

conn = connections.get_connection()

cursor = conn.cursor()



def select_all(client_id):
    query="""SELECT top 100 percent
            dbo.[doc_set_comp].[dsd_reference],
            dbo.[client_data_main].[cdm_id],
            dbo.[doc_set_comp].[field_id_reference],
            dbo.fields.[field_name],
            dbo.fields.[field_description],
            dbo.fields.[field_sequence],
            dbo.[field_types].[ft_type],
            dbo.[field_types].[ft_description],
            dbo.[client_data_main].[payload_text],
            dbo.[client_data_main].[payload_number],
            dbo.[client_data_main].[payload_boolean],
            dbo.cases.[case_id],
            dbo.cases.[client_id_ref],
            dbo.clients.[client_name],
            dbo.clients.client_id,
            dbo.languages.[lang_short],
            dbo.[doc_set_comp].[dsd_reference],
            dbo.[doc_set_def].[dsd_name],
            dbo.[doc_set_def].[dsd_domain],
            dbo.[doc_set_def].[dsd_year]
            FROM
            dbo.[client_data_main]
            JOIN dbo.cases
            ON dbo.[client_data_main].[case_id_reference] = dbo.cases.[case_id]
            JOIN dbo.clients
            ON dbo.cases.[client_id_ref] = dbo.clients.[client_id]
            JOIN dbo.users
            ON dbo.[client_data_main].[user_id_reference] = dbo.users.[user_id]
            JOIN dbo.languages
            ON dbo.cases.[language_ref] = dbo.languages.[lang_id]
            JOIN dbo.[doc_set_comp]
            ON dbo.[client_data_main].[dsc_reference] = dbo.[doc_set_comp].[dsc_id]
            JOIN dbo.[doc_set_def]
            ON dbo.[doc_set_comp].[dsd_reference] = dbo.[doc_set_def].[dsd_id]
            JOIN dbo.fields
            ON dbo.[doc_set_comp].[field_id_reference] = dbo.fields.[field_id]
            JOIN dbo.[field_types]
            ON dbo.fields.[field_typ_id] = dbo.[field_types].[ft_id]
            WHERE
            dbo.clients.[client_id] = ?
            ORDER BY
            dbo.cases.case_id,
            dbo.doc_set_def.dsd_id,
            dbo.fields.[field_sequence]"""
    cursor.execute(query,client_id)
    results=cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    res=[]
    [res.append(dict(zip(columns, row))) for row in results]
    return res

[(print(r['dsd_reference'],r['field_name'],r['payload_text']) )for r in select_all(210)]