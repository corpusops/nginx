#!/usr/bin/env bash
set -ex
cd "$(dirname $0)/.."
export W="${PWD}"
export PACKAGE="nginx"
export PPA="${PACKAGE}"
export REPO="git://anonscm.debian.org/collab-maint/nginx.git"
export DEBEMAIL=${DEBEMAIL:-kiorky@cryptelium.net}
export KEY="${KEY:-0x5616F8C2}"
export VER=${VER:-"$(grep "#define NGINX_VERSION" src/core/nginx.h 2>/dev/null|awk '{print $3}'|sed 's/"//g')"}
export VER="1.10.2"
export FLAVORS="vivid trusty precise"
export FLAVORS="trusty xenial yakkety zesty"
export RELEASES="${RELEASES:-"experimental|yakkety|zesty|stable|unstable|precise|trusty|utopic|vivid|oneric|wily|xenial"}"
if [ "x${VER}" = "x" ];then echo unknownversion;exit -1;fi
if echo $VER | grep -q 1.10; then
    export DEBIAN_REMOTE=origin/master
else
    export DEBIAN_REMOTE=origin/experimental
fi
if [ "x${REPO}" != "x" ];then
    if [ ! -e "${W}/../debian-up" ];then
        git clone "${REPO}" "${W}/../debian-up";
    fi
    cd "${W}/"../debian-up && rm -rf * && git fetch --all && git reset --hard $DEBIAN_REMOTE
    rsync -av --delete --exclude="*.makina.*" \
        --exclude=po/\
        --exclude=changelog\
        "${W}/../debian-up/debian/" "${W}/debian/"
fi
if [ -e "${W}/mc_packaging/debian/" ];then
    rsync -av "${W}/mc_packaging/debian/" "${W}/debian/"
fi
#
# CUSTOM MERGE CODE HERE
# <>
ldap_url=https://github.com/kvspb/nginx-auth-ldap.git
#lua_url=https://github.com/openresty/lua-nginx-module.git
if [ ! -e "${W}/../nginx-auth-ldap" ];then
    git clone https://github.com/kvspb/nginx-auth-ldap.git "${W}/../nginx-auth-ldap"
fi
if [ ! -e "${W}/../nginx-lua" ];then
    git clone https://github.com/openresty/lua-nginx-module.git "${W}/../nginx-lua"
fi
cd "${W}/../nginx-auth-ldap" && git config --replace-all remote.origin.url $ldap_url && git fetch --all && git reset --hard origin/master
cd "${W}/../nginx-lua"       && git config --replace-all remote.origin.url $lua_url && git fetch --all && git reset --hard origin/master
cd "${W}"
rsync -azv --delete --delete-excluded --exclude=.git ../nginx-auth-ldap/ debian/modules/nginx-auth-ldap/
rsync -azv --delete --delete-excluded --exclude=.git ../nginx-lua/ debian/modules/nginx-lua/
rm -rf debian/modules/nginx-auth-ldap/.git
rm -rf debian/nginx*upstart
rm -rf debian/modules/nginx-lua/.git
rm -rf debian/patches/modules/nginx-lua/
/usr/bin/python << EOF
TOADDpre = open('mc_packaging/makefile.in.pre').read().splitlines()
TOADDpost = open('mc_packaging/makefile.in.post').read().splitlines()
with open('debian/rules') as fic:
    lines = fic.read().splitlines()
    content, contentd = [], []
    skip = False
    no_common_skip = False
    no_common_skipped = []
    for l in lines[:]:
        if '_configure_flags :=' in l:
            skip = True
            if 'common' not in l:
                no_common_skip = True
        if l.startswith('%:'):
            skip = False
        if l.startswith('%:'):
            content.extend(TOADDpre[:])
            content.extend(no_common_skipped)
            content.extend(TOADDpost[:])
            #contentd.extend(TOADDpre[:])
            #contentd.extend(no_common_skipped)
            skip = False
            no_common_skip = False
        if no_common_skip:
            no_common_skipped.append(l)
        if not skip:
            content.append(l)
            #contentd.append(l)
for c, suf in (
    (content, ''),
    #(contentd, '.to_diff'
):
    c.append('\noverride_dh_usrlocal:')
    c.append('\techo disabling\n')
    with open('debian/rules'+suf, 'w') as fic:
        fic.write('\n'.join(c))
EOF
cd debian
sed "s/-lldap\"/-lldap -llber\"/g" -i ${W}/debian/modules/nginx-auth-ldap/config
sed "s/FLAVOURS :=.*/FLAVOURS := full light extras/g" -i rules
sed -re "s/\\$.CURDIR.\/configure/\$(CURDIR)\/auto\/configure/g" -i rules
sed -re "s/\\$.CURDIR.\/man/\$(CURDIR)\/docs\/man/g" -i rules
sed -re "s/\\$.CURDIR.\/html/\$(CURDIR)\/docs\/html/g" -i rules
sed -re "s/\.\/configure/.\/auto\/configure/g" -i rules

# handle both one which support --automatic-dbgsym and the one which does not
sed -re 's/dh_strip --package=libnginx-mod-\$\(\*\) --automatic-dbgsym/'\
'dh_strip --package=libnginx-mod-$(*) --automatic-dbgsym'\
' || dh_strip --package=libnginx-mod-$(*)/g' -i rules

# assemble
for i in postrm preinst;do
    ls ../../debian-up/debian/*.${i}|egrep -v 'libnginx|makina'|xargs cat|grep -v "exit 0" > nginx-makina.${i}.u
    cat nginx-makina.${i}.u | uniq > nginx-makina.${i}
    rm -f nginx-makina.${i}.u
    echo "exit 0">>nginx-makina.${i}
done
for i in dirs examples manpages docs install lintian-overrides;do
    ls ../../debian-up/debian/*.${i}|egrep -v 'libnginx|makina'|xargs cat>nginx-makina.${i}.u
    cat nginx-makina.${i}.u | uniq  > nginx-makina.${i}
    rm -f nginx-makina.${i}.u
    cp nginx-makina.${i} nginx-makina.${i}.in
done
cat nginx-makina.lintian-overrides.in|sed -re "s/[^:]+:(.*)/nginx-makina:\1/g" | sort -u > nginx-makina.lintian-overrides
rm -f nginx*makina*.in
# same nginx compile for
for j in common;do
    for i in dirs manpages docs examples lintian-overrides \
             manpages postrm preinst;do
        cp -v nginx-makina.${i} nginx-$j.${i}
    done
done
# make those packages, dummy packages
# get one prerm for our global package
cp nginx-light.prerm nginx-makina.prerm
for j in doc full light extras;do
    for i in dirs postinstall prerm manpages\
                  docs examples install lintian-overrides \
                  manpages postrm preinst;do
        if [ -e "nginx-${j}.${i}" ];then
            echo > nginx-${j}.${i}
        fi
    done
done
for i in nginx-makina.install;do
    cp "${i}" "${i}.in"
    echo "#!/usr/bin/perl -w">"${i}"
    cat "${i}.in"\
        | grep -v "bin/perl" \
        | sed -e 's/^html\(.*\)/print "html\1\\n";/g' \
        | sed -re 's/^(debian|contrib)(.*)/print "\1\2\\n";/g'>>${i}
done
rm -f nginx-common.install nginx-common.install.in nginx-makina.install.in
cp -f nginx-makina.install nginx-common.install
for i in postinst preinst prerm postrm install docs manpages examples;do
    for j in nginx-*${i};do
        if egrep -q '^#!/' ${j} 2>/dev/null;then
            chmod -v +x "${j}"
        fi
    done
done
sed -re "s/\"html\/index.html/\"docs\/html\/index.html/g" -i nginx*
sed -i -re "/README/ d" nginx-*
# dnsmasq bug with insserv !
# rm "${W}/debian/nginx-common.nginx.init"
#
echo "3.0 (native)">"${W}/debian/source/format"
cd "${W}"
CHANGES=""
if [ -e $HOME/.gnupg/.gpg-agent-info ];then . $HOME/.gnupg/.gpg-agent-info;fi
# make a release for each flavor
logfile=../log
if [ -e "${logfile}" ];then rm -f "${logfile}";fi
if [ -e "${logfile}.pipe" ];then rm -f "${logfile}.pipe";fi
mkfifo "${logfile}.pipe"
tee < "${logfile}.pipe" "$logfile" &
exec 1> "${logfile}.pipe" 2> "${logfile}.pipe"
for i in $FLAVORS;do
    sed  -i -re "1 s/${PACKAGE} \([0-9]+.[0-9]+.[0-9]+(-(${RELEASES}))?([^)]*\).*)((${RELEASES});)(.*)/${PACKAGE} (${VER}-${i}\3${i};\6/g" debian/changelog
    dch -i -D "${i}" "packaging for ${i}"
    debuild -k${KEY} -S -sa --lintian-opts -i
done
rm "${logfile}.pipe"
exec 1>&1
egrep "signfile" log|sed "s///g"
CHANGES=$(grep "signfile " ../log|awk '{print  $2}'|grep source.changes)
rm -f log
# upload to final PPA
cd "${W}"
for i in ${CHANGES};do dput "${PPA}" "../${i}";done
# vim:set et sts=4 ts=4 tw=0:
