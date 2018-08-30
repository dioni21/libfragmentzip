#
# specfile to build libfragmentzip
#

# Download source with: spectool -g -R libfragmentzip.spec

%define         version         1.0.0
%define         github_user     dioni21
%define         git_tag         v%{version}

%{!?tag:        %global tag         %{git_tag}}

Name:           libfragmentzip
Version:        %{version}
Release:        1%{?dist}
Summary:        Library for connecting to mobile devices

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.libimobiledevice.org/
Source0:        https://github.com/%{github_user}/%{name}/archive/%{git_tag}.tar.gz#/%{name}-%{version}.tar.gz

Requires:       libzip >= 0.9
Requires:       libcurl >= 1.0
Requires:       zlib

BuildRequires:  libzip-devel >= 0.9
BuildRequires:  libcurl-devel >= 1.0
BuildRequires:  zlib-devel
BuildRequires:  git-core
BuildRequires:  autoconf automake libtool
BuildRequires:  /usr/bin/pkg-config

%{lua:
  handle = io.popen(string.format('tar tfz %s|head -1',rpm.expand('%{S:0}')))
  rootdir = handle:read('*a')
  internal_id = rootdir:match('-([a-f0-9.]+)/')
  handle:close()
  rpm.define(string.format("internal_id %s",internal_id))
}


%description
libfragmentzip is a library allowing to download single files from a remote zip archive


%package devel
Summary:        Development package for libfragmentzip
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with libfragmentzip.


%prep
%autosetup -n %{name}-%{internal_id}

# This is needed to build for CentOS 6
sed -i -e 's/libzip >= 1.0/libzip >= 0.9/' libfragmentzip.pc.in configure.ac

%build
./autogen.sh
%configure --prefix=/usr --disable-silent-rules

# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc AUTHORS COPYING
%{_libdir}/libfragmentzip.so.0*

%files devel
%{_libdir}/pkgconfig/libfragmentzip.pc
%{_libdir}/libfragmentzip.so
%{_libdir}/libfragmentzip.a
%{_includedir}/libfragmentzip/


%changelog
* Fri Aug 31 2018 João Carlos Mendes Luís <jonny@jonny.eng.br> - 1.0
- First RPM spec, made for Fedora COPR

# EOF
