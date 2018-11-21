#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time
from .conflicts import uploadall
from .startup import *

def Daemon():

    try:
        pid = os.fork()
        
        if pid > 0:
            os._exit(0)
            
    except OSError, error:
        print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror)
        os._exit(1)
        
    while (True):
        cloud_dict = get_cloud_dict();
        local_dir = get_local_dir();
        [upload,download,delete] = uploadall(startup.get_index(startup.server_url, startup.AuthKey), startup.home_dir)
        except requests.exceptions.ConnectionError as e:
        logging.exception(e)
        print("error: The server isn't responding. To change/set the server url, use\n\nspc server set_url <url:port>")
        exit(-1)
    except NoHomeDirException as e:
        logging.exception(e)
        print("error: Invalid home directory. Please point to a valid home directory using\n\nspc observe <home-dir>")
        exit(-1)
        startup.upload_files(startup.server_url,startup.AuthKey,startup.home_dir,upload)
        startup.delete_files(startup.server_url,startup.AuthKey,startup.home_dir,delete)
        sleep(86400)

Daemon()
