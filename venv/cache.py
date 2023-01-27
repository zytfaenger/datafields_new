import connections
import functions
import users
import log_functions



def l_all_data_for_a_user(user_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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
                dbo.clients.[client_uuid_id_reference],
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
                dbo.users.user_id=?"""
        cursor.execute(query, user_id)
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        res = []
        [res.append(dict(zip(columns, row))) for row in results]
        return res

# [print(r) for r in l_all_data_for_a_user(180)]

def l_all_info_for_a_user(user_id,language_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
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
                    dbo.clients.[client_uuid_id_reference],
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
                    dbo.users.user_id=? and
                    dbo.field_descriptions.language_id_reference=?"""
        cursor.execute(query, (user_id,language_id))
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        res = []
        [res.append(dict(zip(columns, row))) for row in results]
        return res
# [print(r) for r in l_all_info_for_a_user(180,1)]

class cache_obj():
    def __init__(self):
        self.user_info={}
        self.user_data={}

    def info_add(self,user_id,language_id=1):
        info = l_all_info_for_a_user(user_id,language_id)
        self.user_info[user_id]=info

    def info_get(self,user_id):
        return self.user_info[user_id]

    def data_add(self, user_id):
        data = l_all_data_for_a_user(user_id)
        self.user_data[user_id] = data

    def data_get(self, user_id):
        return self.user_data[user_id]

    def get_fd_cached(self,user_id,case_id,field_id):
        user_data=self.data_get(user_id)

        data=list(filter(lambda r: r['case_id']==case_id and r['field_id']==field_id, user_data))
        if len(data)>0:
            res={}
            res['payload_text']=data[0]['payload_text']
            res['payload_number']=data[0]['payload_number']
            res['payload_boolean']=data[0]['payload_boolean']


            user_info=self.info_get(user_id)
            info=list(filter(lambda r: r['case_id']==case_id and r['field_id']==field_id, user_info))
            if len(info)>0:
                res['label']  = info[0]['field_desc_label']
                res['prompt'] =info[0]['field_desc_prompt']
            return res
        else:
            return None

cache=cache_obj()
cache.data_add(180)
cache.data_add(230)
cache.info_add(180,1)
cache.info_add(230,1)

r180= cache.info_get(180)
r230=cache.info_get(230)
d180=cache.data_get(180)
d230=cache.data_get(230)
# [print(r['client_id']) for r in r180]
# [print(r['client_id']) for r in r230]
# [print(d['client_id_ref']) for d in d180]
#[print(d['client_id_ref']) for d in d230]
# cache.get_fd_cached(180,400,120)
