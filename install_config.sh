#!/usr/bin/env bash
set -euo pipefail

CONFIG_DEST="/etc/desktop_launcher.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_SRC="${SCRIPT_DIR}/desktop_launcher.sample.json"

if [[ ! -f "${CONFIG_SRC}" ]]; then
  echo "install_config.sh: sample config not found at ${CONFIG_SRC}" >&2
  exit 1
fi

if [[ "${EUID}" -ne 0 ]]; then
  echo "install_config.sh: root privileges required to write ${CONFIG_DEST}." >&2
  exec sudo "${BASH_SOURCE[0]}" "$@"
fi

install -m 644 "${CONFIG_SRC}" "${CONFIG_DEST}"
echo "Copied ${CONFIG_SRC} -> ${CONFIG_DEST}"
