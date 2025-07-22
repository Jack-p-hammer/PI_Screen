Thingy-ma-bob

xhost +local:docker
docker build -t pi-nightstand .
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pi-nightstand