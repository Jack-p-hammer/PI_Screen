Thingy-ma-bob

xhost +local:docker
docker build --platform linux/arm64 -t pi-nightstand .
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pi-nightstand