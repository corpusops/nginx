#
Name: nginx
Version: 1.10.3
%global releasen 4
#Release: %{releasen}.git.0.d5caa44%{?dist}
Release: %{releasen}%{?dist}
Summary: High performance web server
URL: http://nginx.org/
Vendor: corpusops
License: 2-clause BSD-like license
Group: %{_group}
Provides: webserver

%global repo nginx
%global user corpusops
%global github https://github.com/%{user}/%{repo}
%global commit %{version}-%{releasen}
%define WITH_CC_OPT $(echo %{optflags} $(pcre-config --cflags)) -fPIC
%define WITH_LD_OPT -Wl,-z,relro -Wl,-z,now -pie
%define configure_flags --prefix=/usr/share/nginx \\\
  --sbin-path=%{_sbindir}/nginx \\\
  --modules-path=%{_libdir}/nginx/modules \\\
  --conf-path=%{_sysconfdir}/nginx/nginx.conf \\\
  --error-log-path=%{_localstatedir}/log/nginx/error.log \\\
  --http-log-path=%{_localstatedir}/log/nginx/access.log \\\
  --pid-path=%{_localstatedir}/run/nginx.pid \\\
  --lock-path=%{_localstatedir}/lock/nginx.lock \\\
  --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \\\
  --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \\\
  --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \\\
  --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \\\
  --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \\\
  --user=%{nginx_user} \\\
  --group=%{nginx_group} \\\
  --with-threads \\\
  --with-http_addition_module \\\
  --with-http_auth_request_module \\\
  --with-http_dav_module \\\
  --with-http_flv_module \\\
  --with-http_gunzip_module \\\
  --with-http_gzip_static_module \\\
  --with-http_mp4_module \\\
  --with-http_random_index_module \\\
  --with-http_realip_module \\\
  --with-http_secure_link_module \\\
  --with-http_slice_module \\\
  --with-http_ssl_module \\\
  --with-http_stub_status_module \\\
  --with-http_sub_module \\\
  --with-http_v2_module \\\
  --with-mail=dynamic \\\
  --with-mail_ssl_module \\\
  --with-stream=dynamic \\\
  --with-stream_ssl_module \\\
  --http-client-body-temp-path=%{_localstatedir}/lib/nginx/body \\\
  --http-fastcgi-temp-path=%{_localstatedir}/lib/nginx/fastcgi \\\
  --http-proxy-temp-path=%{_localstatedir}/lib/nginx/proxy \\\
  --http-scgi-temp-path=%{_localstatedir}/lib/nginx/scgi \\\
  --http-uwsgi-temp-path=%{_localstatedir}/lib/nginx/uwsgi \\\
  --with-debug \\\
  --with-pcre-jit \\\
  --with-ipv6 \\\
  --with-http_geoip_module=dynamic \\\
  --with-http_image_filter_module=dynamic \\\
  --with-http_perl_module=dynamic \\\
  --with-http_xslt_module=dynamic \\\
  --add-module="$PWD/debian/modules/nginx-auth-ldap" \\\
  --add-dynamic-module="$PWD/debian/modules/headers-more-nginx-module" \\\
  --add-dynamic-module="$PWD/debian/modules/nchan" \\\
  --add-dynamic-module="$PWD/debian/modules/nginx-auth-pam" \\\
  --add-dynamic-module="$PWD/debian/modules/nginx-cache-purge" \\\
  --add-dynamic-module="$PWD/debian/modules/nginx-dav-ext-module" \\\
  --add-dynamic-module="$PWD/debian/modules/nginx-development-kit" \\\
  --add-dynamic-module="$PWD/debian/modules/nginx-echo" \\\
  --add-dynamic-module="$PWD/debian/modules/nginx-lua" \\\
  --add-dynamic-module="$PWD/debian/modules/nginx-upload-progress" \\\
  --add-dynamic-module="$PWD/debian/modules/nginx-upstream-fair" \\\
  --add-dynamic-module="$PWD/debian/modules/ngx-fancyindex" \\\
  --add-dynamic-module="$PWD/debian/modules/ngx_http_substitutions_filter_module" \\\
  --with-cc-opt="%{WITH_CC_OPT}" \\\
  --with-ld-opt="%{WITH_LD_OPT}"
%{nil}

# Modules that will come with 1.11
# --with-stream_ssl_preread_module  --with-stream_realip_module"
%global archive %{github}/archive/%{name}-%{commit}.zip
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user www-data
%define nginx_group www-data
%define nginx_loggroup adm
%global shortcommit %(c=%{commit}; echo ${c:0:7})
#
#Source0: nginx-git-0.d5caa44.tar.gz
Source0: %{archive}
#
Requires(pre): shadow-utils
#
Requires: openssl
Requires: systemd-sysv
Requires: dpkg
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
Requires: perl-ExtUtils-Embed
#
BuildRequires: gcc
BuildRequires: dpkg
BuildRequires: perl-ExtUtils-Embed
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

BuildRoot: %{_tmppath}/%{name}-%{version}

%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server.

%prep
#%setup -q -n nginx-git-0.d5caa44
%setup -q -n %{repo}-%{version}

%build
auto/configure --with-debug %{configure_flags}
make %{?_smp_mflags}
%{__mv} objs/nginx objs/nginx-debug
auto/configure %{configure_flags}
make %{?_smp_mflags}
make -f docs/GNUmakefile
%install
%{__rm} -rf $RPM_BUILD_ROOT
vendorarch=$(perl -e "use Config;print substr(\$Config{vendorarch}, 1);")
for i in \
 "$RPM_BUILD_ROOT/$vendorarch" \
 "$RPM_BUILD_ROOT/${vendorarch}/auto/nginx/" \
 "$RPM_BUILD_ROOT%{_libdir}/nginx" \
 "$RPM_BUILD_ROOT%{_libdir}/nginx/modules" \
 "$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig" \
 "$RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d" \
 "$RPM_BUILD_ROOT%{_sysconfdir}/nginx" \
 "$RPM_BUILD_ROOT%{_sysconfdir}/nginx/sites-available" \
 "$RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d" \
 "$RPM_BUILD_ROOT%{_sysconfdir}/nginx/modules-available" \
 "$RPM_BUILD_ROOT%{_sysconfdir}/nginx/modules-enabled" \
 "$RPM_BUILD_ROOT%{_sysconfdir}/ufw/applications.d" \
 "$RPM_BUILD_ROOT%{_datadir}/doc/nginx" \
 "$RPM_BUILD_ROOT%{_datadir}/vim/vimfiles" \
 "$RPM_BUILD_ROOT%{_datadir}/nginx" \
 "$RPM_BUILD_ROOT%{_unitdir}" \
 "$RPM_BUILD_ROOT%{_sysconfdir}/init.d" \
 "$RPM_BUILD_ROOT%{_localstatedir}/log/nginx" \
 "$RPM_BUILD_ROOT%{_localstatedir}/cache/nginx" \
 "$RPM_BUILD_ROOT%{_localstatedir}/run/nginx" \
 "$RPM_BUILD_ROOT%{_localstatedir}/www/html" \
 "$RPM_BUILD_ROOT%{_sbindir}";do \
    %{__install} -m 755 -d "${i}"
done
for i in \
  "$RPM_BUILD_ROOT%{_localstatedir}/lib/nginx" \
;do
 %{__install} -m 770 -o %{nginx_user} -g %{nginx_group} -d "${i}"
done
%{__install}  -g adm -m 755 -d "$RPM_BUILD_ROOT%{_localstatedir}/log/nginx"
cd $RPM_BUILD_ROOT%{_sysconfdir}/nginx && \
  %{__ln_s} ../../%{_libdir}/nginx/modules modules && cd -
%{__install} -m 0644 -p debian/nginx-common.nginx.default \
    "$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx"
%{__install} -m 0644 -p debian/nginx-common.nginx.default \
    "$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx-debug"
echo "DAEMON=%{_sbindir}/nginx-debug" >> \
    "$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx-debug"
%{__install} -p -D -m 0644 objs/nginx.8 \
    $RPM_BUILD_ROOT%{_mandir}/man8/nginx.8

%{__install} -m644 debian/nginx-common.nginx.logrotate \
    "$RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx"
sed -i -re "s/invoke-rc.d/service/g"\
 "$RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx"

%if ( %{use_systemd} )
# install systemd-specific files
%{__install} -m644 debian/nginx-common.nginx.service \
    $RPM_BUILD_ROOT%{_unitdir}/nginx.service
%{__install} -m644 debian/nginx-common.nginx.service \
    $RPM_BUILD_ROOT%{_unitdir}/nginx-debug.service
sed -i -r\
 -e "s/(sysconfig|sbin)\/nginx/\\1\/nginx-debug/" \
 $RPM_BUILD_ROOT%{_unitdir}/nginx.service \
 $RPM_BUILD_ROOT%{_unitdir}/nginx-debug.service
%endif

# install SYSV init stuff
%{__install} -m755 mc_packaging/redhat/init.d/nginx \
  $RPM_BUILD_ROOT%{_sysconfdir}/init.d/nginx
%{__install} -m755 mc_packaging/redhat/init.d/nginx \
  $RPM_BUILD_ROOT%{_sysconfdir}/init.d/nginx-debug
sed -i -r\
 -e "s/(sysconfig|sbin)\/nginx/\\1\/nginx-debug/" \
 $RPM_BUILD_ROOT%{_sysconfdir}/init.d/nginx-debug

%{__install} -D -m644 \
 objs/src/http/modules/perl/blib/arch/auto/nginx/* \
 "$RPM_BUILD_ROOT/${vendorarch}/auto/nginx/"
%{__install} -D -m644 \
 objs/src/http/modules/perl/blib/lib/nginx.pm \
 "$RPM_BUILD_ROOT/$vendorarch"

cp -rf debian/conf/* \
 "$RPM_BUILD_ROOT/%{_sysconfdir}/nginx"
%{__install} -D -m644 debian/ufw/nginx \
 "$RPM_BUILD_ROOT/%{_sysconfdir}/ufw/applications.d"
cp -rf contrib/vim/* \
 "$RPM_BUILD_ROOT/%{_datadir}/vim/vimfiles"
%{__install} -D -m644 docs/html/index.html \
 "$RPM_BUILD_ROOT/%{_localstatedir}/www/html/"
%{__install} -D -m0755 objs/nginx \
 "$RPM_BUILD_ROOT/%{_sbindir}"
%{__install} -D -m0755 objs/nginx-debug \
 "$RPM_BUILD_ROOT/%{_sbindir}"
%{__install} -D -m644 docs/text/* \
 "$RPM_BUILD_ROOT%{_datadir}/doc/nginx"
%{__install} -m 0644 -p ./tmp/*/CHANGES \
    "$RPM_BUILD_ROOT%{_datadir}/doc/nginx"
cp -rf debian/help/docs/* \
 "$RPM_BUILD_ROOT%{_datadir}/doc/nginx"

for mod in objs/*_module.so;do
 bmod=$(basename "$(basename $mod)" .so)
 cp -f $mod "$RPM_BUILD_ROOT%{_libdir}/nginx/modules"
 prio=50
 case $mod in
    *ndk*) prio=10;;
    *) prio=50;;
 esac
 echo "load_module modules/$(basename ${mod});" \
  >$RPM_BUILD_ROOT/%{_sysconfdir}/nginx/modules-available/${prio}_${bmod}.conf
done
cd $RPM_BUILD_ROOT/%{_sysconfdir}/nginx/modules-enabled &&\
 for i in ../modules-available/*;do ln -s $i . ;done && \
 cd -
%{__ln_s} %{_libdir}/nginx/modules \
 $RPM_BUILD_ROOT/usr/share/nginx/modules
chmod  0750    $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
chown root:adm $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
sed -i -r \
  -e "/include.*sites-enabled/d" \
  $RPM_BUILD_ROOT/%{_sysconfdir}/nginx/nginx.conf
%clean
%files
%config(noreplace) %{_sysconfdir}/init.d/nginx
%config(noreplace) %{_sysconfdir}/init.d/nginx-debug
%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/nginx/fastcgi.conf
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/sites-available/default
%config %{_sysconfdir}/nginx/koi-utf
%config %{_sysconfdir}/nginx/koi-win
%config %{_sysconfdir}/nginx/mime.types
%config %{_sysconfdir}/nginx/modules-available/10_ndk_http_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_auth_pam_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_echo_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_fancyindex_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_geoip_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_headers_more_filter_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_image_filter_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_lua_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_perl_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_uploadprogress_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_http_xslt_filter_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_mail_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_nchan_module.conf
%config %{_sysconfdir}/nginx/modules-available/50_ngx_stream_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/10_ndk_http_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_auth_pam_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_echo_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_fancyindex_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_geoip_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_headers_more_filter_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_image_filter_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_lua_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_perl_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_uploadprogress_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_http_xslt_filter_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_mail_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_nchan_module.conf
%config %{_sysconfdir}/nginx/modules-enabled/50_ngx_stream_module.conf
%config %{_sysconfdir}/nginx/win-utf
%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/proxy_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/snippets/fastcgi-php.conf
%config(noreplace) %{_sysconfdir}/nginx/snippets/snakeoil.conf
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/ufw/applications.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx-debug
%config(noreplace) %{_unitdir}/nginx-debug.service
%config(noreplace) %{_unitdir}/nginx.service
/usr/lib%{__isa_bits}/nginx/modules/ndk_http_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_auth_pam_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_echo_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_fancyindex_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_geoip_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_headers_more_filter_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_image_filter_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_lua_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_perl_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_uploadprogress_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_xslt_filter_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_mail_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_nchan_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_stream_module.so
/usr/lib%{__isa_bits}/perl*/vendor_perl/auto/nginx/nginx.bs
/usr/lib%{__isa_bits}/perl*/vendor_perl/auto/nginx/nginx.so
/usr/lib%{__isa_bits}/perl*/vendor_perl/nginx.pm
%{_sbindir}/nginx
%{_sbindir}/nginx-debug
#
%doc %{_datadir}/doc/nginx/CHANGES
%doc %{_datadir}/doc/nginx/LICENSE
%doc %{_datadir}/doc/nginx/README
%doc %{_datadir}/doc/nginx/fcgiwrap
%doc %{_datadir}/doc/nginx/php
%doc %{_datadir}/doc/nginx/support-irc
%doc %{_datadir}/doc/nginx/upstream
%doc %{_datadir}/man/man8/nginx.8.gz
#
%{_sysconfdir}/nginx/conf.d
%{_sysconfdir}/nginx/sites-available
%{_sysconfdir}/nginx/modules
%{_datadir}/nginx/modules
%{_datadir}/vim/vimfiles/ftdetect/nginx.vim
%{_datadir}/vim/vimfiles/indent/nginx.vim
%{_datadir}/vim/vimfiles/syntax/nginx.vim
%{_localstatedir}/cache/nginx
%{_localstatedir}/run/nginx
%{_localstatedir}/www/html/index.html
%attr(0770,%{nginx_user},%{nginx_group}) %{_localstatedir}/lib/nginx
%attr(0750,root,adm) %{_localstatedir}/log/nginx
%pre
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -d %{_localstatedir}/www/html -s /sbin/nologin \
    -c "WEB/www user" %{nginx_user}
%post
%preun
service nginx stop || /bin/true
%postun
%changelog
* Tue Feb 28 2017 Mathieu Le Marec - Pasquet <kiorky@cryptelium.net>
- fix setup source (kiorky@cryptelium.net)

* Tue Feb 28 2017 Mathieu Le Marec - Pasquet <kiorky@cryptelium.net> 1.10.3-3
- release (kiorky@cryptelium.net)

* Tue Feb 28 2017 Mathieu Le Marec - Pasquet <kiorky@cryptelium.net>
- init

