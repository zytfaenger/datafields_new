from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
import os
import pypdf
import uuid

#siehe https://pypi.org/project/azure-keyvault-keys/#retrieve-a-key

def create_key(uuid_name):
    credential = DefaultAzureCredential()
    key_vault_url = "https://easyelvault.vault.azure.net/"
    key_client = KeyClient(vault_url=key_vault_url, credential=credential)
    rsa_key = key_client.create_rsa_key(uuid_name, size=2048)
    aes_key = key_client.create_key()
    return [rsa_key.name,rsa_key.key_type]

def get_key(rsa_name_uuid_text):
    credential = DefaultAzureCredential()
    key_vault_url = "https://easyelvault.vault.azure.net/"
    key_name = rsa_name_uuid_text
    key_client = KeyClient(vault_url=key_vault_url, credential=credential)
    key = key_client.get_key(key_name)
    crypto_client = CryptographyClient(key, credential=credential)
    return crypto_client


def delete_key(rsa_name_uuid_text):
    credential = DefaultAzureCredential()
    key_vault_url = "https://easyelvault.vault.azure.net/"
    key_name = rsa_name_uuid_text
    key_client = KeyClient(vault_url=key_vault_url, credential=credential)
    key = key_client.begin_delete_key(key_name)
    return print(f"Deleted key'{key_name}'")

# uuid_name=str(uuid.uuid1())
# print(str(uuid_name))
# a=create_key(uuid_name)
# print(a)
crypto_client=get_key('e93fae40-ca1f-11ed-a61e-acde48001122')
plaintext = b"Franz Schumacher"

pdf=pypdf.PdfReader
pdf.read()


local_path = "./data"
local_file_name='Lohn2021.pdf'
upload_file_path = os.path.join(local_path, local_file_name)



file= open(file=upload_file_path, mode='rb')
pdf=pypdf.PdfReader
pdf.read(file)







result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, plaintext)
decrypted = crypto_client.decrypt(result.algorithm, result.ciphertext)
print(result.ciphertext)
print(decrypted.plaintext)
# does not work (yet!)

# local_path = "./data"
# local_file_name='Lohn2020.pdf'
# upload_file_path = os.path.join(local_path, local_file_name)
# file=open(upload_file_path)
# result=result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, file)
# decrypted = crypto_client.decrypt(result.algorithm, result.ciphertext)
# newfile=file
# newfile.name='Lohn2020v2.pdf'
# newfile.write(decrypted)
# newfile.close()