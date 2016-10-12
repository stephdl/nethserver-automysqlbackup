%define name nethserver-automysqlbackup
%define version 3.0.RC6
%define release 5
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
Requires: automysqlbackup
BuildRequires: nethserver-devtools

%description
This RPM is an unofficial addon for the Nethserver  
The target audience is the Linux administrator 
who wants to backup their mysql databases with an automatic way.
This script is based on automysqlbackup V3.0



%changelog
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
%{__mkdir} -p root/var/lib/nethserver/automysqlbackup/daily
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/nethserver/automysqlbackup/fullschema
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/nethserver/automysqlbackup/latest
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/nethserver/automysqlbackup/monthly
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/nethserver/automysqlbackup/status
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/nethserver/automysqlbackup/tmp
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/nethserver/automysqlbackup/weekly



%install
/bin/rm -rf $RPM_BUILD_ROOT
(cd root   ;/usr/bin/find . -depth -print | /bin/cpio -dump $RPM_BUILD_ROOT)
/bin/rm -f %{name}-%{version}-filelist
%{genfilelist} $RPM_BUILD_ROOT > %{name}-%{version}-filelist


%files -f %{name}-%{version}-filelist

%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update

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
