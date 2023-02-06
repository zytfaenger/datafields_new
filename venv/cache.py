import connections
import functions
import pyodbc
import users
import log_functions
import globals as G


def l_all_data_for_a_user(anvil_user_id):
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query= """SELECT
                dbo.users.[user_id],
                dbo.users.[user_anvil_user],
                dbo.users.[admin_user],
                dbo.users.[client_id_reference],
                dbo.users.[temp_user],
                dbo.clients.[client_id],
                dbo.clients.[client_user_ref],
                dbo.clients.[client_is_user],
                dbo.clients.[client_name],
                dbo.clients.[client_relation_uuid],
                dbo.cases.[case_id],
                dbo.cases.[client_id_ref],
                dbo.cases.[dsd_reference],
                dbo.cases.[language_ref],
                dbo.cases.[user_id]
                AS[user_id_0],
                dbo.[client_data_main].[cdm_id],
                dbo.[client_data_main].[user_id_reference],
                dbo.[client_data_main].[case_id_reference],
                dbo.[client_data_main].[dsc_reference],
                dbo.[client_data_main].[payload_text],
                dbo.[client_data_main].[payload_number],
                dbo.[client_data_main].[payload_boolean],
                dbo.[doc_set_comp].[dsc_id],
                dbo.[doc_set_comp].[field_id_reference],
                dbo.fields.[field_id],
                dbo.fields.[field_name],
                dbo.fields.[field_description],
                dbo.fields.[field_sequence],
                dbo.fields.[field_typ_id]
            FROM
                dbo.users
                JOIN dbo.clients
                ON dbo.users.[user_id] = dbo.clients.[client_user_ref] 
                JOIN dbo.cases
                ON dbo.clients.[client_id] = dbo.cases.[client_id_ref] 
                JOIN dbo.[client_data_main]
                ON dbo.users.[user_id] = dbo.[client_data_main].[user_id_reference]
                AND dbo.cases.[case_id] = dbo.[client_data_main].[case_id_reference] 
                JOIN dbo.[doc_set_comp]
                ON dbo.[client_data_main].[dsc_reference] = dbo.[doc_set_comp].[dsc_id] 
                JOIN dbo.fields
                ON dbo.[doc_set_comp].[field_id_reference] = dbo.fields.[field_id]
                WHERE
                dbo.users.user_anvil_user=?"""
        cursor.execute(query, anvil_user_id)
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        res = []
        [res.append(dict(zip(columns, row))) for row in results]
        return res

# [print(r) for r in l_all_data_for_a_user(180)]

def l_all_info_for_a_user(anvil_user_id,language_id):
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query= """SELECT
                    dbo.users.[user_id],
                    dbo.users.[user_anvil_user],
                    dbo.users.[admin_user],
                    dbo.users.[client_id_reference],
                    dbo.users.[temp_user],
                    dbo.clients.[client_id],
                    dbo.clients.[client_user_ref],
                    dbo.clients.[client_is_user],
                    dbo.clients.[client_name],
                    dbo.clients.[client_relation_uuid],
                    dbo.cases.[case_id],
                    dbo.cases.[client_id_ref],
                    dbo.cases.[dsd_reference],
                    dbo.cases.[language_ref],
                    dbo.cases.[shadow_case_id],
                    dbo.cases.[shadow_case_indicator],
                    dbo.cases.[user_id] AS [user_id_0],
                    dbo.[doc_set_def].[dsd_id],
                    dbo.[doc_set_def].[dsd_name],
                    dbo.[doc_set_def].[dsd_domain],
                    dbo.[doc_set_def].[dsd_year],
                    dbo.[doc_set_comp].[dsc_id],
                    dbo.[doc_set_comp].[dsd_reference] AS [dsd_reference_0],
                    dbo.[doc_set_comp].[field_id_reference],
                    dbo.[doc_set_comp].[dsc_sequence],
                    dbo.languages.[lang_id],
                    dbo.languages.[lang_short],
                    dbo.fields.[field_id],
                    dbo.fields.[field_typ_id],
                    dbo.fields.[field_name],
                    dbo.fields.[field_description],
                    dbo.fields.[field_sequence],
                    dbo.fields.[field_group],
                    dbo.fields.[field_group_order],
                    dbo.fields.[field_sub_group],
                    dbo.fields.[field_sub_group_value],
                    dbo.fields.[anvil_component_ref],
                    dbo.[field_descriptions].[field_descID],
                    dbo.[field_descriptions].[field_id_reference] AS [field_id_reference_0],
                    dbo.[field_descriptions].[language_id_reference],
                    dbo.[field_descriptions].[field_desc_label],
                    dbo.[field_descriptions].[field_desc_prompt],
                    dbo.[field_types].[ft_id],
                    dbo.[field_types].[ft_type],
                    dbo.[field_types].[ft_description],
                    dbo.[field_types].[ft_sequence],
                    dbo.[field_types].[ft_stores_state],
                    dbo.[field_types].[ft_stores_data],
                    dbo.[field_types].[ft_shadow_store]
                    FROM
                    dbo.users
                    JOIN dbo.clients
                    ON dbo.users.[user_id] = dbo.clients.[client_user_ref] 
                    JOIN dbo.cases
                    ON dbo.clients.[client_id] = dbo.cases.[client_id_ref] 
                    JOIN dbo.[doc_set_def]
                    ON dbo.cases.[dsd_reference] = dbo.[doc_set_def].[dsd_id] 
                    JOIN dbo.[doc_set_comp]
                    ON dbo.cases.[dsd_reference] = dbo.[doc_set_comp].[dsd_reference] 
                    JOIN dbo.fields
                    ON dbo.[doc_set_comp].[field_id_reference] = dbo.fields.[field_id] 
                    JOIN dbo.[field_descriptions]
                    ON dbo.fields.[field_id] = dbo.[field_descriptions].[field_id_reference] 
                    JOIN dbo.languages
                    ON dbo.[field_descriptions].[language_id_reference] = dbo.languages.[lang_id] 
                    JOIN dbo.[field_types]
                    ON dbo.fields.[field_typ_id] = dbo.[field_types].[ft_id]
                    WHERE
                    dbo.users.user_anvil_user=? and
                    dbo.field_descriptions.language_id_reference=?"""
        cursor.execute(query, (anvil_user_id,language_id))
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        res = []
        [res.append(dict(zip(columns, row))) for row in results]
        return res
# [print(r) for r in l_all_info_for_a_user(180,1)]

def get_list_of_active_users(anvil_user_id): #any existing user will do
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query: str = """SELECT 
                            user_id,
                            user_anvil_user as anvil_user
                        FROM 
                            users 
                        WHERE 
                            admin_active=?"""
        cursor.execute(query,1)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


class cache_obj():
    def __init__(self):
        self.user_info={}
        self.user_data={}
        self.conn= {}
        self.language_id={}
        self.user_id={}


    def info_add(self, anvil_user_id, language_id=1):
        info = l_all_info_for_a_user(anvil_user_id, language_id)
        self.user_info[anvil_user_id]=info
        self.language_id[anvil_user_id]=language_id

    def info_get(self, anvil_user_id):
        return self.user_info[anvil_user_id]

    def get_language_id(self,anvil_user_id):
        return self.language_id[anvil_user_id]


    def data_add(self, anvil_user_id):
        data = l_all_data_for_a_user(anvil_user_id)
        self.user_data[anvil_user_id] = data

    def data_get(self, anvil_user_id):
        return self.user_data[anvil_user_id]

    def conn_add(self,anvil_user_id):
        azure = connections.Azure()
        connect_string=azure.connect_string
        conn=pyodbc.connect(connect_string)
        self.conn[anvil_user_id]=conn

    def conn_get(self,anvil_user_id):
        return self.conn[anvil_user_id]


    def user_id_add(self, anvil_user_id):
        user_id = users.l_get_userid_for_anvil_user(anvil_user_id)
        self.user_id[anvil_user_id] = user_id

    def user_id_add_direct(self, anvil_user_id, user_id):
        self.user_id[anvil_user_id] = user_id

    def user_id_get(self, anvil_user_id):
        return self.user_id[anvil_user_id]

    def anvil_user_has_user(self,anvil_user_id):
        try:
            user_id=self.user_id_get(anvil_user_id)
            return True
        except:
            return False

    def make_user_cache(self):
        if self.user_id=={}:
            print('Error: one anvil-user connection must be added first')
        else:
            active_users = get_list_of_active_users(list(self.user_id.keys())[0])
            for u in active_users:
                self.user_id_add_direct(u['anvil_user'], u['user_id'])

    def get_fd_cached(self,anvil_user_id,case_id,field_id):
        user_data=self.data_get(anvil_user_id)

        data=list(filter(lambda r: r['case_id']==case_id and r['field_id']==field_id, user_data))
        if len(data)>0:
            res={}
            res['payload_text']=data[0]['payload_text']
            res['payload_number']=data[0]['payload_number']
            res['payload_boolean']=data[0]['payload_boolean']


            user_info=self.info_get(anvil_user_id)
            info=list(filter(lambda r: r['case_id']==case_id and r['field_id']==field_id, user_info))
            if len(info)>0:
                res['label']  = info[0]['field_desc_label']
                res['prompt'] =info[0]['field_desc_prompt']
            return res
        else:
            return None

# #sequence is important
#create object
#cache=cache_obj()
# #make connections first
# cache.conn_add('[344816,583548811]')
# cache.conn_add('[344816,588718435]')
# #add one user
# cache.user_id_add('[344816,583548811]')
# #then add user_list
# cache.make_user_cache()
# #print(cache.user_id)
# #then get existing_data
#cache.data_add('[344816,583548811]')
# cache.data_add('[344816,588718435]')
# cache.info_add('[344816,583548811]',1)
# cache.info_add('[344816,588718435]',1)
# # print(cache.get_language_id('[344816,583548811]'))
# cache.user_id_add('[344816,583548811]')
# # print(cache.user_id_get('[344816,583548811]'))
# # print(cache.anvil_user_has_user('[344816,583548811]'))
# # print(cache.anvil_user_has_user('[344816,583548812]'))
#
# r180= cache.info_get('[344816,583548811]')
# r230=cache.info_get('[344816,588718435]')
# d180=cache.data_get('[344816,583548811]')
# d230=cache.data_get('[344816,588718435]')
# [print(r['client_id']) for r in r180]
# [print(r['client_id']) for r in r230]
# [print(d['client_id_ref']) for d in d180]
# [print(d['client_id_ref']) for d in d230]
# print(cache.get_fd_cached('[344816,588718435]',400,1260))
