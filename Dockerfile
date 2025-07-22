# syntax=docker/dockerfile:1

########## 1) Choose your arch ##########
# For 32‑bit Pi OS:  arm32v7
# For 64‑bit Pi OS:  arm64v8
ARG ARCH=arm32v7
ARG PYVER=3.11

FROM ${ARCH}/python:${PYVER}-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

########## 2) System deps (covering common wheel builds) ##########
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config gcc g++ \
    libgl1-mesa-glx libgles2-mesa libglu1-mesa \
    libx11-6 libxext6 libxrender1 libsm6 \
    libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 libmtdev-dev \
    libfreetype6 libfontconfig1 libjpeg62-turbo libpng16-16 libtiff5 zlib1g \
    libjpeg-dev zlib1g-dev libfreetype6-dev libpng-dev            \
    libatlas-base-dev gfortran                                     \
    libffi-dev libssl-dev                                          \
    tk xvfb                                                        \
 && rm -rf /var/lib/apt/lists/*

########## 3) Workdir ##########
WORKDIR /app

########## 4) Install Python deps first (cache friendly) ##########
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt -v

########## 5) Copy the rest of your code ##########
COPY . .

########## 6) Kivy env (sdl2 backend works on Pi) ##########
ENV KIVY_NO_ARGS=1 \
    KIVY_METRICS_DENSITY=1 \
    KIVY_GL_BACKEND=sdl2

########## 7) Default: headless via xvfb. For real display, override CMD ##########
CMD ["xvfb-run", "-a", "python", "main.py"]
