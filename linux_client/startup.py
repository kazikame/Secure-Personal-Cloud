import getpass
import hashlib
import json
import os
import sys
import tempfile
from functools import partial
from os import walk, path
from urllib.error import *
import requests
from encryption import *
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

# CONFIG OPTIONS
config_file = 'conf.json'
AuthKey = None
username = ''           # Don't change.
password = ''           # Don't change.
server_url = ''         # Don't change.

if len(sys.argv) == 1:
    print("Secure Personal Cloud.")
    print("Team name: import teamName")
    # TODO: Add Argparse
    exit(0)


def get_auth_key():
    client = requests.Session()
    payload = {'username': username, 'password': password}
    global AuthKey
    AuthKey = client.post(server_url + 'api/login/', data=payload)
    if AuthKey.json().get('key', '0') == '0':
        return False
    else:
        return True


def config_edit():
    data = {}
    with open(config_file) as f:
        try:
            data = json.load(f)
        except Exception as e:
            pass
    data['username'] = input('Username : ')
    temp = getpass.getpass(prompt='Password : ', stream=None)
    temp1 = getpass.getpass(prompt='Confirm Password : ', stream=None)
    while temp != temp1 :
        print ("The Passwords didn't match. Kindly try again.")
        temp = getpass.getpass(prompt='Password : ', stream=None)
        temp1 = getpass.getpass(prompt='Confirm Password : ', stream=None)
    data['password'] = temp
    with open(config_file, 'w') as outfile:
        json.dump(data, outfile)
    global username
    username = data['username']
    global password
    password = data['password']

    if get_auth_key():
        print("Authorization credentials successfully updated.")
    else:
        print("Username/Password incorrect. Please input the correct credentials")
        config_edit()


if not path.isfile(config_file):
    f = open(config_file, 'w')
    data = {'username': '', 'password': '', 'server_url': '', 'home_dir': ''}
    json.dump(data, f)

with open(config_file, 'r') as f:
    data = {}
    try:
        data = json.load(f)
    except Exception as e:
        pass
    if 'server_url' not in data or data['server_url'] == '':
        data['server_url'] = 'http://127.0.0.1:8000/'
        f.close()
        with open(config_file, 'w') as f:
            json.dump(data, f)
    server_url = data['server_url']


with open(config_file, 'r') as f:
    data = {}
    try:
        data = json.load(f)
    except Exception as e:
        pass
    if ('username' not in data or data['username'] == '') or ('password' not in data or data['password'] == ''):
        f.close()
        config_edit()
    else:
        username = data['username']
        password = data['password']

if not AuthKey:
    if get_auth_key():
        pass
    else:
        print("Username/Password incorrect. Please input the correct credentials")
        config_edit()


def md5sum(f):
    d = hashlib.md5()
    for buf in iter(partial(f.read, 128), b''):
        d.update(buf)
    return d.hexdigest()


pbar = None


completed = 0
def progress_update(monitor):
    global completed
    pbar.update(monitor.bytes_read - completed)
    completed = monitor.bytes_read


def upload2(Base_Folder):
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
    algorithm = "AES"
    files = []
    encryptedFiles = []
    size = 0
    upload_success = 0
    upload_failed = 0
    for (root, dirnames, filenames) in walk(To_Be_Uploaded):
        for name in filenames:
            files.append((name, (os.path.relpath(root, Base_Folder))))
            size += os.path.getsize(os.path.join(Base_Folder, root, name))
    global pbar
    pbar = tqdm(total=size*1.003, ncols=80, unit='B', unit_scale=True, unit_divisor=1024)
    with tempfile.TemporaryDirectory() as directory:
        for file in files:
            file_path = file[1]
            tmpfile = os.path.join(directory, file[0])

            f = open(os.path.join(Base_Folder, file_path, file[0]), 'rb')
            md5sum1 = md5sum(f)

            f = open(os.path.join(Base_Folder, file_path, file[0]), 'rb')

            payloadUpload = MultipartEncoder(fields={'file_path': file_path, 'md5sum': md5sum1,
                                                     'file': (file[0], f, 'application/octet-stream')})
            header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0'),
                      'Content-Type': payloadUpload.content_type}
            global completed
            completed = 0
            monitor = MultipartEncoderMonitor(payloadUpload, progress_update)
            r = client.post(server_url + 'api/upload/', data=monitor,  headers=header)
            if (r.status_code == 201):
                upload_success +=1
            else:
                upload_failed +=1

    tqdm.write('Uploaded ' + str(upload_success) + ' files successfully. ' + str(upload_failed) + ' uploads failed.')


def set_url(parameter,url,out):
    with open(out) as f:
        data = json.load(f)
    data[parameter] = url
    with open(out, 'w') as outfile:
        json.dump(data, outfile)


def empty_json():
    data = {}
    with open(config_file, 'w') as outfile:
        json.dump(data, outfile)


def sync(out):
    with open(out) as f:
        data = json.load(f)
    if 'home_dir' not in data or data['home_dir']=='':
        print("No directory being observed.")
        exit(-1)
    upload2(data['home_dir'])


def delete_files(file_list, md5_list):
    client = requests.Session()
    print(AuthKey.text)
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0')}
    payloadDelete = {'file_path': ','.join(file_list), 'md5sum': ','.join(md5_list)}
    print(payloadDelete)

    try:
        r = client.post(server_url + 'api/delete/', data=payloadDelete, headers=header)
        print(r.text)
        r.raise_for_status()

    except HTTPError as e:
        print(e.strerror)


def get_index():
    """
    Returns ALL the filenames of the user and their md5sums
    """
    client = requests.Session()
    print(AuthKey.text)
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0')}
    r = client.post(server_url + 'api/get-index/', headers=header)
    print(r.json())


if sys.argv[1] == 'config':
    config_edit()
if sys.argv[1] == 'set_server':
    set_url('server_url',sys.argv[2],config_file)
if sys.argv[1] == 'observe':
    set_url('home_dir', sys.argv[2], config_file)
if sys.argv[1] == 'sync':
    sync(config_file)
if sys.argv[1] == 'empty_json':
    empty_json(config_file)
