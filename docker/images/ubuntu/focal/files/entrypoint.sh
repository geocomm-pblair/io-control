#!/usr/bin/env bash

# Run the system information script as the non-root user.
su - -c '/info.sh' "${NONROOT_USER}"

# INDENT is a regex for line indents.
INDENT='s/^/  /'

# Write a string to the console with emphasis formatting.
function emphasize() {
  echo -e "\033[1m$1\033[0m"
}

# If the environment specifies a password for the non-root user, set it now.
if [[ -n "${NONROOT_PASSWORD}" ]]; then
  echo "${NONROOT_USER}:${NONROOT_PASSWORD}" | chpasswd
fi

# If the development flag is set, just hang out.  Otherwise continue on as the non-root user.
if [ $((${DEV})) != 0 ]; then
  /usr/sbin/sshd -D
  sleep infinity
else
  exec -c "$*"
fi
