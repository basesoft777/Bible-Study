---
feladat: 196
cim: Gyökérok-kapuk — állítás–adat kapu és követelménylista-kapu, JELENTÉS szinten
kod: GYOKEROK_KAPUK
tipus: feladat
fazis: folyamat
modell: opus
allapot: lezarva
lezarva_osszegzes: állítás–adat kapu és követelménylista-kapu JELENTÉS szinten; a HIBA-szintre emelés (DT771) külön döntés: N165
ag: claude/gyokerok-kapuk-a1d120
pr: 689
ad: két gépi kapu a visszatérő laphibák gyökérokára — a lap számai és „nincs …” mondatai a saját adatukhoz mérve; a kész lap követelménylistájának gépi sorai „N/M követelmény teljesül (gépi)” összegzéssel a CI-ben; mindkettő JELENTÉS
kovetkezo: "lezárva; a PR #689 a main-en"
munka: folyamat
olvas: [sablonok/KESZ_LAP_KOVETELMENY.md, eszkozok/lexikon_general.py, eszkozok/olvasoi_kovetkeztetes.py, eszkozok/olvasoi_kapu.py, eszkozok/ellenoriz.py, eszkozok/ellenorzes/szabalyok.py, .github/workflows/ellenorzes.yml]
ir: [eszkozok/ellenorzes/allitas_adat.py, eszkozok/ellenorzes/kovetelmeny_kapu.py, eszkozok/teszt_gyokerok_kapuk.py, .github/workflows/ellenorzes.yml, naplok/F196_jelentes.md, naplok/ELLENOR_F196.md, dontesek/uj/gyokerok-kapuk-a1d120.md, nyitott/uj/gyokerok-kapuk-a1d120.md, F196_GYOKEROK_KAPUK_BRIEF.md]
fugg: []
---

# F196_GYOKEROK_KAPUK_BRIEF.md — Gyökérok-kapuk

*FELADATOK #196 · Modell: opus · v1 · 2026.11.11*

**Jóváhagyás (a felhasználó, 2026-11-11, szó szerint).** A leírás: „A gyökérok-kapuk: gépi ellenőrzések, hogy ne maradjon ennyi hiba sok kör után. Az egyik az állítás–adat kapu: a lap minden számát és »van/nincs« mondatát az adatához méri … A másik a követelménylista sorai kapuként, hogy a CI kiírja, hány teljesül.” A válasz: „ezeket csináljuk”.

**Indok.** A visszatérő laphibák egyik gyökéroka, hogy a kapuk a formát ellenőrizték, az igazságot nem: a HAMART-001 lapon „A motívumhoz nincs rögzített kapcsolat.” állt, miközben a `kapcsolatok.tsv` 56 sort tartalmazott. Ez a tétel a generátor-kör (ütemezés 3. pont) három tételéből kettőt hoz előre. A HAMART #183 párhuzamosan a generátort írja, ezért a kapuk JELENTÉS-szinten indulnak, és a generátorhoz nem nyúlnak.

**Hatókör.** Nem nyúl: `lexikon/`, `eszkozok/lexikon_general.py`, `eszkozok/visszhang/`, `sablonok/` (a követelménylistát csak olvassa), `adat/` (a SEMA 3.11 generált kapulistáját sem), a `DONTESEK.md` meglévő sorai.

## Teendő

1. **Állítás–adat kapu** (`eszkozok/ellenorzes/allitas_adat.py`). A lap (`lexikon/[ID]_TUDOMANYOS.md`) és a melléklete (`[ID]_KIZARASOK.md`) látható szövegéből egy állítás-katalógus mintái kiveszik a számokat és a „nincs …” mondatokat, és az adatkulcsukhoz mérik: igehely- és versszám, könyvek, ÓSZ/ÚSZ, Kivonat-bontás; a Döntési út számai és okonkénti sorai; a 3. szakasz vizsgált és döntött versei; a kapcsolat-sorok (összes, csomópont, típus, bizonyosság); a motívumközi kapcsolatok; az LXX egyező, eltérő, hiányzó és nem megállapított versei; a 4.13 és a 4.14 számai; a melléklet összegei, okonkénti címsorai és felsorolt versei (tagonként); a generátor minden „nincs …” hiánymondata (a kulcsnak 0-nak kell lennie). Az adat a generátor saját függvényeiből jön, ahol önálló függvény van (`dontesi_ut_adat`, `kizarasok_adat`, `lxx_osszevetes`, `karoli_szavankent`, `kapcsolatok_sorok`, `szerep_kizart.vizsgalt_versek`, `szerep_karoli.*`); ahol a szám blokkfüggvényen belül születik, a kapu ugyanazt a számolást végzi, megjelölve (`SAJAT_SZAMOLAS`, N165).
2. **Követelménylista-kapu** (`eszkozok/ellenorzes/kovetelmeny_kapu.py`). A `KESZ_LAP_KOVETELMENY.md` K-sorainak „Ellenőrzés” cellájából felismeri a gépi szabályt (olvasói kapu-azonosító, VISSZHANG V1–V7, `ellenoriz.py` N., CI E-szám), lefuttatja az adott lapra, és kiírja: „HAMART-001: N/M követelmény teljesül (gépi)”, a nem teljesülő sorok listáját, a HAMART-nál a lista „HAMART-állapot” oszlopával való eltérést; „ember ellenőrzi” a lektor/szerkesztő/nincs/tervezett sor; „gépi, a kapu nem gyűjti” a gépi, de nem futtatható sor. Az E28 csak `--e28`-cal fut (perceket vesz igénybe).
3. **CI** (`.github/workflows/ellenorzes.yml`): új, nem bukó jelentés-lépés (a két kapu kimenete a Step Summary-ba), és a tesztfájl a „Szabaly-tesztek” lépésben.
4. **Tesztek** (`eszkozok/teszt_gyokerok_kapuk.py`): áladatos esetek (a gyökérok-példa, a nem mérhető ≠ egyezés, az alcím szerinti ok, a melléklet tagonként, a cella-felismerés) és a valódi HAMART-001 egy rontott másolaton.
5. **Próba** a HAMART-001-en és az ISTENTISZT-001-en, eredmény: `naplok/F196_jelentes.md`.
6. Döntések helyőrzővel (`dontesek/uj/gyokerok-kapuk-a1d120.md`), nyitott tételek (`nyitott/uj/gyokerok-kapuk-a1d120.md`).

## Garanciák és döntési napló

- G1: a diff csak a fenti `ir` fájlokat érinti.
- G2: a két kapu kilépési kódja JELENTÉS-szinten 0; a `--szigoru` (később) 1-et ad eltérésnél.
- G3: a kapu az adatot nem tölti ki: a nem számolható adatkulcs „nem mérhető”, nem egyezés; a lapon nem álló állítás nem mér.
- G4: TSV-olvasás a `general.tsv_beolvas`-on át (`split('\t')`), UTF-8 wrapper minden új szkriptben.
- D1 (DT772): E-szám nélkül, önálló szkriptként fut, mert az E-szám a `adat/SEMA.md` 3.11 generált kapulistáját írná (E37), az `adat/`-hoz pedig ez a menet nem nyúl (ugyanígy indult az F188 T2 SZAMISMETLES).
- D2 (DT771): a HIBA-szintre emelés a HAMART-001 kiadása után, külön döntéssel.
- ⛔ A merge a felhasználóé.
