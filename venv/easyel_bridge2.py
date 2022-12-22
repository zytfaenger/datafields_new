import anvil.server

import PLZ
import cases_functions
import client_data_main
import doc_set_compositions
import doc_set_definition
import docs_functions
import field_types
import fields_functions
import functions
import language_functions
import log_functions
from connections import get_connection

conn = get_connection()


# anvil.server.connect('server_FTBCZPR7E2WKRCLMHQQYW6VB-IFLJ3H45LTJM3EER')  #modules
anvil.server.connect('server_UN23KJQADJA7XYELHWDPHW23-F6JMSXNZ36WYEYKQ')  #admin

# -------- Logging----------#


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
def select_language_by_id(lang_id):
    return language_functions.l_select_language_by_id(lang_id)


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
def add_field_type(ft_type, description, sequence):
    return field_types.l_add_field_type(ft_type, description, sequence)


@anvil.server.callable
def update_fd_type(id_to_change, ft_type, description, sequence):
    # print("update fieldtype",id_to_change,type,description,sequence)
    field_types.l_update_field_type(id_to_change, ft_type, description, sequence)


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
def l_get_active_fields_for_dd(filter="%"):
    return fields_functions.l_get_active_fields_for_dd(filter)


@anvil.server.callable
def select_field_by_id(f_id):
    return fields_functions.l_select_field_by_id(f_id)

@anvil.server.callable
def get_field_sub_group_value_for_id(f_id):
    return fields_functions.l_get_field_sub_group_value_for_id(f_id)
# print(l_get_field_sub_group_value_for_id(230))
@anvil.server.callable
def get_field_sub_group_for_id(f_id):
    return fields_functions.l_get_field_sub_group_for_id(f_id)

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
def update_field(id_to_change,
                   fd_typ_id,
                   fd_name,
                   fd_description,
                   fd_sequence,
                   fd_group="Case",
                   fd_group_order=1,
                   fd_sub_group=None,
                   fd_sub_group_value=None):

    fields_functions.l_update_field(
            id_to_change,
           fd_typ_id,
           fd_name,
           fd_description,
           fd_sequence,
           fd_group="Case",
           fd_group_order=1,
           fd_sub_group=None,
           fd_sub_group_value=None)



# Zuerst entsprechendes Feld erzeugen!
# l_update_field(290, 100,"Test2","das ist ein Testfeld2",2)

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


def select_dsd_by_case(case_id):
    return doc_set_definition.l_select_dsd_by_case(case_id)


@anvil.server.callable
def add_dsd_entry(name, domain, year):
    return doc_set_definition.l_add_dsd_entry(name, domain, year)


@anvil.server.callable
def update_dsd(id_to_change, name, domain, year):
    doc_set_definition.l_update_dsd(id_to_change, name, domain, year)


@anvil.server.callable
def change_status_dsd_by_id(id_to_change, new_status):
    doc_set_definition.l_change_status_dsd_by_id(id_to_change, new_status)


# ----Doc Set Comp: Document Set Composition --------------

@anvil.server.callable
def get_active_dsc():
    return doc_set_compositions.l_get_active_dsc()


@anvil.server.callable
def get_all_dsc():
    return doc_set_compositions.l_get_all_dsc()


@anvil.server.callable
def select_dsc_by_dsd(dsd):
    return doc_set_compositions.l_select_dsc_by_dsd(dsd)


@anvil.server.callable
def select_dsc_to_store_for_dsd(case_dsd, case_language):
    return doc_set_compositions.l_select_dsc_to_store_for_dsd(case_dsd, case_language)


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
@anvil.server.callable
def update_cdm_entry(user_id, case_id, dsc_id, pl_text, pl_number, pl_boolean):
    client_data_main.l_update_cdm_entry(user_id, case_id, dsc_id, pl_text, pl_number, pl_boolean)


@anvil.server.callable
def set_fd(user_id, case_id, field_id, pl_text, pl_number, pl_boolean):
    client_data_main.l_update_cdm_entry(user_id, case_id, field_id, pl_text, pl_number, pl_boolean)


@anvil.server.callable
def get_fd(case_id, field_id):  # in Client_data_main
    return client_data_main.l_get_fd(case_id, field_id)

@anvil.server.callable
def get_fd_all(case_id, field_id):  # in Client_data_main
    return client_data_main.l_get_fd_all(case_id, field_id)


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

# ---- field.functions.py --------------

@anvil.server.callable()
def get_field_sub_group_value_for_id(f_id):
    return fields_functions.l_get_field_sub_group_value_for_id(f_id)

@anvil.server.callable()
def ensure_doc(case_id, field_id):
    return docs_functions.l_ensure_doc(case_id, field_id)



# print(get_languages())
# last_lang = add_language('en-uk2',
#                           'English - Vereinigtes Königreich',
#                          'British English',
#                          '1399c078-6c0f-11ed-b0bc-acde48001122',
#                          make_timestamp())
# print(last_lang)
#print(get_all_languages())
#print(get_active_languages())
# delete_language_by_short_name('en-uk')
#
# result = get_all_languages()
# print(result)
# result = get_active_languages()
# print(result)
#
# delete_language_by_id(52)
#
# result = get_all_languages()
# print(result)
# result = get_active_languages()
# print(result)

# UUID = ('1399c078-6c0f-11ed-b0bc-acde48001122')
# ts=make_timestamp()
# print(UUID,ts)
# print(8, 'EN-UK', result['lang_german'], result['lang_local'], UUID, ts)
# update_language(last_lang, 'EN-UK995', 'Englisch', 'English', UUID, ts)
# print(get_languages())

anvil.server.wait_forever()
