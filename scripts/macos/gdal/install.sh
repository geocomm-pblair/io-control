#!/usr/bin/env bash
set -eo pipefail

# If `GDAL` is already installed, we're good.
if [ -x "$(command -v gdalinfo)" ]; then
  printf 'GDAL is already installed.\n'
  gdalinfo --version
  exit 0
fi

# Install Homebrew if necessary.
if [ -x "$(command -v brew)" ]; then
  printf 'Homebrew is already installed.\n'
else
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  (echo; echo 'eval "$(/usr/local/bin/brew shellenv)"') >> "${HOME}.zprofile"
  eval "$(/usr/local/bin/brew shellenv)"
fi

# Let's get started.
brew update
brew install gdal
