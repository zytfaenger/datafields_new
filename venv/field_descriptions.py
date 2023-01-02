from connections import get_connection
from language_functions import l_select_language_by_shortname
conn = get_connection()

cursor = conn.cursor()


def l_get_label(lang_short,field_id):
    print(lang_short,"= sprache")
    lang_id=l_select_language_by_shortname(lang_short)[0]['lang_id']
    print(lang_id)
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
        return None
    else:
        return label[0]

def l_get_label_by_id(lang_id,field_id):
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
    label = cursor.fetchone()
    if label is None:
        return None
    else:
        return label[0]




#print(get_label('D-CH',120))

def l_get_prompt(lang_short,field_id):
    #print(lang_short,"= sprache")
    lang_id=l_select_language_by_shortname(lang_short)[0]['lang_id']
    #print(lang_id)
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

#print(get_label('D-CH',120))

def l_get_prompt_by_id(lang_id,field_id):
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