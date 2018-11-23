import getpass
import hashlib
import json
import os
import sys
import tempfile
from functools import partial
from os import path
from urllib.error import *
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
import logging
import re
import cgi
import urllib.parse as urlp
import pathlib
from encryption import encrypt_files, decrypt_files, generate_key
import pickle

sys.path.append('.')
import conflicts
from encryption import *
import lockThread

# CONFIG OPTIONS
config_file = 'conf.json'

# Log Settings
logging.basicConfig(filename='SPC.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


paramalgo, paramkey = 'encryption_schema', 'key'

if len(sys.argv) == 1:
    print("Secure Personal Cloud.")
    print("Team name: import teamName")
    exit(0)

def check_key(scheme,key):
    if (scheme == "AES"):
        if (len(key) != 64):
            return False
        try :
            int(key,16)
            return True
        except Exception as e:
            return False
    if (scheme == "TripleDES"):
        if (len(key) != 48):
            return False
        try :
            int(key,16)
            return True
        except Exception as e:
            return False

    if (scheme == "AES"):
        if (len(key) != 32):
            return False
        try :
            int(key,16)
            return True
        except Exception as e:
            return False
    pass


def check_iv(scheme,key):
    if (scheme == "AES"):
        if (len(key) != 32):
            return False
        try :
            int(key,16)
            return True
        except Exception as e:
            return False
    if (scheme == "TripleES"):
        if (len(key) != 16):
            return False
        try:
            int(key, 16)
            return True
        except Exception as e:
            return False
    pass


def set_key(paramalgo, paramkey):
    with open(config_file) as fhand:
        data = json.load(fhand)

    algoselected = input("Select an encryption schema (enter choice 1, 2, or 3)\n1. AES - The safest encryption we "
                         "got\n2. TripleDES - Another extremely secure schema\n3. RC4 - Internet tells me I can't "
                         "trust this for my life\n")
    if '1' in algoselected:
        data[paramalgo] = "AES"
        algoselected = "AES"
    elif '2' in algoselected:
        data[paramalgo] = "TripleDES"
        algoselected = "TripleDES"
    elif '3' in algoselected:
        data[paramalgo] = "RC4"
        algoselected = "RC4"
    inpu = input("Enter 'file' if you want to store the key in a file (recommended).\n"
                    "Enter 'print' if you want the key to be printed out to terminal (not recommended)\n")
    if inpu == "print":
        keyFile = None
    elif inpu == "file":
        keyFile = os.path.join(data["home_folder"], "key.key")
    else :
        print("Invalid Argument. Exiting...")
        exit(0)
    x = generate_key(algoselected, keyFile)
    if not x:
        print("Error generating key. Try again")
        exit(1)
    else:
        data[paramkey] = keyFile

    with open(config_file, 'w') as fhand:
        json.dump(data, fhand)
    return [data[paramalgo], data[paramkey]]


def store_key_file (file):
    with open(config_file) as fhand:
        data = json.load(fhand)
    if (data.get("encryption_schema") == None):
        print("Specify Encryption :")
        while (True):
            inp = input();
            if (inp == "AES" or inp == "TripleDES" or inp == "RC4"):
                break
            print("Invalid schema. Try again.")
        data["encryption_schema"] = inp
    keyFile = os.path.join(data["home_folder"], "key.key")
    with open(file,'rb') as f:
        key = pickle.load(f)
        if (key.get('key') == None):
            print ("Invalid File. Exiting...")
            exit(0)
        if (key.get('iv') == None and inp != "RC4"):
            print("Invalid File. Exiting...")
            exit(0)
    with open(keyFile,'wb') as fi:
        pickle.dump(key,fi)
    print("Key stored")
    return inp,keyFile
    pass


def store_key():
    with open(config_file) as fhand:
        data = json.load(fhand)
    keyFile = os.path.join(data["home_folder"], "key.key")
    if (data.get("encryption_schema")==None):
        print ("Specify Encryption :")
        while(True):
            inp = input();
            if (inp == "AES" or inp == "TripleDES" or inp == "RC4"):
                break
            print("Invalid schema. Try again.")
        data["encryption_schema"] = inp
    keyFile = os.path.join(data["home_folder"], "key.key")
    dict = {}
    while (True):
        print("Enter the key :")
        keydash = input()
        if (check_key(inp,keydash)):
            keydash = keydash.encode('utf-8')
            break
        else :
            print("Wrong key. Kindly Try again.")
    dict["key"] = keydash;
    if (inp != "RC4"):
        while (True):
            print("Enter the IV :")
            keydash = input()
            if (check_iv(inp,keydash)):
                keydash = keydash.encode('utf-8')
                break
            else :
                print("Wrong IV. Kindly Try again.")
    dict["iv"] = keydash;
    with open(keyFile,'wb') as fi:
        pickle.dump(dict,fi)
    print("Key stored")
    return inp,keyFile
    pass


def take_key():
    print("Specify Encryption : (One of AES, TripleDES, RC4)")
    while (True):
        inp = input();
        if (inp == "AES" or inp == "TripleDES" or inp == "RC4"):
            break
        print("Invalid schema. Try again.")
    encryption_schema = inp
    dict = {}
    while (True):
        print("Enter the key :")
        keydash = input()
        if (check_key(inp,keydash)):
            keydash = keydash.encode('utf-8')
            break
        else :
            print("Wrong key. Kindly Try again.")
    dict["key"] = keydash;
    if (inp != "RC4"):
        while (True):
            print("Enter the IV :")
            keydash = input()
            if (check_key(inp,keydash)):
                keydash = keydash.encode('utf-8')
                break
            else :
                print("Wrong IV. Kindly Try again.")
    dict["iv"] = keydash;
    return encryption_schema,dict


def new_user_key():
    ind = input("Do you wanna store the key? Yes or No :")
    if "Y" in ind.upper():
        dic = store_key()
        return dic
    elif "N" in ind.upper() :
        print("Specify Encryption : (One of AES, TripleDES, RC4)")
        while (True):
            inp = input();
            if (inp == "AES" or inp == "TripleDES" or inp == "RC4"):
                break
            print("Invalid schema. Try again.")
        return [inp,None]
    else:
        print ("Invalid Input. Try again.")
        new_user_key()
    pass


def get_en_key():
    data = {}
    with open(config_file) as f:
        try:
            data = json.load(f)
        except Exception as e:
            pass
    if ('encryption_schema' not in data):
        print("Are you an existing user(Do you have the encryption key?). Enter Yes or No :")
        while (True):
            i = input()
            if "Y" in i.upper():
                return new_user_key();
                break
            elif "N" in i.upper():
                return set_key('encryption_schema', 'key')
                break
    elif ('key' not in data):
        return [data['encryption_schema'],None]
    else:
        return [data['encryption_schema'], data['key']]


def change():
    with tempfile.TemporaryDirectory() as dir1:
        try:
            with open(config_file,'r') as fil:
                data = json.load(fil)
                if ('encryption_schema' not in data):
                    print ("set some schema first")
                    exit (0)
            server_url = get_server_url()
            AuthKey = check_user_pass(server_url)
            [schema, en_key] = get_en_key()
            token = check_if_unlocked(server_url, AuthKey)
            print("Sync locked successfully!")
            updateThread = lockThread.LockUpdate(server_url, AuthKey, token, 10)
            updateThread.setDaemon(True)
            updateThread.start()
            file_list = list((get_index(server_url, AuthKey)).keys())
            download_files(server_url, AuthKey,file_list, dir1, token, schema, en_key)
            with open(config_file, 'r') as fil:
                data = json.load(fil)
                del data['encryption_schema']
                home_key = data['key']
                del data['key']
        except requests.exceptions.HTTPError as e:
            logging.exception(e)
            print("error: Sync locked. Another user is using it, please try again later.")
            exit(0)
        except requests.exceptions.ConnectionError as e:
            logging.exception(e)
            print("error: The server isn't responding. To change/set the server url, use\n\nspc server set_url <url:port>")
            exit(-1)
        with open(config_file, 'w') as fil:
            json.dump(data, fil)
        while (True):
            ind = input("Do you wanna generate the key yourself? Enter Yes or No :")
            if "Y" in ind.upper():
                while (True):
                    id = input("Do you wanna store the key ? Enter Yes or No :")
                    if "Y" in id.upper():
                        schema,en_key = store_key()
                        with open(config_file, 'r') as fil:
                            data = json.load(fil)
                        data['encryption_schema'] = schema;
                        data['key'] = home_key;
                        with open(config_file, 'w') as fil:
                            json.dump(data, fil)
                        break
                    elif "N" in id.upper():
                        print("Specify Encryption : (One of AES, TripleDES, RC4)")
                        while (True):
                            schema = input()
                            if (schema == "AES" or schema == "TripleDES" or schema == "RC4"):
                                break
                            print("Invalid schema. Try again.")
                        en_key = None
                        with open(config_file, 'r') as fil:
                            data = json.load(fil)
                        data['encryption_schema'] = schema;
                        with open(config_file, 'w') as fil:
                            json.dump(data,fil)
                        break
                    else :
                        print("Try again")
                break
            elif "N" in ind.upper():
                schema, en_key = set_key('encryption_schema', 'key')
                break
        newlist = file_list[:]
        delete_files(server_url, AuthKey, file_list, token)
        upload_files(server_url, AuthKey, dir1, newlist, token, schema, en_key)
        unlock_sync(server_url, AuthKey, token)
    pass

# def change_file(dump_file):
#     print("To change key you first need to sync your files")
#     sync()
#     with open(config_file) as fhand:
#         data = json.load(fhand)
#     print("Enter the index(1-3) of the new Encryption schema:")
#     print("1. AES")
#     print("2. TripleDES")
#     print("3. RC4")
#     index = input();
#     if (index == 1):
#         data[paramalgo] == "AES"
#     elif (index == 2):
#         data[paramalgo] == "TripleDES"
#     elif (index == 3):
#         data[paramalgo] == "RC4"
#     else :
#         print("Invalid Index. Exiting...")
#         return;
#     os.remove('key.key')
#     if (data[paramalgo] == "AES" or data[paramalgo] == "TripleDES"):
#         print("Kindly verify your dump_file. It should be have 2 attributes, a key and a IV. Press 1 to exit, or anyother key to continue")
#         index = input()
#         if (index == "1"):
#             print("Exiting...")
#             return
#     else:
#         print("Kindly verify your dump_file. It should be have only attribute, a key. Press 1 to exit, or anyother key to continue")
#         index = input()
#         if (index == "1"):
#             print("Exiting...")
#             return
#     with open(dump_file,'rb') as file:
#         dict = pickle.load(file)
#     if (data.get(paramkey) == None):
#         data[paramkey] = os.path.join(data["home_folder"],'key.key');
#     with open(data[paramkey],'wb') as f:
#         pickle.dump(dict,f)
#     with open(config_file, 'w') as fhand:
#         json.dump(data, fhand)
#
#     server_url = get_server_url()
#     AuthKey = check_user_pass(server_url)
#     home_dir = check_home_dir()
#     [schema, en_key] = get_en_key()
#     token = check_if_unlocked(server_url, AuthKey)
#     delete = list((get_index(server_url, AuthKey)).keys())
#     delete_files(server_url, AuthKey, delete, token)
#     upload_files(server_url, AuthKey, home_dir, delete, token, schema, en_key)
#     print("Your new Encryption Scheme is now set")
#     pass

def print_key():
    with open(config_file) as fhand:
        data = json.load(fhand)
    if (data.get(paramkey) == None):
        print("No Key file. Exiting...")
        exit(0)
    with open(data[paramkey], 'rb') as f:
        oldkey = pickle.load(f)
        print ("Encryption Schema : "+data["encryption_schema"])
        for x in oldkey.keys():
            print (x)
            print (oldkey[x])
    pass

class AuthenticationException(Exception):
    pass


class NoHomeDirException(Exception):
    pass

def sync():
    try:
        server_url = get_server_url()
        AuthKey = check_user_pass(server_url)
        # print(AuthKey.text)
        home_dir = check_home_dir()
        [schema, en_key] = get_en_key()
        token = check_if_unlocked(server_url, AuthKey)
        print("Sync locked successfully!")
        updateThread = lockThread.LockUpdate(server_url, AuthKey, token, 10)
        updateThread.setDaemon(True)
        updateThread.start()
        [upload, download, delete] = conflicts.resolve_conflicts(get_index(server_url, AuthKey), home_dir)
    except requests.exceptions.HTTPError as e:
        logging.exception(e)
        print("error: Sync locked. Another user is using it, please try again later.")
        exit(0)
    except requests.exceptions.ConnectionError as e:
        logging.exception(e)
        print("error: The server isn't responding. To change/set the server url, use\n\nspc server set_url <url:port>")
        exit(-1)
    except NoHomeDirException as e:
        logging.exception(e)
        print("You have not set a home directory. Please point to a valid home directory using:\n\nspc observe <home-dir>")
        exit(-1)
    except ConnectionRefusedError as e:
        logging.exception(e)
        print("error: The server isn't responding. To change/set the server url, use\n\nspc server set_url <url:port>")
        exit(-1)
    del_bool = delete_files(server_url, AuthKey, delete, token)
    down_bool = download_files(server_url, AuthKey, download, home_dir,token,  schema, en_key)
    up_bool = upload_files(server_url, AuthKey, home_dir, upload, token, schema, en_key)

    if (delete and del_bool) and (download and down_bool) and (upload and up_bool):
        print('Sync Successful')
    elif not (delete and download and upload):
        pass
    else:
        print('Sync Unsuccessful. Check SPC.logs for more details.')

    f = unlock_sync(server_url, AuthKey, token)
    if f:
        tqdm.write('Sync unlocked successfully.')
    else:
        tqdm.write("Sync couldn't be unlocked for some reason.\nCheck SPC.logs for more details.")


def check_if_unlocked(server_url, AuthKey):
    client = requests.Session()
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0')}
    r = client.post(urlp.urljoin(server_url, 'api/lock_tokens/'), headers=header)
    if r.status_code == 404 or r.status_code == 403 or r.status_code == 409:
        raise requests.exceptions.HTTPError
    else:
        return r.json().get('token', 0)


def unlock_sync(server_url, AuthKey, token):
    client = requests.Session()
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0')}
    r = client.delete(urlp.urljoin(server_url, 'api/lock_tokens/' + token), headers=header)
    if not (r == 404 or r == 403):
        return True
    else:
        logging.warn(r.text)
        return False


def get_server_url():
    if not path.isfile(config_file):
        f = open(config_file, 'w')
        data = {'username': '', 'password': '', 'server_url': '', 'home_dir': ''}
        json.dump(data, f)

    with open(config_file, 'r') as f:
        data = json.load(f)
    if 'server_url' not in data or data['server_url'] == '':
        u = input('Input Server URL: ')
        u = set_url('server_url', u, config_file)
        return u
    else:
        return data['server_url']


def set_url(parameter, url, out):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    while True:
        if re.match(regex, url) is not None:
            with open(out) as f:
                data = json.load(f)
                data[parameter] = url
            with open(out, 'w') as outfile:
                json.dump(data, outfile)
            break
        else:
            url = input("Invalid URL. Please enter a valid server URL: ")

    return url


def check_user_pass(server_url):
    if not path.isfile(config_file):
        f = open(config_file, 'w')
        data = {'username': '', 'password': '', 'server_url': '', 'home_dir': ''}
        json.dump(data, f)

    data = {}
    with open(config_file) as f:
        try:
            data = json.load(f)
        except Exception as e:
            pass
    if ('username' not in data or data['username'] == '') or ('password' not in data or data['password'] == ''):
        f.close()
        return config_edit(server_url)
    else:
        try:
            AuthKey = get_auth_key(server_url, data['username'], data['password'])
            return AuthKey
        except AuthenticationException as e:
            logging.exception(e)
            print("Username/Password incorrect. Please input the correct credentials")
            return config_edit(server_url)


def check_home_dir():
    with open(config_file) as f:
        data = json.load(f)
    if 'home_dir' not in data or data['home_dir'] == '':
        raise NoHomeDirException
    elif not os.path.isdir(data['home_dir']):
        raise NoHomeDirException
    else:
        return data['home_dir']


def get_auth_key(server_url, username, password):
    client = requests.Session()
    payload = {'username': username, 'password': password}
    AuthKey = client.post(urlp.urljoin(server_url, 'api/login/'), data=payload)
    if AuthKey is None or AuthKey.json().get('key', '0') == '0':
        raise AuthenticationException
    else:
        return AuthKey

def config_edit(server_url=None):
    data = {}
    with open(config_file) as f:
        try:
            data = json.load(f)
        except Exception as e:
            pass
    if server_url is None:
        server_url = get_server_url()
    data['username'] = input('Username : ')
    temp = getpass.getpass(prompt='Password : ', stream=None)
    temp1 = getpass.getpass(prompt='Confirm Password : ', stream=None)
    while temp != temp1:
        print("The Passwords didn't match. Kindly try again.")
        temp = getpass.getpass(prompt='Password : ', stream=None)
        temp1 = getpass.getpass(prompt='Confirm Password : ', stream=None)
    data['password'] = temp
    with open(config_file, 'w') as outfile:
        json.dump(data, outfile)
    username = data['username']
    password = data['password']

    try:
        AuthKey = get_auth_key(server_url, username, password)
        print("Authorization credentials successfully updated.")
        return AuthKey
    except AuthenticationException as e:
        logging.exception(e)
        print("Username/Password incorrect. Please input the correct credentials")
        return config_edit(server_url)


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


def upload_files(server_url, AuthKey, home_dir, files, token, algorithm="AES", key_file=None):
    """
    Main Upload function.

    :param key_file:
    :param algorithm:
    :param files: list of file path strings relative to home_dir
    :param home_dir: base dir
    :param AuthKey: string
    :param server_url: string
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
    # Return if no files to be uploaded
    if len(files) == 0:
        return

    # Make request client
    client = requests.Session()

    # Initialize Default var
    size = 0
    upload_success = 0
    upload_failed = 0
    md5fail = 0
    retryUploads = []
    num = len(files)
    with tempfile.TemporaryDirectory() as directory:
        encrypt_files(algorithm, home_dir, directory, files, key_file)
        old_home = home_dir
        home_dir = directory
        for i in files:
            size += os.path.getsize(os.path.join(home_dir, i))
        global pbar
        pbar = tqdm(total=size * 1.003, ncols=80, unit='B', unit_scale=True, unit_divisor=1024)
        for file in files:
            file_path = os.path.split(file)[0]
            filename = os.path.split(file)[1]

            # Get MD5 of encrypted file
            f = open(os.path.join(home_dir, file_path, filename), 'rb')
            md5sum1 = md5sum(f)
            f.close()

            # Get MD5 of original file
            f_orig = open(os.path.join(old_home, file_path, filename), 'rb')
            md5sum_orig = md5sum(f_orig)
            f_orig.close()

            # File to be uploaded
            f = open(os.path.join(home_dir, file_path, filename), 'rb')

            # Payload
            payloadUpload = MultipartEncoder(fields={'file_path': file_path,
                                                     'md5sum': md5sum1,
                                                     'md5sum_o': md5sum_orig,
                                                     'file': (filename, f, 'application/octet-stream'),
                                                     'token': token})

            # Header
            header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0'),
                      'Content-Type': payloadUpload.content_type, 'num': str(num)}

            # Progress Bar stuff
            global completed
            completed = 0
            monitor = MultipartEncoderMonitor(payloadUpload, progress_update)

            # Response received
            r = client.post(urlp.urljoin(server_url, 'api/upload/'), data=monitor, headers=header)
            if r.status_code == 201:
                upload_success += 1
                tqdm.write(filename + ' uploaded')
            elif r.status_code == 406:
                upload_failed += 1
                md5fail += 1
                retryUploads.append(file)
                logging.warn(r.text)
                tqdm.write(filename + ' failed md5 checksum')
            else:
                upload_failed += 1
                tqdm.write(filename + ' failed to upload')
                logging.warn(r.text)
            num -= 1

    tqdm.write('\nUploaded ' + str(upload_success) + ' file(s) successfully. ' + str(upload_failed) + ' upload(s) failed.')
    if md5fail > 0:
        i = input(str(md5fail) + 'files uploaded incorrectly, would you like to retry sync? (MD5 checksum fail) [Y/n]')
        if i == 'y' or i == 'Y':
            upload_files(server_url, AuthKey, home_dir, retryUploads)
        else:
            return False
    elif upload_failed > 0:
        return False
    else:
        return True


def download_files(server_url, AuthKey, file_list, home_dir, token, algorithm="AES", key_file=None):
    """
    Utility to download files from cloud.
    :param key_file:
    :param algorithm: AES / TripleDES
    :param home_dir:
    :param server_url:
    :param AuthKey: Authentication Token
    :param file_list: List of (relative) file (paths) to be downloaded
    """

    # Return if no files
    if len(file_list) == 0:
        return

    # Make a request client
    client = requests.Session()
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0'), }
    retryDownloads = []
    old_dir = home_dir
    with tempfile.TemporaryDirectory() as tempdir:
        for f in file_list:
            split_path = os.path.split(f)

            payLoad = {'file_path': split_path[0], 'name': split_path[1], 'token': token}
            r = client.post(urlp.urljoin(server_url,'api/download/'), data=payLoad, headers=header, stream=True)

            values, params = cgi.parse_header(r.headers['Content-Disposition'])

            md5 = params['filename']
            filename = f

            pathlib.Path(os.path.split(os.path.join(home_dir, filename))[0]).mkdir(parents=True, exist_ok=True)
            print(os.path.join(home_dir, filename))

            if not os.path.isdir(os.path.dirname(os.path.join(tempdir, f))):
                pathlib.Path(os.path.dirname(os.path.join(tempdir, f))).mkdir(parents=True, exist_ok=True)


            home_dir = tempdir
            with open(os.path.join(home_dir, filename), 'wb') as xx:
                for chunk in r.iter_content(chunk_size=8192):
                    xx.write(chunk)

            with open(os.path.join(home_dir, filename), 'rb') as ff:
                md5c = md5sum(ff)
                if md5c != md5:
                    print(filename + ' failed MD5 checksum.')
                    retryDownloads.append(f)
                else:
                    print(filename + ' downloaded successfully.')
        newfilelist = [f for f in file_list if f not in retryDownloads]
        decrypt_files(algorithm, home_dir, old_dir, newfilelist, key_file)

    if len(retryDownloads) > 0:
        i = input(str(len(retryDownloads)) + ' failed MD5 checksum. Would you like to try to re-download them? [Y/n]: ')
        if i == 'y' or i == 'Y':
            download_files(server_url, AuthKey, retryDownloads, home_dir)
        else:
            return False
    else:
        return True


def set_home_dir(parameter, dir, out):
    if os.path.exists(dir):
        with open(out) as f:
            data = json.load(f)
        data[parameter] = dir
        with open(out, 'w') as outfile:
            json.dump(data, outfile)
    else:
        print("Directory doesn't exist!")
        exit(-1)



def empty_json(home_folder):
    data = {"home_folder":home_folder}
    with open(config_file, 'w') as outfile:
        json.dump(data, outfile)

def delete_files(server_url, AuthKey, file_list, token):
    if len(file_list) == 0:
        return
    client = requests.Session()
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0')}
    name_list = []
    for i in range(0, len(file_list)):
        split_path = os.path.split(file_list[i])
        file_list[i] = split_path[0]
        name_list.append(split_path[1])

    payloadDelete = {'file_path': '```'.join(file_list), 'name_list': '```'.join(name_list), 'token': token}
    try:
        r = client.post(urlp.urljoin(server_url, 'api/delete/'), data=payloadDelete, headers=header)
        if r.status_code == 200:
            print('Deleted ' + str(len(file_list)) + ' file(s) on the cloud successfully.')
        else:
            print('Delete on cloud unsuccessful. Check logs for more details.')
            logging.warn(r.text)
            return False
    except HTTPError as e:
        logging.exception(e.strerror)
        return False
    return True


def get_index(server_url, AuthKey):
    """
    Returns ALL the filenames of the user and their md5sums
    """
    client = requests.Session()
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0')}
    r = client.post(urlp.urljoin(server_url, 'api/get-index/'), headers=header)

    if r.status_code == 400:
        print('Account already in use by some other client. Please try again later.')
        exit(0)
    index_dict = {}
    for i in r.json()['index']:
        index_dict[i['file_path']] = i['md5sum_o']
    return index_dict


def status ():
    server_url = get_server_url()
    AuthKey = check_user_pass(server_url)
    home_dir = check_home_dir()
    [modified, unmodified, cloud,local] = conflicts.get_status(get_index(server_url, AuthKey), home_dir)
    print ("You have "+str(len(modified))+" modified files on the local directory along with "+str(len(local))+" new files and "+str(len(cloud))+" deleted files")
    if (len(modified)>0):
        print ("Modified: ")
        for x in modified:
            print ("\t"+x)
    if (len(cloud)>0):
        print ("Deleted: ")
        for x in cloud:
            print("\t"+x)
    if (len(local)>0):
        print ("New: ")
        for x in local:
            print("\t"+x)
    pass



if len(sys.argv) > 1 and len(sys.argv) < 3:
    if sys.argv[1] == 'config':
        config_edit()
    elif sys.argv[1] == 'set_server':
        set_url('server_url', sys.argv[2], config_file)
    elif sys.argv[1] == 'observe':
        set_home_dir('home_dir', sys.argv[2], config_file)
    elif sys.argv[1] == 'sync':
        sync()
    elif sys.argv[1] == 'print_key':
        print_key()
    elif sys.argv[1] == 'store_key_file':
        store_key_file(sys.argv[2])
    elif sys.argv[1] == 'store_key':
        store_key()
    elif sys.argv[1] == 'empty_json':
        empty_json(sys.argv[2])
    elif sys.argv[1] == 'generate_key':
        set_key('encryption_schema', 'key')
    elif sys.argv[1] == 'change_key':
        change()
    # elif sys.argv[1] == 'change_file':
    #     change_file(sys.argv[2])
    elif sys.argv[1] == 'status':
        status()
    elif sys.argv[1] == 'server':
        print(get_server_url())
else:
    print('Invalid number of arguments.')
    exit(-1)

