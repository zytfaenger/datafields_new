import anvil.tables
import cases_functions
import client_data_main
import clients
import doc_set_compositions
import doc_set_definition
import docs_functions
import field_types
import fields_functions
import functions
import juno
import language_functions
import log_functions
import relations
import users
import PLZ
import globals as G

# anvil.server.connect('server_FTBCZPR7E2WKRCLMHQQYW6VB-IFLJ3H45LTJM3EER')  #modules PDS v1
anvil.server.connect('server_ORIZJ3HLOBXXSFAX5HN3IE5Z-WCKU3CRQDF4JNFDC')  #modules PDS v2
# anvil.server.connect('server_UTEZBTAL4U6QJVKILS4ISDYP-F6JMSXNZ36WYEYKQ')  #admin

#print(G.cached.info_get(230))

# -------- Logging----------#')  #modules PDS v2



def add_log_entry(user, current_timestamp, table_name, table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name, table_id, payload)

# -------- Languages----------#


@anvil.server.callable
def get_active_languages():
    return language_functions.l_get_active_languages()


@anvil.server.callable
def get_all_languages():
    return language_functions.l_get_all_languages()


@anvil.server.callable()
def select_language_by_shortname(short_name):
    return language_functions.l_select_language_by_shortname(short_name)

@anvil.server.callable()
def select_language_by_shortname_modern(anvil_user_id, short_name):
    return language_functions.l_select_language_by_shortname_modern(anvil_user_id,short_name)

@anvil.server.callable()
def select_language_by_id(lang_id):
    return language_functions.l_select_language_by_id(lang_id)


@anvil.server.callable()
def select_language_by_id_modern(anvil_user_id, lang_id):
    return language_functions.l_select_language_by_id_modern(anvil_user_id, lang_id)

@anvil.server.callable()
def select_language_by_case(case_id):
    return cases_functions.l_select_language_short_by_case_id(case_id)




@anvil.server.callable
def add_language(short_name, german_name, local_name):
    return language_functions.l_add_language(short_name, german_name, local_name)


@anvil.server.callable
def update_language(id_to_change, short_name, german_name, local_name):
    language_functions.l_update_language(id_to_change, short_name, german_name, local_name)


@anvil.server.callable
def change_status_language_by_short_name(short_name, new_status):
    language_functions.l_change_status_language_by_short_name(short_name, new_status)


@anvil.server.callable
def change_status_language_by_id(id_to_change: int, new_status: int):
    language_functions.l_change_status_language_by_id(id_to_change, new_status)


# -------- Field-Types----------#
@anvil.server.callable
def get_active_field_types():
    return field_types.l_get_active_field_types()

@anvil.server.callable
def get_active_field_types_for_dd():
    return field_types.l_get_active_field_types_for_dd()


@anvil.server.callable
def get_all_field_types():
    return field_types.l_get_all_field_types()


@anvil.server.callable
def select_field_types_by_shortname(ftype):
    return field_types.l_select_field_types_by_shortname(ftype)


@anvil.server.callable
def select_field_type_by_id(ft_id):
    # print("das esch es",l_select_field_type_by_id(id))
    return field_types.l_select_field_type_by_id(ft_id)


@anvil.server.callable
def add_field_type(ft_type, description, sequence, shadow=True):
    return field_types.l_add_field_type(ft_type, description, sequence, shadow)


@anvil.server.callable
def update_fd_type(id_to_change, ft_type, description, sequence, shadow=True):
    # print("update fieldtype",id_to_change,type,description,sequence)
    field_types.l_update_field_type(id_to_change, ft_type, description, sequence, shadow)


@anvil.server.callable
def change_status_field_type_by_short_name(ft_type, new_status: int):
    field_types.l_change_status_field_type_by_short_name(ft_type, new_status)


@anvil.server.callable
def change_status_field_type_by_id(id_to_change: int, new_status: int):
    field_types.l_change_status_field_type_by_id(id_to_change, new_status)

# -------- Field functions ----------#

@anvil.server.callable
def get_active_fields():
    return fields_functions.l_get_active_fields()

@anvil.server.callable
def get_all_fields():
    return fields_functions.l_get_all_fields()

@anvil.server.callable
def get_fields_table_columns():
    return fields_functions.l_get_fields_table_columns()

@anvil.server.callable
def l_get_active_fields_for_dd(filter="%"):
    return fields_functions.l_get_active_fields_for_dd(filter)

@anvil.server.callable
def get_anvil_field_list_for_dsd_id_in_sequence(dsd_id):
    return doc_set_compositions.l_get_anvil_field_list_for_dsd_id_in_sequence(dsd_id)

@anvil.server.callable
def get_anvil_field_list_for_dsd_id_in_sequence(dsd_id):
    return doc_set_compositions.l_get_anvil_field_list_for_dsd_id(dsd_id)


@anvil.server.callable
def select_field_by_id(f_id):
    return fields_functions.l_select_field_by_id(f_id)

@anvil.server.callable
def get_field_sub_group_value_for_id(f_id):
    return fields_functions.l_get_field_sub_group_value_for_id(f_id)
# print(l_get_field_sub_group_value_for_id(230))

@anvil.server.callable
def get_field_sub_group_value_for_id_modern(anvil_user_id, f_id):
    return fields_functions.l_get_field_sub_group_value_for_id_modern(anvil_user_id,f_id)

@anvil.server.callable
def get_field_sub_group_for_id(f_id):
    return fields_functions.l_get_field_sub_group_for_id(f_id)

@anvil.server.callable
def get_field_sub_group_for_id_modern(anvil_user_id, f_id):
    return fields_functions.l_get_field_sub_group_for_id_modern(anvil_user_id,f_id)


@anvil.server.callable
def add_field(
            fd_typ_id,
            fd_name,
            fd_description,
            fd_sequence,
            ft_field_group="Case",
            ft_group_order=1,
            ft_subgroup=None,
            ft_sub_group_value=None):
        return fields_functions.l_add_field(
            fd_typ_id,
            fd_name,
            fd_description,
            fd_sequence,
            ft_field_group="Case",
            ft_group_order=1,
            ft_subgroup=None,
            ft_sub_group_value=None)


@anvil.server.callable
def update_field(id_to_change, fd_typ_id, fd_name,fd_description,fd_sequence,fd_group="Case",fd_group_order=1,fd_sub_group=None,fd_sub_group_value=None):

    fields_functions.l_update_field(
           id_to_change,
           fd_typ_id,
           fd_name,
           fd_description,
           fd_sequence,
           fd_group,
           fd_group_order,
           fd_sub_group,
           fd_sub_group_value)


# Zuerst entsprechendes Feld erzeugen!


@anvil.server.callable
def change_status_field_id(id_to_change, new_status):
    fields_functions.l_change_status_field_id(id_to_change, new_status)


# ----Doc Set Definition: Document Set Definition

@anvil.server.callable
def get_active_dsd():
    return doc_set_definition.l_get_active_dsd()


@anvil.server.callable
def get_all_dsd():
    return doc_set_definition.l_get_all_dsd()


@anvil.server.callable
def select_dsd_by_id(dsd_id):
    return doc_set_definition.l_select_dsd_by_id(dsd_id)

@anvil.server.callable
def select_dsd_by_id_modern(anvil_user_id,dsd_id):
    return doc_set_definition.l_select_dsd_by_id_modern(anvil_user_id,dsd_id)


@anvil.server.callable
def select_dsd_by_case(case_id):
    return doc_set_definition.l_select_dsd_by_case(case_id)

# @anvil.server.callable
# def select_dsd_id_by_dsd_name(dsd_name:str):
#     return doc_set_definition.l_select_dsd_id_by_dsd_name(dsd_name)

@anvil.server.callable
def select_the_dsd_by_dsd_name_domain_year(dsd_name:str,dsd_domain,dsd_year,dsd_part=0):
    return  doc_set_definition.l_select_the_dsd_by_dsd_name_domain_year(dsd_name, dsd_domain, dsd_year,dsd_part)

@anvil.server.callable
def select_the_dsd_by_dsd_name_domain_year_modern(anvil_user_id,dsd_name:str,dsd_domain,dsd_year,dsd_part=0):
    return  doc_set_definition.l_select_the_dsd_by_dsd_name_domain_year_modern(anvil_user_id,dsd_name, dsd_domain, dsd_year,dsd_part)


@anvil.server.callable
def add_dsd_entry(name, domain, year):
    return doc_set_definition.l_add_dsd_entry(name, domain, year)


@anvil.server.callable
def update_dsd(id_to_change, name, domain, year):
    doc_set_definition.l_update_dsd(id_to_change, name, domain, year)


@anvil.server.callable
def change_status_dsd_by_id(id_to_change, new_status):
    doc_set_definition.l_change_status_dsd_by_id(id_to_change, new_status)

@anvil.server.callable
def get_form_for_a_dsd_id_modern(anvil_user_id, dsd_id):
    return doc_set_definition.l_get_form_for_a_dsd_id_modern(anvil_user_id, dsd_id)


# ----Doc Set Comp: Document Set Composition --------------

@anvil.server.callable
def get_active_dsc():
    return doc_set_compositions.l_get_active_dsc()


@anvil.server.callable
def get_all_dsc():
    return doc_set_compositions.l_get_all_dsc()

@anvil.server.callable
def get_dsd_reference_for_case_id(ca_id):
    return cases_functions.l_get_dsd_reference_for_case_id(ca_id)


@anvil.server.callable
def select_dsc_by_dsd(dsd):
    return doc_set_compositions.l_select_dsc_by_dsd(dsd)

@anvil.server.callable
def ensure_completeness_of_shadow_dsc(dsd_id=120):
    doc_set_compositions.l_ensure_completeness_of_shadow_dsc(dsd_id)


# @anvil.server.callable
# def select_dsc_to_store_for_dsd(case_dsd, case_language):
#     return doc_set_compositions.l_select_dsc_to_store_for_dsd(case_dsd, case_language)


@anvil.server.callable
def select_dsc_by_id(dsc_id):
    return doc_set_compositions.l_select_dsc_by_id(dsc_id)


@anvil.server.callable
def add_dsc_entry(reference, field_id, sequence):
    return doc_set_compositions.l_add_dsc_entry(reference, field_id, sequence)


@anvil.server.callable
def update_dsc(id_to_change, reference, field_id, sequence):
    doc_set_compositions.l_update_dsc(id_to_change, reference, field_id, sequence)


@anvil.server.callable
def change_status_dsc_by_dsd(dsd_reference, new_status):
    doc_set_compositions.l_change_status_dsc_by_dsd(dsd_reference, new_status)


@anvil.server.callable
def change_status_dsc_by_id(id_to_change: int, new_status: int):
    doc_set_compositions.l_change_status_dsc_by_id(id_to_change, new_status)


# @anvil.server.callable
# def get_fd(field_id):
#     a={'Value': 'Schumacher', 'Placeholder': 'Familienname eingeben!'}
#     return a


# ----Client_Data_Main: Document Set Composition --------------
# @anvil.server.callable  not used
# def update_cdm_entry(user_id, case_id, dsc_id, pl_text, pl_number, pl_boolean):
#     client_data_main.l_update_cdm_entry(user_id, case_id, dsc_id, pl_text, pl_number, pl_boolean)


@anvil.server.callable
# def set_fd_direct(user_id, case_id, field_id, pl_text, pl_number, pl_boolean):
#     client_data_main.l_set_fd(user_id, case_id, field_id, pl_text, pl_number, pl_boolean)

@anvil.server.callable
def set_fd(anvil_user_id_txt, case_id, field_id, pl_text, pl_number, pl_boolean):
    return client_data_main.l_set_fd(anvil_user_id_txt, case_id, field_id, pl_text, pl_number, pl_boolean)


@anvil.server.callable
def get_fd(anvil_user_id, case_id, field_id):  # in Client_data_main
    #print('get_fd_debug:',anvil_user_id,case_id,field_id)
    if type(anvil_user_id) is list:
        anvil_user_id=str(anvil_user_id)
        #print('type is now:', type(anvil_user_id) )
    res=G.cached.get_fd_cached(anvil_user_id,case_id,field_id)
    #print('get_fd_res:',res)
    if res is None:
        return client_data_main.l_get_fd(anvil_user_id, case_id, field_id)
    else:
        print('cached')
        return res
@anvil.server.callable
def get_fd_shadow(anvil_user_id, case_id, field_id):  # in Client_data_main
    return client_data_main.l_get_fd_shadow(anvil_user_id, case_id, field_id)


@anvil.server.callable
def select_plz_info_by_plz(i_plz):
    return PLZ.l_select_plz_info_by_plz(i_plz)


@anvil.server.callable
def select_plz_info_by_id(plz_id):
    return PLZ.l_select_plz_info_by_id(plz_id)


# ---- functions.py --------------
@anvil.server.callable()
def ahv_check(avh_string): # checks for validity of number, returns boolean
    return functions.l_ahv_check(avh_string)


# ---- cases functions.py --------------

@anvil.server.callable()
def get_shadow_case_id_for_case_id(ca_id):
    return cases_functions.l_get_shadow_case_id_for_case_id(ca_id)

@anvil.server.callable()
def get_cases_for_userid(anvil_usr_id):
    return cases_functions.l_get_cases_for_userid(anvil_usr_id)

@anvil.server.callable()
def get_case_for_anvil_user_id_and_DSD_modern(anvil_user_id,client_id, dsd_id):
    return cases_functions.l_get_case_for_anvil_user_id_and_DSD_modern(anvil_user_id, client_id, dsd_id)
@anvil.server.callable()
def get_cases_for_temp_user_id(tmp_usr_uuid_str):
    return cases_functions.l_get_cases_for_temp_user_id(tmp_usr_uuid_str)

@anvil.server.callable()
def get_cases_for_temp_user_id_and_DSD(tmp_usr_uuid_str,dsd_id_ref):
    return cases_functions.l_get_cases_for_temp_user_id_and_DSD(tmp_usr_uuid_str,dsd_id_ref)

@anvil.server.callable()
def get_cases_for_a_client_id(client_id):
    return cases_functions.l_get_cases_for_a_client_id(client_id)

@anvil.server.callable()
def get_cases_for_a_client_id_modern(anvil_user_id, client_id):
    return cases_functions.l_get_cases_for_a_client_id_modern(anvil_user_id,client_id)



@anvil.server.callable()
def check_certain_case_exists_for_anvil_userid(anvil_usr_id,dsd_id):
    return cases_functions.l_check_certain_case_exists_for_anvil_userid(anvil_usr_id,dsd_id)

@anvil.server.callable()
def check_certain_case_exists_for_client_id(client_id, dsd_id):
    return cases_functions.l_check_certain_case_exists_for_client_id(client_id, dsd_id)

@anvil.server.callable()
def add_case(client_id,dsd_id,language_ref,user_id,shadow_case_id=0,shdw_case_ind=False):
    return cases_functions.l_add_case(client_id,dsd_id,language_ref,user_id,shadow_case_id,shdw_case_ind)


# ---- user.functions.py --------------

@anvil.server.callable()
def get_anvil_user_components_as_list(anvil_user):
    return users.l_get_anvil_user_components_as_list(anvil_user)

@anvil.server.callable()
def get_userid_for_anvil_user(anvil_user_id):
    return users.l_get_userid_for_anvil_user(anvil_user_id)

@anvil.server.callable()
def get_user_record_for_anvil_user_modern(anvil_user_id:str):
    return users.l_get_user_record_for_anvil_user_modern(anvil_user_id)




@anvil.server.callable()
def get_new_temp_user_id(anvil_usr):
    print('get_new_temp_user_id:', anvil_usr)
    return users.l_get_new_temp_user_id(anvil_usr)

@anvil.server.callable()
def add_user  (u_anvil_usr,
                usr_last_name,
                usr_first_name,
                usr_town,
                e_mail):
    return users.l_add_user (   u_anvil_usr,
                                usr_last_name,
                                usr_first_name,
                                usr_town,
                                e_mail,
                                anvil_user_two_int=True)

# ---- clients.functions.py --------------

@anvil.server.callable()
def add_client_to_clients  (user_ref,client_name="None",client_is_user=False):
    return clients.l_add_client_to_clients(user_ref,client_name,client_is_user)

@anvil.server.callable()
def update_client(client_id_to_change, user_ref, client_is_user,  name):
    return clients.l_update_client(client_id_to_change, user_ref, client_is_user, name)

@anvil.server.callable()
def get_client_by_id(client_id):
    return clients.l_get_client_by_id(client_id)

@anvil.server.callable()
def get_client_by_id_modern(anvil_user_id, client_id):
    return clients.l_get_client_by_id_modern(anvil_user_id,client_id)

@anvil.server.callable()
def ensure_link_code_client(anvil_user_id, client_id):
    return clients.l_ensure_link_code_client_modern(anvil_user_id, client_id)

@anvil.server.callable()
def change_client_relation_uuid_modern(anvil_user_id, client_id, user_id):
    return clients.l_change_client_relation_uuid_modern(anvil_user_id, client_id, user_id)

@anvil.server.callable()
def get_client_string_from_client_id(link_id):
    return clients.l_get_client_string_from_client_id(link_id)







# ---- dokument functions.py --------------

@anvil.server.callable()
def ensure_doc(case_id, field_id):
    return docs_functions.l_ensure_doc(case_id, field_id)


@anvil.server.callable()
def ensure_user_context(anvil_user_text,anv_usr_email,dsd_name,dsd_domain,dsd_year,dsd_part):
    print(anvil_user_text,anv_usr_email,dsd_name,dsd_domain,dsd_year,dsd_part)
    return juno.l_ensure_user_context(anvil_user_text,anv_usr_email,dsd_name,dsd_domain,dsd_year,dsd_part)

# ---- relations functions.py --------------

@anvil.server.callable()
def get_relations_by_receiver_uuid_modern(anvil_user_id, receiver_uuid):
    return relations.l_get_relations_by_receiver_uuid_modern(anvil_user_id,receiver_uuid)

@anvil.server.callable()
def add_relation_to_relations_modern  (anvil_user_id,giver_uuid,case_given,shd_case_given,receiver_uuid,access_type):
    return relations.l_add_relation_to_relations_modern(anvil_user_id, giver_uuid, case_given, shd_case_given, receiver_uuid,access_type)



# ---- juno.functions.py --------------

@anvil.server.callable()
def register_and_setup_user(anvil_user_id,language_id=1):
    return G.l_register_and_setup_user(anvil_user_id,language_id)
@anvil.server.callable()
def update_data_cache(anvil_user_id):
    G.cached.data_add(anvil_user_id)
    G.cached.info_add(anvil_user_id)

@anvil.server.callable()
def get_client_list(anvil_user_id):
    return juno.l_get_client_list(anvil_user_id)
@anvil.server.callable()
def add_client_with_cases(anvil_user_txt, client_desc,dsd,domain,year):
    return juno.l_add_client_with_cases(anvil_user_txt, client_desc, dsd, domain, year)


@anvil.server.callable()
def get_links_for_a_client(anvil_user_id, client_id):
    return relations.l_get_links_for_a_client_modern(anvil_user_id, client_id)


anvil.server.wait_forever()
