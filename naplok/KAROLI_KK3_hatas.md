# KAROLI_KK3_hatas.md — hatásbecslés ⛔

*KK3 — KAROLI_KULCS_BRIEF.md §3. Szkript: `naplok/KAROLI_KK3_hatasbecsles_general.py`,
a KK1 ok-besorolására (`naplok/KAROLI_KK1_ok_besorolas_reszletek.tsv`) és a KK2
tervezetre építve. **Az importert ez a menet nem módosítja** — csak becslés.*

## Összesített hatás

| | Érték |
|---|---|
| Mért `szamozas_elteres` LXX-vers (38 nem-Zsoltár könyv) | 985 |
| **Megoldódna** a G4-importer-javítástól (H1+H2) | **666 (67,6%)** |
| **Továbbra sem oldódik meg** (H3 `EGYIK_SEM` + H5 valódi LXX-eltérés) | 319 (32,4%) |
| Aránnyal a teljes 1 015-re becsülve | **~686 (67,6%)** |

**A Zsoltárok (63 fejezet, ~30 érintett vers) nincs külön mérve** — saját
cím-eltolás-algoritmusa van (`zsolt_felirat_eltolas`), amit a KK1 nem
bontott H1–H5-re; a becslés csak arányosítás, nem külön számítás. **A
`KAROLI_KULCS_BRIEF.md` §1 sikerkritériuma (≥90% csökkenés) ebben a
formában valószínűleg NEM teljesül** — 67,6% egy jelentős, de nem elégséges
javulás; a fennmaradó ~30%-ot (H3 + H5) a G5 szerint kézi, tartalmi
egyeztetéssel kellene tovább csökkenteni egy későbbi menetben, a
`EGYIK_SEM` fejezetek soronkénti feldolgozásával.

## A lexikon 15 sora — becsült új állapot

| Ok | Sorok | Becsült kimenet |
|---|---|---|
| H1 (importer-hiba) | Jób 38:7, 38:16, 38:30 | **megoldódna** |
| H2 (Károli MT-számozás) | Józs 13:12, Ézs 63:13, Jón 2:3, Jón 2:6 | **megoldódna** |
| H3 (`EGYIK_SEM`, kézi kell) | Jób 17:13, 17:16, Hós 13:14 | változatlan marad |
| H4 (generátor-oldali, Józsué B-szöveg) | Józs 12:4, 15:8, 17:15, 18:16 | változatlan marad **ebben a menetben** (G6: csak javaslat) |
| H5 (valódi LXX-eltérés) | Jer 51:46 | változatlan marad |

**7/15 lexikon-sor oldódna meg közvetlenül** a G4-importer-javítástól. A
maradék 8-ból 4 (Józsué, H4) egy **külön, a lexikon-generátort érintő**
javítást igényelne (a jelen menet hatáskörén kívül, G6 szerint csak
javaslat), 3 (H3) kézi tartalmi egyeztetést, 1 (Jer 51:46, H5) véglegesen
"valódi eltérés" marad.

## Előrejelzés a lexikon "Egyezés"-bontására (a 8 TUDOMANYOS oldalon)

| Kategória | Jelenlegi | Becsült, a G4-javítás után |
|---|---|---|
| egyező | 123 | **~130** (+7) |
| kutatói azonosítás függőben | 87 | 87 (változatlan) |
| szamozas_elteres | 15 | **~8** (3 H3 + 4 H4 + 1 H5) |
| eltérő | 3 | 3 (változatlan) |
| nincs LXX_OS-könyv | 5 | 5 (változatlan) |
| LXX-minusz | 1 | 1 (változatlan, de a Jer 51:46 tartalmilag ide illene, ha a generátor a jövőben újraosztályozná) |

**Fontos korlátozás:** ez tisztán **előrejelzés** a KK2-tervezet logikájából
levezetve — a tényleges számot csak a 2. menet (KK4 élesítés → KK5
újragenerálás → KK6 újramérés) adja meg. A KK6 sikerkritériumát (≥90%
csökkenés, vagy okonként indokolt hiány) **ez a becslés előre jelzi, hogy
valószínűleg NEM éri el önmagában** a puszta importer-javítás — a H3/H5
kategóriák kézi feldolgozása nélkül a csökkenés ~68% körül tetőzik.
