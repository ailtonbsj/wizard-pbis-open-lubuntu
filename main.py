#!/bin/bash

if [ ! -f /opt/pbis/bin/domainjoin-cli ]; then
	zenity --error --text "PBIS-Open não instalado!!! Por favor instale-o!" --width=350
	exit
fi

cd /opt/wizard-pbis/
./gui.py
AD_DOMAIN=$(cat /tmp/domain.ad)
AD_USER=$(cat /tmp/user.ad)
AD_PASS=$(cat /tmp/passwd.ad)

domainjoin-cli join --disable ssh $AD_DOMAIN $AD_USER $AD_PASS

hasDomainAdm=`grep "%domain^admins ALL=(ALL) ALL" /etc/sudoers`
if [ "$hasDomainAdm" == "" ]; then
	sed -i 's/%admin ALL=(ALL) ALL/%admin ALL=(ALL) ALL\n%domain^admins ALL=(ALL) ALL/g' /etc/sudoers
fi

/opt/pbis/bin/config UserDomainPrefix $AD_DOMAIN
/opt/pbis/bin/config AssumeDefaultDomain True
/opt/pbis/bin/config LoginShellTemplate /bin/bash
/opt/pbis/bin/config HomeDirTemplate %H/%U


hasSession=`grep "\[success=ok default=ignore\]" /etc/pam.d/common-session`
if [ "$hasSession" == "" ]; then
	echo "session [success=ok default=ignore] pam_lsass.so" >> /etc/pam.d/common-session
fi

greetFile="/usr/share/lightdm/lightdm.conf.d/60-lightdm-gtk-greeter.conf"

hasGuest=`grep "allow-guest" $greetFile`
if [ "$hasGuest" == "" ]; then
echo "allow-guest=false" >> $greetFile
else
	sed 's/allow-guest=true/allow-guest=false/g' $greetFile
fi

hasManualLogin=`grep "greeter-show-manual-login" $greetFile`
if [ "$hasManualLogin" == "" ]; then
echo "greeter-show-manual-login=true" >> $greetFile
else
	sed 's/greeter-show-manual-login=false/greeter-show-manual-login=true/g' $greetFile
fi

zenity --info --text "$(/opt/pbis/bin/domainjoin-cli query)\n\nEh necessario reiniciar!" --width=350
