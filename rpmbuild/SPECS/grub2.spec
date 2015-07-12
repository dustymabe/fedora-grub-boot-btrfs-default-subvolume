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

%if 0%{?rhel}
%global efidir redhat
%endif
%if 0%{?fedora}
%global efidir fedora
%endif

%endif

%global tarversion 2.02~beta2
%undefine _missing_build_ids_terminate_build

Name:           grub2
Epoch:          1
Version:        2.02
Release:        0.16%{?dist}
Summary:        Bootloader with support for Linux, Multiboot and more

Group:          System Environment/Base
License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
Obsoletes:	grub < 1:0.98
Source0:        ftp://alpha.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
#Source0:	ftp://ftp.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
Source4:	http://unifoundry.com/unifont-5.1.20080820.pcf.gz
Source5:	theme.tar.bz2
Source6:	gitignore

Patch0001: 0001-fix-EFI-detection-on-Windows.patch
Patch0002: 0002-grub-core-kern-arm-cache_armv6.S-Remove-.arch-direct.patch
Patch0003: 0003-INSTALL-Cross-compiling-the-GRUB-Fix-some-spelling-m.patch
Patch0004: 0004-NEWS-First-draft-of-2.02-entry.patch
Patch0005: 0005-Merge-branch-master-of-git.sv.gnu.org-srv-git-grub.patch
Patch0006: 0006-NEWS-The-cmosclean-command-in-fact-dates-back-to-1.9.patch
Patch0007: 0007-remove-unused-error.h-from-kern-emu-misc.c.patch
Patch0008: 0008-Don-t-abort-on-unavailable-coreboot-tables-if-not-ru.patch
Patch0009: 0009-NEWS-Add-few-missing-entries.-Correct-existing-ones.patch
Patch0010: 0010-strip-.eh_frame-section-from-arm64-efi-kernel.patch
Patch0011: 0011-use-grub-boot-aa64.efi-for-boot-images-on-AArch64.patch
Patch0012: 0012-fix-32-bit-compilation-on-MinGW-w64.patch
Patch0013: 0013-Change-grub-mkrescue-to-use-bootaa64.efi-too.patch
Patch0014: 0014-arm64-set-correct-length-of-device-path-end-entry.patch
Patch0015: 0015-Makefile.util.def-grub-macbless-Change-mansection-to.patch
Patch0016: 0016-add-part_apple-to-EFI-rescue-image-to-fix-missing-pr.patch
Patch0017: 0017-freebsd-hostdisk.c-is-only-ever-compiled-on-FreeBSD.patch
Patch0018: 0018-Prefer-more-portable-test-1-constructs.patch
Patch0019: 0019-NEWS-Add-few-missing-entries.patch
Patch0020: 0020-grub-core-kern-efi-efi.c-Ensure-that-the-result-star.patch
Patch0021: 0021-util-grub-mount.c-Extend-GCC-warning-workaround-to-g.patch
Patch0022: 0022-reintroduce-BUILD_LDFLAGS-for-the-cross-compile-case.patch
Patch0023: 0023-grub-core-term-terminfo.c-Recognize-keys-F1-F12.patch
Patch0024: 0024-Fix-ChangeLog-date.patch
Patch0025: 0025-Use-_W64-to-detect-MinGW-W64-32-instead-of-_FILE_OFF.patch
Patch0026: 0026-add-BUILD_EXEEXT-support-to-fix-make-clean-on-Window.patch
Patch0027: 0027-fix-include-loop-on-MinGW-due-to-libintl.h-pulling-s.patch
Patch0028: 0028-grub-core-commands-macbless.c-Rename-FILE-and-DIR-to.patch
Patch0029: 0029-Makefile.util.def-Link-grub-ofpathname-with-zfs-libs.patch
Patch0030: 0030-Makefile.am-default_payload.elf-Add-modules.patch
Patch0031: 0031-fix-removal-of-cpu-machine-links-on-mingw-msys.patch
Patch0032: 0032-grub-core-normal-main.c-read_config_file-Buffer-conf.patch
Patch0033: 0033-util-grub-install.c-Fix-a-typo.patch
Patch0034: 0034-use-MODULE_FILES-for-genemuinit-instead-of-MOD_FILES.patch
Patch0035: 0035-Ignore-EPERM-when-modifying-kern.geom.debugflags.patch
Patch0036: 0036-change-stop-condition-to-avoid-infinite-loops.patch
Patch0037: 0037-increase-network-try-interval-gradually.patch
Patch0038: 0038-look-for-DejaVu-also-in-usr-share-fonts-truetype.patch
Patch0039: 0039-Show-detected-path-to-DejaVuSans-in-configure-summar.patch
Patch0040: 0040-add-GRUB_WINDOWS_EXTRA_DIST-to-allow-shipping-runtim.patch
Patch0041: 0041-util-grub-install.c-write_to_disk-Add-an-info-messag.patch
Patch0042: 0042-util-grub-install.c-List-available-targets.patch
Patch0043: 0043-Fix-several-translatable-strings.patch
Patch0044: 0044-do-not-set-default-prefix-in-grub-mkimage.patch
Patch0045: 0045-fix-Mingw-W64-32-cross-compile-failure-due-to-printf.patch
Patch0046: 0046-grub-core-term-serial.c-grub_serial_register-Fix-inv.patch
Patch0047: 0047-grub-install-support-for-partitioned-partx-loop-devi.patch
Patch0048: 0048-grub-core-term-at_keyboard.c-Tolerate-missing-keyboa.patch
Patch0049: 0049-.gitignore-add-missing-files-and-.exe-variants.patch
Patch0050: 0050-util-grub-mkfont.c-Downgrade-warnings-about-unhandle.patch
Patch0051: 0051-grub-core-disk-ahci.c-Do-not-enable-I-O-decoding-and.patch
Patch0052: 0052-grub-core-disk-ahci.c-Allocate-and-clean-space-for-a.patch
Patch0053: 0053-grub-core-disk-ahci.c-Add-safety-cleanups.patch
Patch0054: 0054-grub-core-disk-ahci.c-Properly-handle-transactions-w.patch
Patch0055: 0055-grub-core-disk-ahci.c-Increase-timeout.-Some-SSDs-ta.patch
Patch0056: 0056-util-grub-mkfont.c-Build-fix-for-argp.h-with-older-g.patch
Patch0057: 0057-util-grub-mkrescue.c-Build-fix-for-argp.h-with-older.patch
Patch0058: 0058-add-grub_env_set_net_property-function.patch
Patch0059: 0059-add-bootpath-parser-for-open-firmware.patch
Patch0060: 0060-grub-core-disk-ahci.c-Ignore-NPORTS-field-and-rely-o.patch
Patch0061: 0061-grub-core-kern-i386-coreboot-mmap.c-Filter-out-0xa00.patch
Patch0062: 0062-grub-core-loader-i386-multiboot_mbi.c-grub_multiboot.patch
Patch0063: 0063-grub-core-mmap-i386-uppermem.c-lower_hook-COREBOOT-I.patch
Patch0064: 0064-grub-core-kern-i386-pc-mmap.c-Fallback-to-EISA-memor.patch
Patch0065: 0065-include-grub-i386-openbsd_bootarg.h-Add-addr-and-fre.patch
Patch0066: 0066-ieee1275-check-for-IBM-pseries-emulated-machine.patch
Patch0067: 0067-grub-core-loader-arm64-linux.c-Remove-redundant-0x.patch
Patch0068: 0068-grub-core-lib-relocator.c-Fix-the-case-when-end-of-l.patch
Patch0069: 0069-Fix-grub-probe-0-option.patch
Patch0070: 0070-Fix-partmap-cryptodisk-and-abstraction-handling-in-g.patch
Patch0071: 0071-btrfs-fix-get_root-key-comparison-failures-due-to-en.patch
Patch0072: 0072-grub-core-osdep-linux-getroot.c-grub_util_part_to_di.patch
Patch0073: 0073-Replace-few-instances-of-memcmp-memcpy-in-the-code-t.patch
Patch0074: 0074-include-grub-libgcc.h-Remove-ctzsi2-and-ctzdi2.-They.patch
Patch0075: 0075-Add-missing-endif.patch
Patch0076: 0076-grub-core-lib-syslinux_parse.c-Fix-timeout-quoting.patch
Patch0077: 0077-Improve-LVM-logical_volumes-string-matching.patch
Patch0078: 0078-Tolerate-devices-with-no-filesystem-UUID-returned-by.patch
Patch0079: 0079-Allow-loading-old-kernels-by-placing-GDT-in-conventi.patch
Patch0080: 0080-grub-core-kern-misc.c-__bzero-Don-t-compile-in-GRUB_.patch
Patch0081: 0081-grub-core-commands-verify.c-grub_pubkey_open-Fix-mem.patch
Patch0082: 0082-grub-core-commands-verify.c-grub_pubkey_open-Trust-p.patch
Patch0083: 0083-util-grub-gen-asciih.c-add_glyph-Fix-uninitialised-v.patch
Patch0084: 0084-grub-core-commands-efi-lsefisystab.c-grub_cmd_lsefis.patch
Patch0085: 0085-grub-core-loader-i386-bsd.c-grub_netbsd_boot-Pass-po.patch
Patch0086: 0086-util-grub-install.c-Fix-handling-of-disk-module.patch
Patch0087: 0087-grub-core-commands-loadenv.c-check_blocklists-Fix-ov.patch
Patch0088: 0088-NEWS-The-cmosclean-command-in-fact-dates-back-to-1.9.patch
Patch0089: 0089-Migrate-PPC-from-Yaboot-to-Grub2.patch
Patch0090: 0090-Add-fw_path-variable-revised.patch
Patch0091: 0091-Add-support-for-linuxefi.patch
Patch0092: 0092-Use-linuxefi-and-initrdefi-where-appropriate.patch
Patch0093: 0093-Don-t-allow-insmod-when-secure-boot-is-enabled.patch
Patch0094: 0094-Pass-x-hex-hex-straight-through-unmolested.patch
Patch0095: 0095-Fix-crash-on-http.patch
Patch0096: 0096-IBM-client-architecture-CAS-reboot-support.patch
Patch0097: 0097-Add-vlan-tag-support.patch
Patch0098: 0098-Add-X-option-to-printf-functions.patch
Patch0099: 0099-DHCP-client-ID-and-UUID-options-added.patch
Patch0100: 0100-Search-for-specific-config-file-for-netboot.patch
Patch0101: 0101-blscfg-add-blscfg-module-to-parse-Boot-Loader-Specif.patch
Patch0102: 0102-Move-bash-completion-script-922997.patch
Patch0103: 0103-for-ppc-reset-console-display-attr-when-clear-screen.patch
Patch0104: 0104-Don-t-write-messages-to-the-screen.patch
Patch0105: 0105-Don-t-print-GNU-GRUB-header.patch
Patch0106: 0106-Don-t-add-to-highlighted-row.patch
Patch0107: 0107-Message-string-cleanups.patch
Patch0108: 0108-Fix-border-spacing-now-that-we-aren-t-displaying-it.patch
Patch0109: 0109-Use-the-correct-indentation-for-the-term-help-text.patch
Patch0110: 0110-Indent-menu-entries.patch
Patch0111: 0111-Fix-margins.patch
Patch0112: 0112-Add-support-for-UEFI-operating-systems-returned-by-o.patch
Patch0113: 0113-Disable-GRUB-video-support-for-IBM-power-machines.patch
Patch0114: 0114-Use-2-instead-of-1-for-our-right-hand-margin-so-line.patch
Patch0115: 0115-Use-linux16-when-appropriate-880840.patch
Patch0116: 0116-Enable-pager-by-default.-985860.patch
Patch0117: 0117-F10-doesn-t-work-on-serial-so-don-t-tell-the-user-to.patch
Patch0118: 0118-Don-t-say-GNU-Linux-in-generated-menus.patch
Patch0119: 0119-Don-t-draw-a-border-around-the-menu.patch
Patch0120: 0120-Use-the-standard-margin-for-the-timeout-string.patch
Patch0121: 0121-Fix-grub_script_execute_sourcecode-usage-on-ppc.patch
Patch0122: 0122-Add-.eh_frame-to-list-of-relocations-stripped.patch
Patch0123: 0123-Make-10_linux-work-with-our-changes-for-linux16-and-.patch
Patch0124: 0124-Don-t-print-during-fdt-loading-method.patch
Patch0125: 0125-Honor-a-symlink-when-generating-configuration-by-gru.patch
Patch0126: 0126-Don-t-munge-raw-spaces-when-we-re-doing-our-cmdline-.patch
Patch0127: 0127-Don-t-require-a-password-to-boot-entries-generated-b.patch
Patch0128: 0128-Don-t-emit-Booting-.-message.patch
Patch0129: 0129-Make-CTRL-and-ALT-keys-work-as-expected-on-EFI-syste.patch
Patch0130: 0130-May-as-well-try-it.patch
Patch0131: 0131-use-fw_path-prefix-when-fallback-searching-for-grub-.patch
Patch0132: 0132-Try-mac-guid-etc-before-grub.cfg-on-tftp-config-file.patch
Patch0133: 0133-trim-arp-packets-with-abnormal-size.patch
Patch0134: 0134-Fix-convert-function-to-support-NVMe-devices.patch
Patch0135: 0135-Fix-bad-test-on-GRUB_DISABLE_SUBMENU.patch
Patch0136: 0136-Switch-to-use-APM-Mustang-device-tree-for-hardware-t.patch
Patch0137: 0137-Use-the-default-device-tree-from-the-grub-default-fi.patch
Patch0138: 0138-reopen-SNP-protocol-for-exclusive-use-by-grub.patch
Patch0139: 0139-Reduce-timer-event-frequency-by-10.patch
Patch0140: 0140-always-return-error-to-UEFI.patch
Patch0141: 0141-Add-powerpc-little-endian-ppc64le-flags.patch
Patch0142: 0142-Files-reorganization-and-include-some-libgcc-fuction.patch
Patch0143: 0143-Suport-for-bi-endianess-in-elf-file.patch
Patch0144: 0144-Add-grub_util_readlink.patch
Patch0145: 0145-Make-editenv-chase-symlinks-including-those-across-d.patch
Patch0146: 0146-Generate-OS-and-CLASS-in-10_linux-from-etc-os-releas.patch
Patch0147: 0147-Fix-GRUB_DISABLE_SUBMENU-one-more-time.patch
Patch0148: 0148-Minimize-the-sort-ordering-for-.debug-and-rescue-ker.patch
Patch0149: 0149-Add-GRUB_DISABLE_UUID.patch
Patch0150: 0150-Allow-fallback-to-include-entries-by-title-not-just-.patch
Patch0151: 0151-Initialized-initrd_ctx-so-we-don-t-free-a-random-poi.patch
Patch0152: 0152-Load-arm-with-SB-enabled.patch
Patch0153: 0153-Try-prefix-if-fw_path-doesn-t-work.patch
Patch0154: 0154-Try-to-emit-linux16-initrd16-and-linuxefi-initrdefi-.patch
Patch0155: 0001-Update-to-minilzo-2.08.patch
Patch0156: 0001-Make-grub2-mkconfig-construct-titles-that-look-like-.patch
Patch0157: 0002-Make-rescue-and-debug-entries-sort-right-again-in-gr.patch

BuildRequires:  flex bison binutils python
BuildRequires:  ncurses-devel xz-devel bzip2-devel
BuildRequires:  freetype-devel libusb-devel
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
git config user.email "grub2-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{tarversion} baseline."
git am %{patches}
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
GRUB_MODULES+=" linuxefi multiboot2 multiboot "
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
		-e 's/-mcpu=power7/-mcpu=power6/g'		\
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
%{_sbindir}/%{name}-macbless
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
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
* Tue Apr 28 2015 Peter Jones <pjones@redhat.com> - 2.02-0.16
- Make grub2-mkconfig produce the kernel titles we actually want.
  Resolves: rhbz#1215839

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
