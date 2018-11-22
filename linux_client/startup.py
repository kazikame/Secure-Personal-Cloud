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
from encryption import *
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
import logging
import re
import cgi
import urllib.parse as urlp
import pathlib

sys.path.append('.')
import conflicts

# CONFIG OPTIONS
config_file = 'conf.json'

# Log Settings
logging.basicConfig(filename='SPC.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


if len(sys.argv) == 1:
    print("Secure Personal Cloud.")
    print("Team name: import teamName")
    # TODO: Add Argparse
    exit(0)


class AuthenticationException(Exception):
    pass


class NoHomeDirException(Exception):
    pass


def sync():
    try:
        server_url = get_server_url()
        AuthKey = check_user_pass(server_url)
        home_dir = check_home_dir()
        [upload, download, delete] = conflicts.resolve_conflicts(get_index(server_url, AuthKey), home_dir)
    except requests.exceptions.ConnectionError as e:
        logging.exception(e)
        print("error: The server isn't responding. To change/set the server url, use\n\nspc server set_url <url:port>")
        exit(-1)
    except NoHomeDirException as e:
        logging.exception(e)
        print("error: Invalid home directory. Please point to a valid home directory using:\n\nspc observe <home-dir>")
        exit(-1)
    del_bool = delete_files(server_url, AuthKey, delete)
    print(download)
    down_bool = download_files(server_url, AuthKey, download, home_dir)
    up_bool = upload_files(server_url, AuthKey, home_dir, upload)

    if (delete and del_bool) and (download and down_bool) and (upload and up_bool):
        print('Sync Successful')
    elif not (delete and download and upload):
        pass
    else:
        print('Sync Unsuccessful. Check SPC.logs for more details.')


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


def set_url(parameter,url,out):
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
    if 'home_dir' not in data or data['home_dir']=='':
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


def config_edit(server_url = None):
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
    while temp != temp1 :
        print ("The Passwords didn't match. Kindly try again.")
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


def upload_files(server_url, AuthKey, home_dir, files):
    """
    Main Upload function.

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
    if len(files) == 0:
        return
    client = requests.Session()
    algorithm = "AES"
    encryptedFiles = []

    size = 0
    upload_success = 0
    upload_failed = 0
    md5fail = 0

    retryUploads = []
    for i in files:
        size += os.path.getsize(os.path.join(home_dir, i))
    global pbar
    pbar = tqdm(total=size*1.003, ncols=80, unit='B', unit_scale=True, unit_divisor=1024)
    num = len(files)
    with tempfile.TemporaryDirectory() as directory:
        for file in files:
            file_path = os.path.split(file)[0]
            filename = os.path.split(file)[1]
            tmpfile = os.path.join(directory, filename)

            f = open(os.path.join(home_dir, file_path, filename), 'rb')
            md5sum1 = md5sum(f)

            f = open(os.path.join(home_dir, file_path, filename), 'rb')

            payloadUpload = MultipartEncoder(fields={'file_path': file_path, 'md5sum': md5sum1,
                                                     'file': (filename, f, 'application/octet-stream')})
            header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0'),
                      'Content-Type': payloadUpload.content_type, 'num': str(num)}
            global completed
            completed = 0
            monitor = MultipartEncoderMonitor(payloadUpload, progress_update)
            r = client.post(urlp.urljoin(server_url, 'api/upload/'), data=monitor,  headers=header)
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

    tqdm.write('\nUploaded ' + str(upload_success) + ' file(s) successfully. ' + str(upload_failed) + ' upload(s) failed.\nCheck SPC.logs for more details.')
    if md5fail > 0:
        i = input(str(md5fail) + 'files uploaded incorrectly, would you like to retry sync? (MD5 checksum fail) [Y/n]')
        if i == 'y' or i == 'Y':
            upload_files(server_url, AuthKey, home_dir, retryUploads)
        else:
            return False
    else:
        return True


def download_files(server_url, AuthKey, file_list, home_dir):
    """
    Utility to download files from cloud.

    :param server_url:
    :param AuthKey: Authentication Token
    :param file_list: List of (relative) file (paths) to be downloaded
    """

    if len(file_list) == 0:
        return
    client = requests.Session()
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0'), }
    retryDownloads = []
    for f in file_list:
        split_path = os.path.split(f)
        payLoad = {'file_path': split_path[0], 'name': split_path[1]}
        r = client.post(urlp.urljoin(server_url,'api/download/'), data=payLoad, headers=header, stream=True)
        values, params = cgi.parse_header(r.headers['Content-Disposition'])
        [filename, md5] = params['filename'].split('```')
        pathlib.Path(os.path.split(os.path.join(home_dir, filename))[0]).mkdir(parents=True, exist_ok=True)
        print(os.path.join(home_dir, filename))
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


def empty_json():
    data = {}
    with open(config_file, 'w') as outfile:
        json.dump(data, outfile)


def delete_files(server_url, AuthKey, file_list):
    if len(file_list) == 0:
        return
    client = requests.Session()
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0')}
    name_list = []
    for i in range(0, len(file_list)):
        split_path = os.path.split(file_list[i])
        file_list[i] = split_path[0]
        name_list.append(split_path[1])

    payloadDelete = {'file_path': '```'.join(file_list), 'name_list': '```'.join(name_list)}
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
        index_dict[i['file_path']] = i['md5sum']
    return index_dict


def get_status():
    try:
        server_url = get_server_url()
        AuthKey = check_user_pass(server_url)
        home_dir = check_home_dir()
        [upload, download, delete] = conflicts.resolve_conflicts(get_index(server_url, AuthKey), home_dir)
    except requests.exceptions.ConnectionError as e:
        logging.exception(e)
        print("error: The server isn't responding. To change/set the server url, use\n\nspc server set_url <url:port>")
        exit(-1)
    print('Current directory being observed: ' + home_dir)
    if upload or download or delete:
        print('Your local directory is not in sync with the cloud. To sync, use \n\nspc sync')


if len(sys.argv) > 1:
    if sys.argv[1] == 'config':
        config_edit()
    elif sys.argv[1] == 'set_server':
        set_url('server_url', sys.argv[2], config_file)
    elif sys.argv[1] == 'observe':
        set_home_dir('home_dir', sys.argv[2], config_file)
    elif sys.argv[1] == 'sync':
        sync()
    elif sys.argv[1] == 'empty_json':
        empty_json()
    elif sys.argv[1] == 'status':
        get_status()
