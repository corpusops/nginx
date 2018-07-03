# CorpusOps ppa upgrade workflow
## INSTALL
```sh
sudo apt-get install devscripts debhelper dh-systemd dput python-paramiko python-scp/xenial python3-paramiko python3-scp
git clone https://github.com/corpusops/nginx.git nginxp/nginx
cd nginxp/nginx
git remote add nginx https://github.com/nginx/nginx.git
git fetch --all
```

## Refresh stable
```sh
git checkout stable-1.10
git pull origin
git fetch nginx
git merge nginx/branches/stable-1.10
mc_packaging/sync_debian.sh
```

## Refresh experimental (nginx-mainline)
```sh
git checkout master
git pull origin
git fetch nginx
git merge nginx/master
mc_packaging/sync_debian.sh
```

## Test build in docker
```sh
docker build -t nginxp  -f mc_packaging/Dockerfile .
docker run --name=nginxp1 --rm -v /src_real -ti nginxp bash
```

## redhat RPMS
- [here](https://github.com/corpusops/nginx/releases/tag/redhat)


## Reapplication des patchs

```sh
git diff --raw --binary --full-index   HEAD..master  -- . ':!auto' ':!.hgtags' ':!conf' ':!contrib' ':!src' ':!misc' ':!docs' >local/packaging.diff
rm -rf mc_packaging/ debian/ auto/cc~* .pc/  auto/cc~* .tito/ .gitignore  nginx.spec auto/cc~*
git apply  --index --reject local/packaging.diff
```
