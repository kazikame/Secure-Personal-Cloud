import getpass
import hashlib
import json
import sys
from functools import partial
from os import walk

import requests

from encryption import *


def md5sum(f):
    d = hashlib.md5()
    for buf in iter(partial(f.read, 128), b''):
        d.update(buf)
    return d.hexdigest()


def upload2(username, password, Base_Folder):
    """
    Main Upload function.

    :param username:
    :param password:
    :param Base_Folder: The folder being synced/uploaded
    :return:

    {SITE_URL} = http://127.0.0.1:8000

    Step 1: Get the token by logging in with correct username+password.
    Step 2: Send a post request to {SITE_URL}/api/get_key with the header
            {"Authorisation": "Token {INSERT_TOKEN_NO}"}

            It will return
            {
                "key": {KEY},
                "type": {TYPE}
            }

            IF EMPTY -> Not set -> Go to step 3

    Step 3: Send a post request to {SITE_URL}/api/set_key with the header
            {"Authorisation": "Token {INSERT_TOKEN_NO}"} and POST data:
            {
                "key": {KEY},
                "type": {TYPE}
            }

            If correct token and correct data -> HTTP_202 response.
                                         else -> HTTP_400 error.
            Repeat Step 2.
    """
    To_Be_Uploaded = Base_Folder
    client = requests.Session()
    payload = {'username': username, 'password': password}
    AuthKey = client.post('http://127.0.0.1:8000/api/login/', data=payload)
    algorithm = "AES"
    files = []
    encryptedFiles = []
    for (root, dirnames, filenames) in walk(To_Be_Uploaded):
        for name in filenames:
            files.append((name, (os.path.relpath(root, Base_Folder))))

    with tempfile.TemporaryDirectory() as directory:
        for file in files:
            print("Uploading File: " + file[0])
            file_path = file[1]
            tmpfile = os.path.join(directory,file[0])
            f = open(os.path.join(Base_Folder, file_path, file[0]), 'rb')
            md5sum1 = md5sum(f)
            f = open(os.path.join(Base_Folder, file_path, file[0]), 'rb')
            header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0')}
            print("The Token being sent as a header in POST: " + str(header))
            payloadUpload = {'file_path': file_path, 'md5sum': md5sum1,'filename': file[0],}
            file = {'file': f}
            r = client.post('http://127.0.0.1:8000/api/upload/', data=payloadUpload, files=file, headers=header)
            print("The received JSON file: " + r.text)
            print()


# rmdirCommand = "rm -rf " + Encypted_File_Path
# mkdirCommand = "mkdir " + Encypted_File_Path
# os.system(rmdirCommand)
# os.mkdir(os.path.join(To_Be_Uploaded,"."))


'''
def upload(login_URL,upload_URL,username,password,Base_Folder,To_Be_Uploaded):

    client = requests.Session()
    client.get(login_URL)
    csrftoken = client.cookies['csrftoken']

    payload = {
        'csrfmiddlewaretoken': csrftoken,
        'username': username,
        'password': password
    }
    files = []
    r = client.post(login_URL, data=payload, headers=dict(Referer=login_URL))

    client.get(upload_URL)
    csrftoken = client.cookies['csrftoken']
    for (root, dirnames, filenames) in walk(To_Be_Uploaded):
        for name in filenames:
            files.append((name, (os.path.relpath(root, Base_Folder))))

    for file in files:
        file_path = file[1]
        temp = open(os.path.join(Base_Folder, file_path, file[0]), 'rb')
        md5sum1 = md5sum(temp)
        payload = {
            'csrfmiddlewaretoken': csrftoken,
            'file_path': file_path,
            'md5sum': md5sum1,
        }
        f = {"file": open(os.path.join(Base_Folder,file_path,file[0]), 'rb')}
        r = client.post(upload_URL, data=payload, files=f, headers=dict(Referer=upload_URL))
        print('.',end='',flush=True)

    print('Completed')
    print("Upload Successfull")
'''

def set_url(parameter,url,out):
    with open(out) as f:
        data = json.load(f)
    data[parameter] = url
    with open(out, 'w') as outfile:
        json.dump(data, outfile)


def config_edit(out):
    with open(out) as f:
        data = json.load(f)
    data['username'] = input('Username : ')
    temp = getpass.getpass(prompt='Password : ', stream=None)
    temp1 = getpass.getpass(prompt='Confirm Password : ', stream=None)
    if (temp == temp1) :
        data['password'] = temp
    else :
        while (temp != temp1) :
            print ("The Passwords didn't match. Kindly try again.")
            temp = getpass.getpass(prompt='Password : ', stream=None)
            temp1 = getpass.getpass(prompt='Confirm Password : ', stream=None)
        data['password'] = temp
    print("Your configurations have been updated.")
    with open(out, 'w') as outfile:
        json.dump(data, outfile)


def empty_json(out):
    data = {}
    with open(out, 'w') as outfile:
        json.dump(data, outfile)

def sync(out):
    with open(out) as f:
        data = json.load(f)
    #upload(data['server_url']+'accounts/login/',data['server_url']+'upload/test/',data['username'],data['password'],data['home_dir'],data['home_dir'])
    upload2(data['username'],data['password'],data['home_dir'])


if (sys.argv[1] == 'config'):
    config_edit(sys.argv[2])
if (sys.argv[1] == 'set_server'):
    set_url('server_url',sys.argv[2],sys.argv[3])
if (sys.argv[1] == 'observe'):
    set_url('home_dir',sys.argv[2],sys.argv[3])
if (sys.argv[1] == 'sync'):
    sync(sys.argv[2])
if (sys.argv[1] == 'empty_json'):
    empty_json(sys.argv[2])