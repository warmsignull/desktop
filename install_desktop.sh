#!/usr/bin/env bash
set -euo pipefail

TARGET="/usr/local/bin/desktop"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="${SCRIPT_DIR}/desktop"

if [[ ! -f "${SOURCE}" ]]; then
  echo "install_desktop.sh: launcher script not found at ${SOURCE}" >&2
  exit 1
fi

if [[ "${EUID}" -ne 0 ]]; then
  echo "install_desktop.sh: root privileges required to write ${TARGET}." >&2
  exec sudo "${BASH_SOURCE[0]}" "$@"
fi

install -m 755 "${SOURCE}" "${TARGET}"
echo "Installed ${SOURCE} -> ${TARGET}"
