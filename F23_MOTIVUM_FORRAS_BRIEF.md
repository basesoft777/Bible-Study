---
feladat: 23
cim: Egyforrású motívumdokumentum: forrássablon és mélységi szintek (terv)
kod: MOTIVUM_FORRAS
tipus: feladat
fazis: 1
modell: opus
allapot: megallt
ag: claude/f23-motivum-forras
ad: a B szerkezet terve mérésekkel: szakasz-leképezés, forrássablon-tervezet, szintjelölés a SEMA-ban, CI-szabályok leírása; renderelés és fájlmozgatás nélkül
kovetkezo: "Te: ⛔ az M0 kész (naplok/MOTIVUM_FORRAS_*.tsv); döntés a DT-F23a-ról (javaslat-besorolások, sablonszabaly érték, ⭐-küszöb eltérés: KIRALY-001, MENNY-001, HODIT-001). M1 várja: #12a próza-próba (DT-F32a); utána /kovetkezo"
olvas: [sablonok/, tematikus_lezart/, motivumok/, lexikon/, genezis/, adat/SEMA.md, adat/res_forras.tsv, eszkozok/general.py, CLAUDE.md, ATALAKITASI_TERV.md.md, ADATVAGYON_TERV.md, MUNKATERV.md]
ir: [sablonok/9_PaRDeS_motivum_forras_sablon.md, adat/SEMA.md, naplok/MOTIVUM_FORRAS_lekepezes.tsv, naplok/MOTIVUM_FORRAS_torzscikk_egyedi.tsv, naplok/MOTIVUM_FORRAS_parositas.tsv, naplok/MOTIVUM_FORRAS_naplo_keveredes.tsv, naplok/MOTIVUM_FORRAS_atfedes.tsv, naplok/MOTIVUM_FORRAS_M0.py, naplok/F23_zaras.md]
fugg: [32]
nem_fugg: [22, 52]
---

# F<nn>_MOTIVUM_FORRAS_BRIEF.md — Egyforrású motívumdokumentum: forrássablon és mélységi szintek (terv)

*FELADATOK #<nn> · Modell: opus · v1.4 · 2026.10.05 · döntések: D34–D39 (a naplózó brief rögzíti; a számok a befogadáskor a következő szabad D-számtól csúszhatnak), DT28 (v1.3)*

## 1. Cél

A 2026.09.30-i döntés (D34, „B” út): motívumonként **egyetlen kézi forrás** legyen (`motivumok/[ID].md` + adattáblák). A tematikus sablon adja a szerkezetét. A tematikus tanulmány, a lexikonoldal és minden olvasói nézet ebből **generálódik**, állítható mélységgel. A törzscikk megszűnik.

**Próza-elsőbbség (F32 KONTEXTUS, K1/2).** A `motivumok/[ID].md` összefüggő érvelés markerekkel, amelyekből a generátor kinyeri az adatot; nem adatséma, amelybe prózamezők vannak beszúrva. Az `adat/SEMA.md` a kinyerést írja le, nem a dokumentum szerkezetét; a forrássablon szakaszsorrendet és markereket adhat, mezőhatárokat nem. Az M1 forrássablon **tervezet marad** addig, amíg a KONTEXTUS K1/4 szerinti próba (egy motívum teljes értelmező rétege, az ISTENTISZT-001 mércéjével) le nem futott; a próba helyéről a `DONTESEK.md` DT-F32a tétele dönt. Az M1 terve ezt a feladatot (#32) megelőzően nem indulhat (`fugg: [32]`). **A DT-F32a döntése (Felhasználó, 2026.10.04):** a próba a #12 első fele (**#12a próza-próba**), amely a #23 M0 után és az M1 előtt fut, éles render nélkül (csak `generalt_proba/`); az M1 ezért a #12a eredményét várja (lásd az M0 ⛔ megállását és az M1 előfeltételét). A függés a fejlécben nem rögzíthető számmal, mert a #12a még nem önálló feladat (a #12 kettéválasztása `/befogad` tétel); addig a fejléc `kovetkezo` mezője és ez a szakasz hordozza.

**Egyirányúság (DT28, Felhasználó, 2026.10.05; `CLAUDE.md` „Egyirányúság”, `adat/SEMA.md` 3/9).** Három réteg van, és minden fájl — a B szerkezetben minden szakasz — pontosan egybe tartozik: (a) kanonikus adat (`adat/*.tsv`); (b) kézi próza-forrás markerekkel (`motivumok/[ID].md`); (c) generált kimenet. Az adat csak (b)→(a) irányban mozog (kinyerés a `jeloltek.tsv`-n át, `manual` provenienciával, döntéssel) és (a)→(c) irányban (generálás). (a)→(b) visszaírás nincs. A régi tanulmány, amelyben a motívumadat a prózában áll, egyszerre (a) és (b); a migrációja (#11) **szétválasztás**, nem visszaírás. Ebből a feladatnak három következménye van: a forrássablon a (b) réteg markereit adja meg, és minden markerhez kimondja, mit nyer ki belőle a generátor (M1/1); a SEMA-alfejezet a kinyerést írja le, a 3/9 szabályra építve (M1/2); a pilot-bemenetek a migrációt a szétválasztás kategóriáival mérik (M1/4).

Ez a feladat csak **tervez és mér**. Semmit nem renderel, nem mozgat, és nem ír át meglévő tanulmányt vagy lexikonoldalt. Ezért fér bele a D1 szerinti 1. fázisba: metaadat és séma, amely nem függ a késői forrásoktól. Az eredményére a #9, a #12 és a #11 épít.

## 2. Hatókör

**Benne van:** az M0 felmérés (csak olvas); a forrássablon tervezete; a szintjelölés szabálya a `adat/SEMA.md`-ben; két CI-szabály **leírása** (nem implementálása); a két pilot bemenetének leírása.

**Nincs benne:** a `general.py` módosítása; bármely `tematikus_lezart/`, `motivumok/`, `lexikon/` vagy `genezis/` fájl írása; a `CLAUDE.md` rétegtáblájának átírása (az a #11 dolga); a CI-szabályok implementálása (külön ágon, D6); HTML; a forrásdokumentum mezőkre bontása; a szakaszok külön feladatra vagy író subagentre osztása (F32 K1/1–2).

## 3. Lépések

### M0 — felmérés (csak olvas) ⛔ utána megállás

Minden számot a menetben ténylegesen futtatott parancs kimenetéből vegyél. Becsült vagy emlékezetből vett szám nem kerülhet a naplóba.

1. **Szakasz-leképezés.** Vedd sorra a `sablonok/4_PaRDeS_tematikus_sablon.md`, a `6_PaRDeS_lexikon_oldal_sablon.md` és a `8_PaRDeS_torzscikk_sablon.md` minden szakaszát, a `motivumok/[ID].md` blokkjait és az `adat/res_forras.tsv` réseit. Kimenet: `naplok/MOTIVUM_FORRAS_lekepezes.tsv`, oszlopok:
   `szakasz` · `sablon` · `ma_hol_el` · `B_helye` (`kezi_forras` / `adat` / `generalt`) · `szint` (`olvasoi` / `apparatus` / `belso`) · `aktivalas` (mindig / feltételes: mi a feltétel) · `megjegyzes`.
   `kezi_forras` besorolásnál a `szint` megadása kötelező, és a `megjegyzes` rögzíti, hogy a szakasz az összefüggő érvelés része, nem önálló mező (F32 K1/2).
   A `B_helye` **egyetlen** érték (DT28): egy szakasz nem lehet egyszerre `kezi_forras` és `adat`. Ha ma egy szakasz mindkettőt hordozza (adat a prózában), a `B_helye` a célréteg, és a `megjegyzes` `szetvalasztando` jelölést kap: mi megy az adatrétegbe, mi marad próza.
   Ha egy szakasz besorolása nem egyértelmű, `javaslat` jelölést kap, és az összesítő tételbe kerül.
2. **Csak a törzscikkben létező tartalom.** Motívumonként vesd össze a `lexikon/[ID]_TORZSCIKK.md`-t a `_TUDOMANYOS.md`-vel és a forrásokkal. Van-e olyan állítás vagy adat, amely csak a törzscikkben szerepel? Kimenet: `naplok/MOTIVUM_FORRAS_torzscikk_egyedi.tsv` (motívum, szakasz, szöveg-kivonat legfeljebb 15 szóban, hol kellene élnie). Az üres eredmény elfogadható, de jelölni kell.
3. **Tematikus tanulmányok és motívumok párosítása.** Melyik `tematikus_lezart/*_tematikus.md` melyik motívum-ID-hez tartozik, melyik motívumnak nincs tematikus tanulmánya, és melyik fájl nem tanulmány (pl. ellenőrző jegyzet)? Kimenet: `naplok/MOTIVUM_FORRAS_parositas.tsv`.
4. **NAPLO-keveredés.** Fájlonként számold meg a `tematikus_lezart/` és a `motivumok/` fájlokban:
   - a `【NAPLO: …】` blokkokat;
   - a gyanús, mondaton belüli proveniencia-szöveget: dátum, fájlnév, „l. X pont”, „felismerve / visszaírva / audit során”.

   Ez a migráció (#11) szintjelölési munkájának becslése, és egyben a DT28 mércéje: mennyi (a)-rétegű adat ül ma a (b)-rétegű prózában, vagyis mekkora a szétválasztandó anyag. Kimenet: `naplok/MOTIVUM_FORRAS_naplo_keveredes.tsv`.
5. **Átfedés a bővített tanulmányokkal.** Keress szó szerinti vagy közel szó szerinti bekezdés-átfedést a `genezis/*_bovitett.md` és a `tematikus_lezart/` fájlok között. A módszert (pl. 8 szavas n-gram) a naplóban rögzítsd. Ez mutatja, hol kell a forrásnak hivatkoznia másolás helyett (D34). Kimenet: `naplok/MOTIVUM_FORRAS_atfedes.tsv`.
6. **Összesítés és ⛔ megállás.** Egy `DONTESEK.md`-tétel: a `javaslat` jelölésű besorolások, a 2–5. pont fő számai, és a kérdés, hogy mehet-e az M1. Menet közben máshol ne állj meg (D19). **Az M0 után az M1 akkor sem indul, ha a tétel jóváhagyott:** a DT-F32a szerint előbb a #12a próza-próba fut le (Opus-brief, `generalt_proba/`, éles render nélkül), és az M1 az ő eredményét veszi bemenetként. A #23 menete ezen a ponton megáll, és ezt jelzi a zárásban: „M1 várja: #12a”.

### M1 — terv (a jóváhagyás után)

**⛔ Előfeltétel (DT-F32a, K1/4):** az M1 csak a #12a próza-próba eredményének ismeretében kezdhető: egy motívum teljes értelmező rétege a KONTEXTUS-szabályok szerint elkészült, és az eredmény az ISTENTISZT-001 mércéjét (L1–L5, #10) hozza. Ha a #12a még nem futott le, az M1 nem indul; állj meg, és add vissza a kérdést az orkesztrátornak.

1. **Forrássablon-tervezet:** `sablonok/9_PaRDeS_motivum_forras_sablon.md`. Szakaszonként:
   - kézi vagy adatból generált;
   - mélységi szint;
   - aktiválási feltétel.

   A tematikus szakaszok a ⭐ küszöb (`COUNT(DISTINCT fo_elofordulas)`) alatt inaktívak (D37), ugyanúgy, ahogy ma a 0. és az 1/b szakasz is feltételes. A sablon fejlécében álljon: „tervezet, a #12 pilotja véglegesíti”.
   **Markerek (DT28):** a sablon megnevezi a (b) réteg markereit (a meglévő `RÉS-KEZDET` / `GENERÁLT-KEZDET` jelölők mintájára), és minden markerhez kimondja, **mit nyer ki belőle a generátor** és **melyik adattáblába** (pl. igehely-lista → `jeloltek.tsv`, nem közvetlenül `elofordulasok.tsv`: SEMA 3/2). Marker, amelyből semmit nem nyerünk ki, csak szerkezeti. Egyetlen marker sem jelent visszaírást: a generátor a forrásba nem ír, az adatból a forrásba semmi nem kerül vissza. A tematikus sablon v16 szabályai (pl. a BDB-jelentés oszlop magyarul) változatlanul átkerülnek. Ha egy szabály nem fér bele, `javaslat` jelölést kap.
2. **Szintjelölés a `adat/SEMA.md`-ben:** új alfejezet.
   - Három szint: `olvasoi`, `apparatus`, `belso`.
   - A jelölés blokkszintű, és gépileg olvasható. A jelölő alakját te javasold, a meglévő `RÉS-KEZDET` / `GENERÁLT-KEZDET` jelölők mintájára.
   - A `【NAPLO】` mindig `belso`.
   - A nyilvános nézet engedélyezőlistával válogat, a `belso` réteget buildkor kihagyja, nem rejti el (D36).
   - A D35 szabálya (a generált fájlba kézzel nem írunk) a DT28 óta a SEMA 3/9 integritási szabályban áll; az alfejezet nem ismétli, hanem hivatkozza, és a kinyerés leírásával egészíti ki: markerenként melyik tábla, milyen kulccsal, milyen provenienciával (`forras=manual` a kézi prózából kinyert sornál, SEMA 1.5). Az alfejezet a (b)→(a) irányt írja le; (a)→(b) út nincs.
3. **CI-szabályok leírása** a `naplok/MOTIVUM_FORRAS_ci_terv.md`-ben, a következő szabad E-számmal:
   - (a) az újragenerált nézet bájtazonos a commitolttal;
   - (b) a nyilvános kimenetben nulla `belso` jelölés és nulla `【NAPLO` található.

   Csak leírás. Az implementáció külön ágon megy (D6), a #11 előtt.
4. **Pilot-bemenetek** a `naplok/MOTIVUM_FORRAS_pilot_terv.md`-ben (D38):
   - mit kell tudnia a #12-nek (TEREMT-002, natív);
   - mit kell tudnia a #11 1. lépcsőjének (ISTENTISZT-001, örökölt);
   - milyen nulla-diff vagy elfogadott-diff kategóriákkal mérjük a migrációt;
   - a szétválasztás kategóriái (DT28): a régi tanulmány minden bekezdése egy célrétegbe kerül — `adat` (kinyerve a `jeloltek.tsv`-n át, döntéssel), `forras` (értelmező próza, marad a `motivumok/[ID].md`-ben), `generalt` (ma a forrásban áll, de adatból újraállítható: a migráció után nem kézi), `archivum` (egyik sem; megőrzött, de nem forrás). A pilot akkor sikeres, ha nincs bekezdés két rétegben, és a visszaírás-számláló nulla: egyetlen sor sem került az adatból a forrásba.

## 4. Munkaszabályok

1. **Csak olvas az M0-ban.** Egyetlen meglévő tartalmi fájl sem változik a menetben. Írni csak a 3. pontban felsorolt új fájlokat és a `adat/SEMA.md` új alfejezetét lehet.
2. **⛔ megállás az M0 után** (az M1 a #12a eredményéig vár, DT-F32a), és ha egy meglévő tartalmi fájl nem szándékolt módosulását észleled.
3. **A számok a futtatott parancsokból jönnek**, eltérésnél a fájl az irányadó. Ahol nincs mérés, ott „nincs mérés” áll, nem becslés.
4. **Motívumszintű `ir`:** ez a feladat egyetlen motívumfájlt sem ír, ezért más feladattal párhuzamosan futhat. Ütközhet viszont minden olyan feladattal, amely a `adat/SEMA.md`-t írja; a sorrendet a `feladatok.py` dönti el.
5. **Zárás a `/kovetkezo` szerint:** `fuggetlen-ellenor`, zárójelentés, draft PR, a saját fejléc frissítése.

## 5. Kész, ha

- K1: az öt M0-kimenet létezik. Minden sorhoz van forrásparancs a naplóban.
- K2: a `DONTESEK.md`-tétel jóvá van hagyva.
- K3: a forrássablon-tervezet minden szakasza kap szintet és aktiválási feltételt; `javaslat` csak jóváhagyott tételként maradhat.
- K4: a SEMA-alfejezet és a CI-terv kész. Nincs `general.py`-módosítás, és nincs tartalmi fájl a diffben (`git diff --stat` a naplóban).
- K5: a `fuggetlen-ellenor` jelentése `TISZTA`.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.09.30 | első változat a chat D34–D39 döntései alapján | a feladat 1. fázisú (metaadat, nincs render); Opus, mert a besorolás szakmai ítélet; a CI-szabályok itt csak leírva, implementálás D6 szerint külön |
| v1.1 | 2026.10.04 | F32 K4: `fugg: [32]`; próza-elsőbbség a Célban; „Nincs benne” bővítve; M0/1 `kezi_forras` → `szint` kötelező | a KONTEXTUS (#32) K1/2 és K-D10; a #23-nak nincs értelmező (`munka: ertelmezo`) lépése: nem ír motívumfájlt, ezért jelölés nem kellett |
| v1.2 | 2026.10.04 | DT-F32a (🟢): ⛔ megállási pont az M0 után, az M1 a #12a próza-próba eredményét várja; a #12a a #23 M0 és M1 közé esik | DT-F32a (Felhasználó, 2026.10.04); a függés számmal nem rögzíthető (a #12a nem önálló feladat), ezért a `kovetkezo` fejlécmező és a szöveg hordozza |
| v1.3 | 2026.10.05 | DT28 (3. pont): „Egyirányúság” a Célban; M0/1 `B_helye` egyetlen érték, `szetvalasztando` jelölés; M0/4 a DT28 mércéje; M1/1 markerek: mit nyer ki a generátor és hova, visszaírás nincs; M1/2 a SEMA 3/9-re épít, a kinyerést írja le; M1/4 a szétválasztás négy kategóriája és a visszaírás-számláló | DT28 (Felhasználó, 2026.10.05, PR #195; az 1–2. pont a #197-ben); a brief hatóköre nem bővül: továbbra is csak tervez és mér |
| v1.4 | 2026.10.07 | fejléc `ir`: az öt M0-kimenet (`naplok/MOTIVUM_FORRAS_lekepezes.tsv`, `_torzscikk_egyedi.tsv`, `_parositas.tsv`, `_naplo_keveredes.tsv`, `_atfedes.tsv`) felvéve; a hatókör nem bővül (az M0 eleve ezeket állítja elő) | DT65 (c) (Felhasználó, 2026.10.07): önálló fejléchiba-javítás; az `allapot` és a `fugg` nem változik |
