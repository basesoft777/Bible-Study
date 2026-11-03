#!/bin/sh
# F123 ANTROP-001 új cikk, U1 — a hét lépés determinisztikus része (1., 3–6.) a mai adaton,
# naplózva (adat/auditok.tsv, B4). Kimenet: naplok/F123_ANTROP2_u1_kimenet.txt
L="python eszkozok/lekerdez.py --naplo ANTROP-001 --lepes B4"
{
echo "## 1. gerinc-metszet"
$L gerinc "1Thessz 5:23" "Zsid 4:12"
$L gerinc "Luk 1:46-47" "1Kor 15:45"
$L gerinc "1Móz 2:7" "1Kor 15:45"
echo "## 3. teljes scan (a négy főnév és a két melléknév)"
for s in G4151 G5590 G4152 G5591 H5315 H2416; do $L scan $s; done
echo "## 4. kollokáció"
$L kollokacio G4151 G5590
$L kollokacio G4151 G5591
$L kollokacio G4152 G5590
$L kollokacio G4152 G5591
$L kollokacio H5315 H2416
$L kollokacio H7307 H5315
echo "## 5. igealak"
$L igealak G5591
$L igealak G4152
echo "## 6. LXX-híd"
$L lxx-hid "1Móz 2:7"
$L lxx-hid "Jób 12:10"
$L lxx-hid "Jón 4:8"
} > naplok/F123_ANTROP2_u1_kimenet.txt 2>&1
