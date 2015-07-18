fedora-grub-boot-btrfs-default-subvolume
========================================

Problem
-------

This is an attempt to document adding the functionality to Fedora's
GRUB to respect the default subvolume that is set on a btrfs FS when
looking for grub.cfg and grub modules. The use case I am interested in
for this is to have a single filesystem (the root filesystem `/`) that
includes `/boot/` and can be snapshotted. If `/boot` is included in the
snapshot then it is guaranteed to have the right information at the
time the snapshot was created. If grub's core.img respects default
subvolumes then all you need to do to rollback to a previous snapshot
is to set the default subvolume to that snapshot and reboot. No other
work required.

**NOTE**:: This functionailty used to the default in grub but was removed in:
- 82591fa - Make / in btrfs refer to real root, not the default volume.

Strategy
--------

To get this functionality back I will pull a few patches from SUSE's grub:

- grub2-btrfs-01-add-ability-to-boot-from-subvolumes.patch
- grub2-btrfs-02-export-subvolume-envvars.patch
- grub2-btrfs-03-follow_default.patch
- grub2-btrfs-04-grub2-install.patch
- grub2-btrfs-05-grub2-mkconfig.patch

The patches were taken from the following SUSE srpm that was retrieved
from the following URL and placed in this repo:

- http://download.opensuse.org/source/distribution/13.2/repo/oss/suse/src/grub2-2.02~beta2-20.5.1.src.rpm

The Fedora srpm was retrieved from the following URL and placed in
this repo:

- http://mirror.chpc.utah.edu/pub/fedora/linux/releases/22/Everything/source/SRPMS/g/grub2-2.02-0.16.fc22.src.rpm

Building
--------

Run the following commands from the root of the git repo to download software needed 
and to build the rpm on Fedora 22:

```
dnf install yum-utils gcc rpm-build
yum-builddep grub2
rpmbuild -D "_topdir $(readlink -f ./)/rpmbuild" -ba ./rpmbuild/SPECS/grub2.spec
```



