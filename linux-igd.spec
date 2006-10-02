
Summary:	The Linux UPNP Internet Gateway Device
Name:		linux-igd
Version:	0.95
Release:	1
URL:		http://linux-igd.sourceforge.net/
Source0:	http://dl.sourceforge.net/linux-igd/linuxigd-0.95.tar.gz
# Source0-md5:	0f203a2db5e3fb01496b73e417dbd9a6
Patch0:		%{name}-install.patch
License:	GPL
Group:		Daemons
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	libupnp-devel

%description
This is a deamon that emulates Microsoft's Internet Connection Service
(ICS). It implements the UPnP Internet Gateway Device specification
(IGD) and allows UPnP aware clients, such as MSN Messenger to work
properly from behind a Linux NAT firewall.

%prep
%setup -q -n linuxigd-%{version}
%patch0 -p1

%build
%{__make} OPT="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/linuxigd/
%{_sysconfdir}/linuxigd/*.xml
%config %{_sysconfdir}/upnpd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/upnpd
%{_mandir}/man8/upnpd.8*
%attr(755,root,root) %{_sbindir}/upnpd
%attr(754,root,root) /etc/rc.d/init.d/upnpd

%post
/sbin/chkconfig --add upnpd

%preun
if [ $1 = 0 ] ; then
	/sbin/chkconfig --del upnpd
fi
