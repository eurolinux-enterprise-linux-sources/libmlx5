Name: libmlx5
Version: 1.0.2
Release: 1
Summary: Mellanox ConnectX-IB InfiniBand HCA Userspace Driver

Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://openfabrics.org/
Source: http://www.openfabrics.org/downloads/libmlx5-1.0.2.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: libibverbs-devel >= 1.1.8

%description
libmlx5 provides a device-specific userspace driver for Mellanox
ConnectX HCAs for use with the libibverbs library.

%package devel
Summary: Development files for the libmlx5 driver
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Provides: libmlx5-static = %{version}-%{release}

%description devel
Static version of libmlx5 that may be linked directly to an
application, which may be useful for debugging.

%prep
%setup -q -n %{name}-1.0.2

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{_libdir}/libmlx5.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libmlx5-rdmav2.so
%{_sysconfdir}/libibverbs.d/mlx5.driver
%doc AUTHORS COPYING README

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmlx5.a

%changelog
* Mon Mar 26 2012 Eli Cohen <eli@mellanox.com> - 1.0.0
- First version

