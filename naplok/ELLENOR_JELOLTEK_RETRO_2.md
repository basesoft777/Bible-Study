# Független ellenőrzés, 2. kör — F63_JELOLTEK_RETRO_BRIEF.md · `ae6ee24d..f88dfce2`

*A `fuggetlen-ellenor` jelentése, az orkesztrátor mentette fájlba (az ellenőrnek nem volt fájlíró eszköze). Az 1. kör: `naplok/ELLENOR_JELOLTEK_RETRO.md`. Eredmény: **ELTÉRÉS: 1 tétel** (alacsony). Az ellenőr nem javított semmit.*

## Az 1. kör 9 eltérése

| 1. kör eltérés | eredmény | indok |
|---|---|---|
| 1. E9 / CI | OK | `futtat.py --valtozott` (diff-alap `ae6ee24d`): E9 0, HIBA 0; E25 3 és E27 33 JELENTÉS nem az ág sorai |
| 3. EXTRA, KOLLOKACIO_TAGOK | OK | `EXTRA = {}`; H2403 az `elofordulasok.tsv:211`-ben; `KOLLOKACIO_TAGOK` törölve |
| 3. CSOPORTOS_KIZARAS, G0093 | OK | a G0093 a `Bun` napló 220. sorában („24 igehely, ELUTASÍTVA”), a többi Strong a 209–219. sorban |
| 3. kód saját megjegyzése | **ELTÉRÉS** | `nem_vizsgalt.py:76-77`: „a G2672, G2671, G5351, G5356, G1311, G0093 NINCS az `elofordulasok.strong`-ban” — a G2671, G5351, G5356 és G1311 benne van (`elofordulasok.tsv:247, 250, 251, 252`); csak a G2672 és a G0093 hiányzik |
| 3. HAMART csoportos kizárás 537 | nem ellenőrizhető | a `meres` szkript az ellenőr körében nem futtatható; a mérés és a zárás egyezik |
| 4. tematikus horgony | OK | a `lista` és a mérés is nevesített kategóriaként adja; a H5315+H2416 sehol nem „[normál]” |
| 6. M1, egy commit | OK (rögzítve) | `F63_zaras.md:3`; commitok: F63.5, F63.15, F63.17 |
| 7. M3 fájlnév | OK (rögzítve) | `F63_zaras.md:18` |
| 2. KIRALY-001, 6 új sor | OK | az igehelyek a `Melk.` napló 29. sorában, az elutasítás a 44. sorban; `scan H3548 --szakasz` mind a hatra n=1; munkalap egyezik |
| 5. Copeland | OK | csak a `forras_kereses` előtagja változott (word-diff) |
| 8. 2Pét 3:10, 3:12 | OK | a `Bun` napló 179. sorával egyezik; `nyitva` megmaradt |
| 9. 1Pét 1:6, 1:7 | OK | a `Seg.` napló 61. sorával tartalmilag egyezik; a „mellett” viszony helyesen szerepel |

## Egyéb pontok

- `jeloltek.tsv` a merge-base-hez: `numstat 250 0`, törölt vagy módosított sor 0 (594 fizikai sor); az ágon belüli módosítások csak az F63.5-ben hozzáadott sorokat érintik.
- A „a DT96 és DT97 döntését megerősítem” mondat szó szerint szerepel a `DONTESEK.md` két sorában és a `F63_zaras.md`-ben; a zárás 20 sor. A mondat elhangzása a repóból nem igazolható.
- Motívumfájl, kimenet, `auditok.tsv`: érintetlen; végleges DT/N szám nincs (csak helyőrző).
- A táblasor-Δ: `jeloltek.tsv` +250, minden más 0; a bontás motívumonként: 2 + 0 + 170 + 1 + 60 + 14 + 1 + 2 = 250.
- K1, K2, K4 OK; a K3 részben nem ellenőrizhető (gate.py, ellenoriz.py, teszt nem futtatható az ellenőr körében).

## Eltérés (alacsony)

A `nem_vizsgalt.py:76-77` megjegyzése hamis ténnyel dokumentálja a `CSOPORTOS_KIZARAS` indoklását. A viselkedést nem rontja (a `kor_kategoria` a halmaz alapján dönt), de a DT95 (2) szerinti indoklás ténybelileg hibás.

*Nem ellenőrizhető maradt: az 537-es szám újraszámolása, a `gate.py`, az `ellenoriz.py`, a `teszt_nem_vizsgalt.py` eredménye, a megerősítő chat-mondat elhangzása.*
