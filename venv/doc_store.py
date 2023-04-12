import base64
import uuid
import os
import hashlib
import io
import anvil.media
import anvil
import azure_storage_blob
import clients
import globals as G
from PyPDF2 import PdfReader, PdfWriter
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from pathlib import Path


def l_get_docs_for_a_client_id(anvil_user_id,client_id):
    try:
        azure = G.cached.conn_get(anvil_user_id)
    except:
        G.l_register_and_setup_user(anvil_user_id, 1)
        azure = G.cached.conn_get(anvil_user_id)

    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query: str = """SELECT 
                           my_docs_id id,
                           client_id_ref,
                           doc_typ_id_ref cat,
                           dt.doc_type_sort dt_sort,
                           years_ref year,
                           doc_store_group sort,
                           original_file_name doc,
                           file_description decscriptor,
                           store_file_ext ext
                            
                        FROM 
                            docs_stored ds
                        join docs_doc_types dt on dt.doc_typ_id = ds.doc_typ_id_ref
                        WHERE
                            client_id_ref=? 
                        ORDER BY dt_sort,year,sort"""

        cursor.execute(query, client_id)

        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if results == []:
            return [None]
        else:
            res = []
            for row in results:
                res.append(dict(zip(columns, row)))
            return res

# G.l_register_and_setup_user('[344816,583548811]',1) #Louis
# a=l_get_docs_for_a_client_id('[344816,583548811]',210)
# for i in range(0,len(a)):
#     print(a[i])
def l_internal_get_docs_record_for_an_id (anvil_user_id, client_id,my_docs_id):
    try:
        azure = G.cached.conn_get(anvil_user_id)
    except:
        G.l_register_and_setup_user(anvil_user_id, 1)
        azure = G.cached.conn_get(anvil_user_id)

    azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query: str = """SELECT 
                           my_docs_id, 
                           client_id_ref, 
                           doc_typ_id_ref, 
                           years_ref, 
                           original_file_name, 
                           store_full_file_name, 
                           file_description, 
                           store_filename, 
                           store_file_ext, 
                           doc_store_group, 
                           hash, 
                           our_pdf_encoding
                        FROM 
                            docs_stored ds
                        WHERE
                            client_id_ref=? and
                            my_docs_id=? """

        cursor.execute(query, client_id,my_docs_id)

        columns = [column[0] for column in cursor.description]
        # print(columns)
        results = cursor.fetchall()
        if not results:
            return [None]
        else:
            res = []
            for row in results:
                res.append(dict(zip(columns, row)))
            return res[0]


# G.l_register_and_setup_user('[344816,583548811]',1) #Louis
# a=l_internal_get_docs_record_for_an_id('[344816,583548811]',210,28)
# for i in range(0,len(a)):
#     print(a[i])



def l_add_doc_to_docstore_modern(anvil_user_id, client_id, file, hash):
    orginal_file_name=file.name

    doc_typ_id_ref = 40 #"=nicht zugeordnet"
    doc_store_group = ""
    file_desc = ""
    years_ref='0'
    new_file_name = str(uuid.uuid4())
    file_desc = ""
    file_name, file_extension = os.path.splitext(file.name)
    # print(file_name, file_extension)

    try:
        azure = G.cached.conn_get(anvil_user_id)
    except:
        G.l_register_and_setup_user(anvil_user_id, 1)
        azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query= """ insert into docs_stored
                                     (client_id_ref, 
                                     original_file_name,
                                     doc_typ_id_ref,
                                     doc_store_group, 
                                     file_description, 
                                     years_ref,
                                     store_full_file_name,
                                     store_filename,
                                     store_file_ext,
                                     hash,
                                     our_pdf_encoding
                                      
                                     )
                                     values (?,?,?,?,?,?,?,?,?,?,?)"""
        cursor.execute(query,
                       (client_id,
                        orginal_file_name,
                        doc_typ_id_ref,
                        doc_store_group,
                        file_desc,
                        years_ref,
                        new_file_name,
                        file_name,
                        file_extension,
                        hash,
                        False
                        ))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return (last_id,new_file_name)

# G.l_register_and_setup_user('[344816,583548811]',1)
# print(l_add_doc_to_docstore_modern('[344816,583548811]','210','test.pfd'))

def l_update_doc_store_field_modern(anvil_user_id, my_docs_id_to_change, field,value):
    try:
        azure = G.cached.conn_get(anvil_user_id)
    except:
        G.l_register_and_setup_user(anvil_user_id, 1)
        azure = G.cached.conn_get(anvil_user_id)
    permissible_fields={'doc_typ_id_ref','years_ref','file_description','doc_store_group','our_pdf_encoding'}
    with azure:
        if field in permissible_fields:
            cursor = azure.cursor()
            query = """UPDATE docs_stored
                        SET 
                            {}=?
                        WHERE 
                            my_docs_id=?""".format(field)
            cursor.execute(query, (value,my_docs_id_to_change))
            cursor.commit()
            return "updated"
        else:
            print('field not permitted')
            return "not changed"


# G.l_register_and_setup_user('[344816,583548811]',1)
# l_update_doc_store_field_modern('[344816,583548811]','18','years_ref','2023')
# l_update_doc_store_field_modern('[344816,583548811]','18','doc_typ_id_ref','25')
# l_update_doc_store_field_modern('[344816,583548811]','18','client_id_ref','180')



def ensure_datafolder(foldernmae):
    try:
        os.mkdir("data")
        print('New folder made')
        print(os.getcwd())
    except:
        print('Folder exists')
        print(os.getcwd())


def ensure_datafolder2(data):
    if os.path.exists(data):
        print('path exists')
    else:
        os.mkdir(data)
        print('newly created')



# def l_process_and_import_docs(filelist):
#     for f in filelist:
#         print (f.name)
#         filename,file_extension = os.path.splitext(f.name)
#         print(filename,file_extension)

def store_secret(keyname,token):
    credential = DefaultAzureCredential()
    sec_vault_url = "https://easyelvault.vault.azure.net/"
    secret_client = SecretClient(vault_url=sec_vault_url,credential=credential)
    secret=secret_client.set_secret(keyname,token)
    return secret


#siehe https://pypi.org/project/azure-keyvault-keys/#retrieve-a-key

def get_secret(secname):
    credential = DefaultAzureCredential()
    sec_vault_url = "https://easyelvault.vault.azure.net/"
    sec_client = SecretClient(vault_url=sec_vault_url, credential=credential)
    secret = sec_client.get_secret(secname)
    return secret




def delete_secret(secname):
    credential = DefaultAzureCredential()
    sec_vault_url = "https://easyelvault.vault.azure.net/"
    sec_client =SecretClient(vault_url=sec_vault_url, credential=credential)
    secret = sec_client.begin_delete_secret(secname)
    return sec_client.list_deleted_secrets

# uuid_name=str(uuid.uuid1())
# print(str(uuid_name))
# a=create_key(uuid_name)
# print(a)



# pdf=pypdf.PdfReader
# pdf.read()
#
#
# local_path = "./data"
# local_file_name='Lohn2021.pdf'
# upload_file_path = os.path.join(local_path, local_file_name)

def create_token(pwd):
   password = pwd.encode()
   # print(password)

   salt = os.urandom(16)
   # print(salt)
   kdf = PBKDF2HMAC(
                algorithm = hashes.SHA256(),
                length = 32,
                salt = salt,
                iterations = 480000,
            )
   key = base64.urlsafe_b64encode(kdf.derive(password))
   return key

# print(create_token('1ea4685e-acce-4a42-a2a8-8ccd57d95800'))


def encode(key,file_read):
   f = Fernet(key)
   encoded_file= f.encrypt(file_read)
   return encoded_file

def decode(key,encoded_file):
   #Fernet does the derivation of the url_safe_key!!!
   f = Fernet(key)
   decoded_file = f.decrypt(encoded_file)
   return decoded_file
def write_decoded_file(decoded_file, path_and_filename_and_ending):
   fileout = open(path_and_filename_and_ending, mode='wb')
   fileout.write(decoded_file)
   fileout.close()






# file= open(file=upload_file_path, mode='rb')
# pdf=pypdf.PdfReader
# pdf.read(file)


#
# blob_url = "https://easyelblob.blob.core.windows.net"
# default_credential = DefaultAzureCredential()
#
# # Create the BlobServiceClient object
# blob_service_client = BlobServiceClient(blob_url, credential=default_credential)


#container_name=str(uuid.uuid4())
# container_client=blob_service_client.create_container(container_name)

# Create a local directory to hold blob data



# Create a file in the local data directory to upload and download
# local_file_name = str(uuid.uuid4()) + ".pdf"



# blob_client = blob_service_client.get_blob_client(container='easyelstore', blob=local_file_name)

# print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
#
# # Upload the created file
# with open(file=upload_file_path, mode="rb") as data:
#     blob_client.upload_blob(data)


#
#
#
# uuid= 'c20649da-2589-4816-a61f-35a5c6fcb71z'
# # token = create_token(uuid)
# # print(uuid,token)
# # store_secret(uuid,token)
# secret=get_secret(uuid)
# print(secret.name,secret.value)
# # print(delete_secret(uuid))
# path = os.getcwd()
# venv=str(Path(path).parents[0])
# local_path = venv+"/data"
# print(local_path)
# local_file_name='Lohn2021.pdf'
# upload_file_path = os.path.join(local_path, local_file_name)
# local_file_name='Lohn2021.pdf'
# local_file_name_after = 'Lohn2021encr.pdf'
# local_file_name_after2= 'Lohn2021encrdecr.pdf'
# # pdf_encryption.py
# upload_file_path = os.path.join(local_path, local_file_name)
# download_file_path_enc=os.path.join(local_path,local_file_name_after)
# download_file_path_encdec=os.path.join(local_path,local_file_name_after2)
# reader = PdfReader(upload_file_path)
# writer = PdfWriter(local_file_name_after)
# file = open(upload_file_path,mode='rb')
# token = create_token(uuid,file)
# print(token)
# for page in reader.pages:
#     writer.add_page(page)
# writer.encrypt(uuid)
# writer.write(download_file_path_enc)
#
# reader2 = PdfReader(download_file_path_enc,password=uuid)
# writer2=PdfWriter(local_file_name_after2)
# for page in reader.pages:
#     writer2.add_page(page)
# writer2.write(download_file_path_encdec)


# Dokument speichern(anvil_user_id, client_id, files)
#
# get_the_client_uuid()
# load the files
# für jedes file:
#     generiere eine Dok_uuid
#     lege in der Dokstored einen Eintrag mit original-Name, und original_typ und UUID als Schlüssel ab
#     generiere einen Schlüssel mit der dokument UUID als Seed
#     speichere den Schlüssel im Keyvault secret unter dem dokUUID ab
#     ist die Datei ein PDF?
#         ist es nicht verschlüsselt?
#            verschlüssln des Dokuments mit der client_uuid
#         sonst
#            markieren als Kundenverschlüsselt und Warnung
#
#         als seed
#     wandle die Datei in Bits
#     verschlüssle die Datei mit dem Schlüssel
#     speichere die Datei auf dem Blob-Speicher unter dem neuen UUID_Dokname
#   original-Dateien löschen
#   andere spuren entfernen
#
# Dokument laden (docs_stored_ID)
#
# docs_stored_id record finden
# dokuuid nehmen und aus blob herunterladen --> verschlüsselte Datei
# schlüssel aus keyvault via uuid holen
# verschlüsselte Datei entschlüsseln -> decodierte, noch geschützte Datei
# Datei öffnen mit Client UUID
# Datei unter original-namen downloaden/speichern




# blob_client = blob_service_client.get_blob_client(container='easyelstore', blob=local_file_name)
#
# print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)


def get_hash(file_read):
    if len(file_read) ==0:
        pass
    else:
        hash=hashlib.sha3_384(file_read)
        return str(hash.hexdigest())
def check_hash_present_modern(anvil_user_id, hash):
    try:
        azure = G.cached.conn_get(anvil_user_id)
    except:
        G.l_register_and_setup_user(anvil_user_id, 1)
        azure = G.cached.conn_get(anvil_user_id)
    with azure:
        cursor = azure.cursor()
        query= """ select 
                        my_docs_id,
                        hash
                   from 
                        docs_stored
                   where
                        hash=?"""
        cursor.execute(query,hash)
        res=cursor.fetchall()
        if res == []:
            return False
        elif len(res)==1:
            return True
        else:
            print('Warning: multiple files with identical hash:', hash)
            return True

# G.l_register_and_setup_user('[344816,583548811]',1)
# print(check_hash_present_modern('[344816,583548811]','3426c2087d98d35f740987f70ed4f090abda5c0b41ec381165cfb3e90150a1952d98f637eaaba6fc913ecd0c8ec4d8b8'))

def l_process_and_import_docs(anvil_user_id, client_id, filelist):
    #store in DB with reference
    return_list=[] #um den Status der einzelnen Dokumente zurückzugeben
    for file in filelist:
        # print (file.name)
        file_read = file.get_bytes()
        #make sure that document is entered into table but has no duplicates
        hash = get_hash(file_read)
        # print(file.name, "has Hash:", hash)
        if check_hash_present_modern(anvil_user_id,hash):
            return_list.append(('{} not_stored'.format(file.name),'Datei {} existiert bereits'.format(file.name)))
        else:
            newrecord=l_add_doc_to_docstore_modern(anvil_user_id,client_id,file,hash)
            new_docs_stored_id=newrecord[0] #id of doc stored
            new_file_name_uuid=newrecord[1] #uuid generated and stored

            # print('process und import - new record',newrecord)
            return_list.append(('{} stored'.format(file.name),'Datei {} hinzugefügt'.format(file.name)))

            file_name, file_extension = os.path.splitext(file.name)
            client_doc_id_uuid = clients.l_get_doc_store_uuid_for_a_client(anvil_user_id, client_id)

            if file_extension ==".pdf": #make sure pdf are encrypted (double security)
                file_to_write=io.open("ftw.pdf",'wb')
                file_to_write.write(file_read)
                file_to_write.close()
                file_to_read=io.open("ftw.pdf",'rb')

                current_pdf = PdfReader(file_to_read)
                if current_pdf.is_encrypted is False: # it is a PDF that is not encrypted->encrypt it...
                    file_to_encrypt_pdf=PdfWriter(new_file_name_uuid)
                    for page in current_pdf.pages:
                        file_to_encrypt_pdf.add_page(page)
                    file_to_encrypt_pdf.encrypt(client_doc_id_uuid)
                    file_to_encrypt_pdf.write("file_to_upload_encrypted_pdf.pdf")
                    file_to_encrypt_pdf.close()
                    file_reopen=io.open('file_to_upload_encrypted_pdf.pdf','rb')
                    file_to_encrypt=file_reopen.read()  #need a bytestream...
                    l_update_doc_store_field_modern(anvil_user_id, new_docs_stored_id, 'our_pdf_encoding', True)
                    return_list.append(('{} encrypted'.format(file.name), 'Datei {} is now encrypted'.format(file.name)))
                else: # PDF is encrypted
                    return_list.append('{} not encrypted'.format(file.name), 'Datei {} already encrypted. Key is user responsibility'.format(file.name))
                    file_to_encrypt=file_to_read
                os.remove('ftw.pdf')
                os.remove('file_to_upload_encrypted_pdf.pdf')
            else:
                file_to_encrypt=file_read #other documents are
                return_list.append(('{} not encrypted'.format(file.name), 'Datei {} not pdf'.format(file.name)))
            # now, let's get a key for the encryption

            key=create_token(new_file_name_uuid)
            return_list.append(('{} key created'.format(file.name), 'Key used to encrypt file'))
            # and store it in the secret_store
            secret=store_secret(new_file_name_uuid,key) #base64.urlsafe!
            return_list.append(('{} key stored'.format(file.name), 'Key naming regular'))
            #now use the key to encode the file
            encryped_file_for_BLOB=encode(key,file_to_encrypt)
            upload_result=azure_storage_blob.l_upload_to_blob(new_file_name_uuid,encryped_file_for_BLOB)
            if upload_result:
                return_list.append(('{} File stored'.format(file.name), 'File naming regular'))
            else:
                return_list.append(('{} File NOT stored'.format(file.name), 'Check error messages'))

    return return_list

def l_download_blob(anvil_user_id, client_id, my_docs_id):
    return_message=[]
    docs_record = l_internal_get_docs_record_for_an_id(anvil_user_id, client_id, my_docs_id)
    return_message.append("Got file information from DB")
    blob_name=docs_record['store_full_file_name']
    hash=docs_record['hash']
    our_encoding=docs_record['our_pdf_encoding']
    original_file_name=docs_record['original_file_name']
    file_extension=docs_record['store_file_ext']

    return_message.append("crucial data obtained")

    key=eval(get_secret(blob_name).value) #get rid of string and get_the_value
                                           # careful  key needs to be in the in url-safe-format (size 44 bytes)
                                           # afterward the key will be reduced in decode to 32 bytes
    blob=azure_storage_blob.l_download_blob(blob_name)

    return_message.append("downloaded Blob")
    decoded_blob=decode(key,blob)
    return_message.append("decoded Blob")
    if file_extension==".pdf":
      # this uses a file as intermediate...
        decoded_protected_blob_file = io.open('dpbf.pdf','wb')
        decoded_protected_blob_file.write(decoded_blob)
        decoded_protected_blob_file.close()

        pdf_protected_to_read=io.open('dpbf.pdf','rb')
        reader= PdfReader(pdf_protected_to_read)
        writer=PdfWriter()
        if reader.is_encrypted:
            if our_encoding is True:
                client_doc_id_uuid = clients.l_get_doc_store_uuid_for_a_client(anvil_user_id, client_id)
                reader.decrypt(client_doc_id_uuid)
                for page in reader.pages:
                   writer.add_page(page)
                with open(original_file_name,'wb') as f:
                   writer.write(f)
                os.remove('dpbf.pdf')
            else:
                pdf_to_write = io.open(original_file_name,'wb')
                pdf_to_write.write(decoded_blob)
                pdf_to_write.close()
     # this is more elegant
    # if file_extension == ".pdf":
    #     decoded_protected_blob_file_test=io.BytesIO(decoded_blob)
    #     reader2=PdfReader(decoded_protected_blob_file_test)
    #     writer2=PdfWriter()
    #     if reader2.is_encrypted:
    #         if our_encoding is True:
    #            client_doc_id_uuid = clients.l_get_doc_store_uuid_for_a_client(anvil_user_id, client_id)
    #            reader2.decrypt(client_doc_id_uuid)
    #            return_message.append("Remove Password from pdf")
    #            for pages in reader2.pages:
    #                writer2.add_page(pages)
    #            file_to_return=io.BytesIO()
    #            file_to_return2= io.FileIO("test314.pdf")
    #            writer2.write(file_to_return)
    #            writer2.write(file_to_return2)
    #            print(file_to_return)
    #            print(file_to_return2)
    #            with open(original_file_name,'wb') as t:
    #                writer2.write(t)
    #
    #            return_message.append("original file written")
    #
    #         else:
    #             pdf_to_write = io.open(original_file_name,'wb')
    #             pdf_to_write.write(decoded_blob)
    #             pdf_to_write.close()
    #             return_message.append("client_encrpted file written")
    else:
       file_to_write=io.open(original_file_name,'wb')
       file_to_write.write(decoded_blob)
       file_to_write.close()
       return_message.append("Non-PDF-File written")


    # with open(original_file_name,'rb') as f:
    #     text=f.read()
    a=anvil.media.from_file(original_file_name,name=original_file_name)
    # file_to_return=anvil.BlobMedia(content_type="text/plain",content=text,name=original_file_name)
    return a

#print(l_download_blob('[344816,583548811]',210, 28))
