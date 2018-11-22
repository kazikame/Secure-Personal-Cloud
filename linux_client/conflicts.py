import os, hashlib
from os import walk


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def delete(base, files):
    for x in files:
        os.remove(os.path.join(base, x))


def uploadall(cloud_dict, local_dir):
    local_dict = {}
    for (root, dirnames, filenames) in walk(local_dir):
        for name in filenames:
            md5e = md5(os.path.join(root, name))
            local_dict[os.path.join(os.path.relpath(root, local_dir), name)] = md5e
    if local_dict == cloud_dict:
        return [[], [], []]
    else:

        only_cloud = []
        only_local = []
        modified = []
        unmodified = []

        for x in cloud_dict.keys():
            if local_dict.get(x) is None:
                only_cloud.append(x)
            elif local_dict[x] != cloud_dict[x]:
                modified.append(x)
            else:
                unmodified.append(x)

        for x in local_dict.keys():
            if cloud_dict.get(x) == None:
                only_local.append(x)
        return [only_local+modified, [], only_cloud+modified]

def status(cloud_dict, local_dir):
    local_dict = {}
    for (root, dirnames, filenames) in walk(local_dir):
        for name in filenames:
            md5e = md5(os.path.join(root, name))
            local_dict[os.path.join(os.path.relpath(root, local_dir), name)] = md5e
    if local_dict == cloud_dict:
        return [[], local_dict.keys() ,[], []]
    else:

        only_cloud = []
        only_local = []
        modified = []
        unmodified = []

        for x in cloud_dict.keys():
            if local_dict.get(x) is None:
                only_cloud.append(x)
            elif local_dict[x] != cloud_dict[x]:
                modified.append(x)
            else:
                unmodified.append(x)

        for x in local_dict.keys():
            if cloud_dict.get(x) == None:
                only_local.append(x)
        return [modified,unmodified, only_cloud,only_local]


def resolve_conflicts(cloud_dict, local_dir):  # return [upload,download,delete]
    local_dict = {}
    for (root, dirnames, filenames) in walk(local_dir):
        for name in filenames:
            md5e = md5(os.path.join(root, name))
            local_dict[os.path.join(os.path.relpath(root, local_dir), name)] = md5e
    if local_dict == cloud_dict:
        print("Everything is up to date.")
        return [[], [], []]
    else:

        only_cloud = []
        only_local = []
        modified = []
        unmodified = []
        to_upload = []
        to_delete = []
        to_download = []
        local_delete = []
        for x in cloud_dict.keys():
            if local_dict.get(x) is None:
                only_cloud.append(x)
            elif local_dict[x] != cloud_dict[x]:
                modified.append(x)
            else:
                unmodified.append(x)

        for x in local_dict.keys():
            if (cloud_dict.get(x) == None):
                only_local.append(x)

        print("There are some Merge conflicts.\n\nYou have :")
        print(len(modified), " modified files")
        print(len(only_cloud), " files only on cloud storage")
        print(len(only_local), " files only on local storage")
        print(len(modified), " unmodified files\n")

        if (len(only_cloud) != 0):
            print("The files only on Cloud Storage.")
            i = "V"
            while (i == "V"):
                i = input(
                    "Enter V to view them.\nR to delete all of them.\nD to download them all to local storage.\nQ to "
                    "deal with them individually.\nS to cancel sync.\n")
                if (i == "V"):
                    for x in only_cloud:
                        print(x)
            if (i == "R"):
                to_delete = to_delete + only_cloud
            elif (i == "D"):
                to_download = to_download + only_cloud
            elif i == "S":
                print("sync terminated.")
                exit(0)
            else:
                print(
                    "For all the files displayed, enter one of the options \nR to delete from cloud.\nD to download "
                    "from cloud.\n")
                for x in only_cloud:
                    i = input(x + "\n")
                    while (i != "D" and i != "R"):
                        i = input("Wrong input. Try again\n")
                    if (i == "D"):
                        to_download.append(x)
                    else:
                        to_delete.append(x)

        if (len(only_local) != 0):
            print("The files only on Local Storage.")
            i = "V"
            while (i == "V"):
                i = input(
                    "Enter V to view them.\nR to delete all of them.\nU to upload them all to cloud storage.\nQ to "
                    "deal with them individually.\nS to cancel sync.\n")
                if (i == "V"):
                    for x in only_local:
                        print(x)
            if (i == "R"):
                local_delete = local_delete + only_local
            elif (i == "U"):
                to_upload = to_upload + only_local
            elif i == "S":
                print("sync terminated.")
                exit(0)
            else:
                print(
                    "For all the files displayed, enter one of the options \nR to delete from local.\nU to upload to "
                    "cloud.")
                for x in only_local:
                    i = input(x + "\n")
                    while (i != "U" and i != "R"):
                        i = input("Wrong input. Try again\n")
                    if (i == "U"):
                        to_upload.append(x)
                    else:
                        local_delete.append(x)

        if len(modified) != 0:
            print("The Modified files.")
            i = "V"
            while (i == "V"):
                i = input(
                    "Enter V to view them.\nC to keep the cloud storage versions.\nL to keep local storege "
                    "versions.\nQ to deal with them individually\n")
                if (i == "V"):
                    for x in modified:
                        print(x)
            if (i == "C"):
                local_delete = local_delete + modified
                to_download = to_download + modified
            elif (i == "L"):
                to_upload = to_upload + modified
                to_delete = to_delete + modified
            else:
                print(
                    "For all the files displayed, enter one of the options \nL to keep the local copy.\nC to keep the "
                    "cloud copy.")
                for x in modified:
                    i = input(x + "\n")
                    while (i != "C" and i != "L"):
                        i = input("Wrong input. Try again\n")
                    if (i == "C"):
                        local_delete.append(x)
                        to_download.append(x)
                    else:
                        to_upload.append(x)
                        to_delete.append(x)
        delete(local_dir, local_delete)
        #        print (to_upload,to_download,to_delete)
        return [to_upload, to_download, to_delete]

# dict = {'./Problem - 3.pdf': '996c767a41739f2a0f8589a21a8a8980',
#         './machine.cpp': '4f667540ef54023f33761f4f0c8a858b', 'testcases/out6': 'e3d35920a0ba5870595ea684d3535f8c', 'testcases/out7': '7320dce85a45baa863e8c668e94ae667', 'testcases/inp3': '47c2fd5397fcabc86230200c469db0dc', 'testcases/inp6': '389cf6190fa725b66dc3c90ddd10f3ff', 'testcases/out1': 'a69b01f17a6ae5089fcb5a625c49ab7e', 'testcases/inp2': 'b5aa58994acf4827ee43ce44325ac555', 'testcases/inp7': '220f8f879313bcc759a32fe704095470', 'testcases/inp1': 'a02cb7f57be704ec95c573e97ad8c1e2', 'testcases/inp5': 'f168a2f02f89ca3681732b98b628d20b', 'testcases/out3': 'a69b01f17a6ae5089fcb5a625c49ab7e', 'testcases/out5': '5b17ba66183ebe4d802ef0aacd8f27ec', 'testcases/out2': '01adada3d4081d56210ccd18d2a09157', 'testcases/inp4': 'ce803df86594d99deae5ce34df43398e', 'testcases/out4': '4d51db12fa30733e3e5bd147f21a77f8'}

# resolve_conflicts(dict);
