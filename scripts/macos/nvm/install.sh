#!/usr/bin/env bash
set -o pipefail

# Let's see if nvm is already installed.
if [ -x "$(command -v nvm)" ]; then
  printf 'nvm is already installed.\n'
  nvm -v
  node -v
  npm -v
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

# Update and install `nvm`.
brew update
brew install nvm

# Create file system assets.
mkdir -p ~/.nvm

# Update shell rc scripts.
for rc in ~/.zprofile ~/.profile ~/.bashrc; do
  declare content=$( cat "${rc}" )
  declare recognize="# nvm"
  if [[ " $content " =~ $recognize ]]; then
    echo "${rc} contains init commands."
  else
    echo "Adding init commands to ${rc}."
    echo '' >> ${rc}
    echo '# nvm' >> ${rc}
    echo 'NVM_DIR=~/.nvm' >> ${rc}
    echo 'source $(brew --prefix nvm)/nvm.sh' >> ${rc}
  fi
done

# Update the shell so we may continue.
export NVM_DIR=~/.nvm
source $(brew --prefix nvm)/nvm.sh

nvm install
echo "Node: $(node -v)"
echo "NPM: $(npm -v)"
