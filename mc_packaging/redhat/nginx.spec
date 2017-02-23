Name: nginx
Version: 1.10.3
Release: 2
Summary: High performance web server
URL: http://nginx.org/
Vendor: corpusops
License: 2-clause BSD-like license
Group: %{_group}
Provides: webserver

%global repo https://github.com/corpusops/nginx
%global commit %{version}-%{release}
%global archive %{repo}/archive/%{commit}.zip

%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user www-data
%define nginx_group www-data
%define nginx_loggroup adm
# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} == 1315)

%if 0%{?rhel} == 5
%define _group System Environment/Daemons
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires: initscripts >= 8.36
%endif

%if 0%{?rhel} == 6
%define _group System Environment/Daemons
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires: initscripts >= 8.36
%endif

%if 0%{?rhel} == 7
%define _group System Environment/Daemons
%define epoch 1
Epoch: %{epoch}
Requires(pre): shadow-utils
Requires: systemd
Requires: openssl >= 1.0.1
%endif

# end of distribution specific definitions
%define bdir %{_builddir}/
%define WITH_CC_OPT $(echo %{optflags} $(pcre-config --cflags)) -fPIC
%define WITH_LD_OPT -Wl,-z,relro -Wl,-z,now -pie

Source0: %{archive}

Requires: openssl
Requires: python-twisted
Requires: expat
Requires: openldap
Requires: libxslt-python
Requires: libxslt
Requires: perl
Requires: pcre
Requires: pcre-tools
Requires: pam
Requires: mhash
Requires: luajit
Requires: luajit-fun
Requires: hiredis
Requires: GeoIP
Requires: gd

BuildRequires: mhash-devel
BuildRequires: pam-devel
BuildRequires: openldap-devel
BuildRequires: openssl-devel
BuildRequires: expat-devel
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libxslt-devel
BuildRequires: perl-devel
BuildRequires: pcre-devel
BuildRequires: luajit-devel
BuildRequires: hiredis-devel
BuildRequires: GeoIP-devel
BuildRequires: gd-devel
BuildRequires: zlib-devel

BuildRoot: %{_tmppath}/%{name}-%{version}

%description
#nginx [engine x] is an HTTP and reverse proxy server, as well as
#a mail proxy server.

%prep
%setup -q
set -ex
ls ..
pwd

%build
BASE_CONFIGURE_ARGS="--prefix=/usr/share/nginx \
  --sbin-path=%{_sbindir}/nginx \
  --modules-path=%{_libdir}/nginx/modules
  --conf-path=%{_sysconfdir}/nginx/nginx.conf \
  --error-log-path=%{_localstatedir}/log/nginx/error.log \
  --http-log-path=%{_localstatedir}/log/nginx/access.log \
  --pid-path=%{_localstatedir}/run/nginx.pid \
  --lock-path=%{_localstatedir}/lock/nginx.lock \
  --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
  --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
  --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
  --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
  --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
  --user=%{nginx_user} \
  --group=%{nginx_group} \
  --with-threads \
  --with-http_addition_module \
  --with-http_auth_request_module \
  --with-http_dav_module \
  --with-http_flv_module \
  --with-http_gunzip_module \
  --with-http_gzip_static_module \
  --with-http_mp4_module \
  --with-http_random_index_module \
  --with-http_realip_module \
  --with-http_secure_link_module \
  --with-http_slice_module \
  --with-http_ssl_module \
  --with-http_stub_status_module \
  --with-http_sub_module \
  --with-http_v2_module \
  --with-mail=dynamic \
  --with-mail_ssl_module \
  --with-stream=dynamic \
  --with-stream_ssl_module \
  --with-stream_ssl_preread_module \
  --http-client-body-temp-path=/var/lib/nginx/body \
  --http-fastcgi-temp-path=/var/lib/nginx/fastcgi \
  --http-proxy-temp-path=/var/lib/nginx/proxy \
  --http-scgi-temp-path=/var/lib/nginx/scgi \
  --http-uwsgi-temp-path=/var/lib/nginx/uwsgi \
  --with-debug \
  --with-pcre-jit \
  --with-ipv6 \
  --with-http_geoip_module=dynamic \
  --with-http_image_filter_module=dynamic \
  --with-http_perl_module=dynamic \
  --with-http_xslt_module=dynamic \
  --add-module=%{bdir}/debian/modules/nginx-auth-ldap \
  --add-dynamic-module=%{bdir}/debian/modules/headers-more-nginx-module \
  --add-dynamic-module=%{bdir}/debian/modules/nchan \
  --add-dynamic-module=%{bdir}/debian/modules/nginx-auth-pam \
  --add-dynamic-module=%{bdir}/debian/modules/nginx-cache-purge \
  --add-dynamic-module=%{bdir}/debian/modules/nginx-dav-ext-module \
  --add-dynamic-module=%{bdir}/debian/modules/nginx-development-kit \
  --add-dynamic-module=%{bdir}/debian/modules/nginx-echo \
  --add-dynamic-module=%{bdir}/debian/modules/nginx-lua \
  --add-dynamic-module=%{bdir}/debian/modules/nginx-upload-progress \
  --add-dynamic-module=%{bdir}/debian/modules/nginx-upstream-fair \
  --add-dynamic-module=%{bdir}/debian/modules/ngx-fancyindex \
  --add-dynamic-module=%{bdir}/debian/modules/ngx_http_substitutions_filter_module \
  --with-cc-opt="%{WITH_CC_OPT}" \
  --with-ld-opt="%{WITH_LD_OPT}" \
  --with-stream_realip_module"
cp auto/configure .
./configure ${BASE_CONFIGURE_ARGS} --with-debug
make %{?_smp_mflags}
%{__mv} %{bdir}/objs/nginx  %{bdir}/objs/nginx-debug
./configure ${BASE_CONFIGURE_ARGS}
./configure "%{BASE_CONFIGURE_ARGS}"
make %{?_smp_mflags}

%install

%clean

%files

%pre

%post

%preun

%postun

%changelog
* Thu Feb 23 2017 Mathieu Le Marec - Pasquet <kiorky@cryptelium.net> 1.10.3-2
- new package built with tito

