#!/usr/bin/env bash
set -eo pipefail

# If `GDAL` is already installed, we're good.
if [ -x "$(command -v gdalinfo)" ]; then
  printf 'GDAL is already installed.\n'
  gdalinfo --version
  exit 0
fi

# Resolve the versions from the environment.
GDAL="${GDAL:-3.6.2}"
PROJ="${PROJ:-9.1.1}"

# Create the build directory.
mkdir -p build
pushd build

# Install Apache Arrow (for GDAL)
apt update && \
  apt install -y -V ca-certificates lsb-release wget && \
  wget https://apache.jfrog.io/artifactory/arrow/$(lsb_release --id --short | tr 'A-Z' 'a-z')/apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb
apt install -y -V ./apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb
apt update
apt install -y -V libarrow-dev # For C++
apt install -y -V libarrow-glib-dev # For GLib (C)
apt install -y -V libarrow-dataset-dev # For Apache Arrow Dataset C++
apt install -y -V libarrow-dataset-glib-dev # For Apache Arrow Dataset GLib (C)
apt install -y -V libarrow-acero-dev # For Apache Arrow Acero
apt install -y -V libarrow-flight-dev # For Apache Arrow Flight C++
apt install -y -V libarrow-flight-glib-dev # For Apache Arrow Flight GLib (C)
apt install -y -V libgandiva-dev # For Gandiva C++
apt install -y -V libgandiva-glib-dev # For Gandiva GLib (C)
apt install -y -V libparquet-dev # For Apache Parquet C++
apt install -y -V libparquet-glib-dev # For Apache Parquet GLib (C)

# Install the pre-requisites.
apt update && \
    apt-get install -y \
    cmake \
    libcurl4-openssl-dev \
    libsqlite3-dev \
    libtool \
    libpq-dev \
    libtiff-dev \
    libtiff-tools \
    lsb-core \
    software-properties-common \
    sqlite3

# PROJ
wget "http://download.osgeo.org/proj/proj-${PROJ}.tar.gz" -O proj.tar.gz
mkdir proj && tar -xvf proj.tar.gz -C proj --strip-components=1
pushd proj
mkdir build && cd build && cmake .. && cmake --build . && cmake --build . --target install
popd

# GDAL
wget "https://github.com/OSGeo/gdal/releases/download/v${GDAL}/gdal-${GDAL}.tar.gz" -O gdal.tar.gz
mkdir gdal && tar -xvf gdal.tar.gz -C gdal --strip-components=1
pushd gdal
mkdir build && cd build && cmake .. && cmake --build . && cmake --build . --target install
popd
