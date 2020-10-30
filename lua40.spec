#
# Conditional build:
%bcond_with	default_lua	# build as default lua (symlinks to nil suffix)
#
Summary:	A simple lightweight powerful embeddable programming language
Summary(pl.UTF-8):	Prosty, lekki ale potężny, osadzalny język programowania
Summary(pt_BR.UTF-8):	Lua é uma linguagem de programação poderosa e leve, projetada para estender aplicações.
Name:		lua40
Version:	4.0.1
%define refman_ver 4.0
Release:	12
License:	BSD-like (see docs)
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	a31d963dbdf727f9b34eee1e0d29132c
Source1:	http://www.lua.org/ftp/refman-%{refman_ver}.ps.gz
# Source1-md5:	5454698095c45917ce80c934066cb76c
Patch0:		lua-link.patch
Patch1:		lua-OPT.patch
URL:		http://www.lua.org/
Requires:	%{name}-libs = %{version}-%{release}
%if %{with default_lua}
Provides:	lua = %{version}
Obsoletes:	lua < %{version}
%endif
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

%description -l pl.UTF-8
Lua to język programowania o dużych możliwościach ale lekki,
przeznaczony do rozszerzania aplikacji. Jest też często używany jako
samodzielny język ogólnego przeznaczenia. Łączy prostą proceduralną
składnię (podobną do Pascala) z potężnymi konstrukcjami opisu danych
bazującymi na tablicach asocjacyjnych i rozszerzalnej składni. Lua ma
dynamiczny system typów, interpretowany z bytecodu i automatyczne
zarządzanie pamięcią z odśmiecaczem, co czyni go idealnym do
konfiguracji, skryptów i szybkich prototypów.

Ta wersja ma wkompilowaną obsługę ładowania dynamicznych bibliotek.

%description -l pt_BR.UTF-8
Lua é uma linguagem de programação poderosa e leve, projetada para
estender aplicações. Lua também é freqüentemente usada como uma
linguagem de propósito geral.
Lua combina programação procedural com poderosas construções para
descrição de dados, baseadas em tabelas associativas e semântica
extensível. Lua é tipada dinamicamente, interpretada a partir de
bytecodes, e tem gerenciamento automático de memória com coleta de
lixo. Essas características fazem de Lua uma linguagem ideal para
configuração, automação (scripting) e prototipagem rápida.

%package libs
Summary:	Lua 4.0.x shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Lua 4.0.x
Group:		Libraries
Conflicts:	lua40 < 4.0.1-7

%description libs
Lua 4.0.x shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone Lua 4.0.x.

%package devel
Summary:	Header files for Lua
Summary(pl.UTF-8):	Pliki nagłówkowe dla Lua
Summary(pt_BR.UTF-8):	Arquivos de cabeçalho para a linguagem Lua
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Provides:	lua-devel = %{version}
Obsoletes:	lua-devel <= 4.0.1

%description devel
Header files needed to embed Lua in C/C++ programs and docs for the
language.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do włączenia Lua do programów w C/C++ oraz
dokumentacja samego języka.

%description devel -l pt_BR.UTF-8
Contém os arquivos de cabeçalho para desenvolvimento e extensão da
linguagem Lua.

%package static
Summary:	Static Lua libraries
Summary(pl.UTF-8):	Biblioteki statyczne Lua
Summary(pt_BR.UTF-8):	Bibliotecas estáticas para desenvolvimento com a linguagem Lua
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}
%if %{with default_lua}
Provides:	lua-static = %{version}
Obsoletes:	lua-static < %{version}
%endif

%description static
Static Lua libraries.

%description static -l pl.UTF-8
Biblioteki statyczne Lua.

%description static -l pt_BR.UTF-8
Bibliotecas estáticas para desenvolvimento com a linguagem Lua.

%prep
%setup -q -n lua-%{version}
cp -f %{SOURCE1} refman.ps.gz

%patch0 -p1
%patch1 -p1

%build
%{__make} -j1 all so sobin \
	CC="%{__cc}" \
	OPT="%{rpmcflags}" \
	EXTRA_DEFS="-fPIC -DPIC -D_GNU_SOURCE"

%{__rm} test/{lua,luac}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/lua,%{_datadir}/lua}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir}/lua4.0 \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1

# change name from lua to lua4.0
for i in $RPM_BUILD_ROOT%{_bindir}/lua* ; do
	%{__mv} ${i}{,4.0}
done
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/lua{,4.0}.1
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/luac{,4.0}.1
%{__mv} $RPM_BUILD_ROOT%{_libdir}/liblua{,4.0}.a
%{__mv} $RPM_BUILD_ROOT%{_libdir}/liblualib{,4.0}.a

ln -sf liblua.so.4.0 $RPM_BUILD_ROOT%{_libdir}/liblua4.0.so
ln -sf liblualib.so.4.0 $RPM_BUILD_ROOT%{_libdir}/liblualib4.0.so

%if %{with default_lua}
for f in lua luac ; do
	ln -sf ${f}4.0 $RPM_BUILD_ROOT%{_bindir}/${f}
	echo ".so ${f}4.0.1" >$RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
done
ln -sf liblua4.0.a $RPM_BUILD_ROOT%{_libdir}/liblua.a
ln -sf liblualib4.0.a $RPM_BUILD_ROOT%{_libdir}/liblualib.a
ln -sf lua4.0 $RPM_BUILD_ROOT%{_includedir}/lua
%else
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{lua,lualib}.so
%endif

%{__rm} doc/*.1

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lua4.0
%attr(755,root,root) %{_bindir}/luac4.0
%{_mandir}/man1/lua4.0.1*
%{_mandir}/man1/luac4.0.1*
%if %{with default_lua}
%attr(755,root,root) %{_bindir}/lua
%attr(755,root,root) %{_bindir}/luac
%{_mandir}/man1/lua.1*
%{_mandir}/man1/luac.1*
%endif

%files libs
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY README
%attr(755,root,root) %{_libdir}/liblua.so.4.0
%attr(755,root,root) %{_libdir}/liblualib.so.4.0

%files devel
%defattr(644,root,root,755)
%doc refman.ps.gz doc test
%attr(755,root,root) %{_libdir}/liblua4.0.so
%attr(755,root,root) %{_libdir}/liblualib4.0.so
%{_includedir}/lua4.0
%if %{with default_lua}
%attr(755,root,root) %{_libdir}/liblua.so
%attr(755,root,root) %{_libdir}/liblualib.so
%{_includedir}/lua
%endif

%files static
%defattr(644,root,root,755)
%{_libdir}/liblua4.0.a
%{_libdir}/liblualib4.0.a
%if %{with default_lua}
%{_libdir}/liblua.a
%{_libdir}/liblualib.a
%endif
