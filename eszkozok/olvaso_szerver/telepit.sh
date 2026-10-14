#!/bin/bash
# Az olvasói szerver telepítő/indító szkriptje (#76 M2; WSL-ben és később a VPS-en is ugyanez).
#
# Használat (az olvaso_szerver könyvtárból vagy a repó gyökeréből):
#   PARDES_DB=/út/pardes.db ./telepit.sh kornyezet     # uv sync (Python 3.12, zárolt függőségek)
#   PARDES_DB=/út/pardes.db ./telepit.sh ellenorzes    # frissességi/épségi teszt (K4): hiba esetén nem nulla kilépési kód
#   PARDES_DB=/út/pardes.db ./telepit.sh indit         # gunicorn gthread, 1 worker, 4 szál
#   PARDES_DB=/út/pardes.db ./telepit.sh indit-korlat  # ugyanez 1 vCPU / 2 GB korláttal (systemd-run: AllowedCPUs=0, MemoryMax=2G)
# Környezeti változók: PARDES_DB (kötelező), PARDES_KIADAS (belso|nyilvanos|kereskedelmi), PARDES_BIND (alap: 127.0.0.1:8000),
#                      PARDES_MANIFEST (alap: a repó manifest_pardes_db.tsv-je), PARDES_VENV (alap: ./.venv).
# A szkript nem tölt le adatot, nem módosít a szerveren más fájlt, mint a saját .venv-et és a frissesség-eredményt.
set -euo pipefail

CEL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
: "${PARDES_DB:?a PARDES_DB (a pardes.db útja) kötelező}"
MANIFEST="${PARDES_MANIFEST:-$CEL/manifest_pardes_db.tsv}"
EREDMENY="${PARDES_FRISSESSEG_FAJL:-$CEL/frissesseg_eredmeny.txt}"
export PARDES_DB PARDES_FRISSESSEG_FAJL="$EREDMENY"
VENV="${PARDES_VENV:-$CEL/.venv}"
PY="$VENV/bin/python"

case "${1:-}" in
  kornyezet)
    command -v uv >/dev/null || { echo "uv nincs telepítve"; exit 1; }
    (cd "$CEL" && UV_PYTHON_DOWNLOADS=never uv sync --frozen)
    "$PY" --version
    ;;
  ellenorzes)
    [ -f "$PARDES_DB" ] || { echo "nincs adatbázis: $PARDES_DB"; exit 1; }
    "$PY" "$CEL/frissesseg.py" --db "$PARDES_DB" --manifest "$MANIFEST" | tee "$EREDMENY"
    # a kilépési kód a frissesseg.py-é (a tee ellenére): pipefail
    ;;
  indit)
    [ -f "$PARDES_DB" ] || { echo "nincs adatbázis: $PARDES_DB"; exit 1; }
    cd "$CEL" && exec "$VENV/bin/gunicorn" -c gunicorn_conf.py "alkalmazas:letrehoz()"
    ;;
  indit-korlat)
    [ -f "$PARDES_DB" ] || { echo "nincs adatbázis: $PARDES_DB"; exit 1; }
    exec systemd-run --scope --quiet -p AllowedCPUs=0 -p MemoryMax=2G \
      env PARDES_DB="$PARDES_DB" PARDES_KIADAS="${PARDES_KIADAS:-belso}" PARDES_BIND="${PARDES_BIND:-127.0.0.1:8000}" \
      bash -c "cd '$CEL' && exec '$VENV/bin/gunicorn' -c gunicorn_conf.py 'alkalmazas:letrehoz()'"
    ;;
  *)
    sed -n '2,13p' "${BASH_SOURCE[0]}"
    exit 2
    ;;
esac
