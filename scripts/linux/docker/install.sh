#!/usr/bin/env bash
set -eo pipefail

COMPOSE="v2.17.2"  # the docker-compose version to install

# If `docker` is already installed, we're good.
if [ -x "$(command -v docker)" ]; then
  printf 'Docker is already installed.\n'
  docker --version
  docker-compose --version
  exit 0
fi

# Install Docker.
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
sudo usermod -aG docker ${USER}
su - ${USER}
groups
docker --version

# Install docker-compose.
mkdir -p ~/.docker/cli-plugins/
curl -SL "https://github.com/docker/compose/releases/download/${COMPOSE}/docker-compose-linux-x86_64" -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
docker-compose --version
