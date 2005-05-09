%define _refman_version 4.0
Summary:	A simple lightweight powerful embeddable programming language
Summary(pl):	Prosty, lekki ale potê¿ny, osadzalny jêzyk programowania
Summary(pt_BR):	Lua é uma linguagem de programação poderosa e leve, projetada para estender aplicações.
Name:		lua40
Version:	4.0.1
Release:	10
License:	BSD-like (see docs)
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	a31d963dbdf727f9b34eee1e0d29132c
Source1:	http://www.lua.org/ftp/refman-%{_refman_version}.ps.gz
# Source1-md5:	5454698095c45917ce80c934066cb76c
Patch0:		lua-link.patch
Patch1:		lua-OPT.patch
URL:		http://www.lua.org/
Requires:	%{name}-libs = %{version}-%{release}
Provides:	lua = %{version}
Obsoletes:	lua <= 4.0.1
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
Lua to jêzyk programowania o du¿ych mo¿liwo¶ciach ale lekki,
przeznaczony do rozszerzania aplikacji. Jest te¿ czêsto u¿ywany jako
samodzielny jêzyk ogólnego przeznaczenia. £±czy prost± proceduraln±
sk³adniê (podobn± do Pascala) z potê¿nymi konstrukcjami opisu danych
bazuj±cymi na tablicach asocjacyjnych i rozszerzalnej sk³adni. Lua ma
dynamiczny system typów, interpretowany z bytecodu i automatyczne
zarz±dzanie pamiêci± z od¶miecaczem, co czyni go idealnym do
konfiguracji, skryptów i szybkich prototypów.

Ta wersja ma wkompilowan± obs³ugê ³adowania dynamicznych bibliotek.

%description -l pt_BR
Lua é uma linguagem de programação poderosa e leve, projetada para estender
aplicações. Lua também é freqüentemente usada como uma linguagem de propósito
geral.
Lua combina programação procedural com poderosas construções para descrição
de dados, baseadas em tabelas associativas e semântica extensível. Lua é
tipada dinamicamente, interpretada a partir de bytecodes, e tem gerenciamento
automático de memória com coleta de lixo. Essas características fazem de Lua
uma linguagem ideal para configuração, automação (scripting) e prototipagem
rápida.

%package libs
Summary:	lua 4.0.x libraries
Summary(pl):	Biblioteki lua 4.0.x
Group:		Development/Languages
Conflicts:	lua40 < 4.0.1-7

%description libs
lua 4.0.x libraries.

%description libs -l pl
Biblioteki lua 4.0.x.

%package devel
Summary:	Header files for Lua
Summary(pl):	Pliki nag³ówkowe dla Lua
Summary(pt_BR):	Arquivos de cabeçalho para a linguagem Lua
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Provides:	lua-devel = %{version}
Obsoletes:	lua-devel <= 4.0.1

%description devel
Header files needed to embed Lua in C/C++ programs and docs for the
language.

%description devel -l pl
Pliki nag³ówkowe potrzebne do w³±czenia Lua do programów w C/C++ oraz
dokumentacja samego jêzyka.

%description devel -l pt_BR
Contém os arquivos de cabeçalho para desenvolvimento e
extensão da linguagem Lua.

%package static
Summary:	Static Lua libraries Lua
Summary(pl):	Biblioteki statyczne Lua
Summary(pt_BR):	Bibliotecas estáticas para desenvolvimento com a linguagem Lua
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}
Provides:	lua-static = %{version}
Obsoletes:	lua-static <= 4.0.1

%description static
Static Lua libraries.

%description static -l pl
Biblioteki statyczne Lua.

%description static -l pt_BR
Bibliotecas estáticas para desenvolvimento com a linguagem Lua

%prep
%setup -q -n lua-%{version}
cp -f %{SOURCE1} refman.ps.gz

%patch0 -p1
%patch1 -p1

%build
%{__make} all so sobin \
	OPT="%{rpmcflags}" \
	EXTRA_DEFS="-fPIC -DPIC -D_GNU_SOURCE"

rm -f test/{lua,luac}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/lua,%{_datadir}/lua}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir}/lua40 \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1

# change name from lua to lua40
for i in $RPM_BUILD_ROOT%{_bindir}/* ; do mv $i{,40} ; done
mv $RPM_BUILD_ROOT%{_libdir}/liblua{,40}.a
mv $RPM_BUILD_ROOT%{_libdir}/liblualib{,40}.a
mv $RPM_BUILD_ROOT%{_mandir}/man1/lua{,40}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/luac{,40}.1

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.so
ln -s liblua.so.4.0 $RPM_BUILD_ROOT%{_libdir}/liblua40.so
ln -s liblualib.so.4.0 $RPM_BUILD_ROOT%{_libdir}/liblualib40.so
rm -f doc/*.1

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY README
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc refman.ps.gz doc test
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/lua40

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
