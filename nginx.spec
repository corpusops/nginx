# packaging notes
# we dont use main_version & main_release but directly the vars
# as tito replace only those macros
#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user nginx
%define nginx_group nginx
%define nginx_loggroup adm

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} == 1315)

%if 0%{?rhel} == 6
%define _group System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
%endif

%if 0%{?rhel} == 7
BuildRequires: redhat-lsb-core
%define _group System Environment/Daemons
%define epoch 1
Epoch: %{epoch}
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%define os_minor %(lsb_release -rs | cut -d '.' -f 2)
%if %{os_minor} >= 4
Requires: openssl >= 1.0.2
BuildRequires: openssl-devel >= 1.0.2
%define dist .el7_4
%else
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
%define dist .el7
%endif
%endif

%if 0%{?suse_version} == 1315
%define _group Productivity/Networking/Web/Servers
%define nginx_loggroup trusted
Requires(pre): shadow
Requires: systemd
BuildRequires: libopenssl-devel
BuildRequires: systemd
%endif

# end of distribution specific definitions
%define main_version VERSION_NOTUSED
%define main_release RELEASE_NOTUSED

# tito: make a symlink not to have a big diff
%define bdir %{_builddir}/nginx

%define WITH_CC_OPT $(echo %{optflags} $(pcre-config --cflags)) -fPIC
%define WITH_LD_OPT -Wl,-z,relro -Wl,-z,now -pie

%define BASE_CONFIGURE_ARGS --prefix=%{_sysconfdir}/nginx \\\
  --prefix=%{_sysconfdir}/nginx \\\
  --sbin-path=%{_sbindir}/nginx \\\
  --modules-path=%{_libdir}/nginx/modules \\\
  --conf-path=%{_sysconfdir}/nginx/nginx.conf \\\
  --error-log-path=%{_localstatedir}/log/nginx/error.log \\\
  --http-log-path=%{_localstatedir}/log/nginx/access.log \\\
  --pid-path=%{_localstatedir}/run/nginx.pid \\\
  --lock-path=%{_localstatedir}/run/nginx.lock \\\
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
  --with-stream_ssl_preread_module  \\\
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
  --add-dynamic-module="$PWD/debian/modules/ngx_http_substitutions_filter_module"
%{nil}

Summary: High performance web server
Name: nginx
Version: 0.12.2
Release: 2
Vendor: Nginx, Inc.
URL: http://nginx.org/
Group: %{_group}

%define nginx_home %{_localstatedir}/cache/nginx

Source0: BUILDBYTITOLOCALLY
Source1: logrotate
Source2: nginx.init.in
Source3: nginx.sysconf
Source4: nginx.conf
Source5: nginx.vh.default.conf
Source7: nginx-debug.sysconf
Source8: nginx.service
Source9: nginx.upgrade.sh
Source10: nginx.suse.logrotate
Source11: nginx-debug.service
Source12: COPYRIGHT
Source13: nginx.check-reload.sh

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
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
BuildRequires: luajit-devel
BuildRequires: hiredis-devel
BuildRequires: GeoIP-devel
BuildRequires: gd-devel
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
Requires(pre): shadow-utils

Provides: webserver

%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server.

%if 0%{?suse_version} == 1315
%debug_package
%endif

%prep
%setup -q -n %{name}-%{version}
# tito: make a symlink not to have a big diff
ln -s $PWD ../nginx
cp %{SOURCE2} .
sed -e 's|%%DEFAULTSTART%%|2 3 4 5|g' -e 's|%%DEFAULTSTOP%%|0 1 6|g' \
    -e 's|%%PROVIDES%%|nginx|g' < %{SOURCE2} > nginx.init
sed -e 's|%%DEFAULTSTART%%||g' -e 's|%%DEFAULTSTOP%%|0 1 2 3 4 5 6|g' \
    -e 's|%%PROVIDES%%|nginx-debug|g' < %{SOURCE2} > nginx-debug.init
patch -Np1 debian/patches/0002-Make-sure-signature-stays-the-same-in-all-nginx-buil.patch
patch -Np1 debian/patches/0003-define_gnu_source-on-other-glibc-based-platforms.patch
cd debian/modules
cd nginx-upstream-fair/
patch -Np1 <../patches/nginx-upstream-fair/drop-default-port.patch
patch -Np1 <../patches/nginx-upstream-fair/dynamic-module.patch
patch -Np1 <../patches/nginx-upstream-fair/openssl-1.1.0.patch
cd -
cd nginx-echo
patch -Np1 <../patches/nginx-echo/build-nginx-1.11.11.patch
cd -
cd ngx_http_substitutions_filter_module
patch -Np1 <../patches/ngx_http_substitutions_filter_module/dynamic-module.patch
cd -
cd nginx-cache-purge
patch -Np1 <../patches/nginx-cache-purge/dynamic-module.patch
cd -
cd nginx-dav-ext-module
patch -Np1 <../patches/nginx-dav-ext-module/dynamic-module.patch
cd -
cd ../..

%build
auto/configure %{BASE_CONFIGURE_ARGS} \
    --with-cc-opt="%{WITH_CC_OPT}" \
    --with-ld-opt="%{WITH_LD_OPT}" \
    --with-debug
make %{?_smp_mflags}
%{__mv} %{bdir}/objs/nginx \
    %{bdir}/objs/nginx-debug
auto/configure %{BASE_CONFIGURE_ARGS} \
    --with-cc-opt="%{WITH_CC_OPT}" \
    --with-ld-opt="%{WITH_LD_OPT}"
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
 "$RPM_BUILD_ROOT%{_datadir}/vim/vimfiles" \
    ;do \
    %{__install} -m 755 -d "${i}"
done
for i in \
  "$RPM_BUILD_ROOT%{_localstatedir}/lib/nginx" \
;do
 %{__install} -m 770 -o root -g root -d "${i}"
done
%{__make} DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} docs/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_libdir}/nginx/modules
cd $RPM_BUILD_ROOT%{_sysconfdir}/nginx && \
    %{__ln_s} ../..%{_libdir}/nginx/modules modules && cd -

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
%{__install} -m 644 -p %{SOURCE12} \
    $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE5} \
    $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx
%{__install} -m 644 -p %{SOURCE7} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx-debug

%{__install} -p -D -m 0644 %{bdir}/objs/nginx.8 \
    $RPM_BUILD_ROOT%{_mandir}/man8/nginx.8

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
    $RPM_BUILD_ROOT%{_unitdir}/nginx.service
%{__install} -m644 %SOURCE11 \
    $RPM_BUILD_ROOT%{_unitdir}/nginx-debug.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
%{__install} -m755 %SOURCE9 \
    $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%{__install} -m755 %SOURCE13 \
    $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/check-reload
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 nginx.init $RPM_BUILD_ROOT%{_initrddir}/nginx
%{__install} -m755 nginx-debug.init $RPM_BUILD_ROOT%{_initrddir}/nginx-debug
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%if 0%{?suse_version}
%{__install} -m 644 -p %{SOURCE10} \
    $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%else
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%endif

%{__install} -m755 %{bdir}/objs/nginx-debug \
    $RPM_BUILD_ROOT%{_sbindir}/nginx-debug

cp -rf contrib/vim/* "$RPM_BUILD_ROOT/%{_datadir}/vim/vimfiles"

%{__install} -D -m644 objs/src/http/modules/perl/blib/arch/auto/nginx/* \
 "$RPM_BUILD_ROOT/${vendorarch}/auto/nginx/"
%{__install} -D -m644 objs/src/http/modules/perl/blib/lib/nginx.pm \
 "$RPM_BUILD_ROOT/$vendorarch"
%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx
%{_sbindir}/nginx-debug
/usr/lib%{__isa_bits}/nginx/modules/ndk_http_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_auth_pam_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_cache_purge_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_dav_ext_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_echo_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_fancyindex_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_geoip_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_headers_more_filter_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_image_filter_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_lua_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_perl_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_subs_filter_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_uploadprogress_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_upstream_fair_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_http_xslt_filter_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_mail_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_nchan_module.so
/usr/lib%{__isa_bits}/nginx/modules/ngx_stream_module.so
/usr/lib%{__isa_bits}/perl*/vendor_perl/auto/nginx/nginx.bs
/usr/lib%{__isa_bits}/perl*/vendor_perl/auto/nginx/nginx.so
/usr/lib%{__isa_bits}/perl*/vendor_perl/nginx.pm
/usr/lib%{__isa_bits}/perl*/perllocal.pod
/usr/lib%{__isa_bits}/perl*/vendor_perl/auto/nginx/.packlist

%config(noreplace) %{_sysconfdir}/nginx/html/50x.html
%config(noreplace) %{_sysconfdir}/nginx/html/index.html

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d
%{_sysconfdir}/nginx/modules

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx-debug
%if %{use_systemd}
%{_unitdir}/nginx.service
%{_unitdir}/nginx-debug.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/nginx
%{_initrddir}/nginx-debug
%endif

%attr(0755,root,root) %dir %{_libdir}/nginx
%attr(0755,root,root) %dir %{_libdir}/nginx/modules
%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

%dir %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}-%{version}/COPYRIGHT
%{_mandir}/man3/nginx.3pm.gz
%{_mandir}/man8/nginx.8*
%{_datadir}/vim/vimfiles/ftdetect/nginx.vim
%{_datadir}/vim/vimfiles/ftplugin/nginx.vim
%{_datadir}/vim/vimfiles/indent/nginx.vim
%{_datadir}/vim/vimfiles/syntax/nginx.vim

%pre
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0

%post
# Register the nginx service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl preset nginx-debug.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
    /sbin/chkconfig --add nginx-debug
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using nginx!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Please subscribe to nginx-announce mailing list to get
the most important news about nginx:
* http://nginx.org/en/support.html

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

----------------------------------------------------------------------
BANNER

    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:%{nginx_loggroup} %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
    /sbin/chkconfig --del nginx-debug
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi

%changelog
* Wed Jan 24 2018 Makina Corpus <freesoftware@makina-corpus.com> 1.12.2-2
- bump version & stick to redhat packaging (bring only modules & patches from debian, remove shared conf)

* Tue Dec 26 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.13.8

* Tue Nov 21 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.13.7

* Tue Oct 10 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.13.6

* Tue Sep  5 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.13.5

* Tue Aug  8 2017 Sergey Budnevitch <sb@nginx.com>
- 1.13.4

* Tue Jul 11 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.13.3
- Fixes CVE-2017-7529

* Tue Jun 27 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.13.2

* Tue May 30 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.13.1

* Tue Apr 25 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.13.0

* Tue Apr  4 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.11.13
- CentOS7/RHEL7: made upgrade loops/timeouts configurable via
  /etc/sysconfig/nginx.
- Bumped upgrade defaults to five loops one second each.

* Fri Mar 24 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.11.12

* Tue Mar 21 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.11.11

* Tue Feb 28 2017 Makina Corpus <freesoftware@makina-corpus.com> 1.10.3-4
- bump version (freesoftware@makina-corpus.com)
- fix setup source (freesoftware@makina-corpus.com)

* Tue Feb 28 2017 Makina Corpus <freesoftware@makina-corpus.com>
- fix setup source (freesoftware@makina-corpus.com)

* Tue Feb 28 2017 Makina Corpus <freesoftware@makina-corpus.com> 1.10.3-3
- release (freesoftware@makina-corpus.com)

* Tue Feb 28 2017 Makina Corpus <freesoftware@makina-corpus.com>
- init

* Tue Feb 14 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.11.10

* Tue Jan 24 2017 Konstantin Pavlov <thresh@nginx.com>
- 1.11.9
- Extended hardening build flags.
- Added check-reload target to init script / systemd service.

* Tue Dec 27 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.11.8

* Tue Dec 13 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.11.7

* Tue Nov 15 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.11.6

* Mon Oct 10 2016 Andrei Belov <defan@nginx.com>
- 1.11.5

* Tue Sep 13 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.11.4.
- njs updated to 0.1.2.

* Tue Jul 26 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.11.3.
- njs updated to 0.1.0.
- njs stream dynamic module added to nginx-module-njs package.
- geoip stream dynamic module added to nginx-module-geoip package.

* Tue Jul  5 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.11.2
- njs updated to ef2b708510b1.

* Tue May 31 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.11.1

* Tue May 24 2016 Sergey Budnevitch <sb@nginx.com>
- Fixed logrotate error if nginx is not running
- 1.11.0

* Tue Apr 19 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.9.15
- njs updated to 1c50334fbea6.

* Tue Apr  5 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.9.14

* Tue Mar 29 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.9.13
- Added perl and nJScript dynamic modules
- Fixed Requires section for dynamic modules on CentOS7/RHEL7

* Wed Feb 24 2016 Sergey Budnevitch <sb@nginx.com>
- common configure args are now in macros
- xslt, image-filter and geoip dynamic modules added
- 1.9.12

* Tue Feb  9 2016 Sergey Budnevitch <sb@nginx.com>
- dynamic modules path and symlink in %{_sysconfdir}/nginx added
- 1.9.11

* Tue Jan 26 2016 Konstantin Pavlov <thresh@nginx.com>
- 1.9.10

* Wed Dec  9 2015 Konstantin Pavlov <thresh@nginx.com>
- 1.9.9

* Tue Dec  8 2015 Konstantin Pavlov <thresh@nginx.com>
- 1.9.8
- http_slice module enabled

* Tue Nov 17 2015 Konstantin Pavlov <thresh@nginx.com>
- 1.9.7

* Tue Oct 27 2015 Sergey Budnevitch <sb@nginx.com>
- 1.9.6

* Tue Sep 22 2015 Andrei Belov <defan@nginx.com>
- 1.9.5
- http_spdy module replaced with http_v2 module

* Tue Aug 18 2015 Konstantin Pavlov <thresh@nginx.com>
- 1.9.4

* Tue Jul 14 2015 Sergey Budnevitch <sb@nginx.com>
- 1.9.3

* Tue May 26 2015 Sergey Budnevitch <sb@nginx.com>
- 1.9.1

* Tue Apr 28 2015 Sergey Budnevitch <sb@nginx.com>
- 1.9.0
- thread pool support added
- stream module added
- example_ssl.conf removed

* Tue Apr  7 2015 Sergey Budnevitch <sb@nginx.com>
- 1.7.12

* Tue Mar 24 2015 Sergey Budnevitch <sb@nginx.com>
- 1.7.11

* Tue Feb 10 2015 Sergey Budnevitch <sb@nginx.com>
- 1.7.10

* Tue Dec 23 2014 Sergey Budnevitch <sb@nginx.com>
- 1.7.9

* Tue Dec  2 2014 Sergey Budnevitch <sb@nginx.com>
- 1.7.8

* Tue Sep 30 2014 Sergey Budnevitch <sb@nginx.com>
- 1.7.6

* Tue Sep 16 2014 Sergey Budnevitch <sb@nginx.com>
- epoch added to the EPEL7/CentOS7 spec to override EPEL one
- 1.7.5

* Tue Aug  5 2014 Sergey Budnevitch <sb@nginx.com>
- 1.7.4

* Tue Jul  8 2014 Sergey Budnevitch <sb@nginx.com>
- 1.7.3

* Tue Jun 17 2014 Sergey Budnevitch <sb@nginx.com>
- 1.7.2

* Tue May 27 2014 Sergey Budnevitch <sb@nginx.com>
- 1.7.1
- incorrect sysconfig filename finding in the initscript fixed

* Thu Apr 24 2014 Konstantin Pavlov <thresh@nginx.com>
- 1.7.0

* Tue Apr  8 2014 Sergey Budnevitch <sb@nginx.com>
- 1.5.13
- built spdy module on rhel/centos 6

* Tue Mar 18 2014 Sergey Budnevitch <sb@nginx.com>
- 1.5.12
- spec cleanup
- openssl version dependence added
- upgrade() function in the init script improved
- warning added when binary upgrade returns non-zero exit code

* Tue Mar  4 2014 Sergey Budnevitch <sb@nginx.com>
- 1.5.11

* Tue Feb  4 2014 Sergey Budnevitch <sb@nginx.com>
- 1.5.10

* Wed Jan 22 2014 Sergey Budnevitch <sb@nginx.com>
- 1.5.9

* Tue Dec 17 2013 Sergey Budnevitch <sb@nginx.com>
- 1.5.8
- fixed invalid week days in the changelog

* Tue Nov 19 2013 Sergey Budnevitch <sb@nginx.com>
- 1.5.7

* Tue Oct  1 2013 Sergey Budnevitch <sb@nginx.com>
- 1.5.6

* Tue Sep 17 2013 Andrei Belov <defan@nginx.com>
- 1.5.5

* Tue Aug 27 2013 Sergey Budnevitch <sb@nginx.com>
- 1.5.4
- auth request module added

* Tue Jul 30 2013 Sergey Budnevitch <sb@nginx.com>
- 1.5.3

* Tue Jul  2 2013 Sergey Budnevitch <sb@nginx.com>
- 1.5.2

* Tue Jun  4 2013 Sergey Budnevitch <sb@nginx.com>
- 1.5.1

* Mon May  6 2013 Sergey Budnevitch <sb@nginx.com>
- 1.5.0

* Tue Apr 16 2013 Sergey Budnevitch <sb@nginx.com>
- 1.3.16

* Tue Mar 26 2013 Sergey Budnevitch <sb@nginx.com>
- 1.3.15
- gunzip module added
- set permissions on default log files at installation

* Tue Feb 12 2013 Sergey Budnevitch <sb@nginx.com>
- excess slash removed from --prefix
- 1.2.7

* Tue Dec 11 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.6

* Tue Nov 13 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.5

* Tue Sep 25 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.4

* Tue Aug  7 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.3
- nginx-debug package now actually contains non stripped binary

* Tue Jul  3 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.2

* Tue Jun  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.1

* Mon Apr 23 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.0

* Thu Apr 12 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.15

* Thu Mar 15 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.14
- OpenSUSE init script and SuSE specific changes to spec file added

* Mon Mar  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.13

* Mon Feb  6 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.12
- banner added to install script

* Thu Dec 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.11
- init script enhancements (thanks to Gena Makhomed)
- one second sleep during upgrade replaced with 0.1 sec usleep

* Tue Nov 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.10

* Tue Nov  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.9
- nginx-debug package added

* Tue Oct 11 2011 Sergey Budnevitch <sb@nginx.com>
- spec file cleanup (thanks to Yury V. Zaytsev)
- log dir permitions fixed
- logrotate creates new logfiles with nginx owner
- "upgrade" argument to init-script added (based on fedora one)

* Sat Oct  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.8
- built with mp4 module

* Fri Sep 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.7

* Tue Aug 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.6
- replace "conf.d/*" config include with "conf.d/*.conf" in default nginx.conf

* Wed Aug 10 2011 Sergey Budnevitch
- Initial release
