import json
import getpass
import requests
import sys
import os
from os import walk
import hashlib
from functools import partial
import tempfile

def upload2(username, password, filePath):
    client = requests.Session()
    payload = {'username': username, 'password': password}
    AuthKey = client.post('http://127.0.0.1:8000/api/login/', data=payload)
    print(AuthKey.json())
    f = open(filePath, 'rb')
    header = {'Authorization': 'Token ' + AuthKey.json().get('key', '0')}
    print(header)
    payloadUpload = {'file_path': "", 'md5sum': "10283129038",}
    file = {'file': f}
    r = client.post('http://127.0.0.1:8000/api/upload/', data=payloadUpload, files=file, headers=header)
    print(r.text)


upload2('saksham47', 'RaBBit^7(9', '/home/saksham/Desktop/test.cpp')