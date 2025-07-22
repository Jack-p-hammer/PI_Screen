# syntax=docker/dockerfile:1

ARG ARCH=arm32v7
ARG PYVER=3.11
FROM ${ARCH}/python:${PYVER}-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps (runtime + build for common wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config gcc g++ \
    libgl1-mesa-glx libgles2-mesa libglu1-mesa \
    libx11-6 libxext6 libxrender1 libsm6 \
    libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 libmtdev1 \
    libfreetype6 libfontconfig1 libjpeg62-turbo libpng16-16 zlib1g \
    libjpeg-dev zlib1g-dev libfreetype6-dev libpng-dev libtiff-dev \
    libatlas-base-dev gfortran libffi-dev libssl-dev \
    tk xvfb \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first for caching
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt -v

# Copy the rest
COPY . .

# Kivy env
ENV KIVY_NO_ARGS=1 \
    KIVY_METRICS_DENSITY=1 \
    KIVY_GL_BACKEND=sdl2

# Default: headless
CMD ["xvfb-run", "-a", "python", "main.py"]
