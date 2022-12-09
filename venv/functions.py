import os

def multiplyfs(x:float,y:float):
    return(x*y)
import uuid
import time
import calendar
import secrets
import string
import cryptography
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def store_key(filename,key_to_be_stored):
    with open(filename,"wb") as key_file:
        key_file.write(key_to_be_stored)

def load_key(filename):
    restored_key=open(filename,"rb").read()
    return restored_key


def regenerate_password():
    currdir=os.getcwd()
    #print(currdir)
    os.chdir('/Users/fschumacher/PycharmProjects/datafields/venv/keys')
    try:
        restored_key = load_key("fssecret.key")
    except Exception as e:
        print(e, "-->check file fsssecret.key")

    f = Fernet(restored_key)

    try:
        encrypted_pw = load_key("azure.key")
    except Exception as e:
        print(e, "-->check file azure.key")

    password = f.decrypt(encrypted_pw)
    os.chdir(currdir)
    return password.decode()

def make_timestamp():
    #Returns current gmttime as Integer
    now = time.gmtime()
    return calendar.timegm(now)

def get_user():
    # just as temorary_measure
    return '1399c078-6c0f-11ed-b0bc-acde48001122'

def get_user_id():
    # just as temorary_measure
    return 100



def make_uuid():
    return uuid.uuid1()

