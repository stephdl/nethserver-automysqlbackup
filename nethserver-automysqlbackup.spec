%define name nethserver-automysqlbackup
%define version 3.0.RC6
%define release 12
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

%prep
rm -rf $RPM_BUILD_ROOT

%setup

%build
perl createlinks

%{__mkdir} -p root/var/lib/nethserver/automysqlbackup/daily
%{__mkdir} -p root/var/lib/nethserver/automysqlbackup/fullschema
%{__mkdir} -p root/var/lib/nethserver/automysqlbackup/latest
%{__mkdir} -p root/var/lib/nethserver/automysqlbackup/monthly
%{__mkdir} -p root/var/lib/nethserver/automysqlbackup/status
%{__mkdir} -p root/var/lib/nethserver/automysqlbackup/tmp
%{__mkdir} -p root/var/lib/nethserver/automysqlbackup/weekly



%install
/bin/rm -rf $RPM_BUILD_ROOT
(cd root   ;/usr/bin/find . -depth -print | /bin/cpio -dump $RPM_BUILD_ROOT)
/bin/rm -f %{name}-%{version}-filelist
%{genfilelist} $RPM_BUILD_ROOT \
  --file /sbin/e-smith/runmysqlbackup 'attr(0750,root,root)' \
> %{name}-%{version}-filelist


%files -f %{name}-%{version}-filelist

%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING
%config(noreplace) /etc/automysqlbackup/automysqlbackup.conf
%config(noreplace) /etc/automysqlbackup/myserver.conf
%config(noreplace) /etc/automysqlbackup/rh-mariadb101.conf
%config(noreplace) /etc/automysqlbackup/rh-mariadb102.conf
%config(noreplace) /etc/automysqlbackup/rh-mariadb103.conf

%clean 
rm -rf $RPM_BUILD_ROOT

%pre

%post

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

%changelog
* Sun Nov 29 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-12.ns7
- Dump rh-mariadb103 if installed
- config noreplace configuration files

* Tue Aug 21 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-11.ns7
- Create mysql user in mariadb101 & mariadb102

* Sun Jul 9 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-10.ns7
- Dump rh-mariadb101 or rh-mariadb102 if installed

* Thu Nov 9 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-9.ns7
- added pigz as dependency for multicore support

* Mon Mar 27 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-8.ns7
- The cronJob can be set hourly

* Sun Mar 11 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-7.ns7
- GPL license

* Sat Nov 05 2016 Stephane de Labrusse <stephdl@de-labrusse.fr> 3.0.RC6-6.ns7
- First release to NS7

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
