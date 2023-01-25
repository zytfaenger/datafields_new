import connections
import functions
import users
import log_functions

def l_get_relations_table_columns():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given, 
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active                       
                        FROM 
                            relations
                        WHERE 
                            relations_id=?"""

        cursor.execute(query,"")
        i=0
        cset=[]
        for c in cursor.description:
            #print(c)
            type=""
            if c[1]==int:
                type="number"
            elif c[1]==float:
                type="number"
            elif c[1] == bool:
                type="number"
            elif c[1]==str:
                type="text"
            else:
                type=c[1]
            temp=(i,c[0],type)
            cset.append(temp)
            i= i+1
        return cset
# print(l_get_relations_table_columns())
# [print(c) for c in l_get_relations_table_columns()]



def l_get_active_relations():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given, 
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active                       
                        FROM 
                            relations
                        WHERE 
                            admin_active=?"""
        cursor.execute(query,1)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# [print(r) for r in l_get_active_relations()]


def l_get_all_relations():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given, 
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active                       
                        FROM 
                            relations"""
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# [print(r) for r in l_get_all_relations()]


def l_get_relation_by_id(relations_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given, 
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active                       
                        FROM 
                            relations
                        WHERE 
                            relations_id=?"""
        cursor.execute(query,relations_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        res=[]

        [res.append(dict(zip(columns, row))) for row in results]
        if res is not None:
            return res[0]

#print(l_get_relation_by_id(2))

def l_get_relations_by_giver_uuid(giver_uuid):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given, 
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active                       
                        FROM 
                            relations
                        WHERE 
                            giver_uuid=?"""
        cursor.execute(query,giver_uuid)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        res=[]
        [res.append(dict(zip(columns, row))) for row in results]
        return res

# print('Giver')
# [print(r) for r in l_get_relations_by_giver_uuid('5C0B51FE-978F-11ED-9B62-ACDE48001122')]

def l_get_relations_by_receiver_uuid(receiver_uuid):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given, 
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active                       
                        FROM 
                            relations
                        WHERE 
                            receiver_uuid=?"""
        cursor.execute(query,receiver_uuid)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        res=[]
        [res.append(dict(zip(columns, row))) for row in results]
        return res

# print('Receiver')
# [print(r) for r in l_get_relations_by_receiver_uuid('14FBABE8-978E-11ED-9B62-ACDE48001122')]

def l_get_relations_by_case_id_given(case_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given,
                            cases.dsd_reference,
                            doc_set_def.dsd_name,
                            doc_set_def.dsd_domain,
                            doc_set_def.dsd_year,
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            relations.admin_user, 
                            relations.admin_timestamp, 
                            relations.admin_previous_entry, 
                            relations.admin_active                       
                        FROM relations
                        join EasyEL.dbo.cases on EasyEL.dbo.cases.case_id = EasyEL.dbo.relations.case_id_given
                        join EasyEL.dbo.doc_set_def on EasyEL.dbo.doc_set_def.dsd_id=EasyEL.dbo.cases.dsd_reference 
                        WHERE 
                            case_id_given=?"""
        cursor.execute(query,case_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        res=[]
        [res.append(dict(zip(columns, row))) for row in results]
        return res

# print('Case_id')
# [print(r) for r in l_get_relations_by_case_id_given(640)]

def l_get_relations_by_shdw_case_id_given(shdw_case_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given,
                            cases.dsd_reference,
                            doc_set_def.dsd_name,
                            doc_set_def.dsd_domain,
                            doc_set_def.dsd_year,
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            relations.admin_user, 
                            relations.admin_timestamp, 
                            relations.admin_previous_entry, 
                            relations.admin_active                       
                        FROM relations
                        join EasyEL.dbo.cases on EasyEL.dbo.cases.case_id = EasyEL.dbo.relations.case_id_given
                        join EasyEL.dbo.doc_set_def on EasyEL.dbo.doc_set_def.dsd_id=EasyEL.dbo.cases.dsd_reference 
                        WHERE 
                            shadow_case_id=?"""
        cursor.execute(query,shdw_case_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        res=[]
        [res.append(dict(zip(columns, row))) for row in results]
        return res

# print('Shadow_Case_id')
# [print(r) for r in l_get_relations_by_shdw_case_id_given(630)]


def l_get_relations_by_dsd_id_given_for_cases(dsd_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given,
                            cases.dsd_reference,
                            doc_set_def.dsd_name,
                            doc_set_def.dsd_domain,
                            doc_set_def.dsd_year,
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            relations.admin_user, 
                            relations.admin_timestamp, 
                            relations.admin_previous_entry, 
                            relations.admin_active                       
                        FROM relations
                        join EasyEL.dbo.cases on EasyEL.dbo.cases.case_id = EasyEL.dbo.relations.case_id_given
                        join EasyEL.dbo.doc_set_def on EasyEL.dbo.doc_set_def.dsd_id=EasyEL.dbo.cases.dsd_reference 
                        WHERE 
                            cases.dsd_reference=?"""
        cursor.execute(query,dsd_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        res=[]
        [res.append(dict(zip(columns, row))) for row in results]
        return res

# print('DSD_id')
# [print(r) for r in l_get_relations_by_dsd_id_given_for_cases(130)]

def l_get_relations_by_dsd_id_given_for_shd_cases(dsd_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            relations_id, 
                            giver_uuid, 
                            case_id_given,
                            cases.dsd_reference,
                            doc_set_def.dsd_name,
                            doc_set_def.dsd_domain,
                            doc_set_def.dsd_year,
                            shd_case_id_given, 
                            receiver_uuid, 
                            type_of_access, 
                            relations.admin_user, 
                            relations.admin_timestamp, 
                            relations.admin_previous_entry, 
                            relations.admin_active                       
                        FROM relations
                        join EasyEL.dbo.cases on EasyEL.dbo.cases.case_id = EasyEL.dbo.relations.shd_case_id_given
                        join EasyEL.dbo.doc_set_def on EasyEL.dbo.doc_set_def.dsd_id=EasyEL.dbo.cases.dsd_reference 
                        WHERE 
                            cases.dsd_reference=?"""
        cursor.execute(query,dsd_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        res=[]
        [res.append(dict(zip(columns, row))) for row in results]
        return res

# print('DSD_id for shadow case')
# [print(r) for r in l_get_relations_by_dsd_id_given_for_shd_cases(120)]

def l_get_relation_type_of_acces(relations_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            type_of_access 
                        FROM relations
                        WHERE 
                            relations_id=?"""
        cursor.execute(query,relations_id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        result = cursor.fetchone()
        return result

# print('Type of access')
# [print(r) for r in l_get_relation_type_of_acces(2)]


def add_log_entry(user, current_timestamp, table_name, table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name, table_id, payload)

def l_add_relation_to_relations  (admin_user,giver_uuid,case_given,shd_case_given,receiver_uuid,access_type):
    current_admin_user=admin_user
    timestamp = functions.make_timestamp()
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query = """insert into 
                     relations (
                        giver_uuid,
                        case_id_given,
                        shd_case_id_given,
                        receiver_uuid,
                        type_of_access,
                        admin_user,
                        admin_timestamp,
                        admin_previous_entry,
                        admin_active
                     )
                     values (?,?,?,?,?,?,?,?,?)"""
        cursor.execute(query,
                       (giver_uuid,
                        case_given,
                        shd_case_given,
                        receiver_uuid,
                        access_type,
                        current_admin_user,
                        timestamp,
                        0,
                        1
                        ))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return last_id


# l_add_relation_to_relations('1399C078-6C0F-11ED-B0BC-ACDE48001122',
#                             '5C0B51FE-978F-11ED-9B62-ACDE48001122',
#                             670,
#                             650,
#                             '14FBABE8-978E-11ED-9B62-ACDE48001122',
#                             2)

def l_update_relation(admin_user, relation_id_to_change='=', giver_uuid='=', receiver_uuid='=', type_of_access='=',admin_active='='):
        if (giver_uuid ==        '=' and
            receiver_uuid ==     '=' and
            type_of_access ==    '=' and
            admin_active ==      '=') is True:
                print('No update')
                return None

        current_relation_rec= l_get_relation_by_id(relation_id_to_change)
        if giver_uuid ==        '=':   giver_uuid             = current_relation_rec['giver_uuid']
        if receiver_uuid ==     '=':   receiver_uuid          = current_relation_rec['receiver_uuid']
        if type_of_access ==    '=':   type_of_access         = current_relation_rec['type_of_access']
        if admin_active ==      '=':   admin_active           = current_relation_rec['admin_active']

        current_admin_user = admin_user
        current_timestamp = functions.make_timestamp()
        current_table_name = 'relations'
        current_table_id=relation_id_to_change
        current_payload=str(l_get_relation_by_id(relation_id_to_change))
        #print(current_admin_user,current_timestamp,current_table_name,current_table_id,current_payload)
        previous_log_entry=add_log_entry(current_admin_user,
                                         current_timestamp,
                                         current_table_name,
                                         current_table_id,
                                         current_payload)
        #print(previous_log_entry)
        azure = connections.Azure()
        with azure:
            cursor3 = azure.conn.cursor()
            query="""   UPDATE 
                        relations 
                    SET 
                        giver_uuid=?,
                        receiver_uuid=?,
                        type_of_access=?,
                        admin_user=?,
                        admin_timestamp=?,
                        admin_previous_entry=?,
                        admin_active=?
                    WHERE 
                        EasyEL.dbo.relations.relations_id=?"""
            cursor3.execute(query, (giver_uuid,receiver_uuid,type_of_access,current_admin_user, current_timestamp, previous_log_entry, admin_active, relation_id_to_change))
            cursor3.commit()


#l_update_relation('1399C078-6C0F-11ED-B0BC-ACDE48001122',1,"=","=",1,1)


def l_change_status_relation(admin_user_id, relations_id_to_change, new_status):
    current_admin_user = admin_user_id
    current_timestamp = functions.make_timestamp()
    current_table_name = 'relations-admin_status'
    current_table_id = relations_id_to_change
    current_payload = str(l_get_relation_by_id(relations_id_to_change))
    # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry = add_log_entry(
        current_admin_user,
        current_timestamp,
        current_table_name,
        current_table_id,
        current_payload)

    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""  UPDATE 
                                relations
                            SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE relations_id=?""",
                       (current_admin_user,
                        current_timestamp,
                        previous_log_entry,
                        new_status,
                        relations_id_to_change))
        cursor.commit()
#l_change_status_relation('1399C078-6C0F-11ED-B0BC-ACDE48001122',1,True)

