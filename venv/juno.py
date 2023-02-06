import cases_functions
import client_data_main
import clients
import doc_set_compositions
import doc_set_definition
import users
import globals as G


def ensure_user(anvil_user_id_txt,anv_usr_email):
    if G.cached.anvil_user_has_user(anvil_user_id_txt):
        user_id = G.cached.user_id_get(anvil_user_id_txt)
        print('monitor: cached_user_id')
        return (user_id,True)

    else:
        user_id=users.l_add_user_modern(anvil_user_id_txt,"Eingeben!","Eingeben!","Eingeben!",anv_usr_email)
        if type(user_id) is int:
            print('ensure_user_id',user_id,"gesetzt")
            G.cached.user_id_add_direct(anvil_user_id_txt, user_id)
            return (user_id, True)
        else:
            return (user_id, False)

def ensure_client(anvil_user_id, user_id,client_desc="is User"):
    client_id=clients.l_get_the_client_id_of_a_user_id_modern(anvil_user_id,user_id)
    if client_id is None:
        client_id=clients.l_add_client_to_clients_modern(anvil_user_id,user_ref=user_id, client_is_user=True, client_name=client_desc)
    if type(user_id) is int:
        print('ensure_client_id',client_id,"gesetzt")
        return(client_id, True)
    else:
        return (client_id, False)

def ensure_dsd(anvil_user_id,dsd_name,dsd_domain,dsd_year):
    dsd_id=doc_set_definition.l_select_the_dsd_by_dsd_name_domain_year_modern(anvil_user_id,dsd_name,dsd_domain,dsd_year)
    if dsd_id is None:
        dsd_id=doc_set_definition.l_add_dsd_entry(dsd_name,dsd_domain,dsd_year)
    if type(dsd_id) is int:
        print('ensure_dsd_id',dsd_id,"gesetzt")
        return(dsd_id, True)
    else:
        return (dsd_id, False)

def ensure_case(anvil_user_id, dsd_id,client_id,user_id):
    shd_dsd_id=doc_set_definition.l_select_the_dsd_by_dsd_name_domain_year_modern(anvil_user_id,'Shadowset','all',9999)

    shadow_case_check=cases_functions.l_check_certain_case_exists_for_client_id_modern(anvil_user_id, client_id, shd_dsd_id)
    if shadow_case_check[1] is False:
        shdw_case_id=cases_functions.l_add_case(client_id,shd_dsd_id,1,user_id,0,True)
        shadow_case_check=(shdw_case_id,True)
    if shadow_case_check[1] is True:
         shdw_case_id = shadow_case_check[0]
         shdw_case_ok = shadow_case_check[1]
         print("ensured shadow_case_id",shdw_case_id,"gesetzt")
    else:
        shdw_case_ok = False

    if shdw_case_ok:
        case_check = cases_functions.l_check_certain_case_exists_for_client_id_modern(anvil_user_id, client_id, dsd_id)
        if case_check[1] is False:
            case_id=cases_functions.l_add_case(client_id,dsd_id,1,user_id,shdw_case_id,False)
            case_check=(case_id,True)
            cases_functions.l_update_shadow_case_id_for_a_given_case_id(client_id, case_id, shdw_case_id)
        if case_check[1] is True:
            case_id=case_check[0]
            case_ok=case_check[1]
            if shdw_case_ok is True:
                print('ensure_case_id',case_id,"gesetzt")
                return(case_id, case_ok)
        else:
            print('Strange Result')
            return (case_check, False)
    else:
        return('shadow-case not o.k.', False)


def l_ensure_user_context(anvil_user_id_text,anv_usr_email,dsd_name,dsd_domain,dsd_year):

    context_created = True

# - ensure there is a user
    user_ensured=ensure_user(anvil_user_id_text,anv_usr_email)
    user_id = user_ensured[0]
    user_ok = user_ensured[1]
    if user_ok == False: context_created=False
# - ensure there is a client
    client_ensured=ensure_client(anvil_user_id_text,user_id)
    client_id = client_ensured[0]
    users.l_upate_client_ref(user_id, client_id)     #merken und korrigieren
    client_ok = client_ensured[1]
    if client_ok==False: context_created=False
# - ensure there is dsd = 130
    dsd_ensured=ensure_dsd(anvil_user_id_text,dsd_name,dsd_domain,dsd_year)
    dsd_id = dsd_ensured[0]
    dsd_ok = client_ensured[1]
    if dsd_ok==False: context_created=False
# - ensure there is a case
    case_ensured=ensure_case(anvil_user_id_text,dsd_id,client_id,user_id)
    case_id = case_ensured[0]
    case_ok = case_ensured[1]
    if case_ok==False: context_created=False
    if context_created == True:
        context_result = {'context_created': True,
                          'anvil_user_id_str': anvil_user_id_text,
                          'client_id': client_id,
                          'dsd_id': dsd_id,
                          'case_id': case_id}
    else:
        context_result = {}
        context_result['context_created'] = False

    return context_result

def l_get_client_list(anvil_user_id):
    # user_id=users.l_get_userid_for_anvil_user(anvil_user_id)
    user_id=G.cached.user_id_get(anvil_user_id)
    cl_list = clients.l_get_all_clients_of_a_user_id_modern(anvil_user_id,user_id)
    client_list=[]
    for c in cl_list:
        #print(c['client_id'])
        shd_case=cases_functions.l_get_shadow_case_id_for_client_id_modern(anvil_user_id,c['client_id'])
        #print('Shadow_cas=:',shd_case)

        dsc_name = doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id,shd_case, 110)
        dsc_vorname = doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id,shd_case, 120)
        dsc_street = doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id,shd_case, 140)
        dsc_town = doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id,shd_case, 170)
        dsc_birthday=doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id,shd_case, 210)
        dsc_socsec= doc_set_compositions.l_select_dsc_id_by_case_and_field_modern(anvil_user_id,shd_case, 200)

        client_entry={}
        client_entry['client_id']=c['client_id']
        client_entry['admin_active']=c['admin_active']
        client_entry['client_desc']=c['client_name']
        client_entry['is_user'] = c['client_is_user']
        #client_id
        if dsc_name is None:
            name='None'
        else:
            cdm_entry = client_data_main.l_get_active_cdm_entries_by_case_id_and_dsc_id_modern(anvil_user_id, shd_case, dsc_name)
            if cdm_entry is None:
                name="None"
            else:
                name = cdm_entry[0]['payload_text']
            #print('Name:', name)

        if dsc_vorname is None:
            vorname='None'
        else:
            cdm_entry =client_data_main.l_get_active_cdm_entries_by_case_id_and_dsc_id_modern(anvil_user_id,shd_case,dsc_vorname)
            if cdm_entry is None:
                vorname="None"
            else:
                vorname=cdm_entry [0]['payload_text']
            #print('Vorname:', vorname)

        client_entry['client_name'] =("{}, {}").format(name, vorname)

        #address
        if dsc_street is None:
            address='None'
        else:
            cdm_entry = client_data_main.l_get_active_cdm_entries_by_case_id_and_dsc_id_modern(anvil_user_id, shd_case, dsc_street)
            if cdm_entry is None:
                address = "None"
            else:
                address = cdm_entry[0]['payload_text']
            #print('Adresse:', address)
        client_entry['address'] = address

        # town
        if dsc_town is None:
            town='None'
        else:
            cdm_entry = client_data_main.l_get_active_cdm_entries_by_case_id_and_dsc_id_modern(anvil_user_id, shd_case, dsc_town)
            if cdm_entry is None:
                town = "None"
            else:
                town = cdm_entry[0]['payload_text']
            #print('Town:', town)
        client_entry['town'] = town

        # town
        if dsc_birthday is None:
            birthday='None'
        else:
            cdm_entry = client_data_main.l_get_active_cdm_entries_by_case_id_and_dsc_id_modern(anvil_user_id,shd_case, dsc_birthday)
            if cdm_entry is None:
                birthday = "None"
            else:
                birthday = cdm_entry[0]['payload_text']
            #print('Birthday:', birthday)
        client_entry['birthday'] = birthday

        if dsc_socsec is None:
            socsec='None'
        else:
            cdm_entry = client_data_main.l_get_active_cdm_entries_by_case_id_and_dsc_id_modern(anvil_user_id, shd_case, dsc_socsec)
            if cdm_entry is None:
                socsec = "None"
            else:
                socsec = cdm_entry[0]['payload_text']
            #print('AHV:', socsec)
        client_entry['socsec'] = socsec

        client_list.append(client_entry)

    return client_list

def l_add_client_with_cases(anvil_user_txt, client_desc,dsd,domain,year):

    check_no_duplicate_clients=True #can be implemented later
    if check_no_duplicate_clients is True:
        user_id = users.l_get_userid_for_anvil_user(anvil_user_txt)
        client_id=clients.l_add_client_to_clients(user_ref=user_id, client_is_user=False, client_name=client_desc)
    else:
        client_id = None

    if client_id is None:
        case_result=(None,False)
    else:

        dsd_there=ensure_dsd(anvil_user_txt,dsd,domain,year)
        if dsd_there[1] is True:
            dsd_id=dsd_there[0]
        case_result = ensure_case(anvil_user_txt,dsd_id,client_id,user_id)
    return case_result
#print(l_get_client_list('[344816,524933170]'))

#print(l_ensure_user_context('[344816,581704467]','fs@msfp.ch',"Address","unique",9999))








def get_my_links(client_id):
    pass