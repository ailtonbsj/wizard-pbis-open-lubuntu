#!/bin/bash

if [ ! -f /opt/pbis/bin/domainjoin-cli ]; then
	zenity --error --text "PBIS-Open não instalado!!! Por favor instale-o!" --width=350
	exit
fi

cd /opt/wizard-pbis/
./JoinADWindow.py
AD_DOMAIN=$(cat /tmp/domain.ad)
AD_USER=$(cat /tmp/user.ad)
AD_PASS=$(cat /tmp/passwd.ad)
AD_DCNAME=$(echo $AD_DOMAIN | awk '{split($0,a,"."); print a[1]}')

domainjoin-cli join --disable ssh $AD_DOMAIN $AD_USER $AD_PASS

hasDomainAdm=`grep "%domain^admins" /etc/sudoers`
if [ "$hasDomainAdm" == "" ]; then
	sed -i "s/%admin ALL=(ALL) ALL/%admin ALL=(ALL) ALL\n%$AD_DCNAME\\\\\\\\domain^admins ALL=(ALL) ALL/g" /etc/sudoers
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
	sed -i 's/allow-guest=true/allow-guest=false/g' $greetFile
fi

hasManualLogin=`grep "greeter-show-manual-login" $greetFile`
if [ "$hasManualLogin" == "" ]; then
	echo "greeter-show-manual-login=true" >> $greetFile
else
	sed -i 's/greeter-show-manual-login=false/greeter-show-manual-login=true/g' $greetFile
fi

hasHideUsers=`grep "greeter-hide-users" $greetFile`
if [ "$hasHideUsers" == "" ]; then
	echo "greeter-hide-users=true" >> $greetFile
else
	sed -i 's/greeter-hide-users=false/greeter-hide-users=true/g' $greetFile
fi

dom=$(domainjoin-cli query | grep Domain | awk '{split($0,a," = ");print a[2]}')
if [ "$dom" == "" ]; then
	zenity --error --text "Não foi possível se juntar ao domínio!\nVerifique senha, usuário e nome do domínio!" --width=350
	exit
fi

/opt/pbis/bin/enum-groups | grep Name | grep -v '\^' | grep -v 'dns' | awk '{split($0,a,"\\"); print a[2]}' > /tmp/sGroups
./RequireMembershipWindow.py
restric=$(cat /tmp/restric.ad)
if [ "$restric" != "--Sem Restrição--" ]; then
	sGroup=$(echo $dom)\\$restric
	/opt/pbis/bin/config RequireMembershipOf $sGroup
else
	/opt/pbis/bin/config RequireMembershipOf ''
fi

ipServRaw=$(/opt/pbis/bin/get-status | grep 'DC Address' | awk '{split($0,a,":"); print a[2]}')
ipServ=${ipServRaw//[[:space:]]/}

cat << EOF > /etc/security/pam_mount.conf.xml
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE pam_mount SYSTEM "pam_mount.conf.xml.dtd">
<pam_mount>
<debug enable="0" />
<volume options="nodev,nosuid,dir_mode=0700"
    user="*"
    fstype="cifs"
    server="$ipServ"
    path="publico"
    mountpoint="~/Público"
/>
EOF

while read group; do
	cat << EOF >> /etc/security/pam_mount.conf.xml
<volume options="nodev,nosuid,dir_mode=0700"
    user="*"
    fstype="cifs"
    server="$ipServ"
    path="$group"
    mountpoint="~/${group^}"
    sgrp="$(echo $dom | awk '{split($0,a,"."); print a[1]}')\\$group"
/>
EOF
done < /tmp/sGroups

cat << EOF >> /etc/security/pam_mount.conf.xml
<mntoptions allow="nosuid,nodev,loop,encryption,fsck,nonempty,allow_root,allow_other" />
<mntoptions require="nosuid,nodev" />
<logout wait="0" hup="no" term="no" kill="no" />
<mkmountpoint enable="1" remove="true" />
</pam_mount>
EOF

zenity --info --text "Bem vindo ao Domínio $dom!" --width=350