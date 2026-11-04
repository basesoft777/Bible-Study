#!/bin/sh
# F123 ALVIL-001 új cikk, U1 — a hét lépés determinisztikus része (1., 3–6.) a mai adaton,
# naplózva (adat/auditok.tsv, B4). Kimenet: naplok/F123_ALVIL2_u1_kimenet.txt
L="python eszkozok/lekerdez.py --naplo ALVIL-001 --lepes B4"
{
echo "## 1. gerinc-metszet"
$L gerinc "Zsolt 16:10" "ApCsel 2:27"
$L gerinc "Hós 13:14" "1Kor 15:55"
echo "## 3. teljes scan"
$L scan H7585
$L scan G0086
echo "## 4. kollokáció"
$L kollokacio H7585 H4194
$L kollokacio H7585 H0011
$L kollokacio H7585 H3381
$L kollokacio H7585 H0953
$L kollokacio G0086 G2288
echo "## 5. igealak"
$L igealak H7585
$L igealak G0086
echo "## 6. LXX-híd (kulcsversek; a teljes ÓSZ: naplok/F123_ALVIL2_lxx_hid.py)"
$L lxx-hid "Zsolt 16:10"
$L lxx-hid "Hós 13:14"
} > naplok/F123_ALVIL2_u1_kimenet.txt 2>&1
