FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /Project
ENV PYTHONPATH=/Project/src
# (Optional but helpful) Force IPv4 to reduce flaky apt CDN issues
RUN echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4

# Base system + pip + common deps (with retries + timeout + fix-missing)
RUN apt-get update \
 && apt-get -o Acquire::Retries=10 -o Acquire::http::Timeout="60" install -y --no-install-recommends --fix-missing \
    curl gnupg ca-certificates \
    python3 python3-pip python3-dev \
    gcc g++ make \
    libffi-dev libssl-dev libatomic1 \
    python3-numpy \
    python3-opencv \
    python3-rpi.gpio \
    libzbar0 \
    python3-smbus \
    i2c-tools \
 && rm -rf /var/lib/apt/lists/*

# Build deps needed to compile grpcio on armhf (with retries)
RUN apt-get update \
 && apt-get -o Acquire::Retries=10 -o Acquire::http::Timeout="60" install -y --no-install-recommends --fix-missing \
    build-essential pkg-config cmake \
    libz-dev \
 && rm -rf /var/lib/apt/lists/*

# Force grpc build to be single-threaded (prevents Pi build crashes)
ENV MAKEFLAGS="-j1"
ENV GRPC_PYTHON_BUILD_EXT_COMPILER_JOBS="1"

# Add Raspberry Pi OS Bullseye repository (REQUIRED for picamera2)
RUN curl -fsSL https://archive.raspberrypi.org/debian/raspberrypi.gpg.key \
 | gpg --dearmor -o /usr/share/keyrings/raspi.gpg \
 && echo "deb [signed-by=/usr/share/keyrings/raspi.gpg] http://archive.raspberrypi.org/debian bullseye main" \
 > /etc/apt/sources.list.d/raspi.list

# Install camera stack (with retries)
RUN apt-get update \
 && apt-get -o Acquire::Retries=10 -o Acquire::http::Timeout="60" install -y --no-install-recommends --fix-missing \
    python3-picamera2 \
    libcamera-apps \
 && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -U pip setuptools wheel \
 && python3 -m pip install --no-cache-dir --break-system-packages spidev \
 && python3 -m pip install --no-cache-dir --break-system-packages \
    --no-build-isolation \
    --no-binary=grpcio,grpcio-status \
    grpcio==1.48.2 grpcio-status==1.48.2 \
 && python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt

# App
COPY . .

RUN python3 -m pip install --break-system-packages /Project/src/SPI-Py

EXPOSE 5000
CMD ["python3", "./src/main.py"]
