Just run something like this:

```
./run_in_docker.sh ./hotels.csv
```

Note that this script mounts current directory into ``/host`` docker dir (which is also set as workdir).

So you should copy ``hotels.csv`` to project directory or just make it available from docker container.
