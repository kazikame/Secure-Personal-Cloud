
import os
import tempfile


def encrypt_file(algorithm, keyFile, fpath, encfpath):

    encryptFileCommand = "java FileEncrypt {0} {1} {2} {3} {4}"
    command = encryptFileCommand.format(algorithm, "encrypt", keyFile, fpath, encfpath)
    os.system(command)
    return True


def decrypt_key(encryptedKeyFile, password, decryptedFilePath):
    """
    :param encryptedKeyFile: str - complete path of encrypted key
    :param password: str
    :param decryptedFilePath: str - complete path to store decrypted key
    :return: void
    """
    command = "java KeyEncrypt {0} decrypt {1} {2}"
    os.system(command.format(password,encryptedKeyFile,decryptedFilePath))


def encrypt_key(decryptedKeyFile, password, encryptedFilePath):
    """
    :param decryptedKeyFile: str - complete path of encrypted key
    :param password: str
    :param encryptedFilePath: str - complete path to store decrypted key
    :return: void
    """
    command = "java KeyEncrypt {0} encrypt {1} {2}"
    os.system(command.format(password,decryptedKeyFile,encryptedFilePath))


def change_pass(keyFile,oldpass,newpass):
    """
    :param keyFile: str - path to current (encrypted) key file
    :param oldpass: str
    :param newpass: str
    :return: void
    """
    with tempfile.TemporaryDirectory as d:
        tempKey = os.path.join(d,"temp.key")
        decrypt_key(keyFile, oldpass, tempKey)
        encrypt_key(tempKey, newpass, keyFile)