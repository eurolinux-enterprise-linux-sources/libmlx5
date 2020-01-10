Name: libmlx5
Version: 1.0.1
Release: 3%{?dist}
Summary: Mellanox Connect-IB InfiniBand HCA Userspace Driver
Provides: libibverbs-driver.%{_arch}
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/mlx5/%{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: libibverbs-devel > 1.1.5
%ifnarch ia64 %{sparc} %{arm}
BuildRequires: valgrind-devel
%endif
Requires: rdma
ExcludeArch: s390 s390x

%description
libmlx5 provides a device-specific userspace driver for Mellanox
Connect-IB HCAs for use with the libibverbs library.

%package static
Summary: Static version of the libmlx4 driver
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description static
Static version of libmlx4 that may be linked directly to an
application, which may be useful for debugging.

%prep
%setup -q

%build
%ifnarch ia64 %{sparc} %{arm}
%configure --with-valgrind
%else
%configure
%endif
make CFLAGS="$CFLAGS -fno-strict-aliasing" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# Remove unpackaged files
rm -f %{buildroot}%{_libdir}/libmlx5.{la,so}

%files
%defattr(-,root,root,-)
%{_libdir}/libmlx5-rdmav2.so
%{_sysconfdir}/libibverbs.d/mlx5.driver
%doc AUTHORS COPYING README

%files static
%defattr(-,root,root,-)
%{_libdir}/libmlx5.a

%changelog
* Tue Dec 23 2014 Doug Ledford <dledford@redhat.com> - 1.0.2-3
- Add Requires on rdma
- Related: bz1164618

* Fri Oct 17 2014 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Bump and rebuild against latest libibverbs
- Related: bz1137044

* Fri Feb 28 2014 Doug Ledford <dledford@redhat.com> - 1.0.1-1
- Update to latest upstream release
- Remove files related to setting ports to Ethernet mode as that
  isn't even supported on this card yet and the files that are
  there will be wrong when it is supported
- Resolves: bz1061584

* Thu Jan  9 2014 Daniel Mach <dmach@redhat.com> - 1.0.0-2
- Mass rebuild 2013-12-27

* Thu Sep 12 2013 Doug Ledford <dledford@redhat.com> - 1.0.0-1
- Initial import of upstream package
