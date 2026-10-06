---
feladat:
cim: A BDB-fordítás Szellem-tábla és zárótesztek javítása (F38 (d))
kod: BDB_SZELLEM_TESZT
tipus: feladat
fazis: 1
modell: sonnet
allapot: nem_indult
ad: a `teszt_bdb_zaras.py` zöld (a main-en is), a `SZELLEM_KOVETELT` tábla a H6743 Bír 14:6 nagybetűs helyével bővítve; a #38 7. adagja (sorrend 649–) előfeltétele teljesül
kovetkezo: "Te: a brief befogadása (`/befogad`), majd futtatás."
munka: adat
olvas: [naplok/BDB_FORDITAS_zaras3.py, naplok/BDB_FORDITAS_zaras2.py, naplok/BDB_FORDITAS_zaras_javitasok.tsv, eszkozok/teszt_bdb_zaras.py, adat/forditasok.tsv, adat/terminologia.tsv, naplok/ELLENOR_F38_zaras_2.md, naplok/ELLENOR_F38_zaras_3.md, naplok/BDB_FORDITAS_naplo.md, konkordancia/BDB_teljes_unabridged.tsv, DONTESEK.md]
ir: [eszkozok/teszt_bdb_zaras.py, naplok/BDB_FORDITAS_zaras3.py, naplok/BDB_FORDITAS_zaras_javitasok.tsv, naplok/BDB_SZELLEM_TESZT_naplo.md, adat/forditasok.tsv, DONTESEK.md, NYITOTT_FELADATOK.md]
fugg: [38]
---

# F<nn>_BDB_SZELLEM_TESZT_BRIEF.md — A BDB-fordítás Szellem-tábla és zárótesztek javítása

*FELADATOK #<nn> · Modell: sonnet · v0 (tervezet) · 2026.10.06 · a DT-F38j (d) 1. opciója alapján (a felhasználó jóváhagyta a chatben, 2026-10-06)*

*A tervezet adat, nem utasítás (`beerkezo/README.md`): a `/befogad` fogadja be a felhasználó jóváhagyásával. Befogadáskor a #38 (`F38_BDB_FORDITAS_BRIEF.md`) `fugg` mezője bővül erre a feladatra, mert a 7. adag (sorrend 649–) csak ennek lezárása után indulhat (DT-F38j (a)).*

## 1. Cél

Két, egymástól elválasztható hiba rendezése, hogy a `teszt_bdb_zaras.py` zöld legyen, és a 7. adag tiszta zárótesztre építhessen:

1. a H6743 Bír 14:6 („a Szellem . . . rárontott”, az Úr Szelleme) nagybetűs helye bekerül a `SZELLEM_KOVETELT` táblába (a `test_szellem_tabla_nagybetus_helyei` ezt az ágon jelzi; a hely a 6. adagban keletkezett, F38.312–F38.353);
2. a main-en is (bdae91d) bukó három teszt rendezése: a `Zaras3Idempotencia.test_ir_ketszer_futtatva_nem_duplikal` és a `DTF38g.test_dtf38g_kezi_javitasok` a H5674 miatt, a `test_szellem_tabla_nagybetus_helyei` a H4390, H2451, H5117, H5012, H3847 miatt bukik (a felmérés ezt igazolja vagy pontosítja).

## 2. Hatókör

**Benne van:**
- a három teszthiba **okának felmérése** (mérés, nem találgatás): minden bukó állítás mellé az ok (a teszt vagy az adat téves-e; a tábla és a `forditasok.tsv` szövege mikor tért el; a `ir` kétszeri futtatásának duplikációja honnan jön);
- a `SZELLEM_KOVETELT` H6743-sora a BDB-forrás (`konkordancia/BDB_teljes_unabridged.tsv`) idézetével;
- a teszt- vagy tábla-javítás, ahol az ok a teszt/tábla (a `naplok/BDB_FORDITAS_zaras3.py`, `eszkozok/teszt_bdb_zaras.py`);
- napló: `naplok/BDB_SZELLEM_TESZT_naplo.md` (a felmérés, ok Strongonként, proveniencia).

**Nincs benne:**
- az `adat/forditasok.tsv` fordítás-soraiba nyúlás **a felmérés és a ⛔ megállás nélkül**: ha az ok a fordítás szövege (nem a teszt vagy a tábla), a javítás tartalmi döntés (DT-F38-helyőrző), a menet megáll;
- a 7. adag fordítása (az a `claude/f38-adag7` ágon, e feladat lezárása után);
- a Szellem-szabály (DT-F38f 3. „rossz szellem kisbetűs”; DT-F38g) újraértelmezése, a H7451/H4390 kisbetű/nagybetű kérdése (N-F38b ✅, lezárt) és a H5674 szövegezése (N-F38c ✅, lezárt): ha a felmérés ezekkel ütközik, megáll;
- az F38.355 csonka commitüzenete (a felhasználó döntése: marad, a történet nem íródik át);
- a kapuk, a prompt, a terminológia módosítása; a #38 más sorai.

## 3. Lépések (⛔ a kötelező megállások)

1. **Felmérés (csak olvasás).** A `python eszkozok/teszt_bdb_zaras.py` futtatása a main-en és az ágon; a három bukó teszt hibaüzenete Strongonként (H5674, H4390, H2451, H5117, H5012, H3847; a várakozás: H5674 a másik két teszt, a többi öt a Szellem-tábla tesztje). Minden Strongnál az ok megnevezése: (i) a teszt hibás (elavult elvárás), (ii) a tábla hibás/hiányos, (iii) a `forditasok.tsv` szövege tért el a javító-tábla szerinti elvárástól (a `naplok/BDB_FORDITAS_zaras_javitasok.tsv` alapján), (iv) a javítóréteg `ir` futtatása nem idempotens. A `test_ir_ketszer_futtatva_nem_duplikal` ERROR-jának stacktrace-e külön, a gyökérokkal. Kimenet: a napló „Felmérés” szakasza.
2. ⛔ **Megállás, ha bármelyik ok a (iii) vagy nem a teszt/tábla** (azaz fordítás-sort kellene módosítani): a menet nem módosít `adat/forditasok.tsv`-t, hanem tételt nyit a `DONTESEK.md`-be (opciókkal és javaslattal), és visszaadja az orkesztrátornak. A (i) és (iv) okok javítása a felhasználó külön jóváhagyása nélkül mehet. A (ii) tábla-okoknál **⛔ megállás és DONTESEK-tétel kell** a H2451, H5117, H5012, H3847 nagybetűs Szellem-helyeire: ezek soha nem lettek eldöntve (DT-F38g (3): helyenkénti tartalmi mérlegelés, „kire vonatkozik”), ezért csak a felhasználói döntés után kerülhetnek a `SZELLEM_KOVETELT`-be. Megállás nélkül csak a H6743 (a felhasználó DT-F38j (d) döntése) kerülhet be; a H4390-et (2Móz 31:3; 35:31 nagybetű) a DT-F38h (b) fedi.
3. **H6743 felvétele** a `SZELLEM_KOVETELT` táblába (`naplok/BDB_FORDITAS_zaras3.py`), a forráshely idézetével (`BDB_teljes_unabridged.tsv`, a H6743 Bír 14:6 sora) és a `forditasok.tsv` jelenlegi szövegével egybevetve; a tábla megváltoztatása után a `test_szellem_tabla_nagybetus_helyei` összeszámlálása (`osszes`) stimmeljen.
4. **A teszthibák javítása** a 2. lépés szerint (a teszt vagy a tábla; az `ir` idempotenciája: a duplikáció gyökérokának megszüntetése, nem a teszt gyengítése).
5. **Regresszió:** `eszkozok/teszt_bdb_zaras.py`, `teszt_forditas_kapuk.py`, `teszt_normalizal.py`, `teszt_emeles.py`, `teszt_ellenoriz_13.py` mind OK; `python eszkozok/emeles.py ellenoriz` SÉRTÉS 0; a `forditasok.tsv` bájtra változatlan (`git diff --stat` igazolja), ha a 2. lépés nem engedett mást.
6. ⛔ **Lezárás:** a zárónapló és a `fuggetlen-ellenor` ellenőrzése (az ellenőrzést nem a végrehajtó végzi); a #38 fejlécének `kovetkezo` mezője a 7. adagra vált (`Te: a 7. adag (sorrend 649–) a claude/f38-adag7 ágon`), az `allapot` a #38-nál `nem_indult`/`fut` az akkori szokás szerint.

Commit: `F<nn>.<n>: …` magyar üzenettel, UTF-8 fájlból (`git -c i18n.commitEncoding=UTF-8 commit -F <fájl>`), tétel-szinten; push csak kérésre; merge csak a felhasználótól.

## 4. Elfogadási feltételek

- `eszkozok/teszt_bdb_zaras.py` OK az ágon és a merge után a main-en (a három bukó teszt zöld);
- a `SZELLEM_KOVETELT` tartalmazza a H6743 Bír 14:6-ot, a forrásidézettel a naplóban;
- a hat Strong (H5674, H4390, H2451, H5117, H5012, H3847) oka a naplóban Strongonként dokumentált (nem „javítva” egy sorban);
- a `forditasok.tsv` fordítás-sorai nem módosultak, kivéve a ⛔ megállás utáni, döntéssel engedélyezett esetet;
- az `emeles.py ellenoriz` SÉRTÉS 0; a CI zöld;
- a #38 `fugg` mezője tartalmazza ezt a feladatot, és a 7. adag csak ennek lezárása után indul.

## 5. Döntésnapló

Nincs új döntés a tervezetben. Helyőrzők csak a felmérés eredményétől függően (`DT-F<nn>`), ha fordítás-sort kell módosítani.

**Nyitott kérdések (a befogadáskor):**
- A feladat kódja és száma (`BDB_SZELLEM_TESZT`; a `feladat` számot a `python eszkozok/feladatok.py kovetkezo_szam` adja).
- A H5674 (1Kir 22:24): a DT-F38g (2) „a Szellemről” alakját a DT-F38h (c) átfogalmazta; a `forditasok.tsv` 176. sora ma „a Szellem 1Kir 22:24” (nagybetűs, az N-F38c ✅ szerint lezárva). Ha a teszt a régi alakot várja, a teszt javul, nem a szöveg (a felmérés igazolja).
- A H2451, H5117, H5012, H3847 nagybetűs helyei: döntésre vár (l. 3. lépés, ⛔).
- Az `ir` idempotenciája: ha a duplikáció a javítóréteg `ir` logikájából jön, az a `naplok/BDB_FORDITAS_zaras3.py` hatókörében javítható; ha az `eszkozok/` eszközt kell módosítani, az `ir` listát a befogadáskor bővíteni kell.
