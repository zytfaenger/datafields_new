import base64
import uuid
import os

import clients
import globals as G
from PyPDF2 import PdfReader, PdfWriter
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from pathlib import Path


def l_add_doc_to_docstore_modern(anvil_user_id, client_id, file):
    client_doc_id=clients.l_get_doc_store_uuid_for_a_client(anvil_user_id,client_id)
    orginal_file_name=file.name

    doc_typ_id_ref = 40 #nicht zugeordnet
    doc_store_group = ""
    file_desc = ""
    years_ref='0'
    new_file_name = str(uuid.uuid4())
    file_desc = ""
    file_name, file_extension = os.path.splitext(file.name)
    print(file_name, file_extension)


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
                                     store_file_ext 
                                     )
                                     values (?,?,?,?,?,?,?,?,?)"""
        cursor.execute(query,
                       (client_id,
                        orginal_file_name,
                        doc_typ_id_ref,
                        doc_store_group,
                        file_desc,
                        years_ref,
                        new_file_name,
                        file_name,
                        file_extension
                        ))
        cursor.commit()
        cursor.execute("SELECT @@IDENTITY AS ID;")
        last_id = int(cursor.fetchone()[0])
        return last_id

# G.l_register_and_setup_user('[344816,583548811]',1)
# print(l_add_doc_to_docstore_modern('[344816,583548811]','210','test.pfd'))

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



def l_process_and_import_docs(filelist):
    for f in filelist:
        print (f.name)
        filename,file_extension = os.path.splitext(f.name)
        print(filename,file_extension)

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
   print(password)

   salt = os.urandom(16)
   print(salt)
   kdf = PBKDF2HMAC(
                algorithm = hashes.SHA256(),
                length = 32,
                salt = salt,
                iterations = 480000,
            )
   key = base64.urlsafe_b64encode(kdf.derive(password))
   return key

def encode(key,open_file):
   f = Fernet(key)
   file_read = open_file.read()
   encoded_file= f.encrypt(file_read)
   return encoded_file

def decode(encoded_file,key):
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


def l_process_and_import_docs(anvil_user_id, client_id, filelist):
    for file in filelist:
        print (file.name)
        record=l_add_doc_to_docstore_modern(anvil_user_id,client_id,file)
        print('process und import - new record',record)
        file_name,file_extension = os.path.splitext(file.name)
        print(file_name,file_extension)