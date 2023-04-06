from azure.identity import DefaultAzureCredential
# from azure.keyvault.keys import KeyClient, KeyOperation
# from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
# import os
# import pypdf
# import uuid
#
# #siehe https://pypi.org/project/azure-keyvault-keys/#retrieve-a-key
#
# def create_key(uuid_name):
#     credential = DefaultAzureCredential()
#     key_vault_url = "https://easyelvault.vault.azure.net/"
#     key_client = KeyClient(vault_url=key_vault_url, credential=credential)
#     key_ops = ["encrypt", "decrypt", "sign", "verify", "wrapKey", "unwrapKey"]
#     rsa_key = key_client.create_rsa_key(uuid_name, size=2048, key_operations=key_ops)
#     # aes_key = key_client.create_key()
#     return [rsa_key,rsa_key.name,rsa_key.key_type]
#
# def get_key(rsa_name_uuid_text):
#     credential = DefaultAzureCredential()
#     key_vault_url = "https://easyelvault.vault.azure.net/"
#     key_name = rsa_name_uuid_text
#     key_client = KeyClient(vault_url=key_vault_url, credential=credential)
#     key = key_client.get_key(key_name)
#     crypto_client = CryptographyClient(key, credential=credential)
#     return crypto_client
#
#
# def delete_key(rsa_name_uuid_text):
#     credential = DefaultAzureCredential()
#     key_vault_url = "https://easyelvault.vault.azure.net/"
#     key_name = rsa_name_uuid_text
#     key_client = KeyClient(vault_url=key_vault_url, credential=credential)
#     key = key_client.begin_delete_key(key_name)
#     return print(f"Deleted key'{key_name}'")
#
# # uuid_name=str(uuid.uuid1())
# # print(str(uuid_name))
# # a=create_key(uuid_name)
# # print(a)
#
#
# # pdf=pypdf.PdfReader
# # pdf.read()
# cc=create_key("20230405")
# crypto_client=get_key('20230405')
# DOES NOT WORK ON A FILE - USE AES
# # local_path = "/Users/fschumacher/PycharmProjects/datafields/venv/data"
# # local_file_name='Lohn2021.pdf'
# # full_file_path = os.path.join(local_path, local_file_name)
# # file=open(full_file_path,mode='rb')
# # file_in_mem=file.read()
# # print(file_in_mem)
# #
# # encoded_file = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep,file_in_mem)
# # print("------")
# # print(encoded_file,encoded_file.algorithm,encoded_file.ciphertext)
# # decoded_file = crypto_client.decrypt(encoded_file.algorithm, encoded_file.ciphertext)
# # print(decoded_file)
#
#
#
#
# result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, plaintext)
# decrypted = crypto_client.decrypt(result.algorithm, result.ciphertext)
# print(result.ciphertext)
# print(decrypted.plaintext)
# # does not work (yet!)
#
# # local_path = "./data"
# # local_file_name='Lohn2020.pdf'
# # upload_file_path = os.path.join(local_path, local_file_name)
# # file=open(upload_file_path)
# # result=result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, file)
# # decrypted = crypto_client.decrypt(result.algorithm, result.ciphertext)
# # newfile=file
# # newfile.name='Lohn2020v2.pdf'
# # newfile.write(decrypted)
# # newfile.close()