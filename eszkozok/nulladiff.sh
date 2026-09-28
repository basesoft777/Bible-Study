#!/usr/bin/env bash
# nulladiff.sh -- SZOTAR_BRIEF.md D30: A/B nulla-diff proba.
#
# A "nulla-diff" a HEAD es egy masik commit generalt lexikon/ kimenetet
# hasonlitja ossze -- KULON git worktree-ben, KULON-KULON legeneralva,
# azonos PARDES_DATUM mellett -- SOHA nem a commitolt eles fajlokhoz
# viszonyit (git status --porcelain lexikon/). Ok: a general.py TS mezoje
# mindig a futtatas napja (PARDES_DATUM nelkul), ezert ket kulon napon
# futtatott, tartalmilag azonos generalas is elterne egy commitolt
# pillanatfelvetelhez kepest -- l. a D30 dontesnaplo-bejegyzest.
#
# Hasznalat:
#   eszkozok/nulladiff.sh <alap-commit> [PARDES_DATUM]
#
# PARDES_DATUM alapertelmezese: a mai nap (YYYY-MM-DD). Mindket oldal
# ugyanazt a PARDES_DATUM erteket kapja.
#
# Kimenet: semmi stdout-ra, ha a ket generalt lexikon/ konyvtar (a
# *_TUDOMANYOS.md es *_TORZSCIKK.md fajlok egyutt) bajtra azonos;
# kulonben a `diff -r` kimenete.
#
# Kilepesi kod: 0 = azonos (nulla-diff), 1 = elter, 2 = hasznalati hiba.
#
# Korlat, amit tudni kell: ha az <alap-commit>-en a general.py --cel
# lexikon --ir kivetellel megszakad (pl. egy motivumnak nincs meg egyetlen
# sora sem az adat/res_forras.tsv-ben -- l. D30/TEREMT-002), a szkript ezt
# NEM tekinti vegzetes hibanak -- a megszakadas elott mar kiirt fajlokat
# hasonlitja ossze, es a nem-nulla kilepokodrol csak FIGYELMEZTETEST ir a
# stderr-re. Ha egy fajl emiatt csak az egyik oldalon letezik, azt a
# `diff -r` kulon sorban jelzi -- ez nem hallgatodik el.

set -u

if [ "${1:-}" = "" ]; then
    echo "hasznalat: nulladiff.sh <alap-commit> [PARDES_DATUM]" >&2
    exit 2
fi

ALAP="$1"
PARDES_DATUM="${2:-$(date +%Y-%m-%d)}"

REPO_GYOKER="$(git rev-parse --show-toplevel)" || exit 2
FEJ="$(git rev-parse HEAD)" || exit 2

MUNKA="$(mktemp -d)" || exit 2
cleanup() {
    git -C "$REPO_GYOKER" worktree remove --force "$MUNKA/alap" >/dev/null 2>&1
    git -C "$REPO_GYOKER" worktree remove --force "$MUNKA/fej" >/dev/null 2>&1
    rm -rf "$MUNKA"
}
trap cleanup EXIT

echo "nulladiff: alap=$ALAP fej=$FEJ datum=$PARDES_DATUM munka=$MUNKA" >&2

git -C "$REPO_GYOKER" worktree add --detach "$MUNKA/alap" "$ALAP" >&2 || exit 2
git -C "$REPO_GYOKER" worktree add --detach "$MUNKA/fej" "$FEJ" >&2 || exit 2

for OLDAL in alap fej; do
    (
        cd "$MUNKA/$OLDAL" || exit 2
        PARDES_DATUM="$PARDES_DATUM" PYTHONIOENCODING=utf-8 python eszkozok/general.py --cel lexikon --ir
        PARDES_DATUM="$PARDES_DATUM" PYTHONIOENCODING=utf-8 python eszkozok/general.py --cel torzscikk --ir
    ) >&2
    if [ $? -ne 0 ]; then
        echo "nulladiff: figyelmeztetes -- a(z) '$OLDAL' oldal generalasa nem-nulla kileptekoddal zarult (l. a fejlec Korlat-megjegyzeset)" >&2
    fi
done

DIFF_KIMENET="$(diff -r "$MUNKA/alap/lexikon" "$MUNKA/fej/lexikon")"
if [ -z "$DIFF_KIMENET" ]; then
    echo "nulladiff: RENDBEN -- a ket oldal generalt lexikon/ konyvtara azonos" >&2
    exit 0
fi
echo "$DIFF_KIMENET"
exit 1
