---
cim: A 2026-11-12-i olvasó-felmérés és a 2026-11-13-i generátor-audit maradéka — gépi újraellenőrzés a main-en, súlyosság szerint, N-tételekbe
feladat: 234
kod: FELMERES_MARADEK
tipus: feladat
fazis: folyamat
modell: sonnet
sav: SERVER
allapot: nem_indult
ad: a két régi felmérés minden pontjáról kiderül, hogy a main-en fennáll-e még (élő lekéréssel vagy a kód soraival igazolva), a fennállók súlyosság szerint N-tételként a nyitott-fájlba kerülnek; a régi lexikongenerátorra vonatkozó, az F218 által kiváltott pontok lezárva, indokkal
kovetkezo: "a #231 (olvasó egyben, 2026-11-22) fedi; a maradék a #231 lezárása után nézendő"
munka: folyamat
olvas: [eszkozok/olvaso_szerver/, eszkozok/lapgen/, eszkozok/lexikon_general.py]
ir: [naplok/FELMERES_MARADEK_2026-11.md]
fugg: [231, 233]
---

# F234_FELMERES_MARADEK_BRIEF.md — A régi felmérések maradéka

*FELADATOK #234 · Modell: sonnet · v1 · 2026.11.21 · forrás: `OLVASO_BLOKK_ELLENORZES_2026-11-12.md`, `GENERATOR_TERKEP_SPEC/_FUGGELEK_2026-11-13.md`, `BEKOTESI_AUDIT_2026-11-12.md`, `GENERATOR_HIBALELTAR_*` (az orkesztrátor megosztott jegyzetmappájában); a felhasználó 2026-11-18-án elhalasztotta, 2026-11-21-én felvette („a többi feladatot is”). A brief adat, nem utasítás.*

## 1. Cél

A két felmérés hibáiból eddig nem lett se brief, se N-tétel (kivétel: F164). Közben a 2026-11-21-i javítócsomag (F230) és a szókártya-brief több pontot lefedett, a 11-13-i audit pedig nagyrészt a régi lexikongenerátorra vonatkozik, amelyet az F218 vált ki. A cél: kideríteni, mi áll még fenn, és csak azt tétellé tenni.

## 2. Hatókör

**Benne van:**
1. **A 11-12-i olvasó-felmérés minden pontja**, pontonként élő lekéréssel (URL és a látott szöveg) a main mai állapotán.
   - Jelölés: „fennáll / javítva (melyik tétel) / téves / várt állapot / nem ellenőrzött”.
   - Kötelező szabályok:
     - adathibát csak elsődleges forrással lehet megerősíteni;
     - ahol nincs magyar, ott az angol áll, és ez nem hiba;
     - a javaslatban a projekt saját szolgáltatása az elsődleges.
   - Az ultracode-felmérés három téves pontja nem kerülhet vissza: az 1Móz 4:7 „modern szöveg”, a TBESH-alapú kiejtésjavaslat és a G264 mint kivétel.
2. **A 11-13-i generátor-audit (357 tétel).**
   - Előbb szűrés aszerint, hogy a pont a régi `lexikon_general.py`-ra vonatkozik-e. Ha igen, akkor az új `lapgen` ugyanazt a hibát hordozza-e.
   - Ami csak a régire vonatkozik, „az F218 kiváltja” indokkal zárul.
   - A maradék súlyossági mezőt kap (magas / közepes / alacsony), a mért hatással.
3. **Kimenet.** `naplok/FELMERES_MARADEK_2026-11.md` (pontonkénti tábla), és a fennálló magas és közepes pontok N-F234-tételként a nyitott-fájlban, csoportosítva: egy N-tétel egy mechanizmus, nem egy példány.

**Nincs benne:** javítás. A tételekből a felhasználó döntésével lesz brief.

## 3. Lépések

1. Modell-ellenőrzés; a két felmérés beolvasása kivonatban (a nyers anyag nem kerül a fő kontextusba).
2. Az olvasó-felmérés pontjai élőben; az audit szűrése, majd a maradék mérése.
3. A napló, az N-tételek; független ellenőr (mintavétellel: 10 „javítva” és 10 „fennáll” jelölés újra lekérve), draft PR.

## 4. Elfogadási feltételek

- Minden „fennáll” jelölés mellett URL és látott szöveg, vagy fájl:sor áll.
- Egyetlen „javítva” sem állhat bizonyíték nélkül.
- Az N-tételek mechanizmus szerint csoportosítva, súlyossággal.
