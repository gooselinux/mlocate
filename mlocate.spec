Summary: An utility for finding files by name
Name: mlocate
Version: 0.22.2
Release: 3%{?dist}
License: GPLv2
URL: https://fedorahosted.org/mlocate/
Group: Applications/System
Source0: https://fedorahosted.org/releases/m/l/mlocate/mlocate-%{version}.tar.bz2
Source1: updatedb.conf
Source2: mlocate.cron
# Upstream changeset 87bcb87d48f939b851bdcf9580dfa89fe03438e7
Patch0: mlocate-0.22.2-noop-bind.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(pre): shadow-utils
Requires(triggerpostun): shadow-utils
Requires(post): grep, sed
Obsoletes: slocate <= 2.7-30

%description
mlocate is a locate/updatedb implementation.  It keeps a database of
all existing files and allows you to lookup files by name.

The 'm' stands for "merging": updatedb reuses the existing database to avoid
rereading most of the file system, which makes updatedb faster and does not
trash the system caches as much as traditional locate implementations.

%prep
%setup -q
%patch0 -p1 -b .noop-bind

%build
%configure --localstatedir=%{_localstatedir}/lib
make %{?_smp_mflags} groupname=slocate

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' groupname=slocate

mkdir -p $RPM_BUILD_ROOT{%{_sysconfdir},/etc/cron.daily}
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/updatedb.conf
install -p -m 755 %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/mlocate.cron
# %%ghost semantics is so stupid
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/mlocate/mlocate.db

%find_lang mlocate

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group slocate >/dev/null || groupadd -g 21 -r -f slocate
exit 0

%post
if /bin/grep -q '^[^#]*DAILY_UPDATE' %{_sysconfdir}/updatedb.conf; then
    /bin/sed -i.rpmsave -e '/DAILY_UPDATE/s/^/#/' %{_sysconfdir}/updatedb.conf
fi

%triggerpostun -- slocate <= 2.7-30
getent group slocate >/dev/null || groupadd -g 21 -r -f slocate
exit 0

%files -f mlocate.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
/etc/cron.daily/mlocate.cron
%config(noreplace) %{_sysconfdir}/updatedb.conf
%attr(2711,root,slocate) %{_bindir}/locate
%{_bindir}/updatedb
%{_mandir}/man*/*
%dir %attr(0750,root,slocate) %{_localstatedir}/lib/mlocate
%ghost %{_localstatedir}/lib/mlocate/mlocate.db

%changelog
* Tue Mar 30 2010 Miloslav Trmač <mitr@redhat.com> - 0.22.2-3
- Ignore no-op bind mounts
  Resolves: #577822

* Fri Jan 15 2010 Miloslav Trmač <mitr@redhat.com> - 0.22.2-2
- Add "lustre" to PRUNEFS
- Add all nodev filesystems from the Fedora kernel to PRUNEFS, to make
  (updatedb) work as some users expect
  Related: #543948

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.22.2-1.1
- Rebuilt for RHEL 6

* Fri Oct  2 2009 Miloslav Trmač <mitr@redhat.com> - 0.22.2-1
- Update to mlocate-0.22.2

* Tue Sep 15 2009 Miloslav Trmač <mitr@redhat.com> - 0.22.1-1
- Update to mlocate-0.22.1
- Drop Provides: slocate, per NamingGuidelines

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Miloslav Trmač <mitr@redhat.com> - 0.22-2
- Add /var/cache/ccache to PRUNEPATHS.

* Tue Apr 14 2009 Miloslav Trmač <mitr@redhat.com> - 0.22-1
- Update to mlocate-0.22

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Miloslav Trmač <mitr@redhat.com> - 0.21.1-3
- Merge review fixes, based on a patch by Parag AN:
  - Use %%{_localstatedir}/lib instead of hard-coding /var/lib
  - Use %%{?_smp_mflags}
  - Preserve file time stamps
  - Only create the group if it doesn't exist, hide errors from rpm

* Fri Nov 28 2008 Miloslav Trmač <mitr@redhat.com> - 0.21.1-2
- Add .git to PRUNENAMES
  Resolves: #473227
- Avoid a rpmlint warning

* Tue Oct 28 2008 Miloslav Trmač <mitr@redhat.com> - 0.21.1-1
- Update to mlocate-0.21
  Resolves: #461208

* Mon Jun 30 2008 Miloslav Trmač <mitr@redhat.com> - 0.21-1
- Update to mlocate-0.21
- Define PRUNENAMES to exclude .svn and .hg

* Wed Apr  9 2008 Miloslav Trmač <mitr@redhat.com> - 0.20-1
- Update to mlocate-0.20

* Mon Mar  3 2008 Miloslav Trmač <mitr@redhat.com> - 0.19-1
- Update to mlocate-0.19
- New home page at https://fedorahosted.org/mlocate/ .

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.18-2
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Miloslav Trmač <mitr@redhat.com> - 0.18-1
- Update to mlocate-0.18
- Run updatedb with reduced I/O priority
  Resolves: #254165

* Wed Apr 25 2007 Miloslav Trmac <mitr@redhat.com> - 0.17-1
- Update to mlocate-0.17
  Resolves: #237120

* Tue Mar  6 2007 Miloslav Trmac <mitr@redhat.com> - 0.16-1
- Update to mlocate-0.16
- Enable PRUNE_BIND_MOUNTS by default
  Resolves: #221755

* Fri Jan  5 2007 Miloslav Trmac <mitr@redhat.com> - 0.15-2
- Add gfs and gfs2 to PRUNEFS
  Resolves: #220491

* Thu Nov 16 2006 Miloslav Trmac <mitr@redhat.com> - 0.15-1
- Update to mlocate-0.15
  Resolves: #215763

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.14-2.1
- rebuild

* Sat Mar 18 2006 Miloslav Trmac <mitr@redhat.com> - 0.14-2
- Ship NEWS

* Sat Mar 18 2006 Miloslav Trmac <mitr@redhat.com> - 0.14-1
- Update to mlocate-0.14

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.12-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.12-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sat Dec 31 2005 Miloslav Trmac <mitr@redhat.com> - 0.12-1
- Update to mlocate-0.12

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Miloslav Trmac <mitr@redhat.com> - 0.11-2
- Comment out DAILY_UPDATE from updatedb.conf (#174693)

* Thu Nov 10 2005 Miloslav Trmac <mitr@redhat.com> - 0.11-1
- Update to mlocate-0.11
- Add scriptlets to create group slocate

* Thu Jul 28 2005 Miloslav Trmac <mitr@volny.cz> - 0.10-0.testing.1
- Update to mlocate-0.10

* Thu Jul 28 2005 Miloslav Trmac <mitr@volny.cz> - 0.09-0.testing.1
- Initial build.
