%define _refman_version 4.0
Summary:	A simple lightweight powerful embeddable programming language
Summary(pl):	Prosty, lekki ale pot�ny, osadzalny j�zyk programowania
Name:		lua
Version:	4.0.1
Release:	1
License:	BSD-like (see docs)
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/%{name}-%{version}.tar.gz
Source1:	http://www.lua.org/ftp/refman-%{_refman_version}.ps.gz
Patch1:		%{name}-OPT.patch
URL:		http://www.lua.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lua is a powerful, light-weight programming language designed for
extending applications. It is also frequently used as a
general-purpose, stand-alone language. It combines simple procedural
syntax (similar to Pascal) with powerful data description constructs
based on associative arrays and extensible semantics. Lua is
dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

This version has compiled in support for dynamic libraries in baselib.

%description -l pl
Lua to j�zyk programowania o du�ych mo�liwo�ciach ale lekki,
przeznaczony do rozszerzania aplikacji. Jest te� cz�sto u�ywany jako
samodzielny j�zyk og�lnego przeznaczenia. ��czy prost� proceduraln�
sk�adni� (podobn� do Pascala) z pot�nymi konstrukcjami opisu danych
bazuj�cymi na tablicach asocjacyjnych i rozszerzalnej sk�adni. Lua ma
dynamiczny system typ�w, interpretowany z bytecodu i automatyczne
zarz�dzanie pami�ci� z od�miecaczem, co czyni go idealnym do
konfiguracji, skrypt�w i szybkich prototyp�w.

Ta wersja ma wkompilowan� obs�ug� �adowania dynamicznych bibliotek.

%package devel
Summary:	Header files for Lua
Summary(pl):	Pliki nag��wkowe dla Lua
Group:		Development/Languages
Requires:	%{name} = %{version}

%description devel
Header files needed to embed Lua in C/C++ programs and docs for the
language.

%description devel -l pl
Pliki nag��wkowe potrzebne do w��czenia Lua do program�w w C/C++ oraz
dokumentacja samego j�zyka.

%package static
Summary:	Static Lua libraries Lua
Summary(pl):	Biblioteki statyczne Lua
Group:		Development/Languages
Requires:	%{name}-devel = %{version}

%description static
Static Lua libraries.

%description static -l pl
Biblioteki statyczne Lua.

%prep
%setup -q 
cp -f %{SOURCE1} refman.ps.gz

%patch0 -p1
%patch1 -p1

%build
%{__make} OPT="%{rpmcflags}" \
          EXTRA_DEFS="-fPIC -DPIC -D_GNU_SOURCE" \
	  all so sobin
rm -f test/{lua,luac}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/lua,%{_datadir}/lua}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir} \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1

rm -f doc/*.1

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%dir %{_libdir}/lua
%dir %{_datadir}/lua
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY refman.ps.gz doc test
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
