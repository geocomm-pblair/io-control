#!/usr/bin/env bash

# INDENT is a regex for line indents.
INDENT='s/^/  /'

# Write a string to the console with emphasis formatting.
function emphasize() {
  echo -e "\033[1m$1\033[0m"
}

# Show system details.
emphasize Image
cat /image.info | sed 's/^/  /'
emphasize Ubuntu
cat /etc/lsb-release | sed 's/^/  /'
emphasize User
whoami | sed 's/^/  /'
emphasize GDAL
ogrinfo --version | sed 's/^/  /'
emphasize PROJ
echo PROJ $(proj 2>&1 | head -n 1) | sed 's/^/  /'
emphasize pyenv
pyenv versions | sed 's/^/  /'
