#!/usr/bin/env bash
# Wrapper: the real script lives at the kit root so it can find tools/.
HERE="$(cd "$(dirname "$0")" && pwd)"
exec "$HERE/../../verify.sh" "$@"
