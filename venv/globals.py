import cache
import connections



# make the cached object
global cached
cached = cache.cache_obj()

def l_register_and_setup_user(anvil_user_id,language_id=1):
    cached.conn_add(anvil_user_id) #must be first otherwise user_cache is not set
    cached.user_id_add(anvil_user_id)
    if len(cached.user_id)==1:
        cached.make_user_cache()
    cached.data_add(anvil_user_id)
    cached.info_add(anvil_user_id,language_id)
    # if G.cached.anvil_user_has_user(anvil_user_id) is False:
    #     G.register_user_id(anvil_user_id)