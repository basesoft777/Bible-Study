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
# A FEJ oldal NEM feltetlenul a HEAD commit -- ha a munkafan van commitolatlan
# modositas (a S1 menet tipikus hasznalata: szerkesztes, majd nulla-diff-
# proba MEG A COMMIT ELOTT), a szkript egy `git stash create`-tel keszit egy
# ideiglenes, a git tortenetbe soha be nem kerulo commit-objektumot a HEAD +
# a kovetkezett/munkafa-modositasokbol, es AZT hasznalja FEJ-kent -- a
# munkafat, az indexet es a HEAD-et nem erinti. (Korlat: uj, meg soha nem
# `git add`-elt fajlt a `git stash create` nem vesz fel -- meglevo, kovetett
# fajl modositasat igen.) Ha nincs commitolatlan modositas, a FEJ egyszeruen
# a HEAD.
#
# Kimenet: semmi stdout-ra, ha a ket generalt lexikon/ konyvtar (a
# *_TUDOMANYOS.md es *_TORZSCIKK.md fajlok egyutt) bajtra azonos;
# kulonben a `diff -r` kimenete.
#
# A general.py --cel lexikon/torzscikk a lexikon/ konyvtaron kivul semmit
# nem ir (a tematikus_lezart/naplok/ ala csak a --cel naplok ir, amit ez a
# szkript nem hasznal) -- a diff -r "$MUNKA/alap/lexikon" "$MUNKA/fej/lexikon"
# emiatt a teljes irt kimenetet lefedi, kulon tematikus_lezart-osszevetes
# nem kell.
#
# Kilepesi kod: 0 = azonos (nulla-diff), 1 = elter, 2 = hasznalati/futasi hiba.
#
# Korlat, amit tudni kell -- ASZIMMETRIKUS tures: az ALAP oldal es a FEJ
# (HEAD) oldal generalasa nem egyenrangu.
#   - ALAP: ha a general.py --cel lexikon --ir itt kivetellel megszakad
#     (pl. egy motivumnak nincs meg egyetlen sora sem az adat/res_forras.tsv-
#     ben -- l. D30/TEREMT-002), a szkript ezt NEM tekinti vegzetes hibanak --
#     a megszakadas elott mar kiirt fajlokat hasonlitja ossze, es a nem-nulla
#     kilepokodrol csak FIGYELMEZTETEST ir a stderr-re. Ezt a HEAD-en JAVITOTT
#     hiba korabbi, alap-commitbeli allapotanak elturesere szantuk.
#   - FEJ: ha ITT szakad meg a generalas (barmilyen okbol -- pl. a most
#     bevezetett javitas maga hibas, vagy egy uj regresszio), az VEGZETES:
#     a szkript AZONNAL exit 2-vel all le, diff-et nem szamol, es nem
#     hallgatja el a hibat -- egy hibas FEJ-oldali futas melletti "nulla-diff"
#     hamis biztonsagot adna.

set -u

if [ "${1:-}" = "" ]; then
    echo "hasznalat: nulladiff.sh <alap-commit> [PARDES_DATUM]" >&2
    exit 2
fi

ALAP="$1"
PARDES_DATUM="${2:-$(date +%Y-%m-%d)}"

REPO_GYOKER="$(git rev-parse --show-toplevel)" || exit 2
FEJ="$(git -C "$REPO_GYOKER" stash create 2>/dev/null)"
if [ -z "$FEJ" ]; then
    FEJ="$(git -C "$REPO_GYOKER" rev-parse HEAD)" || exit 2
fi

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
    OLDAL_HIBA=0

    # A ket generalo-hivast KULON kilepokoddal figyeljuk -- ha egy compound
    # `(cmd1; cmd2)`-t egyben futtatnank, a $? csak az UTOLSO parancsra
    # vonatkozna, es egy elszallt --cel lexikon utan egy sikeres --cel
    # torzscikk csendben 0-t adna vissza (elfedve a hibat).
    ( cd "$MUNKA/$OLDAL" && PARDES_DATUM="$PARDES_DATUM" PYTHONIOENCODING=utf-8 \
        python eszkozok/general.py --cel lexikon --ir ) >&2
    [ $? -ne 0 ] && OLDAL_HIBA=1

    ( cd "$MUNKA/$OLDAL" && PARDES_DATUM="$PARDES_DATUM" PYTHONIOENCODING=utf-8 \
        python eszkozok/general.py --cel torzscikk --ir ) >&2
    [ $? -ne 0 ] && OLDAL_HIBA=1

    if [ "$OLDAL_HIBA" -ne 0 ]; then
        if [ "$OLDAL" = "fej" ]; then
            echo "nulladiff: VEGZETES -- a FEJ oldal generalasa (lexikon es/vagy torzscikk) nem-nulla kileptekoddal zarult, diff-et nem szamolok" >&2
            exit 2
        fi
        echo "nulladiff: figyelmeztetes -- az ALAP oldal generalasa (lexikon es/vagy torzscikk) nem-nulla kileptekoddal zarult (l. a fejlec Korlat-megjegyzeset)" >&2
    fi
done

DIFF_KIMENET="$(diff -r "$MUNKA/alap/lexikon" "$MUNKA/fej/lexikon")"
if [ -z "$DIFF_KIMENET" ]; then
    echo "nulladiff: RENDBEN -- a ket oldal generalt lexikon/ konyvtara azonos" >&2
    exit 0
fi
echo "$DIFF_KIMENET"
exit 1
