#!/usr/bin/env bash
set -ex
export DEBEMAIL=${DEBEMAIL:-kiorky@cryptelium.net}
VER=${VER:-1.7.5}
KEY="${KEY:-0x5616F8C2}"
FLAVORS="trusty precise"
cd $(dirname $0)/..
W=$PWD
cd $W/..
if [ ! -e debian-up ];then
    git clone git://anonscm.debian.org/collab-maint/nginx.git debian-up
fi
if [ ! -e nginx-auth-ldap ];then
    git clone https://github.com/kvspb/nginx-auth-ldap.git
fi
cd $W/../debian-up && git fetch --all && git reset --hard origin/master
cd $W/../nginx-auth-ldap && git fetch --all && git reset --hard origin/master
cd $W
#rsync -azv --exclude=changelog --exclude=nginx-lua ../debian-up/debian/ debian/
rsync -azv --exclude=changelog ../debian-up/debian/ debian/
rsync -azv ../nginx-auth-ldap/    debian/modules/nginx-auth-ldap/
#XXX: do not build with 1.7.5
# --add-module=\$(MODULESDIR)/nginx-lua \\\\
/usr/bin/python << EOF
TOADD  = '''
common_configure_flags := \\\\
    --with-cc-opt="\$(debian_cflags)" \\\\
    --with-ld-opt="\$(debian_ldflags)" \\\\
    --prefix=/usr/share/nginx \\\\
    --conf-path=/etc/nginx/nginx.conf \\\\
    --http-log-path=/var/log/nginx/access.log \\\\
    --error-log-path=/var/log/nginx/error.log \\\\
    --lock-path=/var/lock/nginx.lock \\\\
    --pid-path=/run/nginx.pid \\\\
    --http-client-body-temp-path=/var/lib/nginx/body \\\\
    --http-fastcgi-temp-path=/var/lib/nginx/fastcgi \\\\
    --http-proxy-temp-path=/var/lib/nginx/proxy \\\\
    --http-scgi-temp-path=/var/lib/nginx/scgi \\\\
    --http-uwsgi-temp-path=/var/lib/nginx/uwsgi \\\\
    --with-debug \\\\
    --with-http_addition_module \\\\
    --with-http_auth_request_module \\\\
    --with-http_dav_module \\\\
    --with-http_flv_module \\\\
    --with-http_geoip_module \\\\
    --with-http_gzip_static_module \\\\
    --with-http_image_filter_module \\\\
    --with-http_mp4_module \\\\
    --with-http_perl_module \\\\
    --with-http_random_index_module \\\\
    --with-http_realip_module \\\\
    --with-http_secure_link_module \\\\
    --with-http_spdy_module \\\\
    --with-http_ssl_module \\\\
    --with-http_stub_status_module \\\\
    --with-http_sub_module \\\\
    --with-http_xslt_module \\\\
    --with-ipv6 \\\\
    --with-mail \\\\
    --with-mail_ssl_module \\\\
    --with-pcre-jit \\\\
    --add-module=\$(MODULESDIR)/headers-more-nginx-module \\\\
    --add-module=\$(MODULESDIR)/naxsi/naxsi_src \\\\
    --add-module=\$(MODULESDIR)/nginx-auth-pam \\\\
    --add-module=\$(MODULESDIR)/nginx-auth-ldap \\\\
    --add-module=\$(MODULESDIR)/nginx-cache-purge \\\\
    --add-module=\$(MODULESDIR)/nginx-dav-ext-module \\\\
    --add-module=\$(MODULESDIR)/nginx-development-kit \\\\
    --add-module=\$(MODULESDIR)/nginx-echo \\\\
    --add-module=\$(MODULESDIR)/nginx-http-push \\\\
    --add-module=\$(MODULESDIR)/nginx-upload-progress \\\\
    --add-module=\$(MODULESDIR)/nginx-upstream-fair \\\\
    --add-module=\$(MODULESDIR)/ngx-fancyindex \\\\
    --add-module=\$(MODULESDIR)/ngx_http_substitutions_filter_module

light_configure_flags := \$(common_configure_flags)
full_configure_flags := \$(common_configure_flags)
extras_configure_flags := \$(common_configure_flags)
naxsi_configure_flags := \$(common_configure_flags)
'''.splitlines()
with open('debian/rules') as fic:
    lines = fic.read().splitlines()
    content = []
    for l in lines[:]:
        if l.startswith('%:'):
            for a in TOADD:
                content.append(a)
        content.append(l)

with open('debian/rules', 'w') as fic:
    fic.write('\n'.join(content))
EOF
cd debian
sed "s/FLAVOURS :=.*/FLAVOURS := full light extras naxsi/g" -i rules
#sed  "/dh_installlogrotate --package nginx-common --name=nginx/ {
#a\	dh_installlogrotate --package nginx-naxsi --name=nginx
#a\	dh_installlogrotate --package nginx-full --name=nginx
#a\	dh_installlogrotate --package nginx-ligth --name=nginx
#a\	dh_installlogrotate --package nginx-extra --name=nginx
#}
#" -i rules

# assemble
for i in postrm preinst;do
    ls ../../debian-up/debian/*.$i|grep -v makina|xargs cat|grep -v "exit 0"> nginx-makina.$i
    echo "exit 0">>nginx-makina.$i
done
for i in dirs manpages examples manpages install lintian-overrides;do
    ls ../../debian-up/debian/*.$i|grep -v makina|xargs cat>nginx-makina.$i
    cp  nginx-makina.$i nginx-makina.${i}.in
done
cat nginx-makina.lintian-overrides.in|sed -re "s/[^:]+:(.*)/nginx-makina:\1/g" | sort -u > nginx-makina.lintian-overrides
rm -f nginx*makina*.in
# same nginx compile for
for j in common;do
    for i in dirs manpages docs examples lintian-overrides \
             manpages postrm preinst;do
        cp -v nginx-makina.$i nginx-$j.$i
    done
done
# make those packages, dummy packages
for j in doc full light extras naxsi naxsi-ui;do
    for i in dirs manpages docs examples install lintian-overrides \
             manpages postrm preinst;do
        echo > nginx-${j}.${i}
    done
done
for i in nginx-common.install nginx-makina.install;do
    cp ${i} ${i}.in
    echo "#!/usr/bin/perl -w">$i
    cat ${i}.in |\
        grep -v "bin/perl" \
        | sed -e 's/^html\(.*\)/print "html\1\\n";/g' \
        | sed -e 's/^debian\(.*\)/print "debian\1\\n";/g'>>$i
done
cp -f control.in control
sed "s/-lldap\"/-lldap -llber\"/g" -i $W/debian/modules/nginx-auth-ldap/config
cp -f ../../debian-up/debian/nginx-naxsi-ui.nginx-naxsi-ui.init nginx-common.nginx-naxsi-ui.init
rm -f nginx-common.install nginx-common.install.in nginx-makina.install.in
cp -f nginx-makina.install nginx-common.install
cp -f nginx-makina.install.raw nginx-makina.install
cp -f nginx-makina.install.raw nginx-common.install

echo "3.0 (native)">$W/debian/source/format
## make release tarball
#cd $W
#rm -rf ../upstream
#git clone -b master . ../upstream
#cd $W/../upstream
#tar cjf ../nginx_${VER}.orig.tar.bz2 . --exclude=.git
#rm -rf ../upstream

cd $W
CHANGES=""
if [ -e $HOME/.gnupg/.gpg-agent-info ];then
    . $HOME/.gnupg/.gpg-agent-info
fi
# make a release for each flavor
logfile=../log
if [ -e ${logfile} ];then
    rm -f ${logfile}
fi
if [ -e ${logfile}.pipe ];then
    rm -f ${logfile}.pipe
fi
mkfifo ${logfile}.pipe
tee < ${logfile}.pipe $logfile &
exec 1> ${logfile}.pipe 2> ${logfile}.pipe
for i in $FLAVORS;do
    j=$((j+1));
    dch -i -D ${i} "packaging for $i"
    debuild -k${KEY} -S -sa --lintian-opts -i
done
rm ${logfile}.pipe
exec 1>&1
egrep "signfile" log|sed "s///g"
CHANGES=$(grep "signfile " ../log|awk '{print  $2}'|grep source.changes)
rm -f log
# upload to final PPA
cd $W
for i in $CHANGES;do
    dput nginx ../$i
done
# vim:set et sts=4 ts=4 tw=0:
