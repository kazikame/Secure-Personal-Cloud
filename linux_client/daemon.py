#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from time import sleep

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


class AuthenticationException(Exception):
    pass


class NoHomeDirException(Exception):
    pass


def uploadlocal():
    try:
        server_url = get_server_url()
        AuthKey = check_user_pass(server_url)
        home_dir = check_home_dir()
        [upload, download, delete] = conflicts.uploadall(get_index(server_url, AuthKey), home_dir)
    except requests.exceptions.ConnectionError as e:
        logging.exception(e)
        exit(-1)
    except NoHomeDirException as e:
        logging.exception(e)
        exit(-1)
    del_bool = delete_files(server_url, AuthKey, delete)
    up_bool = upload_files(server_url, AuthKey, home_dir, upload)



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
        temp = getpass.getpass(prompt='Password : ', stream=None)
        temp1 = getpass.getpass(prompt='Confirm Password : ', stream=None)
    data['password'] = temp
    with open(config_file, 'w') as outfile:
        json.dump(data, outfile)
    username = data['username']
    password = data['password']

    try:
        AuthKey = get_auth_key(server_url, username, password)
        return AuthKey
    except AuthenticationException as e:
        logging.exception(e)
        return config_edit(server_url)


def md5sum(f):
    d = hashlib.md5()
    for buf in iter(partial(f.read, 128), b''):
        d.update(buf)
    return d.hexdigest()


def upload_files(server_url, AuthKey, home_dir, files):
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
    if len(files) == 0:
        return
    client = requests.Session()
    algorithm = "AES"
    encryptedFiles = []

    size = 0
    upload_success = 0
    upload_failed = 0
    md5fail = 0

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
                      'Content-Type': payloadUpload.content_type}
            global completed
            completed = 0
            monitor = MultipartEncoderMonitor(payloadUpload)
            r = client.post(urlp.urljoin(server_url, 'api/upload/'), data=monitor,  headers=header)
            if r.status_code == 201:
                upload_success += 1
            elif r.status_code == 406:
                upload_failed += 1
                md5fail += 1
                logging.warn(r.text)
            else:
                upload_failed += 1
                logging.warn(r.text)
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
        with open(os.path.join(home_dir, filename), 'wb') as ff:
            for chunk in r.iter_content(chunk_size=8192):
                ff.write(chunk)
        with open(os.path.join(home_dir, filename), 'rb') as ff:
            if md5sum(ff) != md5:
                retryDownloads.append(f)
            else:
                pass
    return True


def set_home_dir(parameter, dir, out):
    if os.path.exists(dir):
        with open(out) as f:
            data = json.load(f)
        data[parameter] = dir
        with open(out, 'w') as outfile:
            json.dump(data, outfile)
    else:
        exit(-1)


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
            pass
        else:
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
    index_dict = {}
    for i in r.json()['index']:
        index_dict[i['file_path']] = i['md5sum']
    return index_dict


def Daemon():
    try:
        pid = os.fork()

        print(pid)
        if pid > 0:
            os._exit(0)

    except OSError as error:
        os._exit(1)

    while True:
        uploadlocal()
        sleep(86400)

Daemon()