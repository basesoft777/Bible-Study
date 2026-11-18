---
feladat: 226
cim: Régi, helyben bukó tesztek — leltár és javítás gyökérok szerint
kod: HELYI_PIROS_TESZTEK
tipus: feladat
fazis: folyamat
modell: sonnet
sav: SYSTEMS
allapot: lezarva
ad: a helyben futó `eszkozok/teszt_*.py` tesztek bukásai besorolva (elavult teszt / kódhiba / elavult adatbázis) és gyökérok szerint javítva vagy jelentve
kovetkezo: "—"
munka: folyamat
olvas: [eszkozok/teszt_futtat.py, eszkozok/teszt_bdb_adatblokk.py, eszkozok/teszt_visszhang_kapu.py, F207_PIROS_TESZTEK_BRIEF.md]
ir: [eszkozok/teszt_bdb_adatblokk.py, eszkozok/teszt_visszhang_kapu.py]
ag: claude/f226-helyi-piros-tesztek
fugg: []
pr: 0
lezarva_osszegzes: "Leltár: 4 bukó teszt (2 visszhang-kapu, 2 bdb_adatblokk) besorolva, mind elavult teszt vagy adat/DB-állapot; kódhiba nincs, kódváltozás nincs"
---

# F226_HELYI_PIROS_TESZTEK_BRIEF.md — Régi, helyben bukó tesztek

*FELADATOK #226 · Modell: sonnet · v1 · 2026.11.18*

<!-- KOZVETLEN_FUTTATAS -->
Hajtsd végre ezt a briefet a `/kovetkezo` szerint; a ⛔ pontokon állj meg.
<!-- /KOZVETLEN_FUTTATAS -->

**Hatókör.** Az F207 mintájára: a helyben bukó tesztek gyökérok szerinti rendezése. Az F207 már megoldott tesztjeihez nem nyúlunk. Az `adat/*`, `lexikon/*`, `sablonok/*`, generált kimenetek érintetlenek.

1. **Leltár (előbb, javítás nélkül).** Friss adatbázissal (`PARDES_DB`, WSL-natív, l. memória és F207 „Futtatási környezet”) futtasd a `python eszkozok/teszt_futtat.py --gyors` parancsot, majd a többi `eszkozok/teszt_*.py` és `eszkozok/olvaso_szerver/teszt_*.py` fájlt a main-en. Táblázat a briefbe vagy `naplok/F226_naplo.md`-be: teszt · hiba szó szerinti sora · ok · besorolás (a: elavult teszt, b: kódhiba, c: elavult adatbázis/környezet).
2. **Ismert bukók:** a `teszt_bdb_adatblokk.py` két tesztje az 1.0-s adaton is bukik; a `teszt_visszhang_kapu` említve volt. Mindkettőt vizsgáld meg, ne vedd készpénznek a besorolást.
3. **Javítás csak gyökérok szerint:** elavult teszt → a teszt kijavítása (nem a feltétel gyengítése, nem kihagyás), tesztenként indoklással; kódhiba → a kódban javítandó, ha az `ir`-en belül van, egyébként jelentés; elavult adatbázis → a környezet frissítése, nem kódváltozás.
4. ⛔ **Megállás**, ha egy javítás adatot (`adat/`, `lexikon/`, `nyilt_mag/`) vagy generált kimenetet érintene, vagy az `ir`-en kívüli fájlt kellene módosítani: tétel a `NYITOTT_FELADATOK.md`-be (placeholderrel, `nyitott/uj/`), megállás.

**Kész, ha:** minden bukó teszt besorolt; a javíthatók zöldek; a többinél jelentés áll. Teszt kihagyása, `skip` vagy a feltétel gyengítése nem javítás.

## Zárás
Leltár a `naplok/F226_naplo.md`-ben. Kódhiba nem volt; a 4 bukás elavult teszt vagy adat/DB-állapot, a szűkítés miatt nem javítva. Független ellenőrzés: dokumentáció-only PR, nem futott.
