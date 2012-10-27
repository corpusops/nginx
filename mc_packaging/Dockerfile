FROM ubuntu
RUN apt-get update -qq && apt-get install -y --force-yes \
    devscripts equivs\
    dbconfig-common python-twisted-web daemon 
ADD debian/control        /src/debian/control
RUN cd /src && \
    mk-build-deps -t "apt-get --no-install-recommends -y --force-yes" -ir debian/control
ADD auto          /src/auto
ADD conf          /src/conf
ADD contrib       /src/contrib
ADD debian        /src/debian
ADD docs          /src/docs
ADD mc_packaging  /src/mc_packaging
ADD misc          /src/misc
ADD src           /src/src
ADD .git          /src/.git
RUN REV=1;cd src && export MAKEOPTS="-j4" && \
    if debuild -i -us -uc -b;then echo SUCCESS; else echo FAIL;fi

