Summary:	Original Bitcoin crypto-currency wallet for automated services
Name:		bitcoind
Version:	0.6.0
Release:	1
Source0:	bitcoind-%version.tar.gz
License:	MIT
Group:		System/Configuration/Boot and Init
URL:		http://bitcoin.org
BuildRequires:	qt4-devel
BuildRequires:	db5.3-devel
BuildRequires:	miniupnpc-devel
BuildRequires:	boost-devel

%description
Bitcoin is an experimental new digital currency that 
enables instant payments to anyone, anywhere in the world.
Bitcoin uses peer-to-peer technology to operate with 
no central authority: managing transactions and issuing 
money are carried out collectively by the network.
Bitcoin is also the name of the open source
software which enables the use of this currency.

%prep
%setup -q -n bitcoin-bitcoin-b3b5ab1

%build
%qmake_qt4
pwd
cd src
%make -f makefile.unix BDB_INCLUDE_PATH='/usr/include/db53/' USE_SSL=1

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1/
install -m 0755 src/bitcoind %{buildroot}%{_bindir}
install -m 0644 contrib/debian/manpages/bitcoind.1 %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
install -m600 contrib/debian/examples/bitcoin.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf




%post
/sbin/chkconfig --add %{name} || :

%preun
if [ $1 -eq 0 ]; then
	service %{name} stop >/dev/null || :
	/sbin/chkconfig --del %{name} || :
fi
exit 0

%postun
if [ "$1" -ge "1" ] ; then
	/sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%_postun_userdel bitcoin
%_postun_groupdel bitcoin
exit 0



%files
%doc README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
