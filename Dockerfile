# Use an official Python image for ARM (Raspberry Pi OS 32-bit/64-bit)
FROM python:3.11-slim-bullseye

# Install system dependencies for Kivy, matplotlib, and fonts
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-setuptools \
    python3-dev \
    build-essential \
    libgl1-mesa-glx \
    libgles2-mesa \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff5 \
    libx11-6 \
    tk \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Optional: Set environment variables for Kivy
ENV KIVY_NO_ARGS=1
ENV KIVY_METRICS_DENSITY=1
ENV KIVY_GL_BACKEND=angle_sdl2

# Expose X11 (if using host X server)
ENV DISPLAY=:0

# For headless mode, you can use xvfb-run to simulate a display
CMD ["xvfb-run", "-a", "python", "main.py"] 