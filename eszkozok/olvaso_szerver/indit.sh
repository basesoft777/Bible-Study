#!/bin/bash
# Az olvasó-szerver közös indítója (#100) — a három asztali parancsikon ezt hívja (WSL `pardes` disztribúció).
#
# Használat:  indit.sh <kiadás: belso|nyilvanos|kereskedelmi> <port>
#
# Sorrend: (1) a porton futó régi példány leállítása; (2) adatbázis-szinkron: a Windows-oldali pardes.db (forrás) és a WSL-beli
# másolat (cél) `meta.epites_ts`-ének összevetése — eltérésnél (vagy hiányzó célnál) másolás ideiglenes névre, majd atomi átnevezés
# (a szinkron-kulcs az epites_ts, NEM a fájl mtime-ja); azonos építési időnél nincs másolás; (3) a szerver indítása újratöltővel
# (alkalmazas.py --ujratolt). A napló minden lépést kiír ("[indit] …"), többek közt azt, hogy másolás történt-e.
#
# Környezeti változók (alapértékekkel; a gépi próba ezekkel dolgozik, hogy ne a valódi adatbázist módosítsa):
#   PARDES_FORRAS_DB   a Windows-oldali pardes.db       (alap: <repó gyökere>/pardes.db az indit.sh helyéből)
#   PARDES_DB          a WSL-beli (cél) másolat         (alap: $HOME/pardes/pardes.db)
#   PARDES_PY          a venv Python 3.12              (alap: $HOME/pardes/eszkozok/olvaso_szerver/.venv/bin/python)
#   PARDES_ZAR         a közös zárfájl (egyidejű indítások sorosítása; alap: $HOME/pardes/.indit.zar)
#   PARDES_INDIT_CSAK_ELOKESZIT=1   csak leállítás + szinkron, a szervert nem indítja (teszt_indito.py, gépi próba)
set -u

KIADAS="${1:-}"
PORT="${2:-}"
case "$KIADAS" in belso|nyilvanos|kereskedelmi) ;; *) echo "[indit] használat: indit.sh <belso|nyilvanos|kereskedelmi> <port>" >&2; exit 2 ;; esac
case "$PORT" in ''|*[!0-9]*) echo "[indit] a port szám kell: '$PORT'" >&2; exit 2 ;; esac

CEL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PARDES_PY:-$HOME/pardes/eszkozok/olvaso_szerver/.venv/bin/python}"
FORRAS="${PARDES_FORRAS_DB:-$CEL/../../pardes.db}"
MASOLAT="${PARDES_DB:-$HOME/pardes/pardes.db}"
ZAR="${PARDES_ZAR:-$HOME/pardes/.indit.zar}"
naplo() { echo "[indit] $(date +%H:%M:%S) $*"; }

[ -x "$PY" ] || { naplo "HIBA: nincs Python a venv-ben: $PY"; exit 1; }

# -- sorosítás: két egymás utáni kattintás ne másolja/indítsa egyszerre ugyanazt (a zárat a szerver felállása után engedjük el)
mkdir -p "$(dirname "$ZAR")"
exec 9>"$ZAR"
flock -w 120 9 || { naplo "HIBA: a zár nem szerezhető meg ($ZAR)"; exit 1; }

# -- (1) a régi példány leállítása ------------------------------------------------------------------------------------------
REGI="$(fuser "$PORT"/tcp 2>/dev/null | tr -s ' ' | sed 's/^ //')"
if [ -n "$REGI" ]; then
  naplo "régi példány a $PORT porton (PID: $REGI) — leállítás"
  fuser -k -TERM "$PORT"/tcp >/dev/null 2>&1
  for _ in $(seq 1 50); do fuser -s "$PORT"/tcp 2>/dev/null || break; sleep 0.1; done
  if fuser -s "$PORT"/tcp 2>/dev/null; then
    naplo "a régi példány nem állt le 5 mp alatt — KILL"
    fuser -k -KILL "$PORT"/tcp >/dev/null 2>&1
    sleep 1
  fi
  naplo "a régi példány leállt"
else
  naplo "a $PORT porton nem futott régi példány"
fi

# -- (2) adatbázis-szinkron ---------------------------------------------------------------------------------------------------
if [ -f "$FORRAS" ]; then
  IFS=$'\t' read -r DONTES F_TS C_TS < <("$PY" "$CEL/allapot.py" dontes "$FORRAS" "$MASOLAT")
  case "$DONTES" in
    azonos)
      naplo "adatbázis: NINCS másolás — a két példány építési ideje azonos ($F_TS)" ;;
    masol)
      naplo "adatbázis: MÁSOLÁS — forrás építve: $F_TS, másolat: ${C_TS:-nincs} (fájl: $FORRAS -> $MASOLAT)"
      mkdir -p "$(dirname "$MASOLAT")"
      TMP="$MASOLAT.uj.$$"
      if cp -f "$FORRAS" "$TMP" && mv -f "$TMP" "$MASOLAT"; then
        naplo "adatbázis: a másolat frissült (ideiglenes név + átnevezés; a régi példányok a régi állományt látják tovább)"
      else
        rm -f "$TMP"
        naplo "HIBA: a másolás sikertelen — a meglévő másolat érintetlen"
        [ -f "$MASOLAT" ] || exit 1
      fi ;;
    *)
      naplo "adatbázis: NINCS másolás — a forrásnak nincs olvasható epites_ts-e ($FORRAS); a meglévő másolat marad" ;;
  esac
else
  naplo "adatbázis: NINCS másolás — nincs Windows-oldali pardes.db ($FORRAS); a meglévő másolat marad"
  FORRAS=""
fi
[ -f "$MASOLAT" ] || { naplo "HIBA: nincs adatbázis-másolat: $MASOLAT"; exit 1; }

if [ "${PARDES_INDIT_CSAK_ELOKESZIT:-}" = "1" ]; then
  naplo "csak előkészítés (PARDES_INDIT_CSAK_ELOKESZIT=1): a szervert nem indítom"
  exit 0
fi

# -- (3) a szerver indítása újratöltővel ------------------------------------------------------------------------------------------
# A zárat egy háttérfolyamat engedi el, amint a port nyitva van (vagy 60 mp után): addig egy újabb kattintás nem előzheti meg a felállást.
( for _ in $(seq 1 300); do (echo > "/dev/tcp/127.0.0.1/$PORT") 2>/dev/null && break; sleep 0.2; done; flock -u 9 ) &
export PARDES_DB="$MASOLAT"
export PARDES_FORRAS_DB="$FORRAS"
naplo "szerver indítása: kiadás=$KIADAS port=$PORT adatbázis=$MASOLAT (újratöltővel)"
cd "$CEL" && exec "$PY" alkalmazas.py --port "$PORT" --kiadas "$KIADAS" --ujratolt
