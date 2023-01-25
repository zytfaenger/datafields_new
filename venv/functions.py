import os
import re


import uuid
import time
import datetime
import calendar
import secrets
import string
import cryptography
from  cryptography.fernet import Fernet


def multiplyfs(x:float,y:float):
    return(x*y)

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

def get_current_date_as_string():
    return datetime.date.today().strftime('%Y-%m-%d')



def get_user():
    # just as temorary_measure
    return '1399c078-6c0f-11ed-b0bc-acde48001122'

def get_user_id():
    # just as temorary_measure
    return 100


def make_uuid():
    return uuid.uuid1()


def l_ahv_check(avh_string): # checks for validity of number, returns boolean
    AHV_Muster=re.compile('\A756.\d\d\d\d.\d\d\d\d.\d\d\Z')
    return(EAN13_check(avh_string,AHV_Muster))

def EAN13_check(string_to_check:str,pattern):
    if pattern.fullmatch(string_to_check):
        ahv_str=string_to_check[0:-1]
        regex=re.compile('[.]')
        ahv_clean_str=(regex.sub('',ahv_str))
        #print(ahv_clean_str)
        counter=0
        ahv_summe=0
        for s in ahv_clean_str:
            counter+=1
            #print(counter)
            nbr=int(s)

            if counter%2 == 0: # gerade
                #print("Die Zahl ist:", nbr,nbr*3)
                ahv_summe+=nbr*3
            else: #ungerade
                #print("Die Zahl ist:", nbr, nbr)
                ahv_summe+=nbr
            #print(ahv_summe)
        #print("AHV-Summe total", ahv_summe)
        prüfziffer=(10-ahv_summe%10)
        #print("PZ",prüfziffer)
        return(int(string_to_check[-1])==prüfziffer)

    else:
        return(False)