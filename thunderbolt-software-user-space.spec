#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Thunderbolt(TM) Linux Software
Summary(pl.UTF-8):	Oprogramowanie linuksowe do technologii Thunderbolt(TM)
Name:		thunderbolt-software-user-space
# use "0" until versioning is stabilized:
# - github/dell release is tagged by date
# - changelog says it's 16.2.59 release
# - individual component versions acc. to changelogs:
#   - daemon 16.2.57
#   - libtbtfwu 1.0.0 release 16.2.59
#   - tbtfwucli 0.0.2 release 16.2.59
Version:	0
%define	subver	2017.01.19
Release:	0.%{subver}.2
License:	BSD
Group:		Libraries
# primary repository is https://github.com/01org/thunderbolt-software-user-space, but release exists only in dell repository
#Source0Download: https://github.com/dell/thunderbolt-software-user-space/releases
Source0:	https://github.com/dell/thunderbolt-software-user-space/archive/%{subver}/%{name}-%{subver}.tar.gz
# Source0-md5:	2876232d622eb83df0f8ec392826ab55
Patch0:		%{name}-glibc.patch
Patch1:		%{name}-dbus-macros.patch
Patch2:		%{name}-install.patch
Patch3:		%{name}-link.patch
URL:		https://01.org/thunderbolt-sw/
BuildRequires:	cmake >= 2.8.8
BuildRequires:	dbus-c++-devel >= 0.5.0
BuildRequires:	libnl-devel >= 1:3.2
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# hardcoded in ThunderboltService/Linux/{CMakeLists.txt,config/*.service}
%define		_libexecdir	/usr/lib

%description
Thunderbolt(TM) Linux Software.

%description -l pl.UTF-8
Oprogramowanie linuksowe do technologii Thunderbolt(TM).

%package -n thunderbolt-software-daemon
Summary:	Thunderbolt(TM) daemon
Summary(pl.UTF-8):	Demon Thunderbolt(TM)
Group:		Daemons

%description -n thunderbolt-software-daemon
Thunderbolt(TM) technology is a transformational high-speed, dual
protocol I/O that provides unmatched performance with up to 40Gbps
bi-directional transfer speeds. It provides flexibility and simplicity
by supporting both data (PCIe, USB3.1) and video (DisplayPort) on a
single cable connection that can daisy-chain up to six devices.

In addition, the Thunderbolt Networking mode allows a connection of
two computers through a Thunderbolt cable.

The Thunderbolt daemon (thunderboltd) is a user-space daemon that
implements 2 main functionalities:
1. Completing the Thunderbolt Networking implementation.
2. Implementing the host FW update functionality.

%description -n thunderbolt-software-daemon -l pl.UTF-8
Technologia Thunderbolt(TM) to szybkie, dwuprotokołowe operacje we/wy
zapewniające wyjątkową przepustowość do 40Gbps w obie strony. Zapewnia
elastyczność i prostotę, obsługując zarówno dane (PCIe, USB3.1), jak i
obraz (DisplayPort) na pojedynczym połączeniu kablowym, którym można
połączyć szeregowo do sześciu urządzeń.

Ponadto tryb sieciowy Thunderbolt pozwala na połączenie kablem dwóch
komputerów.

Demon Thunderbolt (thunderboltd) to demon przestrzeni użytkownika
zapewniający dwie funkcje:
1. Uzupełnienie implementacji Thunderbolt Networking.
2. Aktualizacje firmware'u hosta.

%package -n libtbtfwu
Summary:	Thunderbolt(TM) FW update library
Summary(pl.UTF-8):	Biblioteka do uaktualniania FW systemu Thunderbolt(TM)
Group:		Libraries

%description -n libtbtfwu
This library supplies simpler, safer and higher-level interface of the
FW update functionality supplied by Thunderbolt daemon. It currently
supports FW update for host controller only.

%description -n libtbtfwu -l pl.UTF-8
Ta biblioteka udostępnia prostszy, bezpieczniejszy interfejs wyższego
poziomu funkcji uaktualniania FW udostępnianej przez demona
Thunderbolt. Obecnie obsługuje uaktualnianie firmware'u tylko
kontrolera hosta.

%package -n libtbtfwu-devel
Summary:	Header files for libtbtfwu library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libtbtfwu
Group:		Development/Libraries
Requires:	libtbtfwu = %{version}-%{release}

%description -n libtbtfwu-devel
Header files for libtbtfwu library.

%description -n libtbtfwu-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libtbtfwu.

%package -n libtbtfwu-static
Summary:	Static libtbtfwu library
Summary(pl.UTF-8):	Statyczna biblioteka libtbtfwu
Group:		Development/Libraries
Requires:	libtbtfwu-devel = %{version}-%{release}

%description -n libtbtfwu-static
Static libtbtfwu library.

%description -n libtbtfwu-static -l pl.UTF-8
Statyczna biblioteka libtbtfwu.

%package -n tbtfwucli
Summary:	Thunderbold(TM) FW update sample tool
Summary(pl.UTF-8):	Przykładowe narzędzie do uaktualniania FW systemu Thunderbolt(TM)
Group:		Applications/System
Requires:	libtbtfwu = %{version}-%{release}

%description -n tbtfwucli
This is a preliminary sample of a command line tool that uses the FW
update library. It implements a simple user interface for testing
current FW version of a Thunderbolt host controller, validating FW
image file compatibility with current controller and writing a new FW
image file to the controller flash.

%description -n tbtfwucli -l pl.UTF-8
Ten pakiet zawiera wczesne, przykładowe narzędzie linii poleceń
wykorzystujące bibliotekę do uaktualniania FW. Implementuje prosty
interfejs użytkownika do testowania aktualnej wersji FW kontrolera
hosta Thunderbolt, sprawdzanie zgodności pliku obrazu FW z aktualnym
kontrolerem oraz zapis nowego pliku obrazu FW do pamięci flash
kontrolera.

%prep
%setup -q -n %{name}-%{subver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
TOPDIR=$(pwd)
install -d build-libtbtfwu
cd build-libtbtfwu
# CMakeFiles expect relative CMAKE_INSTALL_LIBDIR
%cmake ../fwupdate/libtbtfwu \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib}
%{__make}
cd ..

install -d build-tbtfwucli
cd build-tbtfwucli
%cmake ../fwupdate/tbtfwucli \
	-DTBT_LIBRARY="$TOPDIR/build-libtbtfwu/libtbtfwu.so"
%{__make}
cd ..

install -d build-daemon
cd build-daemon
%cmake ../ThunderboltService/Linux
%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-libtbtfwu install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C build-tbtfwucli install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C build-daemon install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libtbtfwu -p /sbin/ldconfig
%postun	-n libtbtfwu -p /sbin/ldconfig

%files -n thunderbolt-software-daemon
%defattr(644,root,root,755)
%doc AUTHORS.daemon COPYING.daemon ChangeLog.daemon README README.daemon
%dir %{_libexecdir}/thunderbolt
%attr(755,root,root) %{_libexecdir}/thunderbolt/thunderboltd
%{_datadir}/dbus-1/system-services/com.Intel.Thunderbolt.service
%{systemdunitdir}/thunderbolt.service
/etc/dbus-1/system.d/thunderbolt.conf
/etc/udev/rules.d/10-thunderbolt.rules

%files -n libtbtfwu
%defattr(644,root,root,755)
%doc AUTHORS.libtbtfwu COPYING.libtbtfwu ChangeLog.libtbtfwu README.libtbtfwu
%attr(755,root,root) %{_libdir}/libtbtfwu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtbtfwu.so.1

%files -n libtbtfwu-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtbtfwu.so
%{_includedir}/tbt
%{_pkgconfigdir}/libtbtfwu.pc

%files -n libtbtfwu-static
%defattr(644,root,root,755)
%{_libdir}/libtbtfwu.a

%files -n tbtfwucli
%defattr(644,root,root,755)
%doc AUTHORS.tbtfwucli COPYING.tbtfwucli ChangeLog.tbtfwucli README.tbtfwucli
%attr(755,root,root) %{_bindir}/tbtfwucli
