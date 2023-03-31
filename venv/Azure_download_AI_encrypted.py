from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Create a BlobServiceClient object using your storage account connection string
blob_service_client = BlobServiceClient.from_connection_string("<your-storage-account-connection-string>")

# Create a blob client object for the encrypted PDF file
encrypted_blob_client = blob_service_client.get_blob_client("<your-container-name>", "<encrypted-pdf-file-name>")

# Download the encrypted blob as bytes
encrypted_data = encrypted_blob_client.download_blob().content_as_bytes()

# Retrieve the RSA key from the key vault using the code from my previous answer
# ...

# Load the RSA key into a Key object
key = serialization.load_pem_private_key(rsa_key.encode(), password=None)

# Decrypt the encrypted data using the RSA key
plaintext = key.decrypt(
    encrypted_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save the decrypted data to a file
with open("<path-to-decrypted-pdf-file>", "wb") as data:
    data.write(plaintext)
