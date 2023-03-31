import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient,EncryptionAlgorithm
from azure.storage.blob import BlobServiceClient


# Azure Blob Storage account and container details
account_url = 'https://easyelblob.blob.core.windows.net'
container_name = 'easyelstore'
blob_name = 'fs3'

# Azure Key Vault details
vault_url = 'https://easyelvault.vault.azure.net/'
key_name = 'fs2048'

# Path to the PDF file to be uploaded
local_path = "./data"
local_file_name='Lohn2021.pdf'
pdf_path = os.path.join(local_path, local_file_name)

# Initialize the Azure Blob Storage client
default_credentials = DefaultAzureCredential()
blob_service_client = BlobServiceClient(account_url=account_url, credential=default_credentials)
blob_client = blob_service_client.get_blob_client(container_name, blob_name)

# Read the PDF file contents
with open(pdf_path, "rb") as f:
    pdf_contents = f.read()

# Initialize the Azure Key Vault clients
key_client = KeyClient(vault_url=vault_url, credential=default_credentials)
key = key_client.get_key(key_name)

crypto_client = CryptographyClient(key, credential=default_credentials)

# Encrypt the PDF file contents using the RSA key from the Azure Key Vault
encrypted_data = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, pdf_contents)

# Upload the encrypted PDF file to Azure Blob Storage
blob_client.upload_blob(encrypted_data, overwrite=True)

print(f'Encrypted PDF file uploaded to Azure Blob Storage container: {container_name}, blob: {blob_name}')
