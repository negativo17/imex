Name:           imex
Version:        560.35.03
Release:        1%{?dist}
Summary:        NVIDIA Imex daemon
License:        NVIDIA Proprietary
URL:            http://nvidia.com
ExclusiveArch:  x86_64 aarch64

Source0:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-x86_64/nvidia-%{name}-linux-x86_64-%{version}-archive.tar.xz
Source1:        https://developer.download.nvidia.com/compute/cuda/redist/%{name}/linux-sbsa/nvidia-%{name}-linux-sbsa-%{version}-archive.tar.xz
Source2:        nvidia-%{name}-tmpfiles.conf

%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  systemd-rpm-macros
%else
BuildRequires:  systemd-devel
%endif

%description
Imex process is a privileged/system client of Resource Manager and will
facilitate the mapping of GPU memory (over NVLink) between GPUs via the memory
import and export mechanisms.

%prep
%ifarch x86_64
%setup -q -n nvidia-%{name}-linux-x86_64-%{version}-archive
%endif

%ifarch aarch64
%setup -q -T -b 1 -n nvidia-%{name}-linux-sbsa-%{version}-archive
%endif

%install

install -p -m 0644 -D etc/nvidia-imex/config.cfg %{buildroot}/%{_sysconfdir}/nvidia-%{name}/config.cfg

install -p -m 0644 -D lib/systemd/system/nvidia-imex.service %{buildroot}%{_unitdir}/nvidia-imex.service

install -p -m 0644 -D %{SOURCE1} %{buildroot}%{_tmpfilesdir}/nvidia-%{name}.conf
install -d -m 0755 %{buildroot}/run/nvidia-%{name}/

mkdir -p %{buildroot}/%{_bindir}
install -P -m 0755 usr/bin/* %{buildroot}/%{_bindir}/

%post
%systemd_post nvidia-imex.service

%preun
%systemd_preun nvidia-imex.service

%postun
%systemd_postun nvidia-imex.service

%files
%license LICENSE usr/share/doc/third-party-notices.txt
%{_unitdir}/nvidia-imex.service
%{_bindir}/nvidia-imex
%{_bindir}/nvidia-imex-ctl
%dir %{_sysconfdir}/nvidia-imex
%config %{_sysconfdir}/nvidia-imex/config.cfg
%dir /run/nvidia-%{name}/
%{_tmpfilesdir}/nvidia-%{name}.conf

%changelog
* Thu Sep 19 2024 Simone Caronni <negativo17@gmail.com> - 560.35.03-1
- Update to 560.35.03.

* Thu Jul 11 2024 Simone Caronni <negativo17@gmail.com> - 555.42.06-1
- Update to 555.42.06.

* Thu Mar 14 2024 Simone Caronni <negativo17@gmail.com> - 550.54.14-1
- First build.
