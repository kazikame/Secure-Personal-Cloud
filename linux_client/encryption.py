
import os
import tempfile


def encryptFile(algorithm, keyFile, fpath, encfpath):

    encryptFileCommand = "java FileEncrypt {0} {1} {2} {3} {4}"
    command = encryptFileCommand.format(algorithm, "encrypt", keyFile, fpath, encfpath)
    os.system(command)
    return True


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
    :return: void
    """
    with tempfile.TemporaryDirectory as d:
        tempKey = os.path.join(d,"temp.key")
        decryptKey(keyFile, oldpass, tempKey)
        encryptKey(tempKey, newpass, keyFile)