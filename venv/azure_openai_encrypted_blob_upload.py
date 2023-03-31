from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
import json
import os
import base64


# Upload the PDF file to the container

local_path = "./data"
local_file_name='Lohn2021.pdf'
upload_file_path = os.path.join(local_path, local_file_name)
account_url = "https://easyelblob.blob.core.windows.net"
keyvault_url = "https://easyelvault.vault.azure.net/"
default_credential = DefaultAzureCredential()
rsa_keyname = "fuerdavid"
container="easyelstore"



# Create a BlobServiceClient object using your storage account connection string
blob_service_client = BlobServiceClient(account_url,credential=default_credential)

# Create a container client object
container_client = blob_service_client.get_container_client(container)




with open(upload_file_path, "rb") as data:
    container_client.upload_blob(name='encrypted_steuern_2021v21', data=data)

# Create a SecretClient object using your key vault URL and default credentials
key_client = KeyClient(vault_url=keyvault_url, credential=default_credential)

# Get the RSA key from the key vault
rsa_key = key_client.get_key(rsa_keyname)

# Convert the RSA key from JWK to PEM format
jwk_dict = rsa_key.key
key = rsa.RSAPublicNumbers(
    e=int.from_bytes(base64.urlsafe_b64decode(jwk_dict.e + "==="), byteorder="big"),
    n=int.from_bytes(base64.urlsafe_b64decode(jwk_dict.n + "==="), byteorder="big")
).public_key(default_backend())
pem_key = key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Load the RSA public key into a Key object
public_key = serialization.load_pem_public_key(pem_key, backend=default_backend())










# Retrieve the RSA key from the key vault
#rsa_key = key_client.get_key(rsa_keyname)

key_material=rsa_key._key_material
# jwk = key_client.get_key(rsa_keyname).key
#
# # Convert the JWK to a dictionary and get the values for 'n' and 'e'
# jwk_dict = json.loads(jwk)
# n = int.from_bytes(jwk_dict['n'], 'big')
# e = int.from_bytes(jwk_dict['e'], 'big')
#
# # Create an RSA public key using 'n' and 'e'
# public_numbers = rsa.RSAPublicNumbers(e=e, n=n)
# public_key = public_numbers.public_key(default_backend())

# pem_public_key = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )



# Load the RSA key into a Key object

# key = serialization.load_pem_private_key(key_material, password=None)
# key = serialization.load_pem_private_key(rsa_key.key, password=None, backend=default_backend())


# Encrypt the PDF file using the RSA key
with open(upload_file_path, "rb") as data:
    plaintext = data.read()
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Upload the encrypted file to Azure Blob Storage
container_client.upload_blob(name="<encrypted-pdf-file-name>", data=ciphertext)
