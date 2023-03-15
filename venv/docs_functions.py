import cases_functions
import field_descriptions
import functions
import log_functions
import connections


def l_get_active_docs():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                            doc_id, 
                            case_id_reference, 
                            field_id_reference, 
                            doc_desc_short, 
                            doc_desc_long, 
                            doc_version, 
                            doc_date, 
                            doc_file_ref, 
                            doc_pending, 
                            doc_valid, 
                            doc_next_version, 
                            doc_previous_version,
                            admin_user, 
                            admin_timestamp, 
                            admin_previous_entry, 
                            admin_active
                        FROM 
                            docs
                        WHERE 
                            admin_active=1 
                        ORDER BY case_id_reference,field_id_reference"""

        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# print(l_get_active_docs())

def l_get_all_docs():
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query: str = """SELECT 
                                doc_id, 
                                case_id_reference, 
                                field_id_reference, 
                                doc_desc_short, 
                                doc_desc_long, 
                                doc_version, 
                                doc_date, 
                                doc_file_ref, 
                                doc_pending, 
                                doc_valid, 
                                doc_next_version, 
                                doc_previous_version,
                                admin_user, 
                                admin_timestamp, 
                                admin_previous_entry, 
                                admin_active
                            FROM 
                                docs
                            ORDER BY case_id_reference,field_id_reference"""

        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# [print(r) for r in l_get_all_docs()]

def l_select_doc_by_id(id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""select 
                               doc_id, 
                                case_id_reference, 
                                field_id_reference, 
                                doc_desc_short, 
                                doc_desc_long, 
                                doc_version, 
                                doc_date, 
                                doc_file_ref, 
                                doc_pending, 
                                doc_valid, 
                                doc_next_version, 
                                doc_previous_version,
                                admin_user, 
                                admin_timestamp, 
                                admin_previous_entry, 
                                admin_active
                            from 
                                docs 
                            where doc_id=?""", id)
        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = []
        res = cursor.fetchall()
        if res == []:
            return None
        else:
            for row in res:
                results.append(dict(zip(columns, row)))
                #print(results[0])
            return results[0]

# print(l_select_doc_by_id(110))



def l_get_docs_for_case_id(ca_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
            select 
                    doc_id, 
                    case_id_reference, 
                    field_id_reference, 
                    doc_desc_short, 
                    doc_desc_long, 
                    doc_version, 
                    doc_date, 
                    doc_file_ref, 
                    doc_pending, 
                    doc_valid, 
                    doc_next_version, 
                    doc_previous_version,
                    admin_user, 
                    admin_timestamp, 
                    admin_previous_entry, 
                    admin_active
            from
             docs
            where
             case_id_reference=?   
        """
        cursor.execute(query,ca_id)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
            # print(results[0])
        if results == []:
            return None
        else:
            return results[0]


# print(l_get_docs_for_case_id(100))

def l_get_doc_id_for_a_field_by_case(ca_id, field_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
            select 
                    doc_id
            from
             docs
            where
             case_id_reference=? 
             AND
             field_id_reference=? 
        """
        cursor.execute(query,(ca_id,field_id))
        row = cursor.fetchone()
        if  row == None:
            return None
        else:
            return row[0]


# print(l_get_doc_id_for_a_field_by_case(100,530))

def l_get_case_id_client_id_for_doc_id(d_id):
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query="""
            select 
             case_id_reference,
             cases.client_id_ref
            from
             docs
                inner join EasyEL.dbo.cases on case_id = EasyEL.dbo.docs.case_id_reference
            where
             doc_id=?   
        """
        cursor.execute(query,d_id)
        result = cursor.fetchone()
        rlist=[]
        for r in result:
            rlist.append(r)

        #print(rlist)
        return rlist  # case_id first, then client_id

# print(l_get_case_id_client_id_for_doc_id(8))

def add_log_entry(user, current_timestamp, table_name,table_id, payload):
    return log_functions.log_add_log_entry(user, current_timestamp, table_name,table_id, payload)



def l_add_doc(cs_id,
              fld_id,
              desc_s,
              d_date,
              desc_l="Empty",
              vrs=1,
              d_file_ref="None",
              d_pend=1,
              d_valid=1,
              doc_n_vers=0,
              doc_p_ver=0):
    admin_user=functions.get_user()
    timestamp=functions.make_timestamp()
    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        query= """insert into 
                         docs (
                         case_id_reference, 
                         field_id_reference, 
                         doc_desc_short, 
                         doc_date,  
                         doc_desc_long, 
                         doc_version, 
                         doc_file_ref, 
                         doc_pending, 
                         doc_valid, 
                         doc_next_version, 
                         doc_previous_version,
                         admin_user, 
                         admin_timestamp, 
                         admin_previous_entry, 
                         admin_active 
                      )
                                           values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        cursor.execute(query,(cs_id,
                              fld_id,
                              desc_s,
                              d_date,
                              desc_l,
                              vrs,
                              d_file_ref,
                              d_pend,
                              d_valid,
                              doc_n_vers,
                              doc_p_ver,
                              admin_user,
                              timestamp,
                              0,
                              1))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return last_id

#l_add_doc(100,530,"Ehevertrag",'2022-12-20')

def l_update_doc_by_id(id_to_change,
              ccs_id,
              fld_id,
              desc_s,
              d_date,
              desc_l="Empty",
              vrs=1,
              d_file_ref="None",
              d_pend=1,
              d_valid=1,
              doc_n_vers=0,
              doc_p_ver=0):
    current_adminuser=functions.get_user()
    current_timestamp = functions.make_timestamp()
    current_table_name = 'docs'
    current_table_id=id_to_change
    current_payload=str(l_select_doc_by_id(id_to_change))
    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_adminuser,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)
    azure = connections.Azure()
    with azure:
        cursor3 = azure.conn.cursor()
        query="""   UPDATE 
                        docs 
                    SET 
                        case_id_reference=?, 
                        field_id_reference=?, 
                        doc_desc_short=?,  
                        doc_date=?, 
                        doc_desc_long=?, 
                        doc_version=?, 
                        doc_file_ref=?, 
                        doc_pending=?,  
                        doc_valid=?,  
                        doc_next_version=?, 
                        doc_previous_version=?, 
                        admin_user=?,  
                        admin_timestamp=?, 
                        admin_previous_entry=?,  
                        admin_active=? 
                    WHERE 
                        docs.doc_id=?"""
        cursor3.execute(query,
                       (ccs_id,
                        fld_id,
                        desc_s,
                        d_date,
                        desc_l,
                        vrs,
                        d_file_ref,
                        d_pend,
                        d_valid,
                        doc_n_vers,
                        doc_p_ver,
                        current_adminuser,
                        current_timestamp,
                        previous_log_entry,
                        1,
                        id_to_change))
        cursor3.commit()


# l_update_doc_by_id(5,100,530,"Ehevertrag","2022-12-20","Ehevertrag vom 12.12.2022")



def l_change_admin_status_doc_by_id(id_to_change):
    current_user=functions.get_user()
    #print(current_user)
    current_timestamp = functions.make_timestamp()
    current_table_name = 'docs'
    current_table_id=id_to_change
    current_payload=str(l_select_doc_by_id(id_to_change))
    current_admin_state=l_select_doc_by_id(id_to_change)['admin_active']
    if current_admin_state is True:
        new_status = False
    else:
        new_status = True

    #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
    previous_log_entry=add_log_entry(current_user,
                                     current_timestamp,
                                     current_table_name,
                                     current_table_id,
                                     current_payload)
    #print(previous_log_entry)

    azure = connections.Azure()
    with azure:
        cursor = azure.conn.cursor()
        cursor.execute("""  UPDATE 
                                docs 
                            SET 
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=? 
                            WHERE doc_id=?""",
                           (current_user,current_timestamp,previous_log_entry,new_status,id_to_change))
        cursor.commit()


def l_change_doc_status_doc_by_id(id_to_change):
    current_user=functions.get_user()
    #print(current_user)
    current_timestamp = functions.make_timestamp()
    current_table_name = 'docs'
    current_table_id=id_to_change
    current_payload=str(l_select_doc_by_id(id_to_change))
    if current_payload == 'None':
        print("change_doc_status_doc_by_id", id_to_change, "does not exist --> no change!")
        return None
    else:
        current_admin_state=l_select_doc_by_id(id_to_change)['doc_valid']
        if current_admin_state is True:
            new_status = False
        else:
            new_status = True

        #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
        previous_log_entry=add_log_entry(current_user,
                                         current_timestamp,
                                         current_table_name,
                                         current_table_id,
                                         current_payload)
        #print(previous_log_entry)

        azure = connections.Azure()
        with azure:
            cursor = azure.conn.cursor()
            cursor.execute("""  UPDATE 
                                    docs 
                                SET 
                                    admin_user=?,
                                    admin_timestamp=?,
                                    admin_previous_entry=?,
                                    doc_valid=? 
                                WHERE doc_id=?""",
                               (current_user,current_timestamp,previous_log_entry,new_status,id_to_change))
            cursor.commit()

# l_change_doc_status_doc_by_id(1)

def l_update_doc_by_field_by_id(table, id_field, id_to_change, newvals_list): # gets a list of fieldnames and valuse [('a', 100), ('b', 200)]
    print(newvals_list)
    if newvals_list==None:
        pass
    else:
        current_adminuser = functions.get_user()
        current_timestamp = functions.make_timestamp()
        current_table_name = table
        current_table_id = id_to_change
        current_payload = str(l_select_doc_by_id(id_to_change))
        if current_payload == 'None':
            print("update_doc_by_field_by_id: doc_id",id_to_change, "does not exist --> no change!" )
            return None
        else:

        # print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
            previous_log_entry = add_log_entry(current_adminuser,
                                               current_timestamp,
                                               current_table_name,
                                               current_table_id,
                                               current_payload)
            # print(previous_log_entry)

            for x_field,x_val,x_input_type in newvals_list:
                print(x_field,x_val,x_input_type)

                if x_input_type == "text":
                    query = "UPDATE {} SET {} = '{}' WHERE {} = {}".format(table,x_field,x_val,id_field,id_to_change)

                elif x_input_type == "number":
                    query = "UPDATE {} SET {} = {} WHERE {} = {}".format(table, x_field, x_val, id_field, id_to_change)
                    print(query)
                azure = connections.Azure()
                with azure:
                    cursor3 = azure.conn.cursor()
                    cursor3.execute(query)
                    cursor3.commit()


def l_ensure_doc(case_id,field_id):
    lang_id = cases_functions.l_select_language_short_by_case_id(case_id)
    res= l_get_doc_id_for_a_field_by_case(case_id,field_id)
    if res is None:
        lang_id = cases_functions.l_select_language_id_from_case_id(case_id)
        desc = field_descriptions.l_get_label_by_id(lang_id,field_id)
        doc_date=functions.get_current_date_as_string()
        return l_add_doc(cs_id=case_id, fld_id= field_id, desc_s=desc,d_date=doc_date,desc_l=desc)
    else:
        l_change_admin_status_doc_by_id(res)
        l_change_doc_status_doc_by_id(res)
        return res

# l_ensure_doc(100,529)
# l_ensure_doc(100,490)
# l_update_doc_by_field_by_id('docs','doc_id',1,[('doc_desc_short','Divorce AgreementHappy','text'),
#                                                ('doc_date','2022-12-25','text'),
#                                                ('field_id_reference',530,'number')])


#
# This ist just a sample
# def update_doc_content(indexfield, docid, table_name,field_name,value,value_type):
#     if value_type == "number":
#         fsupdatestring = "update {} set {} = {} where {}={}".format(table_name, field_name, value, indexfield,
#                                                                     docid)
#         print(fsupdatestring)
#         cursor.execute(fsupdatestring)
#         cursor.commit()
#     elif value_type == "text":
#         fsupdatestring = "update {} set {} = '{}' where {}={}".format(table_name, field_name, value, indexfield,
#                                                                       docid)
#         print(fsupdatestring)
#         cursor.execute(fsupdatestring)
#         cursor.commit()
# update_doc_content("doc_id",2,'EasyEL.dbo.docs','doc_desc_short','Divorce Agreement9999','text')

def l_get_all_potential_docs_for_a_client_modern(anvil_user_id,client_id):
    pass