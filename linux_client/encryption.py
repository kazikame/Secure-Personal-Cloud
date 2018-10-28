import os
import tempfile


def encryptFiles(algorithm, keyFile, toBeUploaded, tempDirectory):
    """
    :param algorithm: str - AES/TripleDES/Blowfish
    :param keyFile: str - complete path to decrypted key file
    :param toBeUploaded: str - folder of decrypted files
    :param tempDirectory: str - folder to store encrypted files
    :return: list - encrypted files of tuple objects (name,relpath)
    """
    encryptedFiles = []
    encryptFileCommand = "java FileEncrypt {0} {1} {2} {3} {4}"
    for (root, dirnames, filenames) in os.walk(toBeUploaded):
        tmppath = os.path.join(tempDirectory, os.path.relpath(root, toBeUploaded))
        # copypath = os.path.join(Copy_Path,os.path.relpath(root,To_Be_Uploaded))
        try:
            os.mkdir(tmppath)
            # os.mkdir(copypath)
        except FileExistsError:
            pass
        for file in filenames:
            fpath = os.path.join(root, file)
            encfpath = os.path.join(tmppath, file)
            # decpath = os.path.join(copypath,file)
            command = encryptFileCommand.format(algorithm, "encrypt", keyFile, fpath, encfpath)
            os.system(command)
            encryptedFiles.append((file, (os.path.relpath(root, toBeUploaded))))
    return encryptedFiles


def decryptKey(encryptedKeyFile, password, decryptedFilePath):
    """
    :param encryptedKeyFile: str - complete path of encrypted key
    :param password: str
    :param decryptedFilePath: str - complete path to store decrypted key
    :return: void
    """
    command = "java KeyEncrypt {0} decrypt {1} {2}"
    os.system(command.format(password,encryptedKeyFile,decryptedFilePath))


def encryptKey(decryptedKeyFile, password, encryptedFilePath):
    """
    :param decryptedKeyFile: str - complete path of encrypted key
    :param password: str
    :param encryptedFilePath: str - complete path to store decrypted key
    :return: void
    """
    command = "java KeyEncrypt {0} encrypt {1} {2}"
    os.system(command.format(password,decryptedKeyFile,encryptedFilePath))


def changePass(keyFile,oldpass,newpass):
    """
    :param keyFile: str - path to current (encrypted) key file
    :param oldpass: str
    :param newpass: str
    :return: 
    """
    with tempfile.TemporaryDirectory as d:
        tempKey = os.path.join(d,"temp.key")
        decryptKey(keyFile, oldpass, tempKey)
        encryptKey(tempKey, newpass, keyFile)