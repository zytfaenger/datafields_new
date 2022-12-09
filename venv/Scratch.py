from cryptography.fernet import Fernet

#Verschlüsselung

message="lookup azure in pwstore!"
original_message = message.encode()
newkey=generate_key()
store_key("fssecret.key",newkey)
restored_key=load_key("fssecret.key")
f=Fernet(restored_key)
encrypted_message=f.encrypt(original_message)
store_key("azure.key",encrypted_message)
print(encrypted_message)
azure_encrypted=load_key("azure.key")
decrypted_message=f.decrypt(azure_encrypted)
print(decrypted_message.decode())