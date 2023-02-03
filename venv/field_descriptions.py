import connections
import language_functions
import globals as G

def l_get_label_by_short(lang_short,field_id):
    print(lang_short,"= sprache")
    lang_id=language_functions.l_select_language_by_shortname(lang_short)[0]['lang_id']
    print(lang_id)
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
                select 
                 field_desc_label
                from 
                 field_descriptions
                where 
                 language_id_reference=? AND field_id_reference=?   
            """
        #print(query)
        cursor = azure.conn.cursor()
        cursor.execute(query,(lang_id,field_id))
        label=cursor.fetchone()
        if label == None:
            return None
        else:
            return label[0]

def l_get_label_by_short_modern(anvil_user_id, lang_short,field_id):
    print(lang_short,"= sprache")
    lang_id=language_functions.l_select_language_by_shortname_modern(anvil_user_id, lang_short)[0]['lang_id']
    print(lang_id)
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query="""
                select 
                 field_desc_label
                from 
                 field_descriptions
                where 
                 language_id_reference=? AND field_id_reference=?   
            """
        #print(query)
        cursor.execute(query,(lang_id,field_id))
        label=cursor.fetchone()
        if label == None:
            cursor.close()
            return None
        else:
            cursor.close()
            return label[0]

def l_get_label_by_id(lang_id,field_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
                select 
                 field_desc_label
                from 
                 field_descriptions
                where 
                 language_id_reference=? AND field_id_reference=?   
            """
        cursor.execute(query,(lang_id,field_id))
        label = cursor.fetchone()
        if label is None:
            return None
        else:
            return label[0]


# print(l_get_label_by_id(1,120))

def l_get_label_by_id_modern(anvil_user_id, lang_id,field_id):
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor3 = azure.cursor()
        query="""
                select 
                 field_desc_label
                from 
                 field_descriptions
                where 
                 language_id_reference=? AND field_id_reference=?   
            """
        #print(query)
        cursor3.execute(query,(lang_id,field_id))
        label = cursor3.fetchone()
        if label is None:
            cursor3.close()
            return None
        else:
            cursor3.close()
            return label[0]


# print(l_get_label_by_id(1,120))





def l_get_prompt_by_short(lang_short,field_id):
    #print(lang_short,"= sprache")
    lang_id=language_functions.l_select_language_by_shortname(lang_short)[0]['lang_id']
    #print(lang_id)
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
                select 
                 field_desc_prompt
                from 
                 field_descriptions
                where 
                 language_id_reference=? AND field_id_reference=?   
            """
        #print(query)
        cursor.execute(query,(lang_id,field_id))
        prompt=cursor.fetchone()
        if prompt == None:
            return None
        else:
            return prompt[0]

# print(l_get_prompt('D-CH',120))

def l_get_prompt_by_short_modern(anvil_user_id,lang_short,field_id):
    #print(lang_short,"= sprache")
    lang_id=language_functions.l_select_language_by_shortname_modern(anvil_user_id, lang_short)[0]['lang_id']
    #print(lang_id)
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query="""
                select 
                 field_desc_prompt
                from 
                 field_descriptions
                where 
                 language_id_reference=? AND field_id_reference=?   
            """
        #print(query)
        cursor.execute(query,(lang_id,field_id))
        prompt=cursor.fetchone()
        if prompt == None:
            cursor.close()
            return None
        else:
            cursor.close()
            return prompt[0]

# print(l_get_prompt('D-CH',120))

def l_get_prompt_by_id(lang_id,field_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
                select 
                 field_desc_prompt
                from 
                 field_descriptions
                where 
                 language_id_reference=? AND field_id_reference=?   
            """
        #print(query)
        cursor.execute(query,(lang_id,field_id))
        prompt=cursor.fetchone()
        if prompt is None:
            return None
        else:
            return prompt[0]

def l_get_prompt_by_id_modern(anvil_user_id, lang_id,field_id):
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query="""
                select 
                 field_desc_prompt
                from 
                 field_descriptions
                where 
                 language_id_reference=? AND field_id_reference=?   
            """
        #print(query)
        cursor.execute(query,(lang_id,field_id))
        prompt=cursor.fetchone()
        if prompt is None:
            cursor.close()
            return None
        else:
            cursor.close()
            return prompt[0]