# F203 — A Thayer-lánc, a fordítási lista és a Feed 9. kapujának hibajavítása (jelentés)

*Brief: `F203_THAYER_FORDITAS_BRIEF.md` · ág: `claude/f203-thayer-forditas` · kiindulás: `origin/main` `9926ae54` · végrehajtó:
`claude-opus-5-5` · a leltár: `GENERATOR_HIBALELTAR_2026-11-11.md` C7, C8, B6, B4.*

## Összefoglaló — előtte / utána

| Tétel | Mérőszám | Előtte | Utána |
|---|---|---:|---:|
| C7 (N125, N126) | Thayer-aranyminta (800 sor), jelentéspont = arany | 787 | **795** |
| | seed-201 / -202 / -203 / -204 | 199 / 198 / 194 / 196 | 199 / 198 / 199 / 199 |
| | szakasztábla sorai (`thayer_szakaszok.tsv`) | 17 261 | 17 220 |
| | változott szócikk (a korpuszon, átnézve) | — | 64 (K2c/K2d 54, K1d 10) |
| C7 (N124) | `bcv` nem bibliai műre, Károli-verssel | 3 (G0027 Luk 7:23, 8:18, 8:25) | 0 (`nem_bibliai`) |
| C7 | Thayer-fordítássor: átkulcsolva / elavult / összefűzött + tagsor | — | 38 / 7 / 10 + 10 |
| B6 (N-F12e) | `lista --id HAMART-001` tételei (ebből téves `nincs_forras`) | 42 (18) | 24 (0) |
| B6 | a repóba írt fájl `--kimenet` mellett | 1 | 0 |
| B4 (N-F184a) | DT665 (b) gépi ellenőrzése a 9. kapuban | nincs | blokkszintű lapdiff |
| B4 | érvényes átnézés a mai lapokon (9 lap) | 0 | 0 (indokolt: lásd 3.) |
| C8 (N-F131v) | a lapokon látszó görög rövid glossza magyarul | 0 / 68 | 68 / 68 |
| C8 / C7 | a 13. szabály SÉRTÉS-e (G2671 a HAMART-lapon) | 0 (a F203.1 előtt) → 1 | 0 |

*(proveniencia: scope=adat/thayer_aranyminta.tsv, adat/thayer_szakaszok.tsv, adat/forditasok.tsv, lexikon/*.md (repón kívüli
render) | forras=a lenti futások | ts=2026-11-11)*

## 1. C7 — a Thayer-lánc (F203.1)

### 1.1 A bontó szabályai (`eszkozok/thayer_jelolt/bont.py`)

- **K2c (N126)** — a bekezdés eleji félkövér **betűjelölő** nem fej, ha (1) szám követi („**c.** 6, p. 397{b}, 20)”,
  „**c.** 142 (and in the classics))”), (2) felsorolt utalás („**c.** and d.;”), vagy (3) a jelölő utáni első 80 nem címke
  karakterben, a kettőspont előtt, a bekezdésben nem nyitott „)” áll („**d.** Br. an d. Gal., p. 194ff):”, „**b.** (aa.)),”,
  „**d.** at the end; (Liddell and Scott, II. 3)),”, „**b.** e. above);”). A kettőspont-feltétel a G1799 „**a.** properly: …
  (Rev 14:5 Rec.))” valódi fejét védi.
- **K2d (N126)** — a betűjelölő nem fej, ha az első fej előtti bekezdés(ek)ben nyílt kerek zárójel még nyitva van (az utolsó 120
  karakterben nyílt), és a következő három bekezdés egyikében lezárul (zárójeles etimológia: G0536 „(from ἀπάρχομαι: **a.** …
  **b.** … ἀποδεκατόω)”, G0329, G2855, G2585). A „soha le nem záródó” forrászárójel (G0156 „(ας, ἡ;”) nem nyel el fejet.
- **K1d (N125)** — a „Rec.” nem kizáró előzmény (V007 G5547 „Act 19:4 Rec. b. ὁ Χριστός is a proper name”).
- **Számjelölő kivétel:** a K2c (3) és a K2d csak betűjelölőre vonatkozik. Az első változat a számjelölőre is kiterjedt, és a
  korpuszon négy valódi fejet nyelt el (G0966 „3.”, G1389 „1.”/„2.”, G3180 „1.”/„2.”, G4613 „5.”); ezt a teljes korpusz-diff
  átnézése fogta meg.

### 1.2 Mérés

Az aranyminta (`adat/thayer_aranyminta.tsv`, 800 sor, seed-201–204) a mai `vers_jelentes.general` kimenetével, soronként
(jelentéspont és könyv/vers):

| Állapot | 201 | 202 | 203 | 204 | Összesen | Eltérés |
|---|---:|---:|---:|---:|---:|---|
| előtte (F186 vége) | 199 | 198 | 194 | 196 | 787 | K3, K4, K2b/U014, K1d, K5, K2c×6, K2d, K1e |
| első változat (a számjelölőre is) | 196 | 195 | 191 | 195 | 777 | **10 új hiba** (G1537 ×6, G0156, G3858, G1487 …): elvetve |
| a zárójel-hordozás korlátozva | 199 | 198 | 196 | 197 | 790 | V049, V065, W082, W146: a hordozás valódi fejet nyelt |
| végleges (a lezáródás-feltétellel, „Rec.”) | **199** | **198** | **199** | **199** | **795** | K3, K4, U014, K5, K1e |

**Vakság:** a szabályok a seed-203/204 eseteiből készültek, ezért a 795 nem független szám. A mérvadó vak szám a seed-204
(F186: 196 / 200). Új vak mérés: N-F203a (orkesztrátori döntés, ≈ 1,1 M subagent-token).

**A korpusz-diff kézi átnézése.** A régi és az új szerkezet bekezdésszintű összevetése a teljes Thayeren (5 426 szócikk). A K2c/K2d
54 szócikket érint. A töredékek mind hivatkozás- vagy etimológia-darabok: „c. 3; Herodian, 7, 5, 2.)”, „b. 104:5, 40).”,
„d. Zeitschr. d. deutsch. morgenl. Gesell. xxi. 609);”, „c. 1 says, it is λύπη …)”, „a. an inn-keeper …” (G2585, a καπηλεύω
zárójeles etimológiája). A K1d 10 szócikkben nyit új belső fejet: G1065 g./h., G1209 d., G1487 c., G1538 b., G2198 b., G2632 b.,
G3767 f., G3768 b., G4160 f., G5547 b. Mind valódi pontnak látszik. Hamis fejet a végleges szabály a korpuszon nem nyelt el.

### 1.3 A nyitva maradt alesetek (indoklással)

- **K3 (N123)** — a záró szinonima-jegyzet új `utvonal`-értéket (`zaro`) kíván. Ennek fogyasztója a lapgenerátor
  (`lexikon_general.py`) és a #187 kártyája, ezek nem írhatók ebben a csomagban. Változatlanul nyitva.
- **K1e, K5** — a „visszaugró betű” mechanizmusa (új betűsor a várt betű helyett; a görög α félkövér latin „a.”-ként). Az F186 9.1
  szerint a szabály a korpuszon 50 bekezdést érintett, többségük valódi fej, ezért nincs bevezetve. Egy-egy esetre nem vezethető be.
- **K4** (U049, forrás-torzulás) — nem e csomag tétele.

### 1.4 N124 — a G0027 nem bibliai hivatkozása (`vers_jelentes.py`)

A forrás: „(cf. Ascensio Isa. (edited by Dillmann) Luk 7:23; Luk 8:18, Luk 8:25, etc.)” — **mindhárom** `bcv` az Ascensio
Isaiae fejezet:versét jelöli Lukácsnak (nem csak a 8:18, ahogy az N124 írta). A korpuszon más nem bibliai műre (Enoch, Jubil.,
Psalt. Sal., Test. xii) `bcv` nem mutat. A szabály: a hivatkozás, amely egy `NEM_BIBLIAI_MU` szerinti nem bibliai művel kezdődő
nyitott zárójelben áll, megtartja a sorát és nyers koordinátáját, de Károli-verset nem kap, és a proveniencia `nem_bibliai`. Ez
a BDB DT166 (1) mintája, a fogyasztók a `karoli_vers`-en át keresnek. Ma 3 sor.

### 1.5 Az átkulcsolás — a harmadik egyedi mód helyett általános mód (gyökérok)

Az F186 a Thayer-fordítássorokat kétszer kulcsolta át, mindkétszer a saját szabályváltozásához kötött, egyszeri térképpel
(`bekezdes_elso`, `osszevonas_terkep`). A F203 a harmadik eset, így az F186 `Mai` tesztje, amely az összevonási mód
idempotenciáját mérte, a mai táblán már nem teljesülhetett. Az **általános mód**
(`forditas_atkulcsol.py --regi-rev HEAD` / `--regi-tabla`) a régi szakaszt a szócikk szövegében elfoglalt helye szerint a mai
szakaszra vetíti (legnagyobb átfedés). Azonos hash-nél átkulcsol, különben `elavult`; az egy mai szakaszra eső több régi sorból
összefűzött sor és tagsor lesz (DT-F186f), a meglévő tagsor a fősorát követi. Ez a `bont.py` bármely későbbi változása után
ugyanúgy fut (SEMA 2.14). A mai táblán önmagával összevetve a terv üres, és minden nem elavult Thayer-sor hash-e a kulcsa
szakaszáé (`teszt_forditas_atkulcsol.py` `Mai`).

Eredmény (18 Strong): **38 átkulcsolás** (a fordítás változatlan), **7 elavult** (G1209 sz7, G1538 sz3→sz4, G2198 sz8→sz9,
G2443 sz9, G3767 sz7→sz8, G4160 sz23→sz24, G4190 sz7), **10 összefűzött** + 10 tagsor (G1519 sz22, G2041 sz5, G2168 sz4,
G2250 sz8, **G2671 sz2**, G2889 sz9, G3004 sz32, G3686 sz4, G3778 sz23, G5101 sz5), 7 elavult sor áthelyezve, 3 tagsor követi a
fősorát. Újrafordítás: N-F203b.

### 1.6 A várható lapváltozás (repón kívüli mérés, a lapok nem generálódtak újra)

A lapok görög gerinc-szavai (G0086, G1311, G1941, G1944, G2671, G4151, G4152, G5351, G5356, G5590, G5591) közül csak a
**G2671** (κατάρα, HAMART-001) szakaszai változtak: `cim, fej, -/-/c` → `cim, fej`. A mai HAMART-lapon a G2671 apparátusa egy
hamis pontot mutat: „c (hivatkozás nélkül) — c — (Aeschylus, Euripides, Platón, mások.)”. Ez a „c.” egy kettétört hivatkozás
töredéke, amely a javítás után a fejbe olvad. A fej fordítása ezzel elavul (összefűzve). A HAMART következő kiadása előtt a
G2671 sz2 fordítandó (N-F203b). A vers-tábla a lapszavakon nem változott.

**Mérve (repón kívüli render a mai fán, `PARDES_DATUM=2026-11-04`, a commitolt laphoz képest; `lapdiff_blokk.valtozott_blokkok`):**
HAMART-001 37 sor (a `szocikkek` blokkban a G2671: a hamis „c” pont kiesik, „a szócikk egésze — kárhoztatás, átkozódás, átok”, az
új fej-fordítás; az `lxx` blokkban a görög tooltipek magyar glosszája; a többi eltérés a dátumbélyeg és a ts), ALVIL-001 1, ANTROP-001
2, ISTENTISZT-001 2, TEREMT-002 2 sor (mind az `lxx` blokk tooltipjei, F203.4b). A CI E28-ja ezért mind az 5 migrált lapon piros,
amíg a lapok újra nem generálódnak (a merge előtt vagy vele, az orkesztrátoré).

## 2. B6 — a fordítási lista (F203.2)

- **(1)–(2) téves hiány:** a lista eddig minden `forditas_ehhez`-hívást hiánynak vett, amely üres fordítást adott. Ide tartoztak a
  lapra nem kerülő hívások, és azok is, amelyeknek a magyar szövegét más forrás adja (a BDB-gerinc a `bdb_szakasz_hu.tsv`-ből). Most
  a hiányzó kulcs a renderben egyedi jelölőt kap (`⟦GLF:n⟧`), és csak az a kulcs kerül a listára, amelynek jelölője a renderelt
  lapon áll. Ez pontosan a lapon látszó hiány; a tooltipben (`title`) álló hiányt is mutatja.
- **(3) mellékhatás:** a lista a `--ki` útjára, különben a render (repón kívüli) könyvtárába kerül. A
  `szakasz_cimke_levezet.py ellenoriz` `--ki` nélkül szintén a repón kívül ír.
- **(4) render nélkül** (pl. nincs `res_forras`-sor) a lista megáll, nem ad üres listát.

Előtte / utána a HAMART-001-en: **42 → 24**. Kiesett 13 BDB `nincs_forras` (a gerinc magyarul áll) és 5 Thayer
`nincs_forras`. A 24 TBESG `rovid` valódi hiány: a görög Strong-felirat tooltipje magyar glossza nélkül áll (pl. az LXX-híd
„πᾶς … G3956”).

A 9 lap a javított listával (utána):

| Lap | lapon látszó hiány | ebből TBESG rövid | a lapra nem kerülő / máshonnan magyar hívás |
|---|---:|---:|---:|
| ALVIL-001 | 5 | 5 | 7 |
| ANTROP-001 | 6 | 6 | 7 |
| HAMART-001 | 24 | 24 | 18 |
| HODIT-001 | 24 | 21 | 0 |
| ISTENTISZT-001 | 4 | 4 | 1 |
| KIRALY-001 | 39 | 19 | 0 |
| MENNY-001 | 41 | 14 | 0 |
| TEREMT-001 | 12 | 8 | 0 |
| TEREMT-002 | 10 | 10 | 1 |

A régi formátumú lapokon (HODIT, KIRALY, MENNY, TEREMT-001) a TBESG-n kívül a régi út kulcsai is látszanak (TBESH `teljes` 10,
tW-szócikk 33, MCGED 4, BDB `nyelvi_hatter` 7): ezek a migrációval szűnnek meg vagy N87/N-F203d. A TBESG rövid hiány a 9 lapon
**68 egyedi Strong** (487 karakter); lefordítva (4.).
*(proveniencia: scope=9 lexikonlap, repón kívüli render | forras=eszkozok/glossza_lexikon_forditas.py lista (F203) | ts=2026-11-11)*

## 3. B4 — a Feed 9. kapuja és a DT665 (F203.3)

`eszkozok/lapdiff_blokk.py` a lap két változatát blokkokra bontja. A generált blokk neve a jelölő `#<név>`-e; a kívüli szöveg
neve `kivul:<az előző ## címsor>`; a jelölősor `ts=`-e nem számít. A DT665 (b) teljesül, ha csak a `szocikkek`, a
`kereszthivatkozasok` és a `kolofon` blokk változott. A 9. kapu (`muhely_allapot.vizualis_atnezes`) a mai commitról szóló sor
híján a legutóbbi felhasználói átnézést fogadja el, ha a változatától a mai lapig a (b) teljesül, és az átnézett változat őse a
mainak; a részletben kiírja a kivételt és a kolofon változását ((c) jele). A (c) jelentésbeli felsorolását nem olvassa.

Mérés a valós git-történeten:
- HAMART-001 `520ae8ec → 7aadf8e6`: csak a `kolofon` → teljesül; `890da9f1 → 520ae8ec`: `idezes` is → nem.
- ALVIL-001 `c333c8b4 → 0bfb5bf4`: csak a `szocikkek` → teljesül; `0bfb5bf4 → 02c33d4e`: csak `ts=` → teljesül (azonos tartalom).
- A 9 lap mai állapotán az érvényes átnézések száma 0 → 0. A rögzített átnézések óta (ALVIL 4, ANTROP 3, ISTENTISZT 1 sor) a lapok
  a jelmagyarázatban, a kizárt helyekben, a kapcsolódó motívumokban és a prózában is változtak. A kapu most megnevezi, melyik
  blokk miatt piros.

## 4. C8 — a fordítás hiányai

- **N-F131v (görög rövid glossza):** a TBESG 9 362 Strongjából 201-nek volt magyar rövid sora; **9 161 hiányzik** (87 442 karakter
  forrás). A lapokon ténylegesen látszó hiány 68 Strong (2. pont); **lefordítva (F203.4b)**: `glossza_api_koteg.py`, 4 kérés,
  előfizetői keret (a felhasználó, 2026-11-11: „mehet előfizetésből”), general-purpose subagent `claude-sonnet-5-5` a `prompt`
  fájljából; kapu 67/68, egy javító kör (G0165 „korszak; kor” → „korszak”), 68/68; 68 új sor. A maradék 9 093 Strong (≈ 455
  kérés) a felhasználó döntése szerint (2026-11-11: „Csak az olvasó-fázisban döntsünk”) most nem fordul; az út és az időzítés az
  olvasó-fázisé (N-F203c).
- **Gyökérok a glossza-láncban:** a G0076 „Adam” → „ádám” (a F161.11 után második előfordulás, N88 (2)). Új mankó-jelzés: a TIPNR
  tulajdonnév-indexében álló Strong kisbetűs fordítása jelzés, a beírás `--jelzes-atnezve`-t kér (nem gátol: a népnév a magyarban
  kisbetűs, G3019 „lévita” átnézve helyes). A G0076 kézzel „Ádám”, jelölve.
- **N-F203b, a lapot érintő rész:** a HAMART-001 G2671 fej-szakasza lefordítva (F203.4a): `thayer_api_koteg.py`, adag 9203, a
  batch-kérés bájtra azonos fájlból, subagent `claude-sonnet-5-5`, kapu: kész (1. próba). A `forditas.beir` a Strong teljes
  lefedését kéri, az F31 viszont az érvényes `sz1`-et nem engedi újraírni, ezért az egy sor bájtőrzően, hash-ellenőrzéssel került
  be (N-F203e). A 13. szabály: SÉRTÉS 1 → 0.
- **N87 (22 TBESH-szócikk):** 6 090 karakter forrás (átlag 276). Egyik meglévő fordítási lánc sem fogadja: a glossza-lánc rövid
  glosszára, a Thayer-lánc szakaszra szól. Kell a `glossza_api_koteg.py` kiterjesztése a `TBESH | teljes` kulcsra (N-F203d). A
  szónézetet érinti, lapot nem.
- **N88 (1) `{L:…}`:** a lapokon ma 0 előfordulás; a `forditasok.tsv` 17 UBS-definíciójában, a forrásban 5 395 DBH- és 1 249
  DNTG-sorban áll. A fordítási prompt szabálya szerint a jelölés betűre marad, ezért az átalakítás a megjelenítő dolga
  (lapgenerátor és olvasó). Hogy mivé alakuljon (Károli-név, héber szó vagy angol név), tartalmi döntés: **DT-F203a** (🟡,
  javaslat: Károli-alak, közös segédfüggvény). A lapgenerátor ebben a csomagban nem írható.

## 5. Tesztek

| Teszt | Eredmény | Megjegyzés |
|---|---|---|
| `python eszkozok/teszt_futtat.py --gyors` | 4 bukás a `teszt_olvaso_szerver.py`-ban, a többi zöld | mind a 4 BDB-teszt (`TestF104BdbJeloles.test_kattinthato_helyek`, `TestLapok.test_bdb_jelentesszerkezet_…`, `TestPilotAranymintaval` F76f/F76g); a WSL-adatbázist olvassák (2026-11-02-i építés, a teszt szerint elavult) — a változás nem érinti (az adatbázis nem épült újra) |
| `eszkozok/thayer_jelolt/teszt_bont.py` | 39 OK | + `F203Fejek` (9) |
| `eszkozok/thayer_jelolt/teszt_vers_jelentes.py` | 24 OK | + K2c, K2d, K1d, G0027 |
| `eszkozok/thayer_jelolt/teszt_forditas_atkulcsol.py` | 22 OK | + `TervTabla` (6), `Mai` (általános mód) |
| `eszkozok/thayer_jelolt/teszt_lanc.py` | 42 OK, 1 bukás | a `Sigla.test_tabla_determinisztikus_es_kezi_vedett` az F186 6.3 szerint már előtte bukott (66 ≠ 60) |
| `eszkozok/teszt_glossza_lexikon_forditas.py` | 22 OK | + `Lista` (6) |
| `eszkozok/teszt_glossza_api_koteg.py` | 22 OK, 1 hiba | a `TeljesUt.test_bevesz_kapuz_javit_rogzit_beir` a main-en is hibás (F31 a valós tábla UBS_DNTG G4151 során); + `Tulajdonnev` (2) |
| `eszkozok/teszt_lapdiff_blokk.py` | 10 OK | új |
| `eszkozok/teszt_muhely_allapot.py` | 34 OK, 1 bukás | a `TesztHatarFrissesseg.test_hamart_…` a változás nélkül is bukik (a HAMART határ-frissessége, a #182 területe) |
| `python eszkozok/ellenoriz.py` | 0 SÉRTÉS | a 13. szabály a G2671 fordítása után RENDBEN/JELENTÉS |
| `bont.py`, `vers_jelentes.py`, `forras_javit.py --ellenoriz` | azonos | |
| `python eszkozok/feladatok.py ellenoriz` | 0 hiba | a brief `nem_fugg`-ja a levezetett kört oldja |

## 6. Gyökérok és gépi védelem

- **Átkulcsolás:** a harmadik egyedi átkulcsolás helyett általános mód és `Mai` teszt (1.5).
- **A lista téves hiánya:** a hiányt a renderelt lap dönti el, nem a hívás (2.). Teszt: `teszt_glossza_lexikon_forditas.py` `Lista`.
- **Repóba író alapkimenet:** mindkét érintett eszköz alapkimenete a repón kívül van, teszttel.
- **DT665 (b):** gépi blokkdiff a kapuban, teszttel (`teszt_lapdiff_blokk.py`).
- **Thayer-fejek:** a javított osztályok (K1d, K2c, K2d) a `teszt_vers_jelentes.py` aranyminta-tesztjében és a
  `teszt_bont.py` `F203Fejek` szintetikus eseteiben. A `NEM_JAVITOTT` halmazból kikerültek, így visszaesésük bukást okoz.
