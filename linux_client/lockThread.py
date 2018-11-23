import threading
import time
import requests
import logging

logging.basicConfig(filename='SPC.patch.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class LockUpdate (threading.Thread):
    def __init__(self, server_url, AuthKey, token, update_time):
        threading.Thread.__init__(self)
        self.server_url = server_url
        self.AuthKey = AuthKey
        self.token = token
        self.update_time = update_time
        self.kill = threading.Event()

    def run(self):
        client = requests.Session()
        header = {'Authorization': 'Token ' + self.AuthKey.json().get('key', '0'), }
        urlPatch = self.server_url + '/api/lock_tokens/' + self.token
        r = requests.Response()
        try:
            while not self.kill.is_set():
                r = client.patch(urlPatch, headers=header)
                r.raise_for_status()
                time.sleep(self.update_time)
        except requests.exceptions.HTTPError as e:
            logging.warn(e)
        except Exception as e:
            logging.warn(e)

