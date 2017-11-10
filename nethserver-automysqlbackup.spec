%define name nethserver-automysqlbackup
%define version 3.0.RC6
%define release 8
%define rpmver   3.0.RC6


Summary:automysqlbackup is a script to backup your msql database on nethserver
Name:   %{name}
Version:%{version}
Release:%{release}%{?dist}
License:GPL
Group:  /Web/Application
Source: %{name}-%{version}.tar.gz
URL:    http://sourceforge.net/projects/automysqlbackup/
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
BuildArchitectures: noarch
Requires: nethserver-mysql
Requires: pax
Requires: pigz
Requires: automysqlbackup
BuildRequires: nethserver-devtools

%description
This RPM is an unofficial addon for the Nethserver  
The target audience is the Linux administrator 
who wants to backup their mysql databases with an automatic way.
This script is based on automysqlbackup V3.0



%changelog
* Thu Nov 9 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-8.ns6
- added pigz as dependency for multicore support

* Mon Mar 27 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-7.ns6
- The cronJob can be set hourly

* Sun Mar 11 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-6
- GPL license

* Thu May 21 2015 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-5
- First release to Neth

* Sun Aug 17 2014 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-4
- added my own patch against the --events warning
--Warning: Skipping the data of table mysql.event. Specify the --events option explicitly.

* Sun Oct 27 2013 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6.3
- split the contrib in two versions smeserver-automysqlbackup and automysqlbackup
* Mon Apr 22 2013 Stephane de Labrusse <stephdl@de-labrusse.fr>
- [3.0.RC6] version Based on automysqlbackup V3.0 RC6
* Mon Apr 08 2013 Stephane de Labrusse <stephdl@de-labrusse.fr>
- [0.01] Initial version Based on automysqlbackup V3.0 RC6

%prep
rm -rf $RPM_BUILD_ROOT

%setup

%build
perl createlinks

%install
/bin/rm -rf $RPM_BUILD_ROOT
(cd root   ;/usr/bin/find . -depth -print | /bin/cpio -dump $RPM_BUILD_ROOT)
/bin/rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
  --file /sbin/e-smith/runmysqlbackup 'attr(0750,root,root)' \
> %{name}-%{version}-filelist


%files -f %{name}-%{version}-filelist

%defattr(-,root,root)
%doc COPYING
%clean 
rm -rf $RPM_BUILD_ROOT

%pre

%post

echo "========================================================================================="
echo "	Your Databases are saved in /root/backup/db "
echo "	only Root can access to these folders"                         
echo "	a mail is send to Admin for all logs "
echo " "                                                                   
echo "	Configuration file is /etc/automysqlbackup/myserver.conf"
echo " "
echo "	For a manual play you can use directly"
echo "	automysqlbackup /etc/automysqlbackup/myserver.conf "
echo "	or as a shortcut simply do in a terminal  : automysqlbackup "
echo "	else backups are done every night at 04H00 AM with /etc/cron.daily/runmysqlbackup"
echo "========================================================================================="
echo "	RESTORING"
echo " 	In a root terminal"
echo "	cd /root/backup/db/ and choose your backup"
echo "	gunzip file-name.sql.gz"
echo "	Next you will need to use the mysql client to restore the DB from the sql file."
echo "	mysql database < /path/file.sql"
echo "	NOTE: Make sure you use < and not > in the above command because you are piping the file.sql" 
echo "	to mysql and not the other way around"
echo "========================================================================================="
echo "	Some db configuration for handle this contrib"
echo "	Mailcontent (stdout/log/files/quiet)"
echo "	# What would you like to be mailed to you?"
echo "	# - log   : send only log file (default)"
echo "	# - files : send log file and sql files as attachments (see docs)"
echo "	#- stdout : will simply output the log to the screen if run manually."
echo "	#- quiet : Only send logs if an error occurs to the MAILADDR."
echo "	Sizemail=8000 (bytes)"
echo "	Mailto=root (or any other user@domaine.com)"
echo "	Backupdir=path to the folder where mysql files are saved"
echo " "
echo "	ex: config setprop automysqlbackup Mailcontent files"
echo "========================================================================================="


%preun
%postun
if [ $1 = 0 ] ; then
SMEDB=automysqlbackup
MYSQLUSER=backupuser
echo "======================================================================="
echo "	delete mysql user and revoque all permissions"
# This section deletes backupuser
mysql -u root -e "REVOKE ALL PRIVILEGES ON *.* FROM '$MYSQLUSER'@'localhost';"
mysql -u root -e "DROP USER $MYSQLUSER@localhost;"
echo "	"
# Delete custom template fragment
echo "	delete db configuration automysqlbackup"
echo "======================================================================="

/sbin/e-smith/config delete $SMEDB
fi
