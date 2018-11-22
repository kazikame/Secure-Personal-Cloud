import json
import getpass
import requests
import sys
import os
from os import walk
import hashlib
from functools import partial
import tempfile

publickeypath = "/home/yashs20/rsapublic.der"
privatekeypath = "/home/yashs20/rsaprivate.der"
To_Be_Uploaded = "/home/yashs20/Downloads/outlab5"
Copy_Path = "/home/yashs20/Downloads/outlab5decrypted"
encryptFileCommand = "java Main {0} {1} {2} {3} {4}"
# rmdirCommand = "rm -rf " + Encypted_File_Path
# mkdirCommand = "mkdir " + Encypted_File_Path
# os.system(rmdirCommand)
# os.mkdir(os.path.join(To_Be_Uploaded,"."))

with tempfile.TemporaryDirectory() as directory:
	
	for (root, dirnames, filenames) in walk(To_Be_Uploaded):
		tmppath = os.path.join(directory,os.path.relpath(root,To_Be_Uploaded))
		copypath = os.path.join(Copy_Path,os.path.relpath(root,To_Be_Uploaded))
		try:
			os.mkdir(tmppath)
			os.mkdir(copypath)
		except FileExistsError:
			pass
		for file in filenames:
			fpath = os.path.join(root,file)
			encfpath = os.path.join(tmppath,file)
			decpath = os.path.join(copypath,file)
			command = encryptFileCommand.format("RSA","encrypt",publickeypath,fpath,encfpath)
			os.system(command)
			command = encryptFileCommand.format("RSA","decrypt",privatekeypath,encfpath,decpath)
			os.system(command)


os.system("diff {0} {1}".format(To_Be_Uploaded,Copy_Path))