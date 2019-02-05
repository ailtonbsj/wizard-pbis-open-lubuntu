#!/bin/bash

if [ $(id -u) != "0" ]; then
	echo "need root"
	exit
fi

apt update
apt install python-gi -y
apt install zenity -y
apt install libpam-mount -y
apt install cifs-utils -y

mkdir /opt/wizard-pbis/ -p
cp -rf JoinADWindow.py /opt/wizard-pbis/
cp -rf RequireMembershipWindow.py /opt/wizard-pbis/
cp -rf main.sh /opt/wizard-pbis/
cp -rf wizard-pbis.desktop /usr/share/applications/
cp -rf com.winunix.wizard-pbis.policy /usr/share/polkit-1/actions