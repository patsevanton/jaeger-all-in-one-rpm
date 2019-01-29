%global _prefix /usr/local
%global __strip /bin/true

Name:    jaeger-all-in-one
Version: 1.8.2
Release: 1
Summary: Open source, end-to-end distributed tracing

Group:   Development Tools
URL:     https://github.com/jaegertracing/jaeger
License: ASL 2.0
Source0: https://github.com/jaegertracing/jaeger/releases/download/v%{version}/jaeger-%{version}-linux-amd64.tar.gz
#Source0: jaeger-1.8.2-linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.yaml
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%description
CNCF Jaeger, a Distributed Tracing System

%prep
%setup -q -n jaeger-%{version}-linux-amd64

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -m 0755 -d %{buildroot}%{_bindir}
%{__install} -m 0755 -d %{buildroot}/etc
#%{__install} -m 0755 jaeger-all-in-one %{buildroot}/%{_bindir}/%{name}
cp jaeger-all-in-one %{buildroot}/%{_bindir}/%{name}
%{__install} -m 0644 %{SOURCE2} %{buildroot}/etc/jaeger-all-in-one.yaml

%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE1} \
    %{buildroot}%{_unitdir}/%{name}.service
%endif

%post
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%preun
%if %use_systemd
/usr/bin/systemctl stop %{name}
%endif

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
/etc/jaeger-all-in-one.yaml
%if %{use_systemd}
%{_unitdir}/%{name}.service
%endif
