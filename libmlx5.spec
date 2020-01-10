Name: libmlx5
Version: 1.2.1
Release: 8%{?dist}
Summary: Mellanox Connect-IB InfiniBand HCA Userspace Driver
Provides: libibverbs-driver.%{_arch}
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/mlx5/%{name}-%{version}.tar.gz
# Posted as a 6-part series on linux-rdma@vger.kernel.org on 2016.07.27
Patch1: libmlx5-1.2.1-coverity-fixes.patch
Patch2: 0001-Fix-return-value-of-mlx5_post_send-to-be-aligned-wit.patch
Patch3: 0002-Fix-return-value-of-mlx5_post_recv-srq_recv-to-be-al.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: libibverbs >= 1.2.1
BuildRequires: libibverbs-devel >= 1.2.1
%ifnarch ia64 %{sparc} %{arm}
BuildRequires: valgrind-devel
%endif
Requires: rdma
ExcludeArch: s390 s390x

%description
libmlx5 provides a device-specific userspace driver for Mellanox
Connect-IB HCAs for use with the libibverbs library.

%package static
Summary: Static version of the libmlx5 driver
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description static
Static version of libmlx5 that may be linked directly to an
application, which may be useful for debugging.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
* Thu Aug 11 2016 Jarod Wilson <jarod@redhat.com> - 1.2.1-8
- Take upstream version of mlx5_post_send fix with expanded fixes
- Related: rhbz#1364525

* Fri Aug 05 2016 Jarod Wilson <jarod@redhat.com> - 1.2.1-7
- Fix mlx5_post_send incompatibility with ibv_post_send ABI
- Add explicit Requires: on libibverbs >= 1.2.1
- Resolves: rhbz#1364525

* Wed Aug 03 2016 Jarod Wilson <jarod@redhat.com> - 1.2.1-6
- Sync coverity fixes with what upstream is taking in

* Thu Jul 28 2016 Jarod Wilson <jarod@redhat.com> - 1.2.1-5
- Last-ditch attempt at getting buffer overrun fix correct

* Thu Jul 28 2016 Jarod Wilson <jarod@redhat.com> - 1.2.1-4
- Further rework of coverity fixes based on upstream feedback

* Wed Jul 27 2016 Jarod Wilson <jarod@redhat.com> - 1.2.1-3
- Rework two of the coverity fixups with improved versions

* Wed Jul 27 2016 Jarod Wilson <jarod@redhat.com> - 1.2.1-2
- Fix several issues reported by coverity scan of v1.2.1

* Wed Jul 20 2016 Jarod Wilson <jarod@redhat.com> - 1.2.1-1
- Update to upstream release v1.2.1
- This is libmlx5, not libmlx4, fix descriptions accordingly
- Resolves: bz1298698, bz1275412, bz1275396, bz1296267, bz1296186, bz1288821

* Fri Jul 17 2015 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Fix changelog versions
- Update to latest upstream release
- Resolves: bz1164544

* Tue Dec 23 2014 Doug Ledford <dledford@redhat.com> - 1.0.1-3
- Add Requires on rdma
- Related: bz1164618

* Fri Oct 17 2014 Doug Ledford <dledford@redhat.com> - 1.0.1-2
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
