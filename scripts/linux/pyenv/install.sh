#!/usr/bin/env bash
set -eo pipefail
# Update APT.
sudo apt-get update
# Install packages requires to build python.
sudo apt-get install -y \
  build-essential \
  checkinstall \
  curl \
  libreadline-dev \
  liblzma-dev \
  libncurses-dev \
  libncursesw5-dev \
  libssl-dev \
  libsqlite3-dev \
  tk-dev \
  libgdbm-dev \
  libc6-dev \
  libbz2-dev \
  libffi-dev \
  zlib1g-dev
# Install pyenv.
curl https://pyenv.run | bash
# Update the bash profile.
echo '' >> ~/.bashrc
echo '# pyenv' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
printf '{{check}} Installed pyenv.\n'
printf '{{warn}} You need to restart the shell to use pyenv.\n'
echo 'Start a new shell or use this command:'
echo 'exec "$SHELL"'
