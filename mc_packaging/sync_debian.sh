#!/usr/bin/env bash
set -ex
cd "$(dirname $0)/.."
export W="${PWD}"
export ONLY_REUPLOAD=${ONLY_REUPLOAD-}
export GPG_AGENT_INFO=${GPG_AGENT_INFO:-${HOME}/.gnupg/S.gpg-agent:0:1}
export PACKAGE="nginx"
export PPA="${PACKAGE}"
export PPA="nginx"
export PPASUFFIX="ppa-${PPA}-"
export REPO="https://anonscm.debian.org/git/collab-maint/nginx.git"
export DEBEMAIL=${DEBEMAIL:-freesoftware@makina-corpus.com}
export KEY="${KEY:-0x2B8CDBC4533B8C52}"
export UPSTREAM_W="${W}/../${PACKAGE}-upstream"
export FLAVORS="bionic focal jammy"
export RELEASES="${RELEASES:-"experimental|(un)?stable|precise|trusty|utopic|vivid|oneric|wily|xenial|artful|bionic|disco|focal|jammy|impish|hirsute|groovy|kinetic|UNRELEASED"}"
export VERSION_PARSER="\\(([0-9]+([.-][0-9]+)+)(${PPASUFFIX}[0-9]+|[^)]+)?\\)"
export VER=${VER:-"$(head -n1 debian/changelog|awk '{print$2}'|sed -re "s/$VERSION_PARSER/\1/g")"}
if [ "x${VER}" = "x" ];then echo unknownversion;exit -1;fi
export DEBIAN_REMOTE=origin/master

gitrco() { git reset -- $@;git checkout -- $@; }
if [[ -z $ONLY_REUPLOAD ]];then
if [[ -z ${NO_SYNC-} ]];then
lua_reset="
debian/libnginx-mod-http-lua.nginx
debian/modules/patches/http-lua/discover-luajit-2.1.patch
debian/modules/patches/http-lua/series
debian/tests/lua"
ldap_url=https://github.com/kvspb/nginx-auth-ldap.git
lua_url=https://github.com/openresty/lua-nginx-module.git
shib_url=https://github.com/nginx-shib/nginx-http-shibboleth.git
#http_lua_url="https://salsa.debian.org/nginx-team/libnginx-mod-http-lua.git"
if [ "x${REPO}" != "x" ];then
    if [ ! -e "${UPSTREAM_W}" ];then
        git clone "${REPO}" "${UPSTREAM_W}";
    fi
    cd "${UPSTREAM_W}" \
    && git remote rm origin \
    && git remote add origin "$REPO" \
    && rm -rf * && git fetch --all && git reset --hard $DEBIAN_REMOTE
    rsync -av --delete --exclude="*.makina.*" \
        --exclude=po/\
        --exclude=changelog\
        "${UPSTREAM_W}/debian/" "${W}/debian/"
fi
if [ -e "${W}/mc_packaging/debian/" ];then
    rsync -av "${W}/mc_packaging/debian/" "${W}/debian/"
fi
fi
#
# CUSTOM MERGE CODE HERE
# <>
# if [ ! -e "${W}/../http-lua" ];then
#     git clone "${http_lua_url}" "${W}/../http-lua";
# fi
if [ ! -e "${W}/../nginx-auth-ldap" ];then
    git clone $ldap_urlt "${W}/../nginx-auth-ldap"
fi
if [ ! -e "${W}/../nginx-shib" ];then
    git clone $shib_url "${W}/../nginx-shib"
fi
cd "${W}/../nginx-auth-ldap" && git config --replace-all remote.origin.url $ldap_url     && git fetch --all && git reset --hard origin/master
cd "${W}/../nginx-shib"      && git config --replace-all remote.origin.url $shib_url     && git fetch --all && git reset --hard origin/master
#cd "${W}/../http-lua"        && git config --replace-all remote.origin.url $http_lua_url && git fetch --all && git reset --hard origin/master
cd "${W}"
# rsync -azv --delete --delete-excluded --exclude=.git ../http-lua/ debian/modules/http-lua/
rsync -azv --delete --delete-excluded --exclude=.git ../nginx-auth-ldap/ debian/modules/nginx-auth-ldap/
rsync -azv --delete --delete-excluded --exclude=.git ../nginx-shib/ debian/modules/nginx-shib/
# git reset -- $lua_reset && git checkout -- $lua_reset
rm -rf debian/modules/nginx-auth-ldap/.git
rm -rf debian/nginx*upstart
rm -rf debian/modules/nginx-shib/.git
sed -i -re 's/if (\[ "$\(BUILDDIR_$\*\)" = "\$\(BUILDDIR_extras\)" ]);/if (true || \1);/g' debian/rules
/usr/bin/python << EOF
TOADDinit = open('mc_packaging/makefile.in.init').read().splitlines()
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
            if 'common' not in l and 'basic' not in l:
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
            #if 'MODULESDIR)/nchan ' in l:
            #    no_common_skipped.extend([
            #        '                       --add-dynamic-module=\$(MODULESDIR)/http-lua \\\\',
            #    ])
        if not skip:
            content.append(l)
            #contentd.append(l)
        if 'DH_VERBOSE=1' in l:
            content.extend(TOADDinit)
        #if l.startswith('DYN_MODS :='):
        #    content.append('       http-lua \\\\')
for c, suf in (
    (content, ''),
    #(contentd, '.to_diff'
):
    c.append('\noverride_dh_usrlocal:')
    c.append('\techo disabling\n')
    with open('debian/rules'+suf, 'w') as fic:
        fic.write('\n'.join(c)\
             .replace('if [ "\$(BUILDDIR_\$*)" = "\$(BUILDDIR_extras)" ];', 'if ( true || [ "\$(BUILDDIR_\$*)" = "\$(BUILDDIR_extras)" ] );')
        )
EOF
cd debian
sed "s/-lldap\"/-lldap -llber\"/g" -i ${W}/debian/modules/nginx-auth-ldap/config
sed "s/FLAVOURS :=.*/FLAVOURS := core light extras/g" -i rules
sed -re "s/\\$.CURDIR.\/configure/\$(CURDIR)\/auto\/configure/g" -i rules
sed -re "s/\\$.CURDIR.\/man/\$(CURDIR)\/docs\/man/g" -i rules
sed -re "s/\\$.CURDIR.\/html/\$(CURDIR)\/docs\/html/g" -i rules
sed -re "s/\.\/configure/.\/auto\/configure/g" -i rules

# handle both one which support --automatic-dbgsym and the one which does not
sed -re 's/dh_strip --package=libnginx-mod-\$\(\*\) --automatic-dbgsym/'\
'dh_strip --package=libnginx-mod-$(*) --automatic-dbgsym'\
' || dh_strip --package=libnginx-mod-$(*)/g' -i rules
sed -i -re "s/(dh_installinit --no-stop-on-upgrade --no-start --name=nginx)/\1 || dh_installinit --no-start --name=nginx/g" rules
# handle ubuntu jammy
sed -i -re "s/dh-systemd \(>= 1.5\)/dh-systemd (>= 1.5) | debhelper (>= 13)/g" control
sed -i -r \
    -e "s/aaaccc/aaa/g" \
    control
# assemble
for i in postrm preinst;do
    ls "$UPSTREAM_W"/debian/*.${i}|egrep -v 'libnginx|makina'|xargs cat|grep -v "exit 0" > nginx-makina.${i}.u
    cat nginx-makina.${i}.u | uniq > nginx-makina.${i}
    rm -f nginx-makina.${i}.u
    echo "exit 0">>nginx-makina.${i}
done
for i in dirs examples manpages docs install lintian-overrides;do
    ls "$UPSTREAM_W"/debian/*.${i}|egrep -v 'libnginx|makina'|xargs cat>nginx-makina.${i}.u
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
for j in doc full light extras core dev;do
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
patch -Np2 < "$W/"mc_packaging/helper.patch
fi
cd "${W}"
CHANGES=""
if [ -e $HOME/.gnupg/.gpg-agent-info ];then . $HOME/.gnupg/.gpg-agent-info;fi
# make a release for each flavor
if [[ -z ${NO_UPLOAD-} ]];then
logfile=$W/../log
if [ -e "${logfile}" ];then rm -f "${logfile}";fi
if [ -e "${logfile}.pipe" ];then rm -f "${logfile}.pipe";fi
mkfifo "${logfile}.pipe"
tee < "${logfile}.pipe" "$logfile" &
exec 1> "${logfile}.pipe" 2> "${logfile}.pipe"
for i in $FLAVORS;do
    sed -i -r \
        -e "1 s/$PACKAGE $VERSION_PARSER (${RELEASES});/$PACKAGE (\1\3) $i;/g" \
        -e "1 s/${PPASUFFIX}\)/${PPASUFFIX}1)/g" \
        debian/changelog
    # head -n 1 debian/changelog;exit 1
    "$W/mc_packaging/debian_compat.sh" $i
    dch --upstream -D "${i}" "packaging for ${i}" -l "$PPASUFFIX"
    debuild --no-tgz-check -k${KEY} -S -sa --lintian-opts -i
done
exec 1>&1 2>&2
rm "${logfile}.pipe"
CHANGES=$(egrep "signfile.* dsc " $logfile|awk '{print $3}'|sed -re "s/\.dsc$/_source.changes/g" )
rm -f $logfile
# upload to final PPA
    cd "${W}"
    for i in ${CHANGES};do dput "${PPA}" "../${i}";done
fi
# vim:set et sts=4 ts=4 tw=0:
