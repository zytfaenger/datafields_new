import cases_functions
import clients
import doc_set_definition
import users



def ensure_user(anv_usr_id_txt,anv_usr_email):
    user_id = users.l_get_userid_for_anvil_user(anv_usr_id_txt)
    if user_id is None:
        user_id=users.l_add_user(anv_usr_id_txt,"Eingeben!","Eingeben!",anv_usr_email)
    if type(user_id) is int:
        print('ensure_user_id',user_id,"gesetzt")
        return (user_id, True)
    else:
        return (user_id, False)

def ensure_client(user_id):
    client_id=clients.l_get_the_client_id_of_a_user_id(user_id)
    if client_id is None:
        client_id=clients.l_add_client_to_clients(user_ref=user_id, client_is_user=True, client_name="offen")

    if type(user_id) is int:
        print('ensure_client_id',client_id,"gesetzt")
        return(client_id, True)
    else:
        return (client_id, False)

def ensure_dsd(dsd_name,dsd_domain,dsd_year):
    dsd_id=doc_set_definition.l_select_the_dsd_id_by_dsd_name_domain_year(dsd_name,dsd_domain,dsd_year)
    if dsd_id is None:
        dsd_id=doc_set_definition.l_add_dsd_entry(dsd_name,dsd_domain,dsd_year)
    if type(dsd_id) is int:
        print('ensure_dsd_id',dsd_id,"gesetzt")
        return(dsd_id, True)
    else:
        return (dsd_id, False)

def ensure_case(anvil_user_id,dsd_id,client_id,user_id):
    shd_dsd_id=doc_set_definition.l_select_the_dsd_id_by_dsd_name_domain_year('Shadowset','all',9999)
    shadow_case_check=cases_functions.l_check_certain_case_exists_for_anvil_userid(anvil_user_id, shd_dsd_id)
    if shadow_case_check[1] is False:
        shdw_case_id=cases_functions.l_add_case(client_id,shd_dsd_id,1,user_id,0,True)
        shadow_case_check=(shdw_case_id,True)
    if type(shadow_case_check) is tuple:
        shdw_case_id=shadow_case_check[0]
        shdw_case_ok = shadow_case_check[1]
        print("ensured shadow_case_id",shdw_case_id,"gesetzt")
    else:
        print("Strange_result")
        shdw_case_ok=False

    case_check = cases_functions.l_check_certain_case_exists_for_anvil_userid(anvil_user_id, dsd_id)
    if case_check[1] is False:
        case_id=cases_functions.l_add_case(client_id,dsd_id,1,user_id,shdw_case_id,False)
        case_check=(case_id,True)
    if type(case_check) is tuple:
        case_id=case_check[0]
        case_ok=case_check[1] and shdw_case_ok #both must be o.k.
        print('ensure_case_id',case_id,"gesetzt")
        return(case_id, case_ok)
    else:
        return (case_check, False)
        print('Strange Result')


def l_ensure_user_context(anvil_user_id_text,anv_usr_email,dsd_name,dsd_domain,dsd_year):

    context_created = True

# - ensure there is a user
    user_ensured=ensure_user(anvil_user_id_text,anv_usr_email)
    user_id = user_ensured[0]
    user_ok = user_ensured[1]
    if user_ok == False: context_created=False
# - ensure there is a client
    client_ensured=ensure_client(user_id)
    client_id = client_ensured[0]
    users.l_upate_client_ref(user_id, client_id)
    client_ok = client_ensured[1]
    if client_ok==False: context_created=False
# - ensure there is dsd = 130
    dsd_ensured=ensure_dsd(dsd_name,dsd_domain,dsd_year)
    dsd_id = dsd_ensured[0]
    dsd_ok = client_ensured[1]
    if dsd_ok==False: context_created=False
# - ensure there is a case
    case_ensured=ensure_case(anvil_user_id_text,dsd_id,client_id,user_id)
    case_id = case_ensured[0]
    case_ok = case_ensured[1]
    if case_ok==False: context_created=False
    if context_created == True:
        context_result= {}
        context_result['context_created']=True,
        context_result['anvil_user_id_str'] = anvil_user_id_text
        context_result['client_id'] = client_id,
        context_result['dsd_id'] = dsd_id,
        context_result['case_id'] = case_id
    else:
        context_result = {}
        context_result['context_created'] = False

    return context_result


#print(l_ensure_user_context('[344816,581704467]','fs@msfp.ch',"Address","unique",9999))