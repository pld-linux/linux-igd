# TODO: %%service?
#
# Conditional build:
%bcond_without	iptables	# iptables/netfilter manipulation support

Summary:	The Linux UPnP Internet Gateway Device
Summary(pl.UTF-8):	Linuksowa implementacja UPnP Internet Gateway Device
Name:		linux-igd
Version:	1.0
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	http://downloads.sourceforge.net/linux-igd/linuxigd-%{version}.tar.gz
# Source0-md5:	929f5c4878c91d534613b7c7070215d9
Patch0:		%{name}-install.patch
Patch1:		%{name}-includes.patch
Patch2:		%{name}-iptables.patch
URL:		http://linux-igd.sourceforge.net/
%{?with_iptables:BuildRequires:	iptables-devel >= 1.6}
BuildRequires:	libupnp-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a deamon that emulates Microsoft's Internet Connection Service
(ICS). It implements the UPnP Internet Gateway Device specification
(IGD) and allows UPnP aware clients, such as MSN Messenger to work
properly from behind a Linux NAT firewall.

%description -l pl.UTF-8
Ten pakiet zawiera demona emulującego Internet Connection Service
(ICS) Microsoftu. Implementuje specyfikację UPnP Internet Gateway
Device (IGD) i pozwala klientom obsługującym UPnP, takim jak MSN
Messenger, pracować poprawnie zza linuksowego firewalla z NAT-em.

%prep
%setup -q -n linuxigd-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall" \
	%{?with_iptables:HAVE_LIBIPTC=1}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add upnpd

%preun
if [ "$1" = 0 ]; then
	/sbin/chkconfig --del upnpd
fi

%files
%defattr(644,root,root,755)
%doc CHANGES INSTALL TODO doc/config_options
%dir %{_sysconfdir}/linuxigd
%{_sysconfdir}/linuxigd/*.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upnpd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/upnpd
%attr(755,root,root) %{_sbindir}/upnpd
%attr(754,root,root) /etc/rc.d/init.d/upnpd
%{_mandir}/man8/upnpd.8*
