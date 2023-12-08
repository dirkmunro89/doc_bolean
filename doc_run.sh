#
# get running containers
#
echo $(docker ps -a -q) > existing.log
nri=$(cat existing.log | wc -w)
#
echo "Number of existing containers: "$nri
if [ "$nri" = "0" ]
then
    echo "Spinning up new container"
    docker run --name bolean --mount type=bind,source="$(pwd)"/home,target=/home -it stlpro 
elif [ "$nri" = "1" ]
then
    echo -n "Restarting and attaching to: "
    docker start  `docker ps -q -l` # restart it in the background
    docker attach `docker ps -q -l` # reattach the terminal & stdin
else
    echo "More than one running; kill them all, and spin up new one."
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
    docker run --name bolean --mount type=bind,source="$(pwd)"/home,target=/home -it stlpro
fi
