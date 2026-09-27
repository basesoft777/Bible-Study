# KARB_KB0_kiindulas.md — Kiindulási mérés (KARBANTARTAS_BRIEF.md KB0)

Mérés dátuma: 2026.09.27. Kiinduló commit: `b980c57` (szülő: `68eb348`, a #2/CI PR #57 merge-e).

## 0.1 — `main` állapota

A menet ágának (`claude/karbantartas-brief-kb0-kb4`) kiinduló commitja `b980c57`,
amelynek szülője `68eb348`. Ez a `main`-en levő, #2 (CI) merge utáni commit — a brief
előfeltétele teljesül. A #1 (KK) ág ekkor még nincs bemergelve.

## 0.2 — Őr és argparse nélküli szkriptek (1a)

A brief szerinti 10 szkriptet ellenőrizve: mind a 10-ben nincs `if __name__ ==
"__main__"` őr:

`f3_1_betoltes.py`, `f3_2_betoltes.py`, `f3_4_ellenoriz.py`, `f3_4_elokeszites.py`,
`f3_4_gorog_ellenoriz.py`, `f3_4_join_potlas.py`, `f3_4_munkalap_general.py`,
`f3_4_nema_nemtalalat.py`, `f3_4_zaro_ellenoriz.py`, `merge_karoli_szofaj.py`.

**Friss grep — van-e még más őr nélküli, modulszinten író `eszkozok/*.py`?**
Az `eszkozok/*.py` (66 fájl) közül 12-nek nincs `__main__` szó a forrásában.
A 10 fenti mellett még kettő: `eszkozok/lexikon_general.py`,
`eszkozok/torzscikk_general.py`. Ez a két fájl azonban **nem modulszinten-író**:
a modulszintjükön kizárólag konstans-, regex- és cache-definíciók állnak
(`ROOT`, `ADAT`, `*_TSV` útvonalak, `STRONG_TOKEN_RE`, `SZAKASZOK`,
`VAZ_SABLON` stb.) és függvénydefiníciók; tényleges fájl-I/O vagy `print` a
modulszinten nincs. Ezeket a `general.py --cel lexikon` / `--cel torzscikk`
importálja könyvtárként (l. mindkettő fejléce). A brief hatóköre (1a) rájuk nem
terjed ki, és a KB1 sem nyúl hozzájuk — itt csak jelentés.

## 0.3 — Modulszinten fájlt író szkriptek a 10 közül

8 db ír fájlt modulszinten (mind, kivéve `f3_4_gorog_ellenoriz.py` és
`f3_4_zaro_ellenoriz.py`, amelyek csak olvasnak/ellenőriznek és stdout-ra írnak).
Egyezik a brief 0.3-mal.

## 0.4 — `\r`-t nem strippelő mezőbontás (1b), a 4 mért szkript

Pontos sor-ellenőrzés (a jelenlegi fájlállapot szerint):

| Szkript | Sor | Kód |
|---|---|---|
| `elofordulas_szamlalo.py` | 37 | `parts = line.rstrip("\n").split("\t")` |
| `f3_4_zaro_ellenoriz.py` | 17 | `sorok = [s.rstrip('\n') for s in f]` |
| `frazis_kereses_pozicio_alapon.py` | 58 | `parts = line.rstrip("\n").split("\t")` |
| `tahot_zarojeles_phaseA_kivonat.py` | 84 | `line = line.rstrip('\n')` |

Egyezik a brief 0.4-gyel (a sorszámok is stimmelnek).

## 0.5 — `rstrip("\n")` összesen az `eszkozok/`-ban

A jelen mérésben **36 fájl** tartalmaz `rstrip("\n")` vagy `rstrip('\n')` mintát
(a brief 0.9.25-i mérése 35-öt talált — **1 fájl eltérés**, feltehetően azóta egy új
szkript került be, vagy a mérési mód tér el kismértékben; a lista teljes egészében
elérhető, ha kell, de a brief szerint ez csak jelentés, nem javítási tétel).
A többség a KB1/KB2 hatókörén kívül esik, mert utána nem `\t`-mezőbontás jön
(pl. sima szövegsor-feldolgozás). Nem javítjuk őket — ez a brief §"Nincs benne"
és a KB2 szövege szerint is kizárt kör.

## 0.6 — `eszkozok/ellenoriz.py`

A fájl (726 sor) a menetben **nem módosul** (K2 előfeltétele). A menet nem futtatja
a szkriptet a munkapéldányban (ez a KB0 mérés csak statikus vizsgálat), így a
brief 0.6-os "RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2" számait a KB0 nem
futtatja újra ténylegesen (ehhez a szkript lefuttatása kellene, ami tilos a
munkapéldányban). A KB1/KB3 után az elfogadási feltétel (K2) azt vizsgálja, hogy
maga a fájl bájtra változatlan maradt-e a kiinduló commithoz képest — ez git
diff-fel triviálisan ellenőrizhető, és nem igényli a szkript futtatását.

## 0.7 — `Karoli_Strong_kivonat.tsv` nullázatlan sorok (1c)

A tábla 384 sorból áll (1 fejléc + 383 adatsor). Egy statikus ellenőrző szkripttel
(ideiglenes, a scratchpadban futtatva, nem a munkapéldányban módosítva semmit)
azonosítva: **26 sor, 27 token** nem "H"/"G" + négyjegyű szám alakú (3 jegyű
számok, pl. `H430`, `H776`, `H8414+H922` — az utóbbiban csak a `H922` rész
3-jegyű, a `H8414` már négyjegyű és jó). Ez pontosan egyezik a brief 0.7
számaival (26 sor / 27 token, 13 egyszerű + 13 összetett).

Az érintett igehelyek (Igehely oszlop, `Gen.x.y` alak): Gen.1.1 (×2: H430, H776),
Gen.1.2 (×2: H8414+H922, H7307+H430), Gen.1.3 (×2: H559, H216), Gen.2.7 (H127),
Gen.2.23 (H376), Gen.2.24 (H1320+H259), Gen.3.14 (H779), Gen.3.15 (H342),
Gen.4.15 (H226), Gen.6.2 (×2: H1121+H430, H1323+H120), Gen.7.11 (H699+H8064),
Gen.7.23 (H7604+H389), Gen.9.12 (H226), Gen.9.20 (H376+H127 — 2 rossz token egy
sorban), Gen.9.25 (H779), Gen.9.26 (H430+H8035), Gen.11.1 (H8193+H259),
Gen.13.16 (H6083+H776), Gen.14.18 (H410+H5945), Gen.15.6 (H539), Gen.16.13
(H410+H7210), Gen.16.14 (H883).

## 0.8 — A Károli-tábla olvasói

A 6 olvasó szkript ugyanaz, mint a brief szerint: `f3_4_elokeszites.py`,
`f3_4_join_potlas.py`, `f3_4_zaro_ellenoriz.py`, `merge_karoli_szofaj.py`,
`f4_0c_korut_ellenoriz.py`, `inline_strong_megjelenito.py`. Élő eszköz
(`general.py`, `lekerdez.py`, `jelolt.py`, `betolt.py`, `ellenoriz.py`) egyik sem
olvassa a táblát — grep-pel megerősítve.

## 0.9 — CI a `main`-en

A workflow: `.github/workflows/ellenorzes.yml` (`ellenorzes` job), lépések:

1. Diff-alap/fej meghatározás (`valtozott_fajlok.txt`).
2. **E2–E16** (`eszkozok/ellenorzes/futtat.py`) — a `SZABALYOK_FUGGVENYEI` szótár
   E2, E3, E4, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15 szabályokat futtatja
   (E5 külön, `e5_tartalomvesztes_or`; E16 az önmódosítás-ellenőrzés). Ezek a
   szabályok jellemzően **tanulmány (.md) fájlok tartalmát** vizsgálják:
   proveniencia-jelölés, igehely-formátum, angol kifejezések study-szövegben,
   `spirit`/`lelek` következetesség, Crémer-átírás, kiejtés-hiány, SZPA-idézet
   hossz stb. Egyik szabály sem vizsgálja kifejezetten a `.py` fájlokat vagy a
   `konkordancia/*.tsv` tartalmát tartalmi szempontból — a jelen menet
   változtatásai (13 `eszkozok/*.py`, `Karoli_Strong_kivonat.tsv`, `naplok/KARB_*`)
   ezért **nem várhatóan** váltanak ki E2–E15 találatot.
   E16 (`e16_ellenorzo_onmodositas`) csak akkor jelez, ha a PR érinti magát az
   ellenőrző eszközt (`ONMODOSITAS_MINTAK`) — a menet ezt nem érinti.
3. **E1** (`eszkozok/ellenoriz.py --study`, mindig fut) — csak a
   `study_fajlok_szurese.py` által "study"-nak minősített, változott fájlokra fut.
   A menet egyetlen study-fájlt sem módosít (csak `.py`, `.tsv`, `naplok/`,
   `KARBANTARTAS_BRIEF.md`, `FELADATOK.md`), ezért az E1 bemenete várhatóan üres
   lista, ami RENDBEN-nel zár.
4. PR-komment lépés (`pr_komment.py`) és a záró "Bukás, ha E1 vagy E2-E16 HIBA-t
   jelzett" lépés.

**Következtetés:** a jelen menet változtatásai a CI egyik szabályát sem érintik
tartalmilag — a CI-nek zöldnek kell maradnia. (A tényleges zöld/piros eredményt a
PR megnyitása utáni CI-futás adja; ezt a KB4 jelentés dokumentálja, de a KB4
ezen menetben nem várja meg a CI-t — l. a chat külön utasítása.)

---

*Módszertani megjegyzés:* a KB0 mérés kizárólag statikus (grep, fájlolvasás) volt;
egyetlen `eszkozok/*.py` szkript sem futott a munkapéldányban (G4). A Károli-tábla
nullázatlan sorainak azonosítása egy ideiglenes, csak-olvasó Python-szkripttel
történt, amely a scratchpad könyvtárban futott és a munkapéldány egyetlen fájlját
sem módosította.
