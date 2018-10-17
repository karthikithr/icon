%define __jar_repack %{nil}
%define tomcat_home /opt/tomcat
%define tomcat_group tomcat
%define tomcat_user tomcat
%define tomcat_user_home /home/tomcat
%define tomcat_version 9

Summary:    Apache Servlet/JSP Engine, RI for Servlet 3.1/JSP 2.3 API
Name:       tomcat%{tomcat_version}
Version:    9.0.12
BuildArch:  noarch
Release:    1
License:    Apache Software License
Group:      Networking/Daemons
URL:        http://tomcat.apache.org/
Source0:    apache-tomcat-%{version}.tar.gz
Source1:    %{name}.init
Source2:    %{name}.logrotate
Requires:   jpackage-utils
Requires:   logrotate
Requires:   java >= 1.8.0
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License. Tomcat is intended to be
a collaboration of the best-of-breed developers from around the world.
We invite you to participate in this open development project. To
learn more about getting involved, click here.

This package contains the base tomcat installation that depends on Sun's JDK and not
on JPP packages.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}/
cp -R * %{buildroot}/%{tomcat_home}/

# Remove all webapps
rm -rf %{buildroot}/%{tomcat_home}/webapps/
install -d -m 775 %{buildroot}%{tomcat_home}/webapps
cd %{buildroot}/%{tomcat_home}/
cd -

# Remove *.bat
rm -f %{buildroot}/%{tomcat_home}/bin/*.bat

# Remove extra logging configs
sed -i -e '/^3manager/d' -e '/\[\/manager\]/d' \
    -e '/^4host-manager/d' -e '/\[\/host-manager\]/d' \
    -e '/^java.util.logging.ConsoleHandler/d' \
    -e 's/, *java.util.logging.ConsoleHandler//' \
    -e 's/, *4host-manager.org.apache.juli.AsyncFileHandler//' \
    -e 's/, *3manager.org.apache.juli.AsyncFileHandler//' \
    %{buildroot}/%{tomcat_home}/conf/logging.properties

# Setup Tomcat Home
install -d -m 755 %{buildroot}/%{tomcat_user_home}

# Drop init script
install -d -m 755 %{buildroot}/%{_sysconfdir}/init.d
install    -m 755 %_sourcedir/%{name}.init %{buildroot}/%{_sysconfdir}/init.d/%{name}

# Drop logrotate script
install -d -m 755 %{buildroot}/%{_sysconfdir}/logrotate.d
install    -m 644 %_sourcedir/%{name}.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%pre
getent group %{tomcat_group} >/dev/null || groupadd -r %{tomcat_group}
getent passwd %{tomcat_user} >/dev/null || /usr/sbin/useradd --comment "Tomcat Daemon User" --shell /bin/bash -M -r -g %{tomcat_group} --home %{tomcat_home} %{tomcat_user}

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%{tomcat_user_home}
%{tomcat_home}
%defattr(-,root,root)
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/init.d/%{name}

%post
chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  service %{name} stop > /dev/null 2>&1
  chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
  service %{name} condrestart >/dev/null 2>&1
fi

%changelog
* Fri Oct 12 2018 Manoharan, Senthil Nathan <SenthilNathan.Manoharan@iconplc.com>
- 9.0.12
