%undefine _hardened_build

# Modules always contain just 32-bit code
%define _libdir %{_exec_prefix}/lib

# 64bit intel machines use 32bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%endif
# sparc is always compiled 64 bit
%ifarch %{sparc}
%define _target_platform sparc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif

%if ! 0%{?efi}

%global efi_only aarch64
%global efiarchs %{ix86} x86_64 ia64 %{efi_only}

%ifarch %{ix86}
%global grubefiarch i386-efi
%global grubefiname grubia32.efi
%global grubeficdname gcdia32.efi
%endif
%ifarch x86_64
%global grubefiarch %{_arch}-efi
%global grubefiname grubx64.efi
%global grubeficdname gcdx64.efi
%endif
%ifarch aarch64
%global grubefiarch arm64-efi
%global grubefiname grubaa64.efi
%global grubeficdname gcdaa64.efi
%endif

# Figure out the right file path to use
%global efidir %(eval echo $(grep ^ID= /etc/os-release | sed -e 's/^ID=//' -e 's/rhel/redhat/'))

%endif

%global tarversion 2.02~beta3
%undefine _missing_build_ids_terminate_build

Name:           grub2
Epoch:          1
Version:        2.02
Release:        0.38%{?dist}
Summary:        Bootloader with support for Linux, Multiboot and more

Group:          System Environment/Base
License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
Obsoletes:	grub < 1:0.98
Source0:        ftp://alpha.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
#Source0:	ftp://ftp.gnu.org/gnu/grub/grub-%%{tarversion}.tar.xz
Source4:	http://unifoundry.com/unifont-5.1.20080820.pcf.gz
Source5:	theme.tar.bz2
Source6:	gitignore
Source7:	grub.patches

# generate with do-rebase
%include %{SOURCE7}

# And these are:
# git checkout debuginfo
# git format-patch fedora-23..
Patch10001: 10001-Put-the-correct-.file-directives-in-our-.S-files.patch
Patch10002: 10002-Make-it-possible-to-enabled-build-id-sha1.patch
#Patch10003: 10003-Don-t-tell-the-compiler-to-do-annoying-things-with-.patch
Patch10004: 10004-Add-grub_qdprintf-grub_dprintf-without-the-file-lin.patch
Patch10005: 10005-Make-a-gdb-dprintf-that-tells-us-load-addresses.patch
#Patch10006: 10006-Try-it-in-gentpl-again.patch

BuildRequires:  flex bison binutils python
BuildRequires:  ncurses-devel xz-devel bzip2-devel
BuildRequires:  freetype-devel libusb-devel
BuildRequires:	rpm-devel
%ifarch %{sparc} x86_64 aarch64 ppc64le
# sparc builds need 64 bit glibc-devel - also for 32 bit userland
BuildRequires:  /usr/lib64/crt1.o glibc-static
%else
# ppc64 builds need the ppc crt1.o
BuildRequires:  /usr/lib/crt1.o glibc-static
%endif
BuildRequires:  autoconf automake autogen device-mapper-devel
BuildRequires:	freetype-devel gettext-devel git
BuildRequires:	texinfo
BuildRequires:	dejavu-sans-fonts
BuildRequires:	help2man
%ifarch %{efiarchs}
%ifnarch aarch64
BuildRequires:	pesign >= 0.99-8
%endif
%endif

Requires:	gettext which file
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}
Requires:	os-prober >= 1.58-11
Requires(pre):  dracut
Requires(post): dracut

ExcludeArch:	s390 s390x %{arm}
Obsoletes:	grub2 <= 1:2.00-20%{?dist}

%description
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for PC BIOS systems.

%ifarch %{efiarchs}
%package efi
Summary:	GRUB for EFI systems.
Group:		System Environment/Base
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}
Obsoletes:	grub2-efi <= 1:2.00-20%{?dist}

%description efi
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for EFI systems.

%package efi-modules
Summary:	Modules used to build custom grub.efi images
Group:		System Environment/Base
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}
Obsoletes:	grub2-efi <= 1:2.00-20%{?dist}

%description efi-modules
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for rebuilding your own grub.efi on EFI systems.
%endif

%package tools
Summary:	Support tools for GRUB.
Group:		System Environment/Base
Requires:	gettext os-prober which file system-logos

%description tools
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides tools for support of all platforms.

%package starfield-theme
Summary:	An example theme for GRUB.
Group:		System Environment/Base
Requires:	system-logos
Obsoletes:	grub2 <= 1:2.00-20%{?dist}
Obsoletes:	grub2-efi <= 1:2.00-20%{?dist}

%description starfield-theme
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides an example theme for the grub screen.

%prep
%setup -T -c -n grub-%{tarversion}
%ifarch %{efiarchs}
%setup -D -q -T -a 0 -n grub-%{tarversion}
cd grub-%{tarversion}
# place unifont in the '.' from which configure is run
cp %{SOURCE4} unifont.pcf.gz
cp %{SOURCE6} .gitignore
git init
echo '![[:digit:]][[:digit:]]_*.in' > util/grub.d/.gitignore
echo '!*.[[:digit:]]' > util/.gitignore
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git config gc.auto 0
git add .
git commit -a -q -m "%{tarversion} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name
cd ..
mv grub-%{tarversion} grub-efi-%{tarversion}
%endif

%ifarch %{efi_only}
ln -s grub-efi-%{tarversion} grub-%{tarversion}
%else
%setup -D -q -T -a 0 -n grub-%{tarversion}
cd grub-%{tarversion}
# place unifont in the '.' from which configure is run
cp %{SOURCE4} unifont.pcf.gz
cp %{SOURCE6} .gitignore
git init
echo '![[:digit:]][[:digit:]]_*.in' > util/grub.d/.gitignore
echo '!*.[[:digit:]]' > util/.gitignore
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git config gc.auto 0
git add .
git commit -a -q -m "%{tarversion} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name
%endif

%build
%ifarch %{efiarchs}
cd grub-efi-%{tarversion}
./autogen.sh
%configure							\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed			\
		-e 's/-O.//g'					\
		-e 's/-fstack-protector[[:alpha:]-]\+//g'	\
		-e 's/-Wp,-D_FORTIFY_SOURCE=[[:digit:]]\+//g'	\
		-e 's/--param=ssp-buffer-size=4//g'		\
		-e 's/-mregparm=3/-mregparm=4/g'		\
		-e 's/-fexceptions//g'				\
		-e 's/-fasynchronous-unwind-tables//g'		\
		-e 's/^/ -fno-strict-aliasing /' )"		\
	TARGET_LDFLAGS=-static					\
        --with-platform=efi					\
	--with-grubdir=%{name}					\
        --program-transform-name=s,grub,%{name},		\
	--disable-grub-mount					\
	--disable-werror
make %{?_smp_mflags}

GRUB_MODULES="	all_video boot btrfs cat chain configfile echo \
		efifwsetup efinet ext2 fat font gfxmenu gfxterm gzio halt \
		hfsplus iso9660 jpeg loadenv loopback lvm mdraid09 mdraid1x \
		minicmd normal part_apple part_msdos part_gpt \
		password_pbkdf2 png \
		reboot search search_fs_uuid search_fs_file search_label \
		serial sleep syslinuxcfg test tftp video xfs"
%ifarch aarch64
GRUB_MODULES+=" linux "
%else
GRUB_MODULES+=" backtrace usb usbserial_common "
GRUB_MODULES+=" usbserial_pl2303 usbserial_ftdi usbserial_usbdebug "
GRUB_MODULES+=" linuxefi"
%endif
./grub-mkimage -O %{grubefiarch} -o %{grubefiname}.orig -p /EFI/%{efidir} \
		-d grub-core ${GRUB_MODULES}
./grub-mkimage -O %{grubefiarch} -o %{grubeficdname}.orig -p /EFI/BOOT \
		-d grub-core ${GRUB_MODULES}
%ifarch aarch64
mv %{grubefiname}.orig %{grubefiname}
mv %{grubeficdname}.orig %{grubeficdname}
%else
%pesign -s -i %{grubeficdname}.orig -o %{grubeficdname}
%pesign -s -i %{grubefiname}.orig -o %{grubefiname}
%endif
cd ..
%endif

cd grub-%{tarversion}
%ifnarch %{efi_only}
./autogen.sh
# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
%ifarch %{sparc} ppc ppc64 ppc64le
%define platform ieee1275
%else
%define platform pc
%endif
%configure							\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed			\
		-e 's/-O.//g'					\
		-e 's/-fstack-protector[[:alpha:]-]\+//g'	\
		-e 's/-Wp,-D_FORTIFY_SOURCE=[[:digit:]]\+//g'	\
		-e 's/--param=ssp-buffer-size=4//g'		\
		-e 's/-mregparm=3/-mregparm=4/g'		\
		-e 's/-fexceptions//g'				\
		-e 's/-m64//g'					\
		-e 's/-fasynchronous-unwind-tables//g'		\
		-e 's/-mcpu=power[[:alnum:]]\+/-mcpu=power6/g'	\
		-e 's/^/ -fno-strict-aliasing /' )"		\
	TARGET_LDFLAGS=-static					\
        --with-platform=%{platform}				\
	--with-grubdir=%{name}					\
        --program-transform-name=s,grub,%{name},		\
	--disable-grub-mount					\
	--disable-werror

make %{?_smp_mflags}
%endif

sed -i -e 's,(grub),(%{name}),g' \
	-e 's,grub.info,%{name}.info,g' \
	-e 's,\* GRUB:,* GRUB2:,g' \
	-e 's,/boot/grub/,/boot/%{name}/,g' \
	-e 's,\([^-]\)grub-\([a-z]\),\1%{name}-\2,g' \
	docs/grub.info
sed -i -e 's,grub-dev,%{name}-dev,g' docs/grub-dev.info

/usr/bin/makeinfo --html --no-split -I docs -o grub-dev.html docs/grub-dev.texi
/usr/bin/makeinfo --html --no-split -I docs -o grub.html docs/grub.texi
sed -i	-e 's,/boot/grub/,/boot/%{name}/,g' \
	-e 's,\([^-]\)grub-\([a-z]\),\1%{name}-\2,g' \
	grub.html

%install
set -e
rm -fr $RPM_BUILD_ROOT

%ifarch %{efiarchs}
cd grub-efi-%{tarversion}
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -iname "*.module" -exec chmod a-x {} \;

# Ghost config file
install -m 755 -d $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/
touch $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/grub.cfg
ln -s ../boot/efi/EFI/%{efidir}/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-efi.cfg

install -m 755 %{grubefiname} $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/%{grubefiname}
install -m 755 %{grubeficdname} $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/%{grubeficdname}
install -D -m 644 unicode.pf2 $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/fonts/unicode.pf2
cd ..
%endif

cd grub-%{tarversion}
%ifnarch %{efi_only}
make DESTDIR=$RPM_BUILD_ROOT install

# Ghost config file
install -d $RPM_BUILD_ROOT/boot/%{name}
touch $RPM_BUILD_ROOT/boot/%{name}/grub.cfg
ln -s ../boot/%{name}/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.cfg
%endif

cp -a $RPM_BUILD_ROOT%{_datarootdir}/locale/en\@quot $RPM_BUILD_ROOT%{_datarootdir}/locale/en

mv $RPM_BUILD_ROOT%{_infodir}/grub.info $RPM_BUILD_ROOT%{_infodir}/%{name}.info
mv $RPM_BUILD_ROOT%{_infodir}/grub-dev.info $RPM_BUILD_ROOT%{_infodir}/%{name}-dev.info
rm $RPM_BUILD_ROOT%{_infodir}/dir

# Defaults
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/default
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/default/grub
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub \
	${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/grub

cd ..
%find_lang grub

# Fedora theme in /boot/grub2/themes/system/
cd $RPM_BUILD_ROOT
tar xjf %{SOURCE5}
$RPM_BUILD_ROOT%{_bindir}/%{name}-mkfont -o boot/grub2/themes/system/DejaVuSans-10.pf2      -s 10 /usr/share/fonts/dejavu/DejaVuSans.ttf # "DejaVu Sans Regular 10"
$RPM_BUILD_ROOT%{_bindir}/%{name}-mkfont -o boot/grub2/themes/system/DejaVuSans-12.pf2      -s 12 /usr/share/fonts/dejavu/DejaVuSans.ttf # "DejaVu Sans Regular 12"
$RPM_BUILD_ROOT%{_bindir}/%{name}-mkfont -o boot/grub2/themes/system/DejaVuSans-Bold-14.pf2 -s 14 /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf # "DejaVu Sans Bold 14"

# Make selinux happy with exec stack binaries.
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/
cat << EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/grub2.conf
# these have execstack, and break under selinux
-b /usr/bin/grub2-script-check
-b /usr/bin/grub2-mkrelpath
-b /usr/bin/grub2-fstest
-b /usr/sbin/grub2-bios-setup
-b /usr/sbin/grub2-probe
-b /usr/sbin/grub2-sparc64-setup
EOF

%ifarch %{efiarchs}
mkdir -p boot/efi/EFI/%{efidir}/
ln -s /boot/efi/EFI/%{efidir}/grubenv boot/grub2/grubenv
%endif

# Don't run debuginfo on all the grub modules and whatnot; it just
# rejects them, complains, and slows down extraction.
%global finddebugroot "%{_builddir}/%{?buildsubdir}/debug"
mkdir -p %{finddebugroot}/usr
cp -a ${RPM_BUILD_ROOT}/usr/bin %{finddebugroot}/usr/bin
cp -a ${RPM_BUILD_ROOT}/usr/sbin %{finddebugroot}/usr/sbin

%global dip RPM_BUILD_ROOT=%{finddebugroot} %{__debug_install_post}
%define __debug_install_post ( %{dip}					\
	install -m 0755 -d %{buildroot}/usr/lib/ %{buildroot}/usr/src/	\
	cp -al %{finddebugroot}/usr/lib/debug/				\\\
		%{buildroot}/usr/lib/debug/				\
	cp -al %{finddebugroot}/usr/src/debug/				\\\
		%{buildroot}/usr/src/debug/ )

%clean    
rm -rf $RPM_BUILD_ROOT

%pre tools
if [ -f /boot/grub2/user.cfg ]; then
    if grep -q '^GRUB_PASSWORD=' /boot/grub2/user.cfg ; then
	sed -i 's/^GRUB_PASSWORD=/GRUB2_PASSWORD=/' /boot/grub2/user.cfg
    fi
elif [ -f /boot/efi/EFI/%{efidir}/user.cfg ]; then
    if grep -q '^GRUB_PASSWORD=' /boot/efi/EFI/%{efidir}/user.cfg ; then
	sed -i 's/^GRUB_PASSWORD=/GRUB2_PASSWORD=/' \
	    /boot/efi/EFI/%{efidir}/user.cfg
    fi
elif [ -f /etc/grub.d/01_users ] && \
	grep -q '^password_pbkdf2 root' /etc/grub.d/01_users ; then
    if [ -f /boot/efi/EFI/%{efidir}/grub.cfg ]; then
	# on EFI we don't get permissions on the file, but
	# the directory is protected.
	grep '^password_pbkdf2 root' /etc/grub.d/01_users | \
		sed 's/^password_pbkdf2 root \(.*\)$/GRUB2_PASSWORD=\1/' \
	    > /boot/efi/EFI/%{efidir}/user.cfg
    fi
    if [ -f /boot/grub2/grub.cfg ]; then
	install -m 0600 /dev/null /boot/grub2/user.cfg
	chmod 0600 /boot/grub2/user.cfg
	grep '^password_pbkdf2 root' /etc/grub.d/01_users | \
		sed 's/^password_pbkdf2 root \(.*\)$/GRUB2_PASSWORD=\1/' \
	    > /boot/grub2/user.cfg
    fi
fi

%post tools
if [ "$1" = 1 ]; then
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz || :
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/%{name}-dev.info.gz || :
fi

%triggerun -- grub2 < 1:1.99-4
# grub2 < 1.99-4 removed a number of essential files in postun. To fix upgrades
# from the affected grub2 packages, we first back up the files in triggerun and
# later restore them in triggerpostun.
# https://bugzilla.redhat.com/show_bug.cgi?id=735259

# Back up the files before uninstalling old grub2
mkdir -p /boot/grub2.tmp &&
mv -f /boot/grub2/*.mod \
      /boot/grub2/*.img \
      /boot/grub2/*.lst \
      /boot/grub2/device.map \
      /boot/grub2.tmp/ || :

%triggerpostun -- grub2 < 1:1.99-4
# ... and restore the files.
test ! -f /boot/grub2/device.map &&
test -d /boot/grub2.tmp &&
mv -f /boot/grub2.tmp/*.mod \
      /boot/grub2.tmp/*.img \
      /boot/grub2.tmp/*.lst \
      /boot/grub2.tmp/device.map \
      /boot/grub2/ &&
rm -r /boot/grub2.tmp/ || :

%preun tools
if [ "$1" = 0 ]; then
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz || :
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}-dev.info.gz || :
fi

%ifnarch %{efi_only}
%files -f grub.lang
%defattr(-,root,root,-)
%{_libdir}/grub/*-%{platform}/
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%ghost %config(noreplace) /boot/%{name}/grub.cfg
%doc grub-%{tarversion}/COPYING
%config(noreplace) %ghost /boot/grub2/grubenv
%endif

%ifarch %{efiarchs}
%files efi
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}-efi.cfg
%attr(0755,root,root)/boot/efi/EFI/%{efidir}
%attr(0755,root,root)/boot/efi/EFI/%{efidir}/fonts
%ghost %config(noreplace) /boot/efi/EFI/%{efidir}/grub.cfg
%doc grub-%{tarversion}/COPYING
/boot/grub2/grubenv
# I know 0700 seems strange, but it lives on FAT so that's what it'll
# get no matter what we do.
%config(noreplace) %ghost %attr(0700,root,root)/boot/efi/EFI/%{efidir}/grubenv

%files efi-modules
%defattr(-,root,root,-)
%{_libdir}/grub/%{grubefiarch}
%endif

%files tools -f grub.lang
%defattr(-,root,root,-)
%dir %{_libdir}/grub/
%dir %{_datarootdir}/grub/
%dir %{_datarootdir}/grub/themes
%{_datarootdir}/grub/*
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-get-kernel-settings
%{_sbindir}/%{name}-macbless
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-rpm-sort
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-setpassword
%{_sbindir}/%{name}-sparc64-setup
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-file
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-glue-efi
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-menulst2cfg
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mknetdir
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%ifnarch %{sparc}
%{_bindir}/%{name}-mkrescue
%endif
%{_bindir}/%{name}-mkstandalone
%{_bindir}/%{name}-render-label
%{_bindir}/%{name}-script-check
%{_bindir}/%{name}-syslinux2cfg
%{_datarootdir}/bash-completion/completions/grub
%{_sysconfdir}/prelink.conf.d/grub2.conf
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%attr(0644,root,root) %ghost %config(noreplace) %{_sysconfdir}/default/grub
%{_sysconfdir}/sysconfig/grub
%dir /boot/%{name}
%dir /boot/%{name}/themes/
%dir /boot/%{name}/themes/system
%exclude /boot/%{name}/themes/system/*
%exclude %{_datarootdir}/grub/themes/
%{_infodir}/%{name}*
%{_datadir}/man/man?/*
%doc grub-%{tarversion}/COPYING grub-%{tarversion}/INSTALL
%doc grub-%{tarversion}/NEWS grub-%{tarversion}/README
%doc grub-%{tarversion}/THANKS grub-%{tarversion}/TODO
%doc grub-%{tarversion}/grub.html
%doc grub-%{tarversion}/grub-dev.html grub-%{tarversion}/docs/font_char_metrics.png
%doc grub-%{tarversion}/themes/starfield/COPYING.CC-BY-SA-3.0

%files starfield-theme
%dir /boot/%{name}/themes/
/boot/%{name}/themes/system
%dir %{_datarootdir}/grub/themes
%{_datarootdir}/grub/themes/starfield

%changelog
* Thu Dec 08 2016 Peter Jones <pjones@redhat.com> - 2.02-0.38
- Fix regexp in power compile flags, and synchronize release number with
  other branches.

* Fri Dec 02 2016 pjones <pjones@redhat.com> - 1:2.02-0.37
- Rebased to newer upstream for fedora-25

* Thu Dec 01 2016 Peter Jones <pjones@redhat.com> - 2.02-0.36
- Rebased to newer upstream for fedora-25

* Thu Dec 01 2016 Peter Jones <pjones@redhat.com> - 2.02-0.34
- Fix power6 makefile bits for newer autoconf defaults.
- efi/chainloader: fix wrong sanity check in relocate_coff() (Laszlo Ersek)
  Resolves: rhbz#1347291

* Thu Aug 25 2016 Peter Jones <pjones@redhat.com> - 2.02-0.34
- Update to be newer than f24's branch.
- Add grub2-get-kernel-settings
  Related: rhbz#1226325

* Thu Apr 07 2016 pjones <pjones@redhat.com> - 1:2.02-0.30
- Revert 27e66193, which was replaced by upstream's 49426e9fd
  Resolves: rhbz#1251600

* Thu Apr 07 2016 Peter Jones <pjones@redhat.com> - 2.02-0.29
- Fix ppc64 build failure and rebase to newer f24 code.

* Tue Apr 05 2016 pjones <pjones@redhat.com> - 1:2.02-0.27
- Pull TPM updates from mjg59.
  Resolves: rhbz#1318067

* Tue Mar 08 2016 pjones <pjones@redhat.com> - 1:2.02-0.27
- Fix aarch64 build problem.

* Fri Mar 04 2016 Peter Jones <pjones@redhat.com> - 2.02-0.26
- Rebased to newer upstream (grub-2.02-beta3) for fedora-24

* Thu Dec 10 2015 Peter Jones <pjones@redhat.com> - 2.02-0.25
- Fix security issue when reading username and password
  Related: CVE-2015-8370
- Do a better job of handling GRUB2_PASSWORD
  Related: rhbz#1284370

* Fri Nov 20 2015 Peter Jones <pjones@redhat.com> - 2.02-0.24
- Rebuild without multiboot* modules in the EFI image.
  Related: rhbz#1264103

* Sat Sep 05 2015 Kalev Lember <klember@redhat.com> - 2.02-0.23
- Rebuilt for librpm soname bump

* Wed Aug 05 2015 Peter Jones <pjones@redhat.com> - 2.02-0.21
- Back out one of the debuginfo generation patches; it doesn't work right on
  aarch64 yet.
  Resolves: rhbz#1250197

* Mon Aug 03 2015 Peter Jones <pjones@redhat.com> - 2.02-0.20
- The previous fix was completely not right, so fix it a different way.
  Resolves: rhbz#1249668

* Fri Jul 31 2015 Peter Jones <pjones@redhat.com> - 2.02-0.19
- Fix grub2-mkconfig's sort to put kernels in the right order.
  Related: rhbz#1124074

* Thu Jul 30 2015 Peter Jones <pjones@redhat.com> - 2.02-0.18
- Fix a build failure on aarch64

* Wed Jul 22 2015 Peter Jones <pjones@redhat.com> - 2.02-0.17
- Don't build hardened (fixes FTBFS) (pbrobinson)
- Reconcile with the current upstream
- Fixes for gcc 5

* Tue Apr 28 2015 Peter Jones <pjones@redhat.com> - 2.02-0.16
- Make grub2-mkconfig produce the kernel titles we actually want.
  Resolves: rhbz#1215839

* Sat Feb 21 2015 Till Maas <opensource@till.name>
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Jan 05 2015 Peter Jones <pjones@redhat.com> - 2.02-0.15
- Bump release to rebuild with Ralf Corsépius's fixes.

* Sun Jan 04 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.02-0.14
- Move grub2.info/grub2-dev.info install-info scriptlets into *-tools package.
- Use sub-shell in %%__debug_install_post (RHBZ#1168732).
- Cleanup grub2-starfield-theme packaging.

* Thu Dec 04 2014 Peter Jones <pjones@redhat.com> - 2.02-0.13
- Update minilzo to 2.08 for CVE-2014-4607
  Resolves: rhbz#1131793

* Thu Nov 13 2014 Peter Jones <pjones@redhat.com> - 2.02-0.12
- Make backtrace and usb conditional on !arm
- Make sure gcdaa64.efi is packaged.
  Resolves: rhbz#1163481

* Fri Nov 07 2014 Peter Jones <pjones@redhat.com> - 2.02-0.11
- fix a copy-paste error in patch 0154.
  Resolves: rhbz#964828

* Mon Oct 27 2014 Peter Jones <pjones@redhat.com> - 2.02-0.10
- Try to emit linux16/initrd16 and linuxefi/initrdefi when appropriate
  in 30_os-prober.
  Resolves: rhbz#1108296
- If $fw_path doesn't work to find the config file, try $prefix as well
  Resolves: rhbz#1148652

* Mon Sep 29 2014 Peter Jones <pjones@redhat.com> - 2.02-0.9
- Clean up the build a bit to make it faster
- Make grubenv work right on UEFI machines
  Related: rhbz#1119943
- Sort debug and rescue kernels later than normal ones
  Related: rhbz#1065360
- Allow "fallback" to include entries by title as well as number.
  Related: rhbz#1026084
- Fix a segfault on aarch64.
- Load arm with SB enabled if available.
- Add some serial port options to GRUB_MODULES.

* Tue Aug 19 2014 Peter Jones <pjones@redhat.com> - 2.02-0.8
- Add ppc64le support.
  Resolves: rhbz#1125540

* Thu Jul 24 2014 Peter Jones <pjones@redhat.com> - 2.02-0.7
- Enabled syslinuxcfg module.

* Wed Jul 02 2014 Peter Jones <pjones@redhat.com> - 2.02-0.6
- Re-merge RHEL 7 changes and ARM works in progress.

* Mon Jun 30 2014 Peter Jones <pjones@redhat.com> - 2.02-0.5
- Avoid munging raw spaces when we're escaping command line arguments.
  Resolves: rhbz#923374

* Tue Jun 24 2014 Peter Jones <pjones@redhat.com> - 2.02-0.4
- Update to latest upstream.

* Thu Mar 13 2014 Peter Jones <pjones@redhat.com> - 2.02-0.3
- Merge in RHEL 7 changes and ARM works in progress.

* Mon Jan 06 2014 Peter Jones <pjones@redhat.com> - 2.02-0.2
- Update to grub-2.02~beta2

* Sat Aug 10 2013 Peter Jones <pjones@redhat.com> - 2.00-25
- Last build failed because of a hardware error on the builder.

* Mon Aug 05 2013 Peter Jones <pjones@redhat.com> - 2.00-24
- Fix compiler flags to deal with -fstack-protector-strong

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.00-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Dennis Gilmore <dennis@ausil.us> - 2.00-23
- add epoch to obsoletes

* Fri Jun 21 2013 Peter Jones <pjones@redhat.com> - 2.00-22
- Fix linewrapping in edit menu.
  Resolves: rhbz #976643

* Thu Jun 20 2013 Peter Jones <pjones@redhat.com> - 2.00-21
- Fix obsoletes to pull in -starfield-theme subpackage when it should.

* Fri Jun 14 2013 Peter Jones <pjones@redhat.com> - 2.00-20
- Put the theme entirely ento the subpackage where it belongs (#974667)

* Wed Jun 12 2013 Peter Jones <pjones@redhat.com> - 2.00-19
- Rebase to upstream snapshot.
- Fix PPC build error (#967862)
- Fix crash on net_bootp command (#960624)
- Reset colors on ppc when appropriate (#908519)
- Left align "Loading..." messages (#908492)
- Fix probing of SAS disks on PPC (#953954)
- Add support for UEFI OSes returned by os-prober
- Disable "video" mode on PPC for now (#973205)
- Make grub fit better into the boot sequence, visually (#966719)

* Fri May 10 2013 Matthias Clasen <mclasen@redhat.com> - 2.00-18
- Move the starfield theme to a subpackage (#962004)
- Don't allow SSE or MMX on UEFI builds (#949761)

* Wed Apr 24 2013 Peter Jones <pjones@redhat.com> - 2.00-17.pj0
- Rebase to upstream snapshot.

* Thu Apr 04 2013 Peter Jones <pjones@redhat.com> - 2.00-17
- Fix booting from drives with 4k sectors on UEFI.
- Move bash completion to new location (#922997)
- Include lvm support for /boot (#906203)

* Thu Feb 14 2013 Peter Jones <pjones@redhat.com> - 2.00-16
- Allow the user to disable submenu generation
- (partially) support BLS-style configuration stanzas.

* Tue Feb 12 2013 Peter Jones <pjones@redhat.com> - 2.00-15.pj0
- Add various config file related changes.

* Thu Dec 20 2012 Dennis Gilmore <dennis@ausil.us> - 2.00-15
- bump nvr

* Mon Dec 17 2012 Karsten Hopp <karsten@redhat.com> 2.00-14
- add bootpath device to the device list (pfsmorigo, #886685)

* Tue Nov 27 2012 Peter Jones <pjones@redhat.com> - 2.00-13
- Add vlan tag support (pfsmorigo, #871563)
- Follow symlinks during PReP installation in grub2-install (pfsmorigo, #874234)
- Improve search paths for config files on network boot (pfsmorigo, #873406)

* Tue Oct 23 2012 Peter Jones <pjones@redhat.com> - 2.00-12
- Don't load modules when grub transitions to "normal" mode on UEFI.

* Mon Oct 22 2012 Peter Jones <pjones@redhat.com> - 2.00-11
- Rebuild with newer pesign so we'll get signed with the final signing keys.

* Thu Oct 18 2012 Peter Jones <pjones@redhat.com> - 2.00-10
- Various PPC fixes.
- Fix crash fetching from http (gustavold, #860834)
- Issue separate dns queries for ipv4 and ipv6 (gustavold, #860829)
- Support IBM CAS reboot (pfsmorigo, #859223)
- Include all modules in the core image on ppc (pfsmorigo, #866559)

* Mon Oct 01 2012 Peter Jones <pjones@redhat.com> - 1:2.00-9
- Work around bug with using "\x20" in linux command line.
  Related: rhbz#855849

* Thu Sep 20 2012 Peter Jones <pjones@redhat.com> - 2.00-8
- Don't error on insmod on UEFI/SB, but also don't do any insmodding.
- Increase device path size for ieee1275
  Resolves: rhbz#857936
- Make network booting work on ieee1275 machines.
  Resolves: rhbz#857936

* Wed Sep 05 2012 Matthew Garrett <mjg@redhat.com> - 2.00-7
- Add Apple partition map support for EFI

* Thu Aug 23 2012 David Cantrell <dcantrell@redhat.com> - 2.00-6
- Only require pesign on EFI architectures (#851215)

* Tue Aug 14 2012 Peter Jones <pjones@redhat.com> - 2.00-5
- Work around AHCI firmware bug in efidisk driver.
- Move to newer pesign macros
- Don't allow insmod if we're in secure-boot mode.

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com>
- Split module lists for UEFI boot vs UEFI cd images.
- Add raid modules for UEFI image (related: #750794)
- Include a prelink whitelist for binaries that need execstack (#839813)
- Include fix efi memory map fix from upstream (#839363)

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com> - 2.00-4
- Correct grub-mkimage invocation to use efidir RPM macro (jwb)
- Sign with test keys on UEFI systems.
- PPC - Handle device paths with commas correctly.
  Related: rhbz#828740

* Wed Jul 25 2012 Peter Jones <pjones@redhat.com> - 2.00-3
- Add some more code to support Secure Boot, and temporarily disable
  some other bits that don't work well enough yet.
  Resolves: rhbz#836695

* Wed Jul 11 2012 Matthew Garrett <mjg@redhat.com> - 2.00-2
- Set a prefix for the image - needed for installer work
- Provide the font in the EFI directory for the same reason

* Thu Jun 28 2012 Peter Jones <pjones@redhat.com> - 2.00-1
- Rebase to grub-2.00 release.

* Mon Jun 18 2012 Peter Jones <pjones@redhat.com> - 2.0-0.37.beta6
- Fix double-free in grub-probe.

* Wed Jun 06 2012 Peter Jones <pjones@redhat.com> - 2.0-0.36.beta6
- Build with patch19 applied.

* Wed Jun 06 2012 Peter Jones <pjones@redhat.com> - 2.0-0.35.beta6
- More ppc fixes.

* Wed Jun 06 2012 Peter Jones <pjones@redhat.com> - 2.0-0.34.beta6
- Add IBM PPC fixes.

* Mon Jun 04 2012 Peter Jones <pjones@redhat.com> - 2.0-0.33.beta6
- Update to beta6.
- Various fixes from mads.

* Fri May 25 2012 Peter Jones <pjones@redhat.com> - 2.0-0.32.beta5
- Revert builddep change for crt1.o; it breaks ppc build.

* Fri May 25 2012 Peter Jones <pjones@redhat.com> - 2.0-0.31.beta5
- Add fwsetup command (pjones)
- More ppc fixes (IBM)

* Tue May 22 2012 Peter Jones <pjones@redhat.com> - 2.0-0.30.beta5
- Fix the /other/ grub2-tools require to include epoch.

* Mon May 21 2012 Peter Jones <pjones@redhat.com> - 2.0-0.29.beta5
- Get rid of efi_uga and efi_gop, favoring all_video instead.

* Mon May 21 2012 Peter Jones <pjones@redhat.com> - 2.0-0.28.beta5
- Name grub.efi something that's arch-appropriate (kiilerix, pjones)
- use EFI/$SOMETHING_DISTRO_BASED/ not always EFI/redhat/grub2-efi/ .
- move common stuff to -tools (kiilerix)
- spec file cleanups (kiilerix)

* Mon May 14 2012 Peter Jones <pjones@redhat.com> - 2.0-0.27.beta5
- Fix module trampolining on ppc (benh)

* Thu May 10 2012 Peter Jones <pjones@redhat.com> - 2.0-0.27.beta5
- Fix license of theme (mizmo)
  Resolves: rhbz#820713
- Fix some PPC bootloader detection IBM problem
  Resolves: rhbz#820722

* Thu May 10 2012 Peter Jones <pjones@redhat.com> - 2.0-0.26.beta5
- Update to beta5.
- Update how efi building works (kiilerix)
- Fix theme support to bring in fonts correctly (kiilerix, pjones)

* Wed May 09 2012 Peter Jones <pjones@redhat.com> - 2.0-0.25.beta4
- Include theme support (mizmo)
- Include locale support (kiilerix)
- Include html docs (kiilerix)

* Thu Apr 26 2012 Peter Jones <pjones@redhat.com> - 2.0-0.24
- Various fixes from Mads Kiilerich

* Thu Apr 19 2012 Peter Jones <pjones@redhat.com> - 2.0-0.23
- Update to 2.00~beta4
- Make fonts work so we can do graphics reasonably

* Thu Mar 29 2012 David Aquilina <dwa@redhat.com> - 2.0-0.22
- Fix ieee1275 platform define for ppc

* Thu Mar 29 2012 Peter Jones <pjones@redhat.com> - 2.0-0.21
- Remove ppc excludearch lines (dwa)
- Update ppc terminfo patch (hamzy)

* Wed Mar 28 2012 Peter Jones <pjones@redhat.com> - 2.0-0.20
- Fix ppc64 vs ppc exclude according to what dwa tells me they need
- Fix version number to better match policy.

* Tue Mar 27 2012 Dan Horák <dan[at]danny.cz> - 1.99-19.2
- Add support for serial terminal consoles on PPC by Mark Hamzy

* Sun Mar 25 2012 Dan Horák <dan[at]danny.cz> - 1.99-19.1
- Use Fix-tests-of-zeroed-partition patch by Mark Hamzy

* Thu Mar 15 2012 Peter Jones <pjones@redhat.com> - 1.99-19
- Use --with-grubdir= on configure to make it behave like -17 did.

* Wed Mar 14 2012 Peter Jones <pjones@redhat.com> - 1.99-18
- Rebase from 1.99 to 2.00~beta2

* Wed Mar 07 2012 Peter Jones <pjones@redhat.com> - 1.99-17
- Update for newer autotools and gcc 4.7.0
  Related: rhbz#782144
- Add /etc/sysconfig/grub link to /etc/default/grub
  Resolves: rhbz#800152
- ExcludeArch s390*, which is not supported by this package.
  Resolves: rhbz#758333

* Fri Feb 17 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.99-16
- Build with -Os (bug 782144)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.99-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Matthew Garrett <mjg@redhat.com> - 1.99-14
- fix up various grub2-efi issues

* Thu Dec 08 2011 Adam Williamson <awilliam@redhat.com> - 1.99-13
- fix hardwired call to grub-probe in 30_os-prober (rhbz#737203)

* Mon Nov 07 2011 Peter Jones <pjones@redhat.com> - 1.99-12
- Lots of .spec fixes from Mads Kiilerich:
  Remove comment about update-grub - it isn't run in any scriptlets
  patch info pages so they can be installed and removed correctly when renamed
  fix references to grub/grub2 renames in info pages (#743964)
  update README.Fedora (#734090)
  fix comments for the hack for upgrading from grub2 < 1.99-4
  fix sed syntax error preventing use of $RPM_OPT_FLAGS (#704820)
  make /etc/grub2*.cfg %config(noreplace)
  make grub.cfg %ghost - an empty file is of no use anyway
  create /etc/default/grub more like anaconda would create it (#678453)
  don't create rescue entries by default - grubby will not maintain them anyway
  set GRUB_SAVEDEFAULT=true so saved defaults works (rbhz#732058)
  grub2-efi should have its own bash completion
  don't set gfxpayload in efi mode - backport upstream r3402
- Handle dmraid better. Resolves: rhbz#742226

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.99-11
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Adam Williamson <awilliam@redhat.com> - 1.99-10
- /etc/default/grub is explicitly intended for user customization, so
  mark it as config(noreplace)

* Tue Oct 11 2011 Peter Jones <pjones@redhat.com> - 1.99-9
- grub has an epoch, so we need that expressed in the obsolete as well.
  Today isn't my day.

* Tue Oct 11 2011 Peter Jones <pjones@redhat.com> - 1.99-8
- Fix my bad obsoletes syntax.

* Thu Oct 06 2011 Peter Jones <pjones@redhat.com> - 1.99-7
- Obsolete grub
  Resolves: rhbz#743381

* Wed Sep 14 2011 Peter Jones <pjones@redhat.com> - 1.99-6
- Use mv not cp to try to avoid moving disk blocks around for -5 fix
  Related: rhbz#735259
- handle initramfs on xen better (patch from Marko Ristola)
  Resolves: rhbz#728775

* Sat Sep 03 2011 Kalev Lember <kalevlember@gmail.com> - 1.99-5
- Fix upgrades from grub2 < 1.99-4 (#735259)

* Fri Sep 02 2011 Peter Jones <pjones@redhat.com> - 1.99-4
- Don't do sysadminny things in %preun or %post ever. (#735259)
- Actually include the changelog in this build (sorry about -3)

* Thu Sep 01 2011 Peter Jones <pjones@redhat.com> - 1.99-2
- Require os-prober (#678456) (patch from Elad Alfassa)
- Require which (#734959) (patch from Elad Alfassa)

* Thu Sep 01 2011 Peter Jones <pjones@redhat.com> - 1.99-1
- Update to grub-1.99 final.
- Fix crt1.o require on x86-64 (fix from Mads Kiilerich)
- Various CFLAGS fixes (from Mads Kiilerich)
  - -fexceptions and -m64
- Temporarily ignore translations (from Mads Kiilerich)

* Thu Jul 21 2011 Peter Jones <pjones@redhat.com> - 1.99-0.3
- Use /sbin not /usr/sbin .

* Thu Jun 23 2011 Peter Lemenkov <lemenkov@gmail.com> - 1:1.99-0.2
- Fixes for ppc and ppc64

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.98-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
