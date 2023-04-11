import base64
import os
import sys
import uuid

from azure.identity import ClientSecretCredential, DefaultAzureCredential

from azure.keyvault.keys.crypto import CryptographyClient, KeyWrapAlgorithm,EncryptionAlgorithm
from azure.keyvault.keys import KeyVaultKey, KeyType, KeyClient
from azure.keyvault.secrets import SecretClient

from azure.storage.blob import BlobServiceClient


def l_upload_to_blob(filename, file):
    try:
        account_url = "https://easyelblob.blob.core.windows.net"
        keyvault_url = "https://easyelvault.vault.azure.net/"
        default_credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)
        container_name='easyelstore'
        container_client=blob_service_client.get_container_client(container=container_name)
        blob_client=blob_service_client.get_blob_client(container=container_name,blob=filename)
        input_stream = file
        blob_client.upload_blob(input_stream,blob_type='BlockBlob')
        # with file as data:
        #     container_client.upload_blob(data)
        return True
    except:
        print('Blob nicht geladen!')
        return False