#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time
from conflicts import uploadall
from cloud_dict import get_cloud_dict, get_local_dict,upload

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
        upload(uploadall(cloud_dict,local_dir))
        sleep(86,400)

Daemon()
