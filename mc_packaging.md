
MakinaCorpus ppa upgrade workflow

- Merge nginx stable branch from github nginx repo
```
git merge v1.7.10
```

- Run debian/sync_debian.sh to grab back release stuff & upload ppa candidate
```
debian/sync_debian.sh
```
