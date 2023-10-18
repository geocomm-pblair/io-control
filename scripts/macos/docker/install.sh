#!/usr/bin/env bash
set -eo pipefail

# If `GDAL` is already installed, we're good.
if [ -x "$(command -v docker)" ]; then
  printf 'Docker is already installed.\n'
  docker --version
  docker-compose --version
  exit 0
fi

if [[ $(uname -m) == 'arm64' ]]; then
  curl -o Docker.dmg 'https://desktop.docker.com/mac/main/arm64/Docker.dmg'
else
  curl -o Docker.dmg 'https://desktop.docker.com/mac/main/amd64/Docker.dmg'
fi
sudo hdiutil attach Docker.dmg
sudo /Volumes/Docker/Docker.app/Contents/MacOS/install
sudo hdiutil detach /Volumes/Docker
