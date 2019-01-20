#!/bin/bash

if [ $(id -u) != "0" ]; then
	echo "need root"
	exit
fi

apt install python-gi
apt install zenity

mkdir /opt/wizard-pbis/ -p
cp -rf gui.py /opt/wizard-pbis/
cp -rf main.py /opt/wizard-pbis/
cp -rf wizard-pbis.desktop /usr/share/applications/
cp -rf com.winunix.wizard-pbis.policy /usr/share/polkit-1/actions