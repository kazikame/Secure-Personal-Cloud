if command -v python3 &>/dev/null;
then
    echo foo > /dev/null
else
    apt-get update
    apt-get install python3.6
fi

pip3 install tqdm
pip3 install pycrypto
pip3 install requests-toolbelt

home_folder=$(pwd)
daemon_path=$(echo $home_folder/daemon.py)
config_path=$(echo $home_folder/config.sh)

python3.6 $daemon_path
temp=$(echo "python3.6 $daemon_path")
temp="alias start_daemon='$temp'"
temp=$(echo $temp | sed s/\'/\"/g )
echo $temp >> ~/.bashrc
temp=$(echo bash "$config_path" stop_daemon)
temp="alias stop_daemon='$temp'"
temp=$(echo $temp | sed s/\'/\"/g )
echo $temp >> ~/.bashrc
echo 'alias spc="bash config.sh"' >> ~/.bashrc

temp=$(echo /usr/bin/python3.6 "$daemon_path")
temp="@reboot root $temp"
echo $temp > /etc/cron.d/spc_daemon
