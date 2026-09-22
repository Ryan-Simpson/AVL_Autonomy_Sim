#!/usr/bin/env bash
# ./dev.sh [up|build|shell|stop|clean]
set -euo pipefail
cd "$(dirname "$0")"

export HOST_UID="$(id -u)"
export HOST_GID="$(id -g)"

setup_xauth() {
    local xauth=/tmp/.docker.xauth
    [ -f "$xauth" ] || touch "$xauth"
    xauth nlist "${DISPLAY}" 2>/dev/null \
        | sed -e 's/^..../ffff/' \
        | xauth -f "$xauth" nmerge - 2>/dev/null || true
    chmod 644 "$xauth"
}

case "${1:-up}" in
    build) setup_xauth; docker compose build --progress=plain ;;
    shell) docker compose exec sim bash ;;
    stop)  docker compose down ;;
    clean) docker compose down -v; echo "Volumes removed." ;;
    up|"") setup_xauth; docker compose up -d
           echo; echo "avl-sim is up. More terminals: ./dev.sh shell"; echo
           docker compose exec sim bash ;;
    *) echo "usage: $0 {up|build|shell|stop|clean}" >&2; exit 1 ;;
esac
