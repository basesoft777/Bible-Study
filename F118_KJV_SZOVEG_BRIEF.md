---
feladat: 118
cim: A teljes KJV-szöveg importja új datasetként, a Károli melletti párhuzamos megjelenítés előkészítésével (KJV_SZOVEG)
kod: KJV_SZOVEG
tipus: feladat
fazis: folyamat
munka: adat
modell: opus
allapot: megallt
ag: claude/f118-kjv-szoveg
ad: a `konkordancia/KJV_teljes_szoveg.tsv` versenként a teljes KJV-szöveggel (eBible, Public Domain), a `KJV_Strongs_teljes.tsv`-vel mért vershalmaz- és szóegyezéssel, dataset- és licencsorral; a Károli melletti megjelenítés helye eldöntve, a megjelenítési brief tervezete a `beerkezo/`-ben
kovetkezo: Te: M2 kész — a mérés elfogadása (állapot importált, javaslat); utána M3
olvas: [konkordancia/KJV_Strongs_teljes.tsv, naplok/F19_hianyok.tsv, eszkozok/f19_ebible_import.py, konkordancia/Konyv_normalizalo_tabla.tsv, adat/datasetek.tsv, adat/licencek.tsv, adat/SEMA.md, Rendszerfejlesztesi_playbook.md]
ir: [eszkozok/kjv_szoveg_import.py, eszkozok/teszt_kjv_szoveg_import.py, konkordancia/KJV_teljes_szoveg.tsv, adat/datasetek.tsv, adat/licencek.tsv, adat/SEMA.md, beerkezo/KJV_SZOVEG_MEGJELENITES_BRIEF_TERVEZET.md]
fugg: []
nem_fugg: [38, 48, 107]
---
# F118_KJV_SZOVEG_BRIEF.md — A teljes KJV-szöveg importja és párhuzamos megjelenítése a Károli mellett

*FELADATOK #118 · Modell: opus · v1 · 2026.10.18 · előzmény: #19 (F19, `KJV_Strongs_teljes.tsv`), DT124, DT126, #76 (olvasói konkordancia), #117 (VERSMEGF_JAVITAS)*

## 1. Cél

A `konkordancia/KJV_Strongs_teljes.tsv` (#19) **csak a Strong-címkézett szavakat** tartalmazza: az `eszkozok/f19_ebible_import.py` szándékosan csak a `\w …|strong="…"\w*` szavakat veszi át (a docstring szerint: „a Strong-cimke nelkuli szavak nincsenek benne”). Az 1Móz 1:1-ből így csak a „beginning, God, created …” szavak vannak meg; a névelők, kötőszók, a dőlt betoldások (`\add`) és az írásjelek hiányoznak. Teljes KJV-szöveg nincs a repóban, és a forrás-zip sincs helyben (2026-10-18-i megállapítás).

A felhasználó a teljes KJV-bibliát meg akarja jeleníteni az olvasóban (#76), a Károli mellett, párhuzamos szövegként. A #117 a versmegfeleltetés javításánál ugyanezt a korlátot rögzíti, és a teljes szövegen való utólagos ellenőrzést N-tételbe teszi: ennek is ez a dataset lesz a forrása.

A cél:

1. **új dataset:** `konkordancia/KJV_teljes_szoveg.tsv`, versenként a teljes KJV-szöveggel, KJV-számozással;
2. **mérés** a meglévő `KJV_Strongs_teljes.tsv`-vel (vershalmaz és szóegyezés, 4. pont);
3. **dataset-szabályok** a `Rendszerfejlesztesi_playbook.md` 2. pontja szerint (`datasetek.tsv`, `licencek.tsv`, `SEMA.md`, proveniencia);
4. a **licenc** tisztázása, köztük a DT126 („a GPL-es KJV-fájl sorsa”) viszonya az új datasethez;
5. a **Károli melletti megjelenítés** helyének eldöntése (⛔ M4), és a megjelenítés briefjének tervezete. A megjelenítés maga nem e feladat része (2. pont).

## 2. Hatókör

**Benne van:**
- az importáló (`eszkozok/kjv_szoveg_import.py`, vagy az `f19_ebible_import.py` bővítése: ⛔ M0, DT-F118b) és tesztje;
- a `konkordancia/KJV_teljes_szoveg.tsv` generálása (`# GENERÁLT:` fejléccel, kézzel nem szerkeszthető);
- a mérés (4. pont) és a mérési napló (`naplok/KJV_SZOVEG_meres.md`);
- a `datasetek.tsv` (study-típusonként), a `licencek.tsv` új sora és a `SEMA.md` dataset-leírása;
- a megjelenítési brief tervezete: `beerkezo/KJV_SZOVEG_MEGJELENITES_BRIEF_TERVEZET.md` (⛔ M4).

**Nincs benne:**
- a forrás letöltése: **a zip-et a felhasználó tölti le**; a szkript nem tölthet le (`--munka <mappa>` bemenet, mint az F19-nél);
- a `KJV_Strongs_teljes.tsv` és a `naplok/F19_hianyok.tsv` módosítása vagy újragenerálása;
- a `pardes.db` építése (`eszkozok/sqlite_epit.py`) és az olvasó-szerver (`eszkozok/olvaso_szerver/`): a megjelenítés a ⛔ M4 szerint a #76-ban vagy külön feladatban megy, a #117 merge-e után;
- a `Karoli_versmegfeleltetes*` fájlok és a `tsk_kulcs.py` (#117), az `eszkozok/bdb_jelolt/` és az `adat/bdb_*` (#107), a `claude/f11-m3b` ág fájljai (#11 M3) — ezekhez a menet nem nyúl;
- a DT126 eldöntése (a menet csak a bemenetét adja, 5. pont);
- az ASV (D7: nem importáljuk).

## 3. A forrás

| | |
|---|---|
| Forrás | eBible.org `eng-kjv_usfm.zip`, https://ebible.org/Scriptures/eng-kjv_usfm.zip |
| Várt sha256 | `1bab5d4d030439831fc0b39d7f11001dd8527fc6277405e7f6512273c200c3a4` (a `KJV_Strongs_teljes.tsv` 2. fejlécsora és a `licencek.tsv` KJV_Strongs_teljes sora szerint; letöltve 2026-09-30) |
| Licenc | Public Domain (https://ebible.org/eng-kjv/copr.htm, szó szerinti idézet a `licencek.tsv` KJV_Strongs_teljes sorában); az Egyesült Királyságban a nyomtatásra és importra a Korona szabadalmi joga (letters patent) vonatkozik |
| Hatókör | a zip 81 fájlja közül csak a 66 kanonikus könyv (az apokrifok kimaradnak; az F19 hatókör-megjegyzése, `naplok/F19_hianyok.tsv` 6. sor) |
| Várt méret | kanonikus versek (v>0): 31 102; ebből Strong-címkés 31 099, címke nélküli 3; plusz a 0. versű helyek (zsoltárfeliratok, `\d`) — az F19 mérése (`naplok/F19_hianyok.tsv` 8. sor) |

**Ha a felhasználó által letöltött zip sha256-ja eltér** a fentitől, a menet ⛔ megáll: az eBible azóta új csomagot adhatott ki, és a mérés (4. pont) a `KJV_Strongs_teljes.tsv`-vel csak azonos forráson érvényes. A felhasználó dönt: a régi csomag felkutatása, vagy az új csomag elfogadása mért eltéréslistával (és akkor a #19-táblával való különbség naplózva).

A zip **nem kerül a repóba**, és nem kerül kibontásra a repóban: az importáló a `zipfile` modullal közvetlenül olvas (mint az `f19_ebible_import.py`).

## 4. Lépések (⛔ a kötelező megállások)

Minden lépés külön commit (`F118.0:`, `F118.1:` …), munkaág `claude/f118-kjv-szoveg` a `main`-ről. Első lépés a modell-ellenőrzés (CLAUDE.md).

### M0 — ⛔ terv (csak olvas)

1. **USFM-jelölőleltár.** A zip 66 kanonikus könyvében előforduló összes USFM-jelölő gyakorisági táblája (`\c`, `\v`, `\d`, `\q*`, `\qa`, `\s*`, `\ms*`, `\p`, `\m`, `\f…\f*`, `\x…\x*`, `\w…\w*`, `\add…\add*`, `\nd…\nd*`, `\wj…\wj*`, `\pb`, …), és jelölőnként a javasolt bánásmód: **szöveg marad** / **jelölve marad** (pl. `\add` → dőlt betoldás) / **kimarad** (lábjegyzet, kereszthivatkozás, oldaltörés) / **külön kezelendő**. *Ismert csapda:* az `f19_ebible_import.parse_usfm` a vers nélküli sor szövegét az aktuális vershez fűzi; így pl. a Zsolt 119 akrosztichon-fejlécei (`\qa`, ha előfordulnak) az előző vers szövegébe kerülnének. Az F19-nél ez nem számított (csak a címkés szavakat vette át), itt számít.
2. **Táblaforma javaslata.** Kiindulási javaslat (a ⛔ dönt):
   `Igehely` (STEP-alak, `Gen.1.1`, KJV-számozás, a zsoltárfelirat verse `0` — mint a `KJV_Strongs_teljes.tsv`-ben, így a kettő kulcsa közvetlenül illeszthető) · `Szöveg` (tiszta olvasószöveg, írásjelekkel, jelölők nélkül) · `Szöveg_jelolt` (a dőlt betoldások `[…]` között; további jelölés csak az 1. pont döntése szerint).
   Fejlécsorok: `# GENERÁLT: eszkozok/kjv_szoveg_import.py — kézzel nem szerkesztendő.`, proveniencia (`scope=KJV teljes (66 kanonikus könyv, angol számozás) | forras=…eng-kjv_usfm.zip sha256=… | ts=…`), licencsor, `# ÁLLAPOT:` sor a mérés eredményével.
   A STEP-alak miatt a táblát a `konkordancia/Konyv_normalizalo_tabla.tsv` konvertálja a magyar igehelyformára (CLAUDE.md, „Igehely-formátum”); a `SEMA.md` és a `datasetek.tsv` ezt kiírja.
3. **⛔ Döntés (DT-F118b): saját importáló vagy az `f19_ebible_import.py` bővítése.**
   - (a) **saját importáló** `eszkozok/kjv_szoveg_import.py`: a könyvlistát és ha megfelel, a vers-szétvágást az `f19_ebible_import`-ból importálja (kódmásolás nélkül), a szövegtisztítást viszont maga végzi az 1. pont szerint; a `KJV_Strongs_teljes.tsv` és az F19-generátor érintetlen. *Javaslat ez,* mert az F19-generátor kimenete mért és befagyasztott (`# ÁLLAPOT:` sor, `F19_hianyok.tsv`), a #48 pedig írja az `f19_ebible_import.py`-t (fejléc-hivatkozások).
   - (b) **az `f19_ebible_import.py` bővül** egy második kimenettel: egy forrásolvasás, egy generátor; de a bővítés után a `KJV_Strongs_teljes.tsv`-nek és az `F19_hianyok.tsv`-nek bájtra azonosan kell újragenerálódnia (igazolandó), az `F19` futtatása a luvlylavnder-klónt és az ASV-zipet is kéri, és ütközik a #48 `ir` listájával.
4. **⛔ Döntés (DT-F118a): licenc** — az 5. pont kérdései.

A terv `naplok/KJV_SZOVEG_M0.md`-be kerül. ⛔ Jóváhagyás.

### M1 — ⛔ kis minta (playbook 3. pont)

A felhasználó letölti a zip-et egy repón kívüli mappába; a menet ellenőrzi a sha256-ot (3. pont). Minta: 1Móz 1:1–3, Zsolt 3:0–2 (felirat), Zsolt 119:1 és 119:9 (akrosztichon-határ), Mt 1:1, Jel 22:21, továbbá a 3 címke nélküli kanonikus vers (`naplok/F19_hianyok.tsv`). Mindegyiknél: a `Szöveg` és a `Szöveg_jelolt` mező, és mellette a vers nyers USFM-szövege. ⛔ A felhasználó jóváhagyja a mintát.

### M2 — teljes import és mérés

1. A teljes tábla generálása; teszt (`eszkozok/teszt_kjv_szoveg_import.py`): a minta-versek rögzített elvárt értékkel, a jelölőtisztítás egységtesztjei, a fejlécsorok.
2. **Mérés** (`naplok/KJV_SZOVEG_meres.md`, saját proveniencia-sorral; a mérőkód a naplóban vagy a tesztben, nem a generátorban):
   - **M-a vershalmaz.** Jelölje S a `KJV_Strongs_teljes.tsv` versei halmazát, T az új tábláét. Elvárás: **S ⊆ T**, és a **T ∖ S** pontosan a `naplok/F19_hianyok.tsv` címke nélküli versei (a 3 kanonikus vers és a címke nélküli 0. versek); minden további eltérés tételesen listázva. A kanonikus versek száma (v>0) 31 102.
   - **M-b szóegyezés.** Versenként a `KJV_Strongs_teljes.tsv` `Angol szó` mezői (`Szósorszám` sorrendben) a `Szöveg` tokenjeinek **sorrendtartó részsorozataként** megtalálhatók. Normalizálás: kisbetű, írásjelek le, az aposztróf-változatok (`’`/`'`) egyesítve; a többszavas `Angol szó` (pl. „man’s hand”) szavanként illesztve. Elvárás: **minden** Strong-címkézett szó megtalálható; a nem illeszkedő szavak tételes listája `naplok/KJV_SZOVEG_szoegyezes_hiany.tsv`-be, okkal. **Nem 0 megmagyarázatlan eltérésnél ⛔ megállás.**
   - **M-c épség.** Üres `Szöveg` mező: 0 (vagy indokolt lista); a versek könyvenkénti száma; a vers-hidak (`\v n-m`) száma; a kimaradt jelölők számlálója az M0 leltára szerint.
3. A tábla `# ÁLLAPOT:` sorába a mérés eredménye kerül; az állapot `importált, javaslat`, amíg a felhasználó el nem fogadja.

### M3 — dataset-szabályok (playbook 2. pont)

- `adat/licencek.tsv`: új sor `KJV_teljes_szoveg` néven, a DT-F118a szerint; a szó szerinti licencidézet a copr.htm-ből (a KJV_Strongs_teljes sor idézete újrahasználható, a lekérés dátumával; ha a menet újra lekéri, új dátummal).
- `adat/datasetek.tsv`: study-típusonként (`bovitett`, `tematikus`, `melyelemzes`, `lexikon_oldal`) a sor; a `kotelezoseg` javasolt értéke `ajanlott` (párhuzamos szöveg, nem lexikai forrás), a `megjegyzes`-ben: KJV-számozás, STEP-alakú `Igehely`, a `Konyv_normalizalo_tabla.tsv` konverziója, a Strong-címkék **nincsenek** benne (azok a `KJV_Strongs_teljes.tsv`-ben).
- `adat/SEMA.md`: a dataset leírása a `KJV_Strongs_teljes` mellé (a 2. táblák szakaszban), a két KJV-tábla viszonyával.
- A TSV-k olvasása `split('\t')`, írása `'\t'.join()`; táblát író lépés írás előtt összeveti a sorokat az eredetivel, eltérésnél megáll (CLAUDE.md).

### M4 — ⛔ a megjelenítés helye (DT-F118c) és a megjelenítési brief tervezete

A megjelenítés a #76 olvasó-szerverében (`eszkozok/olvaso_szerver/`, `pardes.db`) a vers-lapon mutatja a KJV-szöveget a Károli mellett. **A #117 merge-e előtt nem indulhat**, mert a Károli-vers ↔ KJV-vers párosítás forrása a `Karoli_versmegfeleltetes.tsv`, amelyet a #117 javít. A #76 M3 jelenleg fut, és az `eszkozok/olvaso_szerver/` a #76 `ir` listájában áll.

⛔ Döntés (DT-F118c):
- (a) **a #76 része**: a #76 briefje új mérföldkövet kap (pl. „M3b — párhuzamos KJV-szöveg”), a #76 saját menete írja be; a #76 `fugg` listája kiegészül a 117-tel és a 118-cal;
- (b) **külön feladat**: a menet megírja a `beerkezo/KJV_SZOVEG_MEGJELENITES_BRIEF_TERVEZET.md` tervezetet, a `/befogad` fogadja be, `fugg: [117, 118]`, az `ir` listájában `eszkozok/sqlite_epit.py` és `eszkozok/olvaso_szerver/` — így a #76-tal egyszerre nem fut, a sorrendet a `fuggesek` adja. *Javaslat ez,* mert a #76 M3 futása közben a #76 briefjét más menet nem módosíthatja, és a #11 M3 is írja a `sqlite_epit.py`-t.

Mindkét esetben a tervezet (vagy a #76-mérföldkő) tartalma legalább:
- **`pardes.db`:** új tábla (javaslat: `kjv_szoveg`: `igehely` Károli-kulcs, `kjv_igehely`, `szoveg`, `szoveg_jelolt`, `mod`), a `sqlite_epit.py` meglévő `_kjv` betöltőjének mintájára (`Karoli_versmegfeleltetes.tsv` `igehely_kjv` → Károli-vers); a `SZARMAZTATOTT_LICENC` sora; az `azonos_feltetelezett` tartalék csak ott, ahol a javított tábla nem ad párt, és jelölve;
- **egy Károli-vers – több KJV-vers** (és fordítva, versösszevonás, `f22/versosszevonas.tsv`, eltolt fejezetek): minden párosított KJV-vers a saját KJV-versszámával jelenik meg; a Károli-vers nélküli KJV-vers (pl. „nincs pár”) nem vész el némán, hanem a jelentésben számolva;
- **blokk:** új vers-blokk (pl. `vers.kjv_szoveg`, jelleg `forras`, licencsor a `licencek.tsv`-ből), az Olvasópult nézetben a Károli-szöveg mellett párhuzamos hasábként; a meglévő `vers.kjv` szavankénti blokk (Strong-címkés, GPL-jelölésű) változatlan marad;
- **kiadási kapcsoló:** a DT-F118a szerint; ha a szövegréteg közkincs, a nyilvános kiadásban is megmarad, a `vers.kjv` szavankénti blokk viszont a DT124 szerint továbbra is kimarad;
- **mérés:** a `pardes.db` újraépítése a WSL-natív `~/pardes/pardes.db`-n, a tesztek a `python eszkozok/teszt_futtat.py` hívással; a vers-lap vizuális összevetése a #60 pilottal (a látvány mércéje), nem csak számokkal.

## 5. Licenc és a DT126

**A kérdés.** A DT126 a `KJV_Strongs_teljes.tsv` **Strong-címkerétegéről** szól: a felhasználó DT124-es döntése szerint a címkeréteg GPL (CrossWire `kjv.conf`: „DistributionLicense=GPL”), és a playbook 2. pontja szerint GPL-forrás publikus repóba nem építendő be. Megoldja-e ezt az eBible PD-forrás?

**Amit a repó adata mond** (`adat/licencek.tsv` KJV_Strongs_teljes sor, F42/DT-F42d):
- az eBible a KJV-t „Public Domain”-nek nyilvánítja, és „You may copy the King James Version of the Holy Bible freely.” (copr.htm);
- az eBible szövege a CrossWire-től is származik („courtesy of the Crosswire Bible Society and eBible.org”, copr.htm), a CrossWire-modul GPL-nyilatkozatot ad, és a CrossWire szerzői joga a „this effort”-ra vonatkozik (a jelölésre és a Strong-adatra; a szöveg alapjogát a modul a Koronának tulajdonítja);
- a `licencek.tsv` sora ezért ma `tisztazatlan` a `kereskedelmi`/`share_alike` oszlopban, **a címkeréteg miatt**; a KJV-szöveg közkincs volta (kor, eBible-nyilatkozat) változatlan.

**Amit a menet ebből levezet (értelmezés, nem jogi vélemény):**
- az új dataset **nem tartalmaz Strong-címkét**, csak a szöveget; a DT126 GPL-kérdése (a címkeréteg) így nem terjed ki rá közvetlenül;
- a **DT126-ot viszont nem oldja meg**: a `KJV_Strongs_teljes.tsv` sorsa (kivezetés, maradás, elhagyás) ugyanaz a kérdés marad. Az új dataset a DT126 bemenete: ha a DT126 az 1. vagy a 3. opciót választja, a teljes KJV-szöveg a nyilvános kiadásban is megjeleníthető marad, a szavankénti Strong-blokk nélkül (az angol szavankénti blokkot a BSB, CC0, adja);
- nyitott: az eBible tiszta szövegében van-e a CrossWire-nek olyan saját hozzájárulása (szövegjavítás, írásmód), amelyre a GPL-nyilatkozat kiterjedhet. A repó adata ezt nem mondja ki; üresen marad, és explicit jelölendő.

**⛔ Döntés (DT-F118a), az M0-ban:**
1. a `KJV_teljes_szoveg` sor `kozkincs` (kor + eBible-nyilatkozat), `tisztazott`, `kereskedelmi` feltételesen (UK Korona-szabadalom), `share_alike` nem; a GPL-kérdés a címkerétegnél (DT126) marad;
2. a sor `tisztazatlan`, amíg a szövegréteg CrossWire-hozzájárulása nem tisztázott (pl. egy független PD-kiadással való versenkénti összevetés, vagy a CrossWire/eBible kifejezett nyilatkozata); a megjelenítés addig csak a belső kiadásban;
3. más.

A döntés a `DONTESEK.md`-be kerül helyőrzővel (DT-F118a), utána megállás.

## 6. Elfogadási feltételek

- **E1.** A `konkordancia/KJV_teljes_szoveg.tsv` generált (`# GENERÁLT:` fejléc), proveniencia-, licenc- és állapotsorral; a forrás sha256-ja egyezik a 3. pontéval, vagy az eltérést a felhasználó ⛔-nél elfogadta.
- **E2.** M-a: S ⊆ T, a T ∖ S azonos az `F19_hianyok.tsv` címke nélküli verseivel; 31 102 kanonikus vers.
- **E3.** M-b: minden Strong-címkézett szó megtalálható a teljes szövegben; megmagyarázatlan eltérés 0.
- **E4.** M-c: üres szövegmező 0 (vagy indokolt lista); a jelölőleltár minden jelölőjének bánásmódja dokumentált és tesztelt.
- **E5.** `licencek.tsv`, `datasetek.tsv`, `SEMA.md` frissítve a DT-F118a szerint; `python eszkozok/feladatok.py ellenoriz` 0.
- **E6.** A `KJV_Strongs_teljes.tsv`, a `F19_hianyok.tsv`, a #117, a #107, a #76 és a #11 M3 fájljai érintetlenek (`git diff --stat` a zárásban).
- **E7.** A DT-F118c eldöntve; (b) esetén a megjelenítési brief tervezete a `beerkezo/`-ben, `fugg: [117, 118]`-cal.
- **E8.** Független ellenőrzés (`fuggetlen-ellenor`) a zárás előtt.

## 7. Döntésnapló

| Helyőrző | Kérdés | Hol |
|---|---|---|
| DT-F118a | a `KJV_teljes_szoveg` licencállapota; viszony a DT126-hoz | M0, 5. pont |
| DT-F118b | saját importáló vagy az `f19_ebible_import.py` bővítése | M0 3. |
| DT-F118c | a megjelenítés helye: a #76 része vagy külön feladat | M4 |

## 8. Kapcsolódás

#19 (F19, KJV_Strongs_teljes), #48 (a régi KJV-fájlok kivezetése; írja az `f19_ebible_import.py`-t), #60 (pilot), #76 (olvasói konkordancia; M7: DT126), #117 (versmegfeleltetés; az N-tétele a teljes szövegen való utólagos ellenőrzésről e datasetre épül), DT124, DT126, DT-F42d, D7.

**A fejléc `nem_fugg` mezőjének oka:** a levezetett függés a #38-tól (`Konyv_normalizalo_tabla.tsv`), a #48-tól (`f19_ebible_import.py`) és a #107-től (`Rendszerfejlesztesi_playbook.md`) csak olvasott fájlon át jön; az import ezeknek a mai állapotát olvassa, a változásuk a kimenetet nem érinti (a könyvtábla 66 könyves listája és a playbook 2. pontja stabil). Ha a DT-F118b a (b) opciót választja, a #48 függése valós: a `nem_fugg`-ból a 48 kikerül.
