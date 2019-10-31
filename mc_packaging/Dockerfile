FROM ubuntu
ADD mc_packaging/sources.list /etc/apt/sources.list
ENV __mirror__=http://ubuntu.mirrors.ovh.net/ubuntu/
RUN  id=$(cat /etc/lsb-release |grep CODE|awk -F= '{print $2}') &&\
    sed -ire "s|__mirror__|$__mirror__|g" /etc/apt/sources.list &&\
    sed -i -re "s/xenial/$id/g" /etc/apt/sources.list &&\
    apt update && apt install -y lsb-release && \
    apt-get update -qq && apt-get install -y --force-yes \
    devscripts equivs\
    dbconfig-common python-twisted-web daemon
ADD debian/control        /src/debian/control
RUN cd /src && \
    mk-build-deps -t "apt-get --no-install-recommends -y --force-yes" -ir debian/control
ADD auto          /src/auto/
ADD conf          /src/conf/
ADD contrib       /src/contrib/
ADD debian        /src/debian/
ADD docs          /src/docs/
ADD mc_packaging  /src/mc_packaging/
ADD misc          /src/misc/
ADD src           /src/src/
ADD .git          /src/.git/
RUN REV=2;cd src && export MAKEOPTS="-j4" && \
    if debuild -i -us -uc -b;then echo SUCCESS; else echo FAIL; exit 1;fi

