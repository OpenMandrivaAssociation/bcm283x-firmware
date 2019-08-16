%global debug_package %{nil}

# Tarfile created using git 		
# git clone https://github.com/raspberrypi/firmware.git
# cd firmware/boot
# tar cJvf ../bcm283x-firmware-%{gitshort}.tar.xz *bin *dat *elf bcm2709*dtb bcm271*dtb LICENCE.broadcom COPYING.linux overlays/
%define gitshort 3822340
%global efi_esp_root /boot/efi

Name:          bcm283x-firmware
Version:       20190801
Release:       1.%{gitshort}%{?dist}
Summary:       Broadcom bcm283x firmware for the Raspberry Pi
# see LICENSE.broadcom
# DT Overlays covered under Linux Kernel GPLv2
License:       Redistributable, no modification permitted
URL:           https://github.com/raspberrypi/

ExclusiveArch: %{armx}

BuildRequires: efi-filesystem
BuildRequires: efi-srpm-macros
Requires:      efi-filesystem

Source0:       %{name}-%{gitshort}.tar.xz
Source1:       config.txt
Source2:       config-64.txt

# From Linux kernel
Source5:       bcm2836-rpi-2-b.dtb
Source6:       bcm2837-rpi-3-a-plus.dtb
Source7:       bcm2837-rpi-3-b.dtb
Source8:       bcm2837-rpi-3-b-plus.dtb
Source9:       bcm2837-rpi-cm3-io3.dtb

%description
Firmware for the Broadcom bcm283x SoC as shipped in devices such as the
Raspberry Pi.

%prep
%setup -q -n %{name}-%{gitshort} -c %{name}-%{gitshort}

%build

%install
mkdir -p %{buildroot}%{efi_esp_root}/overlays
%ifarch %{arm}
install -p %{SOURCE1} %{buildroot}%{efi_esp_root}/config.txt
%endif
%ifarch aarch64
install -p %{SOURCE2} %{buildroot}%{efi_esp_root}/config.txt
%endif
install -p *bin %{buildroot}%{efi_esp_root}
install -p *dat %{buildroot}%{efi_esp_root}
install -p *elf %{buildroot}%{efi_esp_root}
install -p %{SOURCE5} %{buildroot}%{efi_esp_root}
install -p %{SOURCE6} %{buildroot}%{efi_esp_root}
install -p %{SOURCE7} %{buildroot}%{efi_esp_root}
install -p %{SOURCE8} %{buildroot}%{efi_esp_root}
install -p %{SOURCE9} %{buildroot}%{efi_esp_root}
install -p overlays/README %{buildroot}%{efi_esp_root}/overlays
install -p overlays/*.dtbo %{buildroot}%{efi_esp_root}/overlays

%pre
# Remove in Fedora 32 or there abouts
if [ -d /boot/fw ]; then
   mkdir /boot/efi
   echo "`blkid /dev/[sm][dm]*1 |grep vfat |head -1 | awk '{print $3}'`        /boot/efi               vfat    umask=0077,shortname=winnt 0 2"  >> /etc/fstab
   mount /boot/efi
   rmdir /boot/fw
fi

%files
# DT Overlays covered under Linux Kernel GPLv2
%license LICENCE.broadcom COPYING.linux
%config(noreplace) %{efi_esp_root}/config.txt
%{efi_esp_root}/overlays
%{efi_esp_root}/*bin
%{efi_esp_root}/*dat
%{efi_esp_root}/*elf
%{efi_esp_root}/*.dtb
