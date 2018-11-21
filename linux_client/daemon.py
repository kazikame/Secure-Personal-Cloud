#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time
<<<<<<< HEAD
from startup import *
=======
import startup
>>>>>>> d6f52b35a1d07ae0fbde8d9a04fc4ba09ccd6a32

def Daemon():

    try:
        pid = os.fork()
        
        if pid > 0:
            os._exit(0)
            
    except OSError, error:
        print ('Unable to fork. Error: %d (%s)' % (error.errno, error.strerror))
        os._exit(1)
        
    while (True):
        startup.uploadlocal()
        sleep(86400)

Daemon()
