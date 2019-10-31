#!/usr/bin/env bash
set -ex
cd $(dirname $0)/redhat
#rm -f tip.tar.gz
curl -OLv "http://hg.nginx.org/pkg-oss/archive/tip.tar.gz"
rm -rf redhat/rpm
tar xzf tip.tar.gz --strip-components=1
rm -rf debian .hg*
cd rpm/SPECS
for i in *.spec;do
    mv $i ${i}.orig
done
# vim:set et sts=4 ts=4 tw=80:
