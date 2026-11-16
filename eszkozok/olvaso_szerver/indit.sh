#!/bin/bash
# Az olvasó-szerver közös indítója (#100) — a három asztali parancsikon ezt hívja (WSL `pardes` disztribúció).
#
# Használat:  indit.sh <kiadás: belso|nyilvanos|kereskedelmi> <port>
#
# Sorrend: (0) a főcheckout frissítése (F225): csak `belso` kiadásnál, a főcheckoutban, a main ágon: `git fetch`, és ha a munkafa tiszta,
# `git merge --ff-only origin/main` (a `git pull --ff-only` két lépésben); különben kihagyja, és a napló kiírja, miért; (1) a porton futó régi
# példány leállítása; (2) adatbázis-szinkron: a Windows-oldali pardes.db (forrás) és a WSL-beli másolat (cél) `meta.epites_ts`-ének összevetése
# — eltérésnél (vagy hiányzó célnál) másolás ideiglenes névre, majd atomi átnevezés (a szinkron-kulcs az epites_ts, NEM a fájl mtime-ja);
# azonos építési időnél nincs másolás; (3) a szerver indítása újratöltővel (alkalmazas.py --ujratolt). A napló minden lépést kiír
# ("[indit] …"), többek közt azt, hogy másolás vagy frissítés történt-e.
#
# ELŐNÉZETI MÓD (F225): ha a szkript linkelt worktree-ben áll (a repó gyökerében a `.git` egy fájl), vagy PARDES_ELONEZET=1, az indító
#   - SOHA nem ír a közös adatbázis-másolatba (nincs szinkron: a `~/pardes/pardes.db` csak olvasható; a forrás alapja a főcheckout pardes.db-je,
#     csak a lábléc összevetéséhez);
#   - nem frissíti a főcheckoutot;
#   - a porton futó példányt csak akkor állítja le, ha annak munkakönyvtára ez a checkout; idegen checkout példányánál megáll (kilépési kód 3),
#     és szabad portot javasol (8775–8779).
# Előnézet: `wsl -d pardes -e bash -lc "cd <worktree WSL-útja> && ./eszkozok/olvaso_szerver/indit.sh belso 8775"` (vagy a .claude/launch.json olvaso-ag).
#
# Környezeti változók (alapértékekkel; a gépi próba ezekkel dolgozik, hogy ne a valódi adatbázist módosítsa):
#   PARDES_FORRAS_DB   a Windows-oldali pardes.db       (alap: <repó gyökere>/pardes.db az indit.sh helyéből)
#   PARDES_DB          a WSL-beli (cél) másolat         (alap: $HOME/pardes/pardes.db)
#   PARDES_PY          a venv Python 3.12              (alap: $HOME/pardes/eszkozok/olvaso_szerver/.venv/bin/python)
#   PARDES_ZAR         a közös zárfájl (egyidejű indítások sorosítása; alap: $HOME/pardes/.indit.zar)
#   PARDES_INDIT_CSAK_ELOKESZIT=1   csak leállítás + szinkron, a szervert nem indítja (teszt_indito.py, gépi próba)
#   PARDES_ELONEZET    1: előnézeti mód; 0: nem az (alap: linkelt worktree = 1, főcheckout = 0)
#   PARDES_FRISSIT     0: a főcheckout frissítése ki (alap: be, a fenti feltételekkel); a tesztek a valódi checkoutot ezzel védik
#   PARDES_GIT         a frissítéshez használt git (alap: a /mnt/<meghajtó> alatti checkoutnál a Windows `git.exe`, különben `git`: a WSL-git
#                      a /mnt/c-n ~85 s alatt fut, és hamisan „piszkos” munkafát mér — F225 mérés; a `git.exe` 0,3 s)
set -u

KIADAS="${1:-}"
PORT="${2:-}"
case "$KIADAS" in belso|nyilvanos|kereskedelmi) ;; *) echo "[indit] használat: indit.sh <belso|nyilvanos|kereskedelmi> <port>" >&2; exit 2 ;; esac
case "$PORT" in ''|*[!0-9]*) echo "[indit] a port szám kell: '$PORT'" >&2; exit 2 ;; esac

CEL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GYOKER="$(cd "$CEL/../.." && pwd)"
PY="${PARDES_PY:-$HOME/pardes/eszkozok/olvaso_szerver/.venv/bin/python}"
MASOLAT="${PARDES_DB:-$HOME/pardes/pardes.db}"
ZAR="${PARDES_ZAR:-$HOME/pardes/.indit.zar}"
naplo() { echo "[indit] $(date +%H:%M:%S) $*"; }

[ -x "$PY" ] || { naplo "HIBA: nincs Python a venv-ben: $PY"; exit 1; }

# -- előnézeti mód (F225): linkelt worktree (a `.git` fájl) vagy PARDES_ELONEZET=1
if [ -n "${PARDES_ELONEZET:-}" ]; then ELONEZET="$PARDES_ELONEZET"
elif [ -f "$GYOKER/.git" ]; then ELONEZET=1
else ELONEZET=0; fi
if [ "$ELONEZET" = "1" ]; then
  IFS=$'\t' read -r _SZEREP FO_GYOKER _MF < <("$PY" "$CEL/allapot.py" checkout "$CEL")
  FORRAS="${PARDES_FORRAS_DB:-${FO_GYOKER:-$GYOKER}/pardes.db}"
  naplo "mód: ELŐNÉZET (checkout: $GYOKER; főcheckout: ${FO_GYOKER:-ismeretlen}) — nincs adatbázis-szinkron, nincs főcheckout-frissítés, idegen példányt nem állítok le"
else
  FORRAS="${PARDES_FORRAS_DB:-$CEL/../../pardes.db}"
fi

# -- sorosítás: két egymás utáni kattintás ne másolja/indítsa egyszerre ugyanazt (a zárat a szerver felállása után engedjük el)
mkdir -p "$(dirname "$ZAR")"
exec 9>"$ZAR"
flock -w 120 9 || { naplo "HIBA: a zár nem szerezhető meg ($ZAR)"; exit 1; }

# -- (0) a főcheckout frissítése (F225) -----------------------------------------------------------------------------------------
# Feltételek (mindegyik kell): PARDES_FRISSIT nem 0; belso kiadás; nem előnézet; a repó gyökerében `.git` KÖNYVTÁR (főcheckout, nem worktree); az ág main.
# `git fetch` mindig (a munkafát nem érinti, és a lábléc lemaradás-jelzése csak friss origin/main mellett igaz); az előreléptetés csak tiszta
# munkafánál (a követett fájlok módosítatlanok; a követetlenek nem akadályozzák). Hiba sehol nem állítja meg az indítást.
frissit_fo() {
  [ "${PARDES_FRISSIT:-1}" = "0" ] && { naplo "frissítés: kihagyva — PARDES_FRISSIT=0"; return 0; }
  [ "$KIADAS" = "belso" ] || { naplo "frissítés: kihagyva — csak a belso kiadásnál (kiadás: $KIADAS)"; return 0; }
  [ "$ELONEZET" = "1" ] && { naplo "frissítés: kihagyva — előnézeti mód (a főcheckoutot nem húzzuk)"; return 0; }
  [ -d "$GYOKER/.git" ] || { naplo "frissítés: kihagyva — nem főcheckout (nincs .git könyvtár: $GYOKER)"; return 0; }
  local ag G
  ag="$("$PY" "$CEL/allapot.py" git "$GYOKER" | cut -f1)"
  [ "$ag" = "main" ] || { naplo "frissítés: kihagyva — a főcheckout nem a main ágon áll (ág: $ag)"; return 0; }
  G="${PARDES_GIT:-}"
  if [ -z "$G" ]; then
    case "$GYOKER" in /mnt/*) command -v git.exe >/dev/null 2>&1 && G=git.exe ;; esac
    G="${G:-git}"
  fi
  command -v "$G" >/dev/null 2>&1 || { naplo "frissítés: kihagyva — nincs git ($G)"; return 0; }
  export GIT_TERMINAL_PROMPT=0
  local ki
  if ! ki="$(cd "$GYOKER" && timeout 90 "$G" fetch --quiet origin main 2>&1)"; then
    naplo "frissítés: kihagyva — a git fetch sikertelen (${ki:-nincs kimenet}); a main nem frissült"
    return 0
  fi
  local piszkos
  piszkos="$(cd "$GYOKER" && timeout 90 "$G" --no-optional-locks status --porcelain --untracked-files=no 2>&1 | tr -d '\r')"
  if [ -n "$piszkos" ]; then
    naplo "frissítés: KIHAGYVA — a munkafa nem tiszta ($(printf '%s\n' "$piszkos" | wc -l) módosított követett fájl, pl.: $(printf '%s\n' "$piszkos" | head -n 2 | tr '\n' ';')); a git fetch lefutott, a main nem lépett előre"
    return 0
  fi
  local elotte utana
  elotte="$(cd "$GYOKER" && "$G" rev-parse HEAD | tr -d '\r')"
  if ! ki="$(cd "$GYOKER" && timeout 120 "$G" merge --ff-only --quiet origin/main 2>&1)"; then
    naplo "frissítés: kihagyva — a main nem léptethető előre az origin/main-re (${ki:-nincs kimenet})"
    return 0
  fi
  utana="$(cd "$GYOKER" && "$G" rev-parse HEAD | tr -d '\r')"
  if [ "$elotte" = "$utana" ]; then
    naplo "frissítés: a főcheckout naprakész (${utana:0:8})"
    return 0
  fi
  naplo "frissítés: a főcheckout előrelépett: ${elotte:0:8} -> ${utana:0:8} (git fetch + merge --ff-only origin/main)"
  FRISSULT=1
}
FRISSULT=0
[ "${PARDES_FRISSITVE:-}" = "1" ] || frissit_fo
if [ "$FRISSULT" = "1" ]; then
  # az indit.sh maga is változhatott: a bash a szkriptet menet közben olvassa, ezért a frissített fájllal újraindul (a zárat előbb elengedi)
  naplo "újraindítás a frissített indit.sh-val"
  flock -u 9
  exec env PARDES_FRISSITVE=1 bash "${BASH_SOURCE[0]}" "$@"
fi

# -- (1) a régi példány leállítása ------------------------------------------------------------------------------------------
REGI="$(fuser "$PORT"/tcp 2>/dev/null | tr -s ' ' | sed 's/^ //')"
if [ -n "$REGI" ] && [ "$ELONEZET" = "1" ]; then
  # előnézetből csak a saját checkout példánya állítható le: a munkakönyvtár a $CEL (vagy alatta)
  CEL_REAL="$(readlink -f "$CEL")"
  IDEGEN=""
  for P in $REGI; do
    CWD="$(readlink -f "/proc/${P//[!0-9]/}/cwd" 2>/dev/null)"
    case "$CWD" in "$CEL_REAL"|"$CEL_REAL"/*) ;; *) IDEGEN="$IDEGEN $P:${CWD:-ismeretlen}" ;; esac
  done
  if [ -n "$IDEGEN" ]; then
    IDEGEN_CWD="${IDEGEN# }"; IDEGEN_CWD="${IDEGEN_CWD%% *}"; IDEGEN_CWD="${IDEGEN_CWD#*:}"
    IDEGEN_AG="$("$PY" "$CEL/allapot.py" git "$IDEGEN_CWD" 2>/dev/null | cut -f1)"
    naplo "HIBA: a $PORT porton idegen példány fut (PID:munkakönyvtár:$IDEGEN; ág: ${IDEGEN_AG:-ismeretlen}) — előnézetből nem állítom le"
    SZABAD=""
    for Q in 8775 8776 8777 8778 8779; do
      [ "$Q" = "$PORT" ] && continue
      fuser -s "$Q"/tcp 2>/dev/null || { SZABAD="$Q"; break; }
    done
    naplo "${SZABAD:+szabad port: $SZABAD — indítsd így: indit.sh $KIADAS $SZABAD}${SZABAD:-nincs szabad port a 8775–8779 tartományban}"
    exit 3
  fi
fi
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
if [ "$ELONEZET" = "1" ]; then
  # előnézetben a közös másolat SOHA nem íródik: a szerver csak olvassa (mode=ro); a forrás csak a lábléc összevetéséhez kell
  if [ -f "$FORRAS" ]; then naplo "adatbázis: ELŐNÉZET — NINCS másolás; a közös másolat ($MASOLAT) csak olvasható; a lábléc a forrással ($FORRAS) veti össze"
  else FORRAS=""; naplo "adatbázis: ELŐNÉZET — NINCS másolás; a közös másolat ($MASOLAT) csak olvasható; nincs forrás-adatbázis az összevetéshez"; fi
elif [ -f "$FORRAS" ]; then
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
MOD="főcheckout"; [ "$ELONEZET" = "1" ] && MOD="előnézet"
naplo "szerver indítása: kiadás=$KIADAS port=$PORT mód=$MOD adatbázis=$MASOLAT (újratöltővel); cím: http://localhost:$PORT/"
cd "$CEL" && exec "$PY" alkalmazas.py --port "$PORT" --kiadas "$KIADAS" --ujratolt
