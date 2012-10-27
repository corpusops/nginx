# MakinaCorpus ppa upgrade workflow
## INSTALL
```
apt-get install devscripts
git clone https://github.com/makinacorpus/nginx.git nginxp/nginx
cd nginxp/nginx
git remote add nginx https://github.com/nginx/nginx.git
git fetch --all
```

## Refresh stable
```
git checkout stable-1.10
git pull origin
git fetch nginx
git merge nginx/branches/stable-1.10
mc_packaging/sync_debian.sh
```

## Refresh experimental (nginx-mainline)
```
git checkout master
git pull origin
git fetch nginx
git merge nginx/master
mc_packaging/sync_debian.sh
```

## Test build in docker
```
docker build -t nginxp  -f mc_packaging/Dockerfile .
docker run --name=nginxp1 --rm -v /src_real -ti nginxp bash
```
