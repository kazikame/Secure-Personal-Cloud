#!/bin/bash

server="set_url"
config="config_edit"
observe="observe"
sync="sync"

dic_file="conf.json"

if [ "$1" == "$server" ]
then
    python3 startup.py empty_json "$dic_file"
    python3 startup.py set_server "$2" "$dic_file"
fi

if [ "$1" == "$config" ]
then
    python3 startup.py config "$dic_file"
fi

if [ "$1" == "$observe" ]
then
    python3 startup.py observe "$2" "$dic_file"
fi

if [ "$1" == "$sync" ]
then
    python3 startup.py sync "$dic_file"
fi
