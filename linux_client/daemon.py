#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time
from startup import *

def Daemon():

    try:
        pid = os.fork()
        
        if pid > 0:
            os._exit(0)
            
    except OSError, error:
        print ('Unable to fork. Error: %d (%s)' % (error.errno, error.strerror))
        os._exit(1)
        
    while (True):
        startup.uploadlocal();
        sleep(86400)

Daemon()
