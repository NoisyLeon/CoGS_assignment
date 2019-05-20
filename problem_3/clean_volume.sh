docker rm -v $(docker ps -a --no-trunc -q)
#docker volume rm $(docker volume ls -qf dangling=true)
