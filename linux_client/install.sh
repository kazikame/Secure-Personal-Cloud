#!/usr/bin/env bash

if command -v python3 &>/dev/null;
then
    echo foo > /dev/null
else
    apt-get update
    apt-get install python3
fi

sudo -H pip3 install tqdm
sudo -H pip3 install pycrypto
sudo -H pip3 install requests-toolbelt
sudo -H pip3 install requests

home_folder=$(pwd)
temp="export SPC_PATH='$home_folder'"
temp=$(echo $temp | sed s/\'/\"/g )
echo $temp >> ~/.bashrc

daemon_path=$(echo $home_folder/daemon.py)
config_path=$(echo $home_folder/config.sh)
json_path=$(echo $home_folder/conf.json)

python3 startup.py empty_json $home_folder

temp=$(echo "python3 $daemon_path")
temp="alias start_daemon='$temp'"
temp=$(echo $temp | sed s/\'/\"/g )
echo $temp >> ~/.bashrc

temp=$(echo bash "$config_path" stop_daemon)
temp="alias stop_daemon='$temp'"
temp=$(echo $temp | sed s/\'/\"/g )
echo $temp >> ~/.bashrc

temp=$(echo bash "$config_path")
temp="alias spc='$temp'"
temp=$(echo $temp | sed s/\'/\"/g )
echo $temp >> ~/.bashrc

temp=$(echo /usr/bin/python3 "$daemon_path")
temp="@reboot $temp"
(crontab -l 2>/dev/null; echo "$temp") | crontab -
update-rc.d cron defaults

sudo mkdir -p /usr/local/man/man1
sudo cp spc /usr/local/man/man1/spc.1
sudo gzip /usr/local/man/man1/spc.1

exec bash