#!/bin/bash
# Az adatbázis háttér-újraépítése (#101, DT-F101b) — az indit.sh indítja (setsid + nohup), a parancsikon kézi „újraépítés” indítója is ezt hívja.
#
# Lépések: (1) állapotfájl: fut; (1b) a forrás pillanatképe a WSL natív lemezére (tar; a /mnt-ről közvetlenül építve mérve 266 s, natívról 96 s: #101 M1 mérés);
# (2) építés a pillanatképből ideiglenes névre (az `sqlite_epit.py` maga is csak ideiglenes névre ír, és az integritás-sértésnél nem ír fájlt); (3) az új fájl ellenőrzése (`allapot.py db_ellenoriz`: quick_check, epites_ts és forrás-azonosító van); (4) siker után
# másolás a Windows-oldali pardes.db helyére (ideiglenes név + atomi átnevezés; az idejét méri és kiírja). A WSL-másolatot az indító következő
# indításkor szinkronizálja (a futó szerver alatt nem cserélünk fájlt); (5) állapotfájl: kesz | elbukott. Hiba esetén a meglévő adatbázisok érintetlenek.
#
# Környezet (az indit.sh adja; a teszt ezekkel dolgozik):
#   PARDES_GYOKER           a repó gyökere (a forrás: adat/, konkordancia/)
#   PARDES_PY               a venv Python
#   PARDES_DB               a WSL-beli másolat (cél)
#   PARDES_FORRAS_DB        a Windows-oldali pardes.db (a másolat célja építés után)
#   PARDES_EPITES_ALLAPOT   állapotfájl (egy sor: allapot<TAB>ido<TAB>pid<TAB>uzenet<TAB>naplo)
#   PARDES_EPITES_NAPLO     az építés naplója
#   PARDES_EPIT_PARANCS     (teszthez) az építés helyett futtatott parancs; az első argumentuma a kimeneti fájl
#
# Kézi használat (a „PaRDeS adatbázis újraépítése” asztali parancsikon): `epit_hatter.sh --kezi` — a környezeti változók alapértékei a szkript
# helyéből és a $HOME/pardes-ból jönnek, a zárat maga veszi (PARDES_EPIT_ZAR, alap: $HOME/pardes/.epit.zar), és a naplót a terminálra is kiírja.
set -u
CEL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEZI=0; [ "${1:-}" = "--kezi" ] && KEZI=1
GYOKER="${PARDES_GYOKER:-$(cd "$CEL/../.." && pwd)}"
PY="${PARDES_PY:-$HOME/pardes/eszkozok/olvaso_szerver/.venv/bin/python}"
MASOLAT="${PARDES_DB:-$HOME/pardes/pardes.db}"
FORRAS="${PARDES_FORRAS_DB-$GYOKER/pardes.db}"
ALLAPOT="${PARDES_EPITES_ALLAPOT:-$HOME/pardes/epites_allapot.tsv}"
NAPLO="${PARDES_EPITES_NAPLO:-$HOME/pardes/epites.log}"
if [ "$KEZI" = "1" ]; then
  ZAR="${PARDES_EPIT_ZAR:-$HOME/pardes/.epit.zar}"
  mkdir -p "$(dirname "$ZAR")"
  exec 8>"$ZAR"
  flock -n 8 || { echo "[epit] már fut egy másik újraépítés ($ZAR) — várd meg, vagy nézd a naplót: $NAPLO"; exit 1; }
fi
TMP="$MASOLAT.epit.$$"
SNAP="$MASOLAT.forras.$$"

ido() { date '+%Y-%m-%dT%H:%M:%S'; }
masodperc() { date +%s; }
allapot_ir() {   # $1 állapot, $2 üzenet (egy sor, tab nélkül)
  local uz="${2//$'\t'/ }"; uz="${uz//$'\n'/ }"
  printf '%s\t%s\t%s\t%s\t%s\n' "$1" "$(ido)" "$$" "$uz" "$NAPLO" > "$ALLAPOT.tmp.$$" && mv -f "$ALLAPOT.tmp.$$" "$ALLAPOT"
}
mkdir -p "$(dirname "$ALLAPOT")" "$(dirname "$NAPLO")" "$(dirname "$MASOLAT")"
: > "$NAPLO"
if [ "$KEZI" = "1" ]; then exec > >(tee -a "$NAPLO") 2>&1; else exec >>"$NAPLO" 2>&1; fi
trap 'rm -f "$TMP" "$TMP.epit" "$ALLAPOT.tmp.$$"; [ -n "${SNAP:-}" ] && [ -d "$SNAP" ] && rm -rf -- "$SNAP"' EXIT
echo "[epit] $(ido) indul: gyökér=$GYOKER kimenet=$TMP"
allapot_ir fut "az építés fut"

TS0="$(masodperc)"
mkdir -p "$SNAP"
(cd "$GYOKER" && tar -c --exclude=.git --exclude='*.db' --exclude='*.db.*' --exclude='*.zar' .) | tar -x -C "$SNAP"
PS=("${PIPESTATUS[@]}")
if [ "${PS[0]:-1}" -ne 0 ] || [ "${PS[1]:-1}" -ne 0 ]; then
  allapot_ir elbukott "a forrás pillanatképe nem készült el ($GYOKER -> $SNAP); a meglévő adatbázisok érintetlenek"
  exit 1
fi
echo "[epit] $(ido) pillanatkép kész: $SNAP ($(( $(masodperc) - TS0 )) s)"
T0="$(masodperc)"
if [ -n "${PARDES_EPIT_PARANCS:-}" ]; then
  bash -c "$PARDES_EPIT_PARANCS" _ "$TMP"; RC=$?
else
  "$PY" "$SNAP/eszkozok/sqlite_epit.py" --mod teljes --gyoker "$SNAP" --kimenet "$TMP"; RC=$?
fi
T1="$(masodperc)"
echo "[epit] $(ido) az építés kilépési kódja: $RC (idő: $((T1 - T0)) s)"
if [ "$RC" -ne 0 ] || [ ! -f "$TMP" ]; then
  OK="$(grep -m1 -E 'INTEGRITÁS-SÉRTÉS|HIBA' "$NAPLO" | head -c 200)"
  allapot_ir elbukott "az építés elbukott (kilépési kód: $RC${OK:+; $OK}); a meglévő adatbázisok érintetlenek"
  exit 1
fi
ELL="$("$PY" "$CEL/allapot.py" db_ellenoriz "$TMP" 2>&1)"
if [ "$ELL" != "ok" ]; then
  echo "[epit] az új adatbázis ellenőrzése bukott: $ELL"
  allapot_ir elbukott "az új adatbázis ellenőrzése bukott ($ELL); a meglévő adatbázisok érintetlenek"
  exit 1
fi
# A WSL-másolatot NEM cseréljük itt: a futó szerver ugyanazt a fájlt olvassa, és a csere után régi gyorsítótár-kulccsal és régi meta-adattal keverné az új
# adatot (ELLENOR_F101). A Windows-oldali pardes.db cseréje után az indító 2. lépése (szinkron) a következő indításkor másolja át (egy kattintás); addig a
# lábléc jelzi, hogy az adatbázis régebbi a Windows-oldalinál. A régi Windows-oldali állomány a csere pillanatáig érintetlen.
MASOLAS=""
if [ -n "$FORRAS" ]; then
  T2="$(masodperc)"
  if cp -f "$TMP" "$FORRAS.uj.$$" && mv -f "$FORRAS.uj.$$" "$FORRAS"; then
    MASOLAS="; másolás a Windows-oldalra: $(( $(masodperc) - T2 )) s"
    echo "[epit] $(ido) a Windows-oldali pardes.db kicserélve: $FORRAS$MASOLAS"
  else
    rm -f "$FORRAS.uj.$$"
    allapot_ir elbukott "a Windows-oldali pardes.db cseréje sikertelen ($FORRAS); a meglévő adatbázisok érintetlenek"
    exit 1
  fi
else
  # nincs Windows-oldali példány: a WSL-másolat cseréje az egyetlen út
  if ! mv -f "$TMP" "$MASOLAT"; then
    allapot_ir elbukott "a WSL-másolat cseréje sikertelen; a meglévő adatbázisok érintetlenek"
    exit 1
  fi
  echo "[epit] $(ido) a WSL-másolat kicserélve: $MASOLAT"
fi
allapot_ir kesz "az újraépítés kész (pillanatkép: $((T0 - TS0)) s, építés: $((T1 - T0)) s$MASOLAS)"
echo "[epit] $(ido) kész"
exit 0
