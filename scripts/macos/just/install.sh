#!/usr/bin/env bash
set -eo pipefail

# Install just.
if [ -x "$(command -v just)" ]; then
  printf 'just is already installed.\n'
  just --version
  exit 0
fi

# Install Homebrew if necessary.
if [ -x "$(command -v brew)" ]; then
  printf 'Homebrew is already installed.\n'
else
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  (echo; echo 'eval "$(/usr/local/bin/brew shellenv)"') >> "${HOME}/.zprofile"
  eval "$(/usr/local/bin/brew shellenv)"
fi

# Install just.
brew update
brew install just
just --version
