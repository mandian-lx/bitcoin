#% {?_javapackages_macros:%_javapackages_macros}

%define major 0
%define libname %mklibname bitcoinconsensus %{major}
%define devname %mklibname bitcoinconsensus -d
%define _disable_lto 1

Summary:	P2P Digital Currency
Name:		bitcoin
Version:	0.14.2
Release:	1
License:	MIT
Group:		Networking/Other
Url:		http://www.bitcoin.org
Source0:	https://github.com/%{name}/%{name}/archive/%{name}-%{version}.tar.gz
Source1:	bitcoind.service
Source2:	bitcoind-tmpfiles.conf
Patch0:		bitcoin-fix-desktop-icon-name.patch
BuildRequires:	ccache
BuildRequires:	git
BuildRequires:	imagemagick
BuildRequires:	lcov
#BuildRequires:	java-devel
BuildRequires:	boost-devel
BuildRequires:	db52-devel
BuildRequires:	miniupnpc-devel
BuildRequires:	pkgconfig(libzmq)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(libqrencode)
BuildRequires:	qt5-linguist-tools

%description
Bitcoin is a free open source peer-to-peer electronic cash system that is
completely decentralized, without the need for a central server or trusted
parties. Users hold the crypto keys to their own money and transact directly
with each other, with the help of a P2P network to check for double-spending.

Full transaction history is stored locally at each client. This requires
several GB of space, slowly growing.

#----------------------------------------------------------------------------

%package -n bitcoind
Summary:	Headless daemon for Bitcoin crypto-currency
Group:		Networking/Other
Requires(pre):	rpm-helper

%description -n bitcoind
Bitcoin is a free open source peer-to-peer electronic cash system that is
completely decentralized, without the need for a central server or trusted
parties. Users hold the crypto keys to their own money and transact directly
with each other, with the help of a P2P network to check for double-spending.

Full transaction history is stored locally at each client. This requires
several GB of space, slowly growing.

This package provides bitcoind, headless bitcoin daemon.

%files -n bitcoind
%doc COPYING README.md
%{_mandir}/man1/%{name}d.1*
#%{_mandir}/man5/%{name}.conf.5*
%{_bindir}/bitcoind
%dir %attr(700,bitcoin,bitcoin) %{_var}/lib/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_unitdir}/bitcoind.service
%{_sbindir}/rcbitcoind
%{_tmpfilesdir}/bitcoind.conf
%{_presetdir}/86-bitcoind.preset

%pre -n bitcoind
%_pre_useradd bitcoin %{_var}/lib/%{name} /bin/false
%_pre_groupadd bitcoin

#----------------------------------------------------------------------------

%package qt
Summary:	An end-user Qt GUI for the Bitcoin crypto-currency
Group:		Networking/Other

%description qt
Bitcoin is a free open source peer-to-peer electronic cash system that is
completely decentralized, without the need for a central server or trusted
parties. Users hold the crypto keys to their own money and transact directly
with each other, with the help of a P2P network to check for double-spending.

Full transaction history is stored locally at each client. This requires
several GB of space, slowly growing.

This package provides bitcoin-qt, a GUI for Bitcoin based on Qt.

%files qt
%doc COPYING README.md
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}-qt.1*

#----------------------------------------------------------------------------

%package tests
Summary:	Automated tests for bitcoin client
Group:		Networking/Other

%description tests
Bitcoin is a free open source peer-to-peer electronic cash system that is
completely decentralized, without the need for a central server or trusted
parties. Users hold the crypto keys to their own money and transact directly
with each other, with the help of a P2P network to check for double-spending.

Full transaction history is stored locally at each client. This requires
several GB of space, slowly growing.

This package provides automated tests for bitcoin-qt and bitcoind.

%files tests
%doc COPYING README.md
%{_bindir}/bench_bitcoin
%{_bindir}/test_bitcoin
%{_bindir}/test_bitcoin-qt

#----------------------------------------------------------------------------

%package utils
Summary:	An end-user cli for the Bitcoin crypto-currency
Group:		Networking/Other

%description utils
Bitcoin is a free open source peer-to-peer electronic cash system that is
completely decentralized, without the need for a central server or trusted
parties. Users hold the crypto keys to their own money and transact directly
with each other, with the help of a P2P network to check for double-spending.

Full transaction history is stored locally at each client. This requires
several GB of space, slowly growing.

This package provides bitcoin-cli (CLI tool to interact with the daemon) and
bitcoin-tx utility.

%files utils
%doc COPYING README.md
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-tx
%{_mandir}/man1/%{name}-cli.1*
%{_mandir}/man1/%{name}-tx.1*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Bitcoin consensus shared library
Group:		System/Libraries

%description -n %{libname}
The purpose of this library is to make the verification functionality
that is critical to Bitcoin’s consensus available to other applications,
e.g. to language bindings such as python-bitcoinlib or alternative node
implementations.

%files -n %{libname}
%doc COPYING README.md
%{_libdir}/libbitcoinconsensus.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Developmont files for bitcoin consensus library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	bitcoinconsensus-devel = %{EVRD}

%description -n %{devname}
The purpose of this library is to make the verification functionality
that is critical to Bitcoin’s consensus available to other applications,
e.g. to language bindings such as python-bitcoinlib or alternative node
implementations.

This package contains development files.

%files -n %{devname}
%doc COPYING README.md
%{_includedir}/bitcoinconsensus.h
%{_libdir}/libbitcoinconsensus.so
%{_libdir}/pkgconfig/libbitcoinconsensus.pc

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1

# (tpg) fix linking with llvm-ar
sed -i -e 's/\-rs/rs/g' src/leveldb/Makefile*

%build
%global optflags %{optflags} -I/usr/include/db52
autoreconf -fi
%configure \
	--disable-static \
	--with-cli=yes \
	--with-daemon=yes \
	--with-gui=qt5 \
	--with-miniupnpc \
	--with-qrencode \
	--with-incompatible-bdb

%make

%install
%makeinstall_std

install -D -m 0644 contrib/debian/bitcoin-qt.desktop %{buildroot}%{_datadir}/applications/%{name}-qt.desktop

# install menu icons
for N in 16 32 48 64 128 256;
do
convert share/pixmaps/bitcoin256.png -scale ${N}x${N} $N.png;
install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done

#install -D -m 0644 contrib/debian/manpages/bitcoin.conf.5 %{buildroot}%{_mandir}/man5/bitcoin.conf.5
install -D -m 0644 contrib/debian/examples/bitcoin.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
mkdir -p %{buildroot}%{_var}/lib/%{name}

mkdir %{buildroot}%{_sbindir}
ln -sv /sbin/service %{buildroot}%{_sbindir}/rcbitcoind
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/bitcoind.service
install -d -m 0755 %{buildroot}%{_tmpfilesdir}/
install -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/bitcoind.conf

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-bitcoind.preset << EOF
enable bitcoind.service
EOF
