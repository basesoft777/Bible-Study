# BDB_SZELETELO — M0: aranyminta és mérések (F99.1–F99.3)

*Feladat: FELADATOK #99 (`F99_BDB_SZELETELO_BRIEF.md`), ág: `claude/bdb-szeletelo`. Modell: `claude-opus-5-5` (a brief `modell: opus` mezőjével egyezik). Állapot: az M0 1–3. lépése kész, a 4. lépés (OSHL `<etym>`) nem futott (6. szakasz), az 5. lépés döntései a `DONTESEK.md`-ben (DT-F99a–f). Eszköz: `eszkozok/olvaso_pilot/bdb_szelet_m0.py` (csak olvas; `--dump`, `--arany`, `--hivatkozas`, `--jelolo`).*

## 1. Eredmény röviden

- **Aranyminta** (`adat/bdb_aranyminta.tsv`, SEMA 2.28): 32 szócikk, 14 magyar fordítással is; benne a beszélgetés nyolc szócikke. A minta a mérések előtt készült, a szócikkek szövegének olvasásából; a független ellenőr átnézte (`naplok/ELLENOR_F99_minta.md`: 11 eltérés, 5 bizonytalan pont), a felhasználó döntései szerint javítva (F99.6, 2.4): 658 sor, ebből 607 `fuggetlen_ellenor`, 51 `modell_ellenorizetlen` (az új vagy javított sorok a H6440, H7307, H0430-on kívül; a három szócikket a felhasználó a második ellenőrzés alapján elfogadta, F99.7).
- **A mai szeletelő az aranymintán** (a javított mintán): szerkezeti eltérés nélkül 15 / 32 szócikk angolul, 7 / 14 magyarul; a használati csoportokat (184 várt csoport) egyáltalán nem bontja; a jelentéscímek 169 / 195 (magyar) és 24 / 43 (angol) esetben egyeznek. A 0 eltérés feltétele messze van; a hibák hét osztályba esnek (2.3).
- **Hivatkozások** (angol BDB, 8099 szócikk): 160 459 hivatkozás 8025 szócikkben — 107 321 kiírt könyvvel, 42 397 örökölt, 10 738 vesszős vers-folytatás, 3 feloldhatatlan. Álhivatkozás-jelölt 1062 (368 nem bibliai mű, 253 tapadt sigla, 441 közeli sigla), és 790 a nemi tanú („noun masculine^Gen 1:27”), amely **valódi** bibliai hivatkozás. Az MT → Károli átkulcsoláshoz a brief forrása, a `Karoli_versmegfeleltetes.tsv`, a hivatkozások 89%-ánál (141 959) nem ad MT-számot; a Macula `karoli` oszlopa mindenre ad, de ismert hibás régiókkal (DT-F99a).
- **Bevezetők** (angol): a csoport-bevezetők túlnyomó része mondatkezdő vagy vessző utáni helyzetben áll, jelentéshatáron ritkán; az „absolute” 663-szor az alaktanban (status absolutus) áll, nem használati csoport. A kész magyar szócikkekben ugyanannak a bevezetőnek két-három alakja él (followed by: „utána” 527, „követi” 302, ragos héber 460), és az angol–magyar szám szócikkenként ritkán egyezik (DT-F99b).

## 2. Aranyminta (M0.1)

### 2.1 Összetétel és módszer

| Csoport | Szócikkek |
|---|---|
| a beszélgetés nyolc szócikke (mind magyarul is) | H1242 בֹּקֶר, H0776 אֶרֶץ, H7451 רַע, H3615 כָּלָה, H0559 אָמַר, H6440 פָּנֶה, H7307 רוּחַ, H0430 אֱלֹהִים |
| további magyar (az F60.35 átnézés nehéz esetei) | H7121, H0157, H3027, H0834, H2490, H1157 |
| csak angol: több törzsű ige | H3176, H5203, H6504, H4900, H8213 |
| csak angol: homonima-sor, jelöletlen második címszó | H6696 (II–IV), H4686, H4060, H5766 (עָוֶל + עַוְלָה), H8213 (+ arámi שְׁפֵל) |
| csak angol: arámi ige | H1124, H5648, H2939 |
| csak angol: főnév, tulajdonnév, csonk | H5145, H4111, H5022, H0196, H0382, H5379 |

Az eljárás: a `--dump` a szócikk szövegét a jelölő-jelöltek (gondolatjel, törzsnév, szám, betű, római címszó) előtt tördelve és a csoport-bevezető jelöltekkel írta ki; a várt szerkezetet ebből, a szöveg olvasásával rögzítettem, angolul és (ahol van) magyarul. A szeletelő mai kimenete a dumpban látszott, de nem forrása a mintának; ahol eltért, a szöveg döntött (pl. H5203: a „(on ground, compare Niph`al 1)” hivatkozás, nem törzsfejléc). A minta szintjei: szócikk (címszó, homonima-szám), szakasz, törzs, jelentés, alpont, csoport; minden csomóponthoz szövegkezdet (horgony) és jelentéscím. Ahol a forrás hiányos (H0834 שֶׁ: a 3. jelölő hiányzik, a „b.” kétszer áll), `kihagy` sor zárja ki a részfát, okkal.

**A csoport-sorok** a DT-F99b előtti, szigorú jelöltlistán állnak: mondatkezdő (`;` `.` `:` `—` után) `absolute`, `followed by`, `with` + héber / accusative / suffix, `figurative`, `Inf. abs. as adverb`, `in phrase(s)`, `opposed to`, `especially`, valamint a zárójeles harmadik szint `(1)`, `(a)`. Az alpont első tagmondata (pl. H1242 1/e „opposed to עֶרֶב”) az alpont feje, nem csoport; a „so” és az „also” nem nyit csoportot (a BDB-ben a felsorolt igehelyek folytatása). Ha a DT-F99b mást dönt, a csoport-sorok átírandók (a többi szint független tőle).

### 2.2 Összevetés a mai szeletelővel

`# Aranyminta-összevetés: scope=adat/bdb_aranyminta.tsv (32 szócikk, F99.6-os javított minta) × bdb_szelet.szeletel | forras=BDB_teljes_unabridged.tsv@d4b15b2faea6 + forditasok.tsv@f01130a1be9a + bdb_szelet@9f3f57ab | ts=2026-10-15T14:50` (az első, javítás előtti futás: `edf8ce69`, 2026-10-15T14:00: eltérés nélkül 16 / 32 és 7 / 14, 151 csoport) (WSL venv, a címekhez a szerver `blokkok._fo_cim` és `jelentes_cim` függvénye)

| Strong | várt csomópont | csoport | EN szerkezeti eltérés | HU szerkezeti eltérés | HU/EN cím-eltérés |
|---|---|---|---|---|---|
| H0196, H0382, H5379 | 0 | 0 | 0 | — | 0 |
| H5022 | 0 | 0 | 1 (fölösleges 1) | — | 0 |
| H4111 | 2 | 0 | 0 | — | 1 |
| H2939 | 1 | 0 | 1 (hiányzik 1) | — | 0 |
| H3176 | 8 | 5 | 2 (hiányzik 2) | — | 2 |
| H5203 | 9 | 0 | 0 | — | 3 |
| H6504 | 10 | 1 | 5 (hiányzik 3, fölösleges 2) | — | 0 |
| H4900 | 10 | 1 | 2 (hiányzik 2) | — | 1 |
| H6696 | 7 | 6 | 1 (fölösleges 1) | — | 2 |
| H4686 | 3 | 0 | 0 | — | 1 |
| H5145 | 7 | 0 | 0 | — | 1 |
| H5766 | 4 | 0 | 7 (hiányzik 4, fölösleges 3) | — | 0 |
| H8213 | 10 | 1 | 3 (hiányzik 2, fölösleges 1) | — | 3 |
| H4060 | 5 | 0 | 0 | — | 2 |
| H1124 | 2 | 3 | 0 | — | 0 |
| H5648 | 6 | 0 | 0 | — | 3 |
| H1242 | 10 | 6 | 0 | 0 | 2 |
| H0776 | 22 | 2 | 0 | 0 | 3 |
| H7451 | 22 | 7 | 8 (hiányzik 8) | 8 (hiányzik 8) | 1 |
| H3615 | 23 | 13 | 12 (hiányzik 7, fölösleges 5) | 0 | 1 |
| H0559 | 8 | 11 | 5 (hiányzik 4, rossz kezdet 1) | 1 (hiányzik 1) | 2 |
| H6440 | 45 | 35 | 40 (hiányzik 31, fölösleges 9) | 40 (hiányzik 31, fölösleges 9) | 1 |
| H7307 | 40 | 7 | 0 | 0 | 1 |
| H0430 | 15 | 4 | 0 | 0 | 3 |
| H7121 | 43 | 20 | 0 | 0 | 5 |
| H3027 | 34 | 33 | 28 (hiányzik 24, fölösleges 4) | 28 (hiányzik 24, fölösleges 4) | 3 |
| H0834 | 50 | 16 | 31 (hiányzik 29, rossz kezdet 2) | 30 (hiányzik 29, rossz kezdet 1) | 1 |
| H2490 | 30 | 4 | 6 (hiányzik 4, fölösleges 2) | 9 (hiányzik 7, fölösleges 2) | 1 |
| H1157 | 5 | 2 | 1 (rossz kezdet 1) | 1 (rossz kezdet 1) | 1 |
| H0157 | 10 | 7 | 1 (rossz kezdet 1) | 0 | 1 |

Összesen: szerkezeti eltérés nélküli szócikk angolul 15 / 32, magyarul 7 / 14; eltérés 173 (EN) és 143 (HU) — benne a címek; csoport: 184 várt, 0 bontva. A cím-eltérés a megjelenített nyelven számít (a magyar fordítású szócikkeknél magyarul).

### 2.3 A hibaosztályok (a minta szövegéből)

1. **Pont nélküli személyszám jelentés-sorszámnak** (az F60.35 szabálya csak a ponttal álló alakot zárja ki): H3615 EN („3 feminine singular”, „1 singular”), H0157 EN („1 singular אֵהָ֑ב”), H1157 („1 plural בַּעֲדֵנוּ”, magyarul is), H6696 IV („1 singular suffix”). A magyar fordítás ponttal írja, ezért magyarul a H3615 és a H0157 helyes.
2. **Könyvnév része jelölőnek** („1 Kings 21”, „1 Samuel 14”, „2 Chron”): H5022, H0559 EN (az igazi 1. jelentés „263.1Say” tapadt alakban áll, az „1 Kings 5:19” lett az 1.).
3. **Törzsfejléc írásjel nélkül**: igehely vagy idézet után (H6504 „Est 3:8 Hiph`il Perfect”, H0559 „… to God.' Hiph`il Perfect”), illetve a szófaj után az egyetlen törzs (H2939 „verb Pa`el feed”). A H6504-ben a Hiph`il két jelentése a Pu`al alá került.
4. **Jelölő hivatkozó törzsnév után**: H4900 „compare Niph`al 6. trail seed” — a 6. és 7. Qal-jelentés elvész (az 5.-be olvad).
5. **Jelöletlen második címszó** (római szám nélkül, mondat közben: nőnemű alak, al-címszó, arámi címszó): H5766 עַוְלָה, H7451 רָעָה, H8213 שְׁפֵל, H3027 יַד, H0834 בַּאֲשֶׁר / מֵאֲשֶׁר / כַּאֲשֶׁר / שֶׁ. A számozott jelentések a fő címszóhoz kerülnek, vagy elvesznek. **Római homonima-fej előfordulásszámmal** („II. רַע_126 noun”, magyarul „II. [חלל] denominativum ige”): a `CIM` minta nem ismeri fel (H7451, H2490 HU). **Fő rész római számmal** (H6440 „II. מְּנֵי with prepositions”): nem homonima, de a számozás újraindul; a mai szeletelő a II. 1–8-at az I. 7–8 alá teszi.
6. **Elveszett számozott jelentések** a sorrend-feltétel miatt: H3027 4–5 (a „4 יָד is used…” nem jelölő a szeletelőnek), H2490 III Hiph`il 2, a tapadt alpont-jelölő („c.as to hands”, H3027 1/c).
7. **Csoport és cím**: csoportbontás nincs. A cím-eltérések jellemzően: a cím a használati megjegyzést is viszi („wait, tarry for, followed by לְ”, „make, accusative of thing”); a `=` határ levágja a jelentést („Képletesen = erő, hatalom” → „Képletesen”); a héber szó a címben megszakítja („jelenlét, személy, a ׳י-é” → „jelenlét, személy, a”); a szó eleji zárójel kiesik („(szél)irány” → „irány”); igehellyel vagy héberrel kezdődő jelentésnél a cím a kettőspont előtti egy szó („all Isaiah”).

8. **(F99.6) OCR-torzult jelölők**: a forrásban a jelölő tapadt vagy torzult alakban áll (`-1בְּיַד`, `-2אֶליַֿד`, `3as a conjunction`, `(β)`, `(ε)`); a felhasználó döntése szerint ezek jelölők (H3027 5/a–5/h, H0834 שֶׁ 3., H0430 4/b, H6440 II 7/a). A H3176 Hiph`il két számozatlan, önálló jelentése (`okkod=szamozatlan_jelentes`) a szeletelőnek egy szövegtömb.

**Ami jó:** a számozott jelentések és alpontok az egyszerű főnévi és igei szócikkekben (H1242, H0776, H7307, H0430, H7121, H5145, H4060, H5648) hibátlanok mindkét nyelven; a szakasz-felismerés a szabályos „II. <héber> noun” fejeknél (H4686, H4060, H6696) működik.

### 2.4 A független ellenőrzés és a javítás (F99.5–F99.6)

A független ellenőr (`naplok/ELLENOR_F99_minta.md`) 11 eltérést (E1–E11) és 5 bizonytalan pontot (B1–B5) talált; a felhasználó döntései (2026-10-15) szerint a minta javítva (`adat/bdb_aranyminta.tsv`, 622 → 658 sor):

| Szócikk | Változás | Döntés |
|---|---|---|
| H3027 | 5/a: (1), (2) csoport (az 5/b-ből átkerült (1) és az OCR-alakú `-2`); 5/b: (1)–(4) (az OCR-alakú `-1`, `-2`); 5/g, 5/h: a `-2` (2) csoport; a hamis „a (2) hiányzik” megjegyzések törölve; 5/c (4): a horgony „(4) בְּיַד”, a hamis „nincs szóköz” megjegyzés törölve | E1, B5 (498) |
| H0834 | שֶׁ: saját 3. jelentés („3as a conjunction”, magyarul „3kötőszóként”) 3/a, 3/b alponttal és a 3/a (a), (b) csoportjával; a két `kihagy` sor és a hamis „hiányzik” indok törölve; a שֶׁ 1. megjegyzése javítva („see מָה 1e b.”); zárójeles csoport: 2. (a)(b), 4/b (a)(β)(γ)(δ) (a `kihagy -/4/b` helyett), 6. (a)(b)(c), 8/a (a)(β)(γ), שֶׁ 4/b (a)(b) | E2, E3, B5 (562) |
| H0430 | az „(a) angel / (b) prophet” a 3. jelentés csoportja (nem a 2/b-é); 4/b (β) csoport | E4, E5 |
| H6440 | II 7/a (ε) csoport; II 1/a „with יָצָא” csoport | E6, E7 |
| H2490 | III Hiph`il 2: négy „with” csoport (Infinitive, ו consecutive, בְּ, מן) | E8 |
| H1157 | 2: „with כִּמֶּר” és „With לְ ׳מִבַּעַד” csoport | E9 |
| H7307 | 4/d „especially 104:29” csoport | E10 |
| H7121 | Qal 4/a „with acc of roll, book” csoport (az „acc” = with accusative) | E11 |
| H5766 | „I. עַלְוָה transposed from עַוְלָה”: `utalo` sor (`okkod=utalo_cimszo`), nem szakasz | B1 |
| H1242 | 1/b „& especially” csoport (a „; &” mondatkezdő) | B2 |
| H3176 | Hiph`il: két számozatlan jelentés (`Hiph'il/-1` „wait, tarry”, `Hiph'il/-2` „wait for, hope for”), `okkod=szamozatlan_jelentes`; az „absolute hope” csoport a második alá | B4 |
| H0559 | Qal/4 megjegyzés: „compare 1 Kings 5:20” könyvnév | B5 (234) |

**B3 (H6696 Qal/2, a felhasználó döntése: marad).** Az első „with עַל of city” vessző után áll („shut in, besiege, with עַל of city”), ezért a csoportszabály szerint nem csoport, hanem a jelentés fejének része; a párhuzamos négy tag („; with עַל person”, „; with אֶל of city”, „; with אֶל person”, „; with אֵת of city only”) mondatkezdő, ezért csoport. A minta szabálykövető, de **aszimmetrikus**: az olvasó négy csoportot lát, az ötödik párhuzamos használat a fejben marad. Ha a megjelenítés (M4) ezt zavarónak mutatja, a csoportszabály (DT-F99b (1)) módosítása a helye, nem a mintáé.

Az ellenőrzés jelölése (`ellenorzes`): a többi szócikk változatlan sora `fuggetlen_ellenor`, az új vagy javított sorok `modell_ellenorizetlen`; a H6440, H7307, H0430 a F99.6-ban `modell_ellenorizetlen` volt, a felhasználó a második ellenőrzés alapján elfogadta, ezért a F99.7-től minden soruk `fuggetlen_ellenor` (607 / 51).

**Határeset (H0430 3.; a felhasználó döntése, 2026-10-15: marad csoport nélkül).** A 3. jelentésben álló „in many phrases” nem csoport: a DT-F99b (1) (a) listája szó szerinti (`in phrase(s)`), a „many” közbeékelt jelzővel álló alak nem illeszkedik. Ha az M3 bevezető-felismerése ezt is fogná, a minta e pontja átírandó.

A H0430 1/a megjegyzése javítva (F99.7): a `cim` mező üres, a cím nem vizsgált (a korábbi „a cím a kettőspontig” pontatlan volt). `felhasznalo`-t a modell nem ír. Minden nem üres horgony (1017) a forrásszövegben megvan (pontozás nélkül, NFC).

## 3. Hivatkozás-mérés (M0.2)

`scope=angol BDB, minden szócikk (8099); hivatkozás = könyvvel kiírt vagy könyv nélküli fejezet:vers, és a vesszős vers-folytatás | forras=BDB_teljes_unabridged.tsv@d4b15b2faea6 + bdb_konyv_javit.TOKEN/CSUPASZ/LEK/LANCTORO + Macula_heber_* (MT-versek, MT→Károli) + bdb_szelet_m0@edf8ce69 | ts=2026-10-15T13:59`

| Tétel | Érték |
|---|---|
| hivatkozás összesen / szócikk hivatkozással | 160 459 / 8025 (a 8099-ből) |
| kiírt könyvvel / örökölt / vers-folytatás („18:18, 25”) / feloldhatatlan (könyv nincs előtte) | 107 321 / 42 397 / 10 738 / 3 |
| nem bibliai mű (Talmud, Korán, apokrif, kommentár-sigla a `LANCTORO`-ból és az utánuk örökölt) | 368 |
| többértelmű könyvalak (Kings, Sam, De, Jes …) / ismeretlen alak | 19 / 2 |
| sigla: a hivatkozás a `^`-hoz tapad („De^Job 34:36”, „COT^Gen 23:16”, „Dr^1Sam 10:19”) | 253 |
| sigla: `^`-os szó a megelőző két szóban („Dl^w); city Ezek 26:17”, „Schr^COT Judges 1:37”) | 441 |
| nemi tanú („noun masculine^Prov 14:4”: hol igazolt a nem) — **bibliai hivatkozás** | 790 |
| ÓSZ-hivatkozás (bibliai, feloldott) / ÚSZ | 159 978 / 89 |
| MT-ben nem létező vers (Macula versei; kiírt 451, örökölt 109, folytatás 9) | 569 |
| Károli-versmegfeleltetés: MT-osztályú sor (MT = Károli) | 11 020 |
| Károli-versmegfeleltetés: KJV-osztályú sor, **MT-szám nincs** a táblában | 141 959 |
| Károli-versmegfeleltetés: KEZI-osztályú sor / nincs sor az MT-kulcsra | 2 176 / 4 254 |
| Macula `karoli`: azonos vers / más Károli-vers / nincs Károli-megfelelő | 150 781 / 7 256 / 1 372 |
| független próba: az OSHL BDB-XML strukturált igehelyei közül megvan a feloldásban | 3191 / 3515 (90,8%) |

Megjegyzések:
- **Az előzetes mérés** (a brief 2. lépése: 150 082 hivatkozás; 103 293 kiírt, 46 438 örökölt, 351 feloldhatatlan) más határokkal készült; a vers-folytatás nélkül itt 149 721. A feloldhatatlan 3 (nem 351), mert a könyvet a szócikk elejéig visszafelé öröklöm, és a nem bibliai alak is lánc-elem (utána az öröklés `nem_bibliai`).
- **A hiányzó OSHL-helyek** (9%) mintája: egyfejezetes könyv fejezet nélkül („Obad 8”: a mai minta nem ismeri fel), és a két forrás eltérése (H0012: BDB „8:6”, OSHL „8:8”; H0033: BDB „8:32”, OSHL „8:52”). A pontos arány az M2 200-as mintáján mérendő.
- **MT → Károli.** A `Karoli_versmegfeleltetes.tsv` MT-oszlopa csak az MT-osztályú (Károli = MT) sorokban áll; a KJV-osztályú versekben, ahol a Károli a KJV számozását követi, az MT-szám hiányzik, pedig az MT ≠ KJV helyek ide esnek (1Krón 6, 1Móz 32, 2Sám 19, 5Móz 13/23/29, Jóel, Mal, Jób 40–41 stb.). A Macula `karoli` oszlopa minden MT-szóhoz ad Károli-verset, és a BDB-hivatkozások MT-osztályú versein egyszer sem mond ellent a táblának; a hibás régiói ismertek (`naplok/F85_jelentes.md`: Ézs 3, Ézs 9, Én 6, Hós 2, 12; N-F85b). Néhány eltolás gyanús (Préd 9 +2, Préd 10 −3, Neh 4 +6), ezeket a Macula-oszlop javítása nélkül nem minősítem.
- **A BDB az MT számozását követi** (pl. „Malachi 3:19”, „Gen 32:1” a „he rose early” sorban, „Hosea 12:15”), ezért az átkulcsolás szükséges.

## 4. Jelölő-mérés (M0.3)

`scope=angol BDB (8099 szócikk) és magyar BDB (674 szócikk, a szerver bdb_magyar-szabálya); helyzet a mai szeletelő csomópontjaihoz képest | forras=BDB_teljes_unabridged.tsv@d4b15b2faea6 + forditasok.tsv@f01130a1be9a + bdb_szelet@edf8ce69 | ts=2026-10-15T13:59`

A helyzet: *csomópont eleje* (a jelentés vagy alpont első szava), *mondatkezdő* (`;` `.` `:` `—` után), *vessző után*, *mondat közben*, *zárójelben*, *alaktan* (az első törzs vagy jelentés előtt). A szeletelő hibái (2.3) a helyzet-besorolást kis mértékben torzítják.

**Angol (8099 szócikk)**

| bevezető | szócikk | össz | csomópont eleje | mondatkezdő | vessző után | mondat közben | zárójelben | alaktan |
|---|---|---|---|---|---|---|---|---|
| absolute | 1986 | 2913 | 57 | 956 | 223 | 845 | 169 | 663 |
| followed by | 435 | 1709 | 53 | 563 | 396 | 292 | 372 | 33 |
| with + héber | 944 | 2637 | 87 | 854 | 527 | 523 | 553 | 93 |
| with accusative | 418 | 1079 | 56 | 321 | 441 | 157 | 80 | 24 |
| with infinitive | 34 | 36 | 4 | 12 | 6 | 10 | 3 | 1 |
| with suffix | 112 | 131 | 4 | 33 | 15 | 38 | 18 | 23 |
| Inf. abs. (as adverb) | 291 | 406 | 15 | 266 | 6 | 59 | 49 | 11 |
| in phrase(s) | 150 | 162 | 11 | 29 | 21 | 94 | 4 | 3 |
| figurative | 1111 | 1962 | 173 | 481 | 249 | 310 | 689 | 60 |
| opposed to | 448 | 798 | 7 | 82 | 67 | 38 | 576 | 28 |
| especially | 772 | 1249 | 46 | 312 | 295 | 220 | 230 | 146 |
| also | 1932 | 3817 | 5 | 735 | 348 | 1471 | 829 | 429 |
| so | 1927 | 3391 | 4 | 776 | 920 | 352 | 1058 | 281 |
| often | 434 | 904 | 21 | 118 | 45 | 459 | 188 | 73 |
| rarely | 94 | 120 | 13 | 28 | 11 | 26 | 24 | 18 |
| (n) zárójeles szám | 151 | 509 | 0 | 0 | 0 | 0 | 496 | 13 |
| (a) zárójeles betű | 84 | 485 | 0 | 0 | 0 | 0 | 476 | 9 |

**Magyar (674 szócikk)**

| bevezető | szócikk | össz | csomópont eleje | mondatkezdő | vessző után | mondat közben | zárójelben | alaktan |
|---|---|---|---|---|---|---|---|---|
| abszolút használatban | 174 | 469 | 35 | 214 | 122 | 42 | 46 | 10 |
| abszolút (egyéb) | 11 | 13 | 0 | 3 | 1 | 2 | 5 | 2 |
| status absolutus | 247 | 322 | 5 | 55 | 7 | 47 | 5 | 203 |
| utána | 103 | 527 | 24 | 202 | 121 | 54 | 113 | 13 |
| követi | 65 | 302 | 4 | 64 | 42 | 122 | 67 | 3 |
| ragos héber (-val/-vel) | 80 | 460 | 9 | 121 | 48 | 185 | 90 | 7 |
| tárgyesetével | 117 | 498 | 31 | 6 | 11 | 423 | 27 | 0 |
| infinitivus absolutus | 133 | 221 | 2 | 160 | 4 | 24 | 29 | 2 |
| kifejezésekben / fordulatokban | 97 | 146 | 1 | 2 | 1 | 131 | 10 | 1 |
| átvitt értelemben | 145 | 406 | 52 | 102 | 39 | 45 | 157 | 11 |
| képletesen | 66 | 172 | 19 | 54 | 18 | 27 | 53 | 1 |
| ellentéte | 115 | 283 | 1 | 34 | 20 | 33 | 190 | 5 |
| szemben | 34 | 54 | 0 | 3 | 6 | 33 | 9 | 3 |
| különösen | 373 | 852 | 58 | 306 | 220 | 101 | 110 | 57 |
| továbbá | 325 | 861 | 3 | 472 | 196 | 47 | 62 | 81 |
| így | 454 | 1427 | 0 | 430 | 422 | 154 | 323 | 98 |
| gyakran | 256 | 664 | 19 | 99 | 38 | 343 | 126 | 39 |
| ritkán | 102 | 156 | 14 | 35 | 7 | 32 | 43 | 25 |
| (n) zárójeles szám | 95 | 412 | 0 | 0 | 0 | 0 | 403 | 9 |
| (a) zárójeles betű | 64 | 398 | 0 | 0 | 0 | 0 | 388 | 10 |

**Az angol–magyar szám szócikkenként** (a kész magyar szócikkek, jelentésrégió, zárójelen kívül; „azonos” = ugyanannyi bevezető mindkét nyelven, legalább egy):

| angol | magyar megfelelő | azonos | eltérő | egyik sem |
|---|---|---|---|---|
| absolute | abszolút használatban / abszolút | 80 | 205 | 389 |
| followed by | utána / követi | 85 | 66 | 523 |
| figurative | átvitt értelemben / képletesen | 155 | 73 | 446 |
| opposed to | ellentéte / szemben | 43 | 54 | 577 |
| especially | különösen | 236 | 94 | 344 |
| in phrase(s) | kifejezésekben / fordulatokban | 47 | 52 | 575 |
| Inf. abs. (as adverb) | infinitivus absolutus | 123 | 5 | 546 |

Olvasat:
- A csoportok határa a BDB-ben **a mondatkezdő helyzet** (`;` után); jelentéshatáron a bevezető ritka (absolute 57, followed by 53). A vessző utáni és mondat közbeni előfordulások többnyire egy igehely-felsorolás belső megjegyzései, nem csoportfejek: a biztonságos szabály a mondatkezdő helyzet.
- Az **„absolute”** kétértelmű: 663 az alaktanban (status absolutus), és a jelentésrégióban is áll főnévi alaknévként („— absolute ׳ר Gen 26:29”, H7451 רָעָה). Ez a DT27 kapu nélküli döntésének oka; csoport-bevezető csak a jelentésrégióban és igei szócikkben, vagy a magyar „abszolút használatban” alakkal azonosítható.
- A **„so” és „also”** a leggyakoribb mondatkezdő szavak, de felsorolás-folytatók; csoportnak venni hamis határt adna (a 3391 + 3817 előfordulásból 1511 mondatkezdő).
- A **zárójeles harmadik szint** (`(1)`, `(a)`) mindig zárójelként mérődik (a szeletelő zárójel-felismerője a nyitó zárójel miatt), de a minta szerint valódi tagolás (H3615 Pi`el 2c, H6440 II 4a, H7121 Niph`al 2d).
- A magyarban **a followed by háromféleképpen** áll („utána” 527, „követi” 302, és a magyar ragozás miatt a „+ X-val” alak 460), a figurative kétféleképpen („átvitt értelemben” 406, „képletesen” 172), az opposed to kétféleképpen („ellentéte” 283, „szemben” 54). A „with + héber” csoportnak nincs magyar bevezetője (a magyar ragoz: „עַל-val”). Az M3 egyező-szám szabálya a mai fordításon a csoportok kisebbik részét bontaná.

## 5. OSHL `<etym>` (M0.4) — nem futott

A `LexicalIndex.xml` (OSHL @ `21c9add13bc727d3a951361778e97e3ff7afd1ce`, sha256 `8f7a605c…`) nincs a gépen (repó, `D:\`, WSL-home és ideiglenes könyvtárak átnézve); a repóban csak a belőle generált `OSHL_lexikalis_index.tsv` és `OSHL_BDB_igehelyek.tsv` van, egyikben sincs `<etym>`. A letöltés (`python eszkozok/oshl_index_import.py --letolt`: a GitHub codeload tarball a rögzített commitról, SHA-ellenőrzéssel) felhasználói engedélyt kíván, ezért nem indítottam: DT-F99f. Az engedély után a mérés (main / sub / single darabszám, a sub-célok feloldhatósága a Strong-kulcsainkra, a לַיְלָה H3915 családja) a #99 ágán pótolható, mielőtt az M1 indul.

**Az M0.4 előkészítése (F99.7, DT-F99f (b) után; a letöltés még nem indult).** A forrás adatai a GitHub git-fa API-jából (`gh api repos/openscriptures/HebrewLexicon/git/trees/21c9add13bc727d3a951361778e97e3ff7afd1ce`: csak metaadat, fájltartalom nélkül):

| Tétel | Érték |
|---|---|
| repó, commit | `openscriptures/HebrewLexicon` @ `21c9add13bc727d3a951361778e97e3ff7afd1ce` (2019-09-02T22:24:11Z) |
| útvonal | `LexicalIndex.xml` (a repó gyökerében) |
| méret | **1 782 592 bájt** (kb. 1,7 MiB) |
| git blob SHA-1 | `d11eb2078532f3119c70822bd27a91b484d4727b` |
| várt SHA-256 (`oshl_index_import.py`, `LEXICAL_INDEX_SHA256`) | `8f7a605c58899d2f44430149c143c00903976e1e91232476677972a69e5bc85f` |
| letöltési út (DT-F99f (b)) | `https://raw.githubusercontent.com/openscriptures/HebrewLexicon/21c9add13bc727d3a951361778e97e3ff7afd1ce/LexicalIndex.xml`, a repón kívüli ideiglenes könyvtárba; utána a git blob SHA-1 és a SHA-256 ellenőrzése, eltérésnél megállás |

`scope=openscriptures/HebrewLexicon git-fa a rögzített commiton | forras=GitHub REST API git/trees + commits | ts=2026-10-15`

## 6. Mellékes leletek

- A `Karoli_versmegfeleltetes.tsv` MT-oszlopa csak az MT-osztályú sorokban áll (KJV-osztályú sorban üres) — az MT → Károli átkulcsolásnak önmagában nem elég forrása (DT-F99a).
- A Macula `karoli` oszlopának gyanús eltolásai (Préd 9, 10, 12; Neh 4) az N-F85b körébe tartoznak, ott nyitottak.
- Az OSHL BDB-XML és a BDB-szöveg néhol eltér (H0012, H0033): az OSHL nem aranyminta, csak független próba.
- A brief N-F99a (translationWords nyers Markdown) és N-F99b (OSHL-táblázat mobilon) a záráskor kerül a `NYITOTT_FELADATOK.md`-be.

## 7. Döntési kérdések (⛔, `DONTESEK.md`)

- **DT-F99a** — álhivatkozás-szűrés és MT → Károli átkulcsolás (3. szakasz).
- **DT-F99b** — a csoport-bevezetők listája, kötelező magyar alakja, kapu, időzítés a #38-ban, a kész 674 szócikk (4. szakasz).
- **DT-F99c** — a szeletelő helye élesben.
- **DT-F99d** — a modell-magyarázat teljes futása (az M6 mérése után dönthető; most előjegyzés).
- **DT-F99e** — az aranyminta átnézése (a „0 eltérés” mércéje csak ellenőrzött mintán értelmes). Eldöntve (b): a független ellenőr átnézte (F99.5), a minta a felhasználó döntései szerint javítva (F99.6, 2.4); a H6440, H7307, H0430 felhasználói átnézése nyitott.
- **DT-F99f** — a `LexicalIndex.xml` letöltése az M0.4-hez és az M1-hez.

## 8. Reprodukálás

```
python eszkozok/olvaso_pilot/bdb_szelet_m0.py --hivatkozas
python eszkozok/olvaso_pilot/bdb_szelet_m0.py --jelolo
wsl -d pardes -e bash -lc 'cd /mnt/c/Users/bases/Desktop/Bible-Study && ~/pardes/eszkozok/olvaso_szerver/.venv/bin/python eszkozok/olvaso_pilot/bdb_szelet_m0.py --arany'
python eszkozok/olvaso_pilot/bdb_szelet_m0.py --dump H1242 --nyelv hu --ki <könyvtár>
```

A `--arany` Windows-Pythonnal is fut, de a szerver `blokkok` modulja nélkül (nincs `markupsafe`) a címek összevetése kimarad, és ezt kiírja. Az eredmények determinisztikusak (a `ts` mezőn kívül); a fenti számok a `edf8ce69` állapoton futottak.
