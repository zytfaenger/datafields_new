import uuid
import functions
import users
import globals as G

def l_add_link(anvil_user_id,client_id,email="anymail@gmail"):
    u1=uuid.uuid1() #generate new UUID
    clo_id=uuid.uuid3(u1,email)
    user_record=users.l_get_user_record_for_anvil_user_modern(anvil_user_id)
    admin_user=user_record['admin_user']
    timestamp = functions.make_timestamp()
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor=azure.cursor()

        query="""insert into client_link_offer (
                        clo_id,
                        clo_giver_id,
                        clo_mailid,
                        clo_link_consumed,
                        clo_consuming_receiver_id,
                        clo_link_searchable,
                        admin_user,
                        admin_previous_entry,
                        admin_timestamp,
                        admin_active) 
                        values(?,?,?,?,?,?,?,?,?,?) """
        cursor.execute(query,
                           (clo_id,
                            client_id,
                            email,
                            False,
                            "",
                            True,
                            admin_user,
                            0,
                            timestamp,
                            1))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return last_id

def get_clo_by_id_modern(anvil_user_id,clo_id):
    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query="""select * 
        
                    from client_link_offer
                    where clo_id=?"""


def l_claim_offer(clo_id,claiming_user_id,clo_mail):  #update uuid is another function below!!
    current_admin_user_rec = users.l_get_user_by_id(user_ref)
    if current_admin_user_rec is None:
        print('update_client: User given does not exist:', user_ref)
        return None
    else:
        if type(current_admin_user_rec) != dict:
            print('add_client: current_admin_user should be dict!:', current_admin_user_rec,
                  type(current_admin_user_rec))
            return None
        else:
            current_admin_user = current_admin_user_rec['admin_user']
            current_timestamp = functions.make_timestamp()
            current_table_name = 'clients'
            current_table_id=client_id_to_change
            current_payload=str(l_get_client_by_id(client_id_to_change))
            #print(current_user,current_timestamp,current_table_name,current_table_id,current_payload)
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
                                clients 
                            SET 
                                client_user_ref=?,
                                client_is_user=?,
                                client_name=?,
                                admin_user=?,
                                admin_timestamp=?,
                                admin_previous_entry=?,
                                admin_active=?
                            WHERE 
                                EasyEL.dbo.clients.client_id=?"""
                cursor3.execute(query, (user_ref,client_is_user,name,current_admin_user, current_timestamp, previous_log_entry, 1, client_id_to_change))
                cursor3.commit()


# l_update_client(190, 160,False,"Roger Rabbit")
