from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm


key_vault_url = "https://easyelvault.vault.azure.net/"
key_name = "fuerdavid"

credential = DefaultAzureCredential()

key_client = KeyClient(vault_url=key_vault_url, credential=credential)

key = key_client.get_key(key_name)
crypto_client = CryptographyClient(key, credential=credential)
plaintext = b"plaintext"
result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, plaintext)
decrypted = crypto_client.decrypt(result.algorithm, result.ciphertext)
print(result)
#siehe https://pypi.org/project/azure-keyvault-keys/#retrieve-a-key