#!/usr/bin/env bash
set -eo pipefail

# Install xcode (if necessary).
xcode-select --install

# If `pyenv` is already installed, we're good.
if [ -x "$(command -v pyenv)" ]; then
  printf 'pyenv is already installed.\n'
  pyenv --version
  exit 0
fi

# Install Homebrew if necessary.
if [ -x "$(command -v brew)" ]; then
  printf 'Homebrew is already installed.\n'
else
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  (echo; echo 'eval "$(/usr/local/bin/brew shellenv)"') >> /Users/pat/.zprofile
  eval "$(/usr/local/bin/brew shellenv)"
fi

# Update and install `pyenv`.
brew update
brew install pyenv
pyenv --version

# Update shell rc scripts.
for rc in ~/.zprofile ~/.profile ~/.bashrc; do
  echo '' >> ${rc}
  echo '# pyenv' >> ${rc}
  echo 'eval "$(pyenv init -)"' >> ${rc}
done
