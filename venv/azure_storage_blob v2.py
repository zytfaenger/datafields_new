import base64
import os
import sys
import uuid

from azure.identity import ClientSecretCredential, DefaultAzureCredential

from azure.keyvault.keys.crypto import CryptographyClient, KeyWrapAlgorithm,EncryptionAlgorithm
from azure.keyvault.keys import KeyVaultKey, KeyType, KeyClient
from azure.keyvault.secrets import SecretClient

from azure.storage.blob import BlobServiceClient



account_url = "https://easyelblob.blob.core.windows.net"
keyvault_url = "https://easyelvault.vault.azure.net/"

default_credential = DefaultAzureCredential()

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=default_credential)


#container_name=str(uuid.uuid4())
# container_client=blob_service_client.create_container(container_name)

# Create a local directory to hold blob data
local_path = "./data"


# Create a file in the local data directory to upload and download
# local_file_name = str(uuid.uuid4()) + ".pdf"
local_file_name='Lohn2021.pdf'
upload_file_path = os.path.join(local_path, local_file_name)

# Write text to the file
# file = open(file=upload_file_path, mode='w')
# file.write("Hello, World!")
# file.close()

credential = DefaultAzureCredential()

key_client = KeyClient(keyvault_url, credential=credential)

key = key_client.get_key('fuerdavid')

crypo_client=CryptographyClient(key,credential=credential)



# Create a blob client using the local file name as the name for the blob
blob_client = blob_service_client.get_blob_client(container='easyelstore', blob=local_file_name)
blob_client.encryption_version='2.0'
key_bytes=crypo_client.wrap_key(key=key,algorithm=KeyWrapAlgorithm.rsa_oaep)
kvk=KeyVaultKey(key_id=key.id,key_ops=['unwrapKey', 'wrapKey'],k=key_bytes,kty=KeyType.rsa)


blob_client.key_encryption_key=kvk
print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

# Upload the created file
with open(file=upload_file_path, mode="rb") as data:
    blob_client.upload_blob(data)

