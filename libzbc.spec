#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	gtk		# GTK+ 3 based GUI
%bcond_without	static_libs	# static library
#
Summary:	Library for accessing and managing ZBC/ZAC devices
Summary(pl.UTF-8):	Biblioteka do dostępu i zarządzania urządzeniami ZBC/ZAC
Name:		libzbc
Version:	6.2.0
Release:	1
License:	BSD or LGPL v3+
Group:		Libraries
#Source0Download: https://github.com/westerndigitalcorporation/libzbc/releases
Source0:	https://github.com/westerndigitalcorporation/libzbc/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	dc09ad813d878c17fd09d97731b17e1b
URL:		https://github.com/westerndigitalcorporation/libzbc
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_gtk:BuildRequires:	gtk+3-devel >= 3.0}
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libzbc is a simple library providing functions for manipulating SCSI
and ATA devices supporting the Zoned Block Command (ZBC) and
Zoned-device ATA command set (ZAC) specifications.

%description -l pl.UTF-8
libzbc to prosta biblioteka udostępniająca funkcje do operowania na
urządzeniach SCSI i ATA obsługujących specyfikacje ZBC (Zoned Block
Command - strefowych poleceń blokowych) i ZAC (Zoned-device ATA
Command - poleceń ATA urządzeń strefowych).

%package devel
Summary:	Header files for libzbc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libzbc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libzbc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libzbc.

%package static
Summary:	Static libzbc library
Summary(pl.UTF-8):	Statyczna biblioteka libzbc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libzbc library.

%description static -l pl.UTF-8
Statyczna biblioteka libzbc.

%package apidocs
Summary:	API documentation for libzbc library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libzbc
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libzbc library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libzbc.

%package gui
Summary:	GUI tools for libzbc
Summary(pl.UTF-8):	Narzędzia dla libzbc z graficznym interfejsem użytkownika
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gui
GUI tools for libzbc.

%description gui -l pl.UTF-8
Narzędzia dla libzbc z graficznym interfejsem użytkownika.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_gtk:--disable-gui} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with apidocs}
cd documentation
doxygen libzbc.doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzbc.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING.BSD README.md
%attr(755,root,root) %{_bindir}/zbc_*
%attr(755,root,root) %{_libdir}/libzbc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzbc.so.6
%{_mandir}/man8/zbc_*.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzbc.so
%{_includedir}/libzbc
%{_pkgconfigdir}/libzbc.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libzbc.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc documentation/html/{search,*.css,*.html,*.js,*.png}
%endif

%if %{with gtk}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gzbc
%attr(755,root,root) %{_bindir}/gzviewer
%{_datadir}/polkit-1/actions/org.gnome.gzbc.policy
%{_datadir}/polkit-1/actions/org.gnome.gzviewer.policy
%{_desktopdir}/gzbc.desktop
%{_desktopdir}/gzviewer.desktop
%{_pixmapsdir}/gzbc.png
%{_pixmapsdir}/gzviewer.png
%{_mandir}/man8/gzbc.8*
%{_mandir}/man8/gzviewer.8*
%endif
