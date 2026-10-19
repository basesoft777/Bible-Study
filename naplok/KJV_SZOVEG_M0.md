# KJV_SZOVEG M0 — terv és mérés (#118, `F118_KJV_SZOVEG_BRIEF.md` 4. pont, M0)

**Egyeztetett eltérés: új csomag (sha256 `00532b6db1825cb78fd34de2097fc280ce03ee22ef0bdac5243ef4beaca4d447`, 2 766 294 bájt, a zip bejegyzései 2026-10-17-esek).** A brief 3. pontja az `1bab5d4d030439831fc0b39d7f11001dd8527fc6277405e7f6512273c200c3a4` hash-t várja (a #19-es letöltés, 2026-09-30). A felhasználó döntése (2026-10-18, az orkesztrátoron át): „Az új (2026-10-17-i) csomagból menjen a #118. Az M0 mérje és naplózza a #19-es táblától való eltérést (fájllista, versek, Strong-címkék).” A zip helye: `C:\Users\bases\Desktop\kjv_munka\kjv.zip`, a repón kívül. Kibontás nélkül, `zipfile`-lal olvastam, `python -I`-vel.

*proveniencia: scope=KJV_SZOVEG M0 (66 kanonikus könyv; a fájllista a teljes zip) | forras=kjv.zip sha256=00532b6db1825cb78fd34de2097fc280ce03ee22ef0bdac5243ef4beaca4d447 (2766294 bájt) + konkordancia/KJV_Strongs_teljes.tsv | ts=2026-10-18T15:23:34Z* — a mérőkód: `naplok/KJV_SZOVEG_M0_meres.py` (csak olvas; az F19-parse-t és az F06-mérést változatlanul importálja), a kimenete: `naplok/KJV_SZOVEG_M0_meres_kimenet.txt`, a részletek: `naplok/KJV_SZOVEG_M0_jelolok.tsv`, `naplok/KJV_SZOVEG_M0_versnelkuli.tsv`.

## 1. Az új csomag és a #19-es tábla (kiegészítő mérés)

| Mérés | Új csomag | #19 / F06 (repó) | Egyezik |
|---|---|---|---|
| zip-bejegyzések | 84: 66 kanonikus `.usfm`, 14 apokrif (1ES 1MA 2ES 2MA BAR BEL ESG JDT MAN S3Y SIR SUS TOB WIS), `00-FRT` (előszó), `copr.htm`, `keys.asc`, `latin.css` | F06: 81 `\id`-jelölt fájl (`naplok/F06_kjv_asv.tsv`) | igen (81 = 66 + 14 + FRT) |
| F06-mérés, a teljes zip (`fj2/kjv_asv.usfm_meres`) | könyv 81, vers 36 822, Strong-os vers 31 099, Strong-címke 349 308 | ugyanez (F06, 2026-09-29) | igen |
| F06-mérés, 66 kanonikus könyv | könyv 66, vers 31 102, Strong-os vers 31 099 | ugyanez | igen |
| F19-parse: kanonikus versek (v>0) | 31 102; ebből címkés 31 099; címke nélküli 3: Mk 9:43, Lk 6:41, Lk 17:36 | `F19_hianyok.tsv` 8. sor: 31 102 / 31 099 / 3, ugyanez a három vers | igen |
| F19-parse: 0. versek (zsoltárfeliratok, `\d`) | 116, mind címkés | 116 | igen |
| vershidak / parse-anomália | 0 / 0 | 0 / 0 | igen |
| versek halmaza: S (a tábla versei) és T | \|S\| = 31 215 (v>0: 31 099, v=0: 116); \|T_címkés\| = 31 215; \|T_összes\| = 31 218 | — | S = T_címkés; S ∖ T = ∅; **T ∖ S = {Mk 9:43, Lk 6:41, Lk 17:36}**, 0. vers nincs benne |
| Strong-címkék összesen | 349 308 | 349 308 | igen |
| versenkénti címkeszám | 0 vers tér el | — | igen |
| (vers, szósorszám, Strong) | közös 349 308; csak a táblában 0; csak az újban 0 | — | igen |
| (vers, szósorszám, Strong, `Angol szó`) | közös 349 308; 0 / 0; a sorrend is azonos | — | igen |
| kulcs-Strongok | H430=2605 H776=2504 H1=1212 H3068=6518 G746=58 G2316=1359 | a tábla 3. fejlécsora: ugyanez | igen |
| **bájtszintű tábla** | az `f19_ebible_import.ir_teljes` az új csomagból, a tábla saját fejlécsoraival, ideiglenes könyvtárba (repón kívül) | `konkordancia/KJV_Strongs_teljes.tsv` | **igen, bájtra** (sha256 `5a7891145401aa62…` mindkettő) |
| `copr.htm` a zipben | a `licencek.tsv` KJV_Strongs_teljes sorában idézett négy mondat szó szerint benne van; az oldal dátuma 2026-09-26 | a sor: „az oldal saját dátuma: 2026-09-26” | igen |

**Következtetés.** Az új csomag a Strong-réteg tekintetében azonos a #19-es forrással: az F19-generátor belőle bájtra a `KJV_Strongs_teljes.tsv`-t adja. Az eltérés csak a csomagolásé (új zip, 2026-10-17-es bejegyzésdátumok). Eltéréslista ezért nem készült (`naplok/KJV_SZOVEG_M0_strong_elteres.tsv` nincs). A nem Strong-címkés szövegrészt (névelők, `\add`, írásjelek, lábjegyzetek) a #19-es zip hiányában nem lehet a régi csomaggal összevetni. A #19-es tábla ezeket nem tartalmazza, ezért ez a mérés nem terjed ki rájuk.

*Mellékes következmény:* mivel az `1bab5d4d…` zip nincs meg sehol, az új zip lett a #19-tábla egyetlen meglévő, bájtra visszaigazolt nyers forrása (l. DT212).

## 2. USFM-jelölőleltár (66 kanonikus könyv) és bánásmód

A darabszámok a nyitó jelölőket számolják (a zárók száma minden párosnál azonos). A „beágyazott” a `\+jelölő` alakot jelenti. Teljes tábla: `naplok/KJV_SZOVEG_M0_jelolok.tsv`. A „veszteség” oszlop azt mondja meg, mit dob el az importáló. A DT226 (2) szerint ezt a dataset leírásában naplózni kell, és az M-c mérés számolja.

| Jelölő | db | Kontextus | Bánásmód | `Szöveg` | `Szöveg_jelolt` | Veszteség (mit dob el, naplózandó) |
|---|---|---|---|---|---|---|
| `\id` `\h` `\toc1` `\toc2` `\toc3` `\mt1` | 66-66 | fejléc (az első `\c` előtt) | **kimarad** | — | — | a könyvcím-metaadat (a könyvnevet a `Konyv_normalizalo_tabla.tsv` adja) |
| `\mt2` | 2 | fejléc | **kimarad** | — | — | ugyanaz |
| `\c` | 1 189 | szerkezet | kulcs (`Igehely` fejezete) | — | — | nincs |
| `\v` | 31 102 | szerkezet | kulcs (`Igehely` verse); vershíd 0 | — | — | nincs |
| `\d` | 116 (mind Zsoltárok) | zsoltárfelirat | **külön kezelendő**: saját sor, a vers `0` (mint a `KJV_Strongs_teljes.tsv`-ben) | a felirat szövege | a felirat jelölt alakja | nincs |
| `\s1` | 36 | vers nélküli sor | **külön kezelendő** (3. pont): 22 a Zsolt 119 akrosztichon-fejléce, 14 páli utóirat (Róm 16:27 … Zsid 13:25) | nem kerül a versszövegbe | nem kerül a versszövegbe | nincs, ha a 4. pont `Elotte`/`Utoirat` oszlopa elfogadott, különben a 36 sor |
| `\tl` | 22 | csak a Zsolt 119 `\s1`-ben (`א ALEPH.`) | a `\s1`-gyel együtt | — | — | a `\tl` jelölés (a héber betű és a név szövegként megmarad) |
| `\w … \w*`, `\+w … \+w*` | 313 813 + 35 495 = 349 308; attribútum mindig csak `strong` | szöveg | **szöveg marad**, a jelölő és a `strong=` attribútum kimarad | a szó | a szó | a Strong-címke: szándékosan, mert a `KJV_Strongs_teljes.tsv`-ben megvan, és a DT124/DT126 miatt ide nem kerül (DT210) |
| `\add … \add*`, `\+add` | 20 887 + 623 | szöveg | **jelölve marad** (dőlt betoldás) | a szöveg, jelölő nélkül | `[…]` között | `Szöveg`: a betoldás-jelölés (a `Szöveg_jelolt` megőrzi) |
| `\nd … \nd*`, `\+nd` | 6 876 + 16 (+ 65 lábjegyzetben) | szöveg (Isten neve, a forrásban már „LORD” nagybetűvel) | **szöveg marad**, a jelölő kimarad | a szöveg | a szöveg | a `\nd` jelölés (a nagybetűs írásmód megmarad) |
| `\wj … \wj*` | 2 038 | szöveg (Jézus szavai) | **szöveg marad**, a jelölő kimarad *(a ⛔ dönthet úgy, hogy a `Szöveg_jelolt` jelölje, pl. `‹…›`)* | a szöveg | a szöveg | a „vörös betűs” jelölés |
| `\p` | 4 635 | bekezdés | **kimarad** | — | — | a bekezdés-tagolás |
| `\q1` | 2 461 | költői sor | **kimarad** | — | — | a költői sortagolás |
| `\b` | 209 | üres sor (versszak) | **kimarad** | — | — | a versszak-tagolás |
| `\f … \f*` (benne `\fr`, `\ft`, `\+nd`) | 6 959 | lábjegyzet (KJV-széljegyzetek: „Heb. …”, „or, …”) | **kimarad** | — | — | a 6 959 széljegyzet (később önálló dataset lehet; most nem) |
| `\x`, `\pb`, `\qa`, `\ms`, `\s2+`, `\q2+` | 0 | — | — | — | — | — |
| `¶` (karakter, nem jelölő) | 2 970 vers | szöveg | **jelölve marad** | kimarad | marad | `Szöveg`: a pilcrow |
| `’` (U+2019) · `æ`/`Æ` · `—` | 1 997 · 93/3 · 1 | szöveg | **szöveg marad** | marad | marad | nincs (az M-b normalizálása egyesíti az aposztrófot) |

Többsoros lábjegyzet: 0. Az F19-parszoló `RE_FN`-je (`re.S`) így is helyes. A `\w` attribútuma mindig csak `strong` (349 308/349 308). A többszavas `\w` 9 328 db (pl. „man’s hand”), ezért az M-b szavanként illeszt.

## 3. A vers nélküli sorok csapdája (mért)

Az `f19_ebible_import.parse_usfm` a vers nélküli sor szövegét az aktuális vershez fűzi, a fejezet első verse előtt pedig eldobja. A `\c` utáni, szöveget hordozó, `\v` nélküli sorok száma 152 (`naplok/KJV_SZOVEG_M0_versnelkuli.tsv`):

| Csoport | db | Az F19-logika sorsa | Példa (az F19 `szoveg` mezője) |
|---|---|---|---|
| `\d` zsoltárfelirat | 116 | a 0. verse kerül (helyes) | Zsolt 3:0: „A Psalm of David, when he fled from Absalom his son.” |
| `\s1` Zsolt 119 akrosztichon-fejléc | 22 | 1-et eldob (ALEPH, a 119:1 előtt); **21-et az előző vers végére fűz** (119:8, 16 … 168) | Zsolt 119:8: „… O forsake me not utterly. ב BETH.” |
| `\s1` páli utóirat | 14 | **a levél utolsó versének végére fűzi** | Róm 16:27: „… for ever. Amen. Written to the Romans from Corinthus, and sent by Phebe …” |

Az új importálónak ezért a `\s1`-et külön kell kezelnie (4. pont), nem az F19 vershez fűző logikájával.

**Az F19 `szoveg` mezője olvasószövegnek sem alkalmas** (ez a DT211 bemenete): a záró jelölőt szóközre cseréli, ezért 4 305 versben szóköz áll az írásjel előtt (pl. 1Krón 2:42: „Jerahmeel were , Mesha”, `\add were\add*,`-ből). A pilcrow 2 970 versben benne marad, a `\add`-jelölés elvész, és a 35 `\s1`-sor a versszövegbe kerül.

## 4. Táblaforma-javaslat (a ⛔ dönt)

`konkordancia/KJV_teljes_szoveg.tsv`, versenként egy sor, a 66 kanonikus könyv KJV-számozással, várhatóan 31 218 sorral (31 102 + 116):

| Oszlop | Tartalom |
|---|---|
| `Igehely` | STEP-alak (`Gen.1.1`), KJV-számozás, a zsoltárfelirat verse `0`. A kulcs közvetlenül illeszthető a `KJV_Strongs_teljes.tsv`-hez; a magyar alakra a `Konyv_normalizalo_tabla.tsv` konvertál. |
| `Szöveg` | tiszta olvasószöveg írásjelekkel; jelölő, `¶` és lábjegyzet nélkül; a szóközök a forrás szerint (az írásjel előtt nincs szóköz) |
| `Szöveg_jelolt` | mint a `Szöveg`, de a dőlt betoldás `[…]` között, és a `¶` megmarad (további jelölés, pl. `\wj`, csak a ⛔ döntése szerint) |
| `Elotte` *(új javaslat)* | a vers előtt álló `\s1` címsor: csak a Zsolt 119:1, 9, … 169 (22 cella, pl. `א ALEPH.`); máshol üres |
| `Utoirat` *(új javaslat)* | a könyv utolsó verse után álló `\s1` utóirat: 14 cella (Róm 16:27 … Zsid 13:25); máshol üres |

*Alternatíva az `Elotte`/`Utoirat` helyett:* a 36 `\s1`-sor kimarad, a veszteségnaplóban darabszámmal. A versszövegbe fűzés semmiképp sem jó, mert az F19-hiba ismétlése lenne.

Fejlécsorok (a brief szerint): `# GENERÁLT: eszkozok/kjv_szoveg_import.py — kézzel nem szerkesztendő.`; `# proveniencia: scope=KJV teljes (66 kanonikus könyv, angol számozás) | forras=https://ebible.org/Scriptures/eng-kjv_usfm.zip sha256=00532b6d…d447 | ts=…`; `# licenc: …` (a DT210 szerint); `# ÁLLAPOT: …` (az M2 mérése); és új sorként `# veszteség: …`, a 2. pont kimaradó jelölőinek darabszámával (DT226 (2)).

Az M2 elvárásai a mért alapon: **T ∖ S pontosan a 3 címke nélküli kanonikus vers** (a 116 zsoltárfelirat mind címkés, tehát nem tartozik a T ∖ S-be; a brief M-a pontjának „címke nélküli 0. versek” része üres halmaz). Üres `Szöveg`: 0 várható (az F19-tisztítás után is 0).

## 5. Döntési tételek (⛔, `DONTESEK.md`: DT210, DT211, DT212)

### DT211 — saját importáló vagy az F19 bővítése

- **(a) saját importáló** `eszkozok/kjv_szoveg_import.py`. Az `f19_ebible_import`-ból importálja a `lista_konyvek`-et és a `RE_FN` / `RE_V` mintát, kódmásolás nélkül. A vers-szétvágást és a szövegtisztítást viszont maga végzi, mert az F19 `parse_usfm` a kettőt egy ciklusban keveri, és a vershez fűzés éppen a hibás rész (3. pont). A teszt rögzíti, hogy a saját versek halmaza azonos a `f19.parse_usfm` verseinek halmazával (31 218), így a kulcs-kompatibilitás géppel igazolt. A `KJV_Strongs_teljes.tsv` és az F19-generátor érintetlen marad.
- **(b) az `f19_ebible_import.py` bővül** egy második kimenettel. Ehhez a `parse_usfm`-et át kell írni (`\s1`, szóközök, `\add`). Utána igazolni kell, hogy a `KJV_Strongs_teljes.tsv` és az `F19_hianyok.tsv` bájtra azonos marad. Az F19 futtatása a luvlylavnder-klónt és az ASV-zipet is kéri. Ütközik a #48 `ir` listájával, és a `nem_fugg`-ból a 48 kikerül.
- **Javaslat: (a).** A mérés szerint az F19-parse a vershalmaz és a Strong-réteg referenciája (bájtra reprodukálható), a szövegtisztítása viszont alkalmatlan, tehát a jó részét importálni kell, a hibás részét nem.

### DT210 — a `KJV_teljes_szoveg` licence; viszony a DT126-hoz

A repó adata szerint (`adat/licencek.tsv` KJV_Strongs_teljes sor; a mostani zip `copr.htm`-je ugyanazt a négy mondatot tartalmazza, az oldal dátuma 2026-09-26) az eBible a KJV-t „Public Domain”-nek nyilvánítja. A CrossWire `kjv.conf` a szöveg alapjogát a Koronának tulajdonítja, a GPL-nyilatkozata pedig a CrossWire „this effort”-jára (jelölés, Strong-adat) vonatkozik. Az új dataset Strong-címkét és `\w`-attribútumot nem tartalmaz.

- **1.** `kozkincs` (kor + eBible-nyilatkozat), `tisztazott`; `kereskedelmi` feltételesen (UK Korona-szabadalom), `share_alike` nem. A GPL-kérdés a címkerétegnél (DT126) marad.
- **2.** `tisztazatlan`, amíg a szövegréteg esetleges CrossWire-hozzájárulása (szövegjavítás, írásmód) nem tisztázott: független PD-kiadással való versenkénti összevetéssel, vagy a CrossWire/eBible nyilatkozatával. A megjelenítés addig csak a belső kiadásban lehet.
- **3.** más.
- **Javaslat: 1.** A dataset a GPL-lel érintett réteget (címke, jelölés) nem hordozza, a szöveg kora és az eBible nyilatkozata adott. A nyitott kérdés (a CrossWire szövegszintű hozzájárulása) a repó adatából nem dönthető el. Ez üresen marad, és a licencsor megjegyzésében explicit jelölendő; nem töltjük ki. A DT126-ot ez **nem oldja meg**, csak a bemenete. A nyilvános kiadás előtti jogi átnézés (DT124, DT-M6) változatlan. Értelmezés, nem jogi vélemény.

### DT212 — a nyers zip helye (DT226 és a brief 3. pontja)

**A feszültség.** A DT226 (a felhasználó elfogadta 2026-10-18-án; egyelőre csak a `claude/f107-bdb-jelolt-szoveg` ágon, a `Rendszerfejlesztesi_playbook.md` 2. pontjában) szerint a nyers forrás SHA-256-tal megőrzendő, **a repóban, hacsak a méret vagy a licenc nem engedi**. A brief 3. pontja szerint viszont „a zip nem kerül a repóba”. Mért adatok:

- **Méret:** 2 766 294 bájt. Ez nem akadály: a repóban már ott van a 84 MB-os `konkordancia/lexikonok_nyers/BDB.lexicon`, és a DT225 a 24,7 MB-os `DictBDB.json`-t is a repóba tette.
- **Licenc:** a zip a teljes Strong-címkeréteget tartalmazza (349 308 `strong=` attribútum), amelyet a DT124 GPL-nek tekint. A playbook 2. pontja szerint GPL-forrás publikus repóba nem építendő be, és a DT126 (a `KJV_Strongs_teljes.tsv` sorsa) 🟡 nyitott. A licenc tehát a DT126 eldöntéséig nem engedi.
- **Kockázat:** az eBible gördülő kiadással dolgozik. A #19-es `1bab5d4d…` csomag már nem kapható meg, ezért a mostani zip az egyetlen meglévő, bájtra visszaigazolt nyers forrása a #19-táblának is (1. pont). Egyetlen példánya van, a felhasználó asztalán.
- Gitignore-olt minta létezik: `konkordancia/_nyers/` (cremer, `konkordancia/README.md` 140. sor). Worktree-ben a gitignore-olt fájl nem látszik, ezért az importáló a `--munka` útvonalat kapja.

Opciók:
- **(a)** a zip a repóba (pl. `konkordancia/forras/eng-kjv_usfm_2026-10-17.zip`), a hash a dataset-leírásban. Teljesíti a DT-F107d-t, de a GPL-címkeréteget a publikus repóba teszi, és ezzel elébe megy a DT126-nak. A brief 3. pontja módosulna.
- **(b)** a zip a repón kívül marad (a brief szerint). A hash, az URL, a letöltés dátuma, a fájllista és a hely a dataset leírásába kerül (a DT226 „ha a licenc nem engedi” ága), a táblafejlécbe pedig a hash. Kiegészítés: második példány egy, a felhasználó által megnevezett helyen.
- **(c)** gitignore-olt helyi másolat `konkordancia/_nyers/kjv/` alatt (a cremer mintája), a hash a dataset-leírásban. Licencszempontból a (b)-vel azonos, a hely egységes, de nem verziózott, és a worktree-k nem látják.
- **(d)** most (b), és a DT126 dönt: ha a DT126 a 2. opciót választja (a GPL-címkeréteg marad a nyilvános repóban), a zip is bekerülhet (a); ha az 1. vagy a 3. opciót, kint marad.
- **Javaslat: (d)**, a (b) második példányával. A DT226 (2) (a veszteség naplózása) a 2. pont veszteség-oszlopával és a tábla `# veszteség:` fejlécsorával teljesül. *Egyeztetendő:* a DT226 „a dataset README-je” helyet ír elő. A brief `ir` listájában nincs dataset-README (`konkordancia/KJV_teljes_szoveg_README.md`), csak a `SEMA.md`. Vagy az `ir` bővül, vagy a `SEMA.md` dataset-leírása tölti be ezt a szerepet.

## 6. Egyéb megfigyelések

- A brief 3. pontjának „várt mérete” (31 102 kanonikus vers, 31 099 címkés, 3 címke nélküli, + 0. versek) az új csomagon pontosan teljesül; a 0. versek száma 116.
- A `\s1`-es páli utóiratok és a Zsolt 119 fejlécei a `KJV_Strongs_teljes.tsv`-t nem érintik (a címke nélküli szöveg nem került bele), az új datasetet viszont igen. Ezért kell a `\s1` külön kezelése.
- A DT226 még nincs a main-en. Ha a #107 nem mergelődik, a DT212 tárgytalanná válik, és a brief 3. pontja marad érvényben.
