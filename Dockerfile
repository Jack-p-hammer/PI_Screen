# Use a 32-bit ARM Python image for Raspberry Pi OS
FROM arm32v7/python:3.11-slim-bullseye

# Install system dependencies for Kivy, matplotlib, and GUI support
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
    libmtdev1 \
    libinput10 \
    libudev1 \
    libusb-1.0-0 \
    libxcb1 \
    libxkbcommon0 \
    libxcursor1 \
    libxrandr2 \
    libxi6 \
    libxinerama1 \
    libxss1 \
    libxcomposite1 \
    libxdamage1 \
    libxtst6 \
    libxft2 \
    libxfixes3 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Kivy
ENV KIVY_NO_ARGS=1
ENV KIVY_METRICS_DENSITY=1
ENV KIVY_GL_BACKEND=angle_sdl2

# Expose X11 (for host X server)
ENV DISPLAY=:0

# Start the dashboard (no xvfb, use real display)
CMD ["python", "main.py"]
