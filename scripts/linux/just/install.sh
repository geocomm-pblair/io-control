#!/usr/bin/env bash
set -eo pipefail

# If just is already installed, we're all good here.
if [ -x "$(command -v just)" ]; then
    printf "\\U1F44D just is already installed.\n"
    just --version
    exit 0
fi

# Create the local bin directory (if it doesn't exist).
mkdir -p ~/bin
# If the bin directory isn't in the PATH, let's add it now.
if [[ ":$PATH:" == *":$HOME/bin:"* ]]; then
  printf "\\U1F44D Your PATH contains %s.\n" "$HOME/bin"
else
  echo "Your path is missing ~/bin, you might want to add it."
  export PATH="$PATH:$HOME/bin"
  echo 'export PATH=$PATH:$HOME/bin'  # >> ~/.bashrc
  printf "\\U2705 Your ~/.bashrc file was updated to add %s to your path." "$HOME/bin"
fi

# Download and extract just to ~/bin/just.
sudo apt-get update
sudo apt-get install -y curl
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin

# If the bin directory isn't in the PATH, let's add it now.
if [[ ":$PATH:" == *":$HOME/bin:"* ]]; then
  printf "\\U1F44D Your PATH contains %s.\n" "$HOME/bin"
else
  echo "Your path is missing ~/bin, you might want to add it."
  export PATH="$PATH:$HOME/bin"
  echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc
  printf "\\U2705 %s file was updated to add %s to your path." "$HOME/.bashrc" "$HOME/bin"
fi

## just should now be executable.
just --help
printf "\\U1F44D Installed %s to %s.\n" "$(just --version)" "$HOME/bin"
