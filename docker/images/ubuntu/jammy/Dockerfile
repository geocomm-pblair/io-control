ARG BASE_IMAGE
FROM ${BASE_IMAGE} as build
SHELL ["/bin/bash", "-c"]

ARG DEBIAN_FRONTEND=noninteractive

# NONROOT_USER is the runtime user.
ENV NONROOT_USER=nonroot
ENV NONROOT_HOME=/home/${NONROOT_USER}
# BUILD_ROOT is the root directory for source code compilation.
ARG BUILD_ROOT=/build
# PYTHON is the default (global) python version for pyenv.
ARG PYTHON
# PROJ is the PROJ version.
ARG PROJ
# GDAL is the GDAL version.
ARG GDAL

# IMAGE_NAME identifies the Docker image.
ARG IMAGE_NAME
ENV IMAGE_NAME=${IMAGE_NAME}
# IMAGE_VERSION identifies the Docker image version.
ARG IMAGE_VERSION
ENV IMAGE_VERSION=${IMAGE_VERSION}

# Prepare apt.
RUN apt-get update
RUN apt-get install -y apt-utils

# Install build utilities.
RUN apt-get install -y curl wget

# Create the non-root user.
RUN useradd -m -s /usr/bin/bash -d "/home/${NONROOT_USER}" "${NONROOT_USER}"
# Copy home directory files into place.
COPY files/home/* ${NONROOT_HOME}/

# Update shell control scripts.
RUN for f in ".bashrc" ".profile"; do cat "${NONROOT_HOME}/.env.rc" >> "${NONROOT_HOME}/$f"; done

# Install github
RUN apt-get install -y git
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
RUN apt-get update
RUN apt-get install -y gh

# Install just
USER ${NONROOT_USER}
RUN mkdir "${NONROOT_HOME}/bin"
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to "${NONROOT_HOME}/bin"
RUN ${NONROOT_HOME}/bin/just --version

# Install pyenv
USER root
RUN apt-get install -y \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    make \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev
USER ${NONROOT_USER}
WORKDIR ${NONROOT_HOME}
COPY files/home/.pyenv.rc .
RUN curl https://pyenv.run | bash
RUN for f in ".bashrc" ".profile"; do cat "${NONROOT_HOME}/.pyenv.rc" >> "${NONROOT_HOME}/$f"; done
RUN export PATH="${NONROOT_HOME}/.pyenv/bin:${PATH}" && echo ${PATH}
RUN export PATH="${NONROOT_HOME}/.pyenv/bin:${PATH}" &&  \
    pyenv update && \
    pyenv install ${PYTHON} && \
    pyenv global ${PYTHON} && \
    echo $(pyenv versions)

# vim (for field troubleshooting). nano also, if you prefer.
USER root
RUN apt-get install -y vim nano
USER ${NONROOT_USER}
RUN mkdir -p "${NONROOT_HOME}/.vim/pack/vendor/start"
RUN echo set number >> "${NONROOT_HOME}/.vimrc"
RUN echo set relativenumber >> "${NONROOT_HOME}/.vimrc"

# Install Apache Arrow (for GDAL)
USER root
RUN apt update && \
  apt install -y -V ca-certificates lsb-release wget && \
  wget https://apache.jfrog.io/artifactory/arrow/$(lsb_release --id --short | tr 'A-Z' 'a-z')/apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb
RUN apt install -y -V ./apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb
RUN apt update
RUN apt install -y -V libarrow-dev # For C++
RUN apt install -y -V libarrow-glib-dev # For GLib (C)
RUN apt install -y -V libarrow-dataset-dev # For Apache Arrow Dataset C++
RUN apt install -y -V libarrow-dataset-glib-dev # For Apache Arrow Dataset GLib (C)
RUN apt install -y -V libarrow-acero-dev # For Apache Arrow Acero
RUN apt install -y -V libarrow-flight-dev # For Apache Arrow Flight C++
RUN apt install -y -V libarrow-flight-glib-dev # For Apache Arrow Flight GLib (C)
RUN apt install -y -V libgandiva-dev # For Gandiva C++
RUN apt install -y -V libgandiva-glib-dev # For Gandiva GLib (C)
RUN apt install -y -V libparquet-dev # For Apache Parquet C++
RUN apt install -y -V libparquet-glib-dev # For Apache Parquet GLib (C)

# GDAL
USER root
RUN apt update && \
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

WORKDIR ${BUILD_ROOT}
RUN wget "http://download.osgeo.org/proj/proj-${PROJ}.tar.gz" -O proj.tar.gz
RUN mkdir proj && tar -xvf proj.tar.gz -C proj --strip-components=1
RUN cd proj && mkdir build && cd build && cmake .. && cmake --build . && cmake --build . --target install

WORKDIR ${BUILD_ROOT}
RUN wget "https://github.com/OSGeo/gdal/releases/download/v${GDAL}/gdal-${GDAL}.tar.gz" -O gdal.tar.gz
RUN mkdir gdal && tar -xvf gdal.tar.gz -C gdal --strip-components=1
RUN cd gdal && mkdir build && cd build && cmake .. && cmake --build . && cmake --build . --target install

# Add development-time utilities for the development user.
USER root
RUN apt install sudo
# Set a random password for running sudo.  This particular password won't be known, but it should be set by the
# entrypoint at runtime..
RUN echo "${NONROOT_USER}:${NONROOT_USER}" | chpasswd

# Give sudo privileges to the non-root user.
RUN usermod -aG sudo "${NONROOT_USER}"

# Clean up.
WORKDIR /
RUN rm -rf ${BUILD_ROOT}
RUN for f in ".env.rc" ".pyenv.rc"; do rm "${NONROOT_HOME}/$f"; done

# Install SSH.
USER root
RUN apt-get update && \
    apt-get install -y openssh-client openssh-server && \
    mkdir -p /var/run/sshd

# Prepare the default entry point.
USER root
COPY files/entrypoint.sh /
COPY files/info.sh /
RUN chmod +x /info.sh

# Place build information into a standard file.
RUN echo "${IMAGE_NAME}:${IMAGE_VERSION}" >> /image.info
RUN cat /image.info


# Let's go.
WORKDIR /home/${NONROOT_USER}
USER root
ENTRYPOINT ["/bin/bash", "-l", "/entrypoint.sh"]
