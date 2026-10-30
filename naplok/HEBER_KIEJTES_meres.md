# Gépi magyaros héber kiejtés — pontosságmérés (N-F131w, DT426 utóhang)

*Mérés, nem átállás. Adat (`adat/`) nem változott, lexikonlap nem generálódott újra, a szkript nincs bekötve a lapokba. Az átállásról a felhasználó dönt (⛔).*

- **Modell:** `claude-opus-5-5` (a session saját környezetéből)
- **Proveniencia:** `scope=adat/kiejtes_kivetelek.tsv (26 héber sor) + naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv (héber arany/valodi) + konkordancia/TBESH.txt + konkordancia/TAHOT_kivonat.tsv (ISTENTISZT-001 helyek) + konkordancia/OSHL_lexikalis_index.tsv | forras=naplok/HEBER_KIEJTES_meres.py | ts=2026-10-30`
- **Kimenetek:** `naplok/HEBER_KIEJTES_meres.tsv` (soronkénti tábla, A/B/C), `naplok/HEBER_KIEJTES_meres_osszesito.txt` (összesítő és STEP-proxy). Újrafuttatás: `python naplok/HEBER_KIEJTES_meres.py` (kb. 30 s).

## 1. Röviden

| Kérdés | Mért válasz |
|---|---|
| Pontos egyezés a jóváhagyott lemma-kiejtésekkel, pontozott héberből | **24/26 (92%) keresztellenőrizve** (leave-one-out); a 26-on kalibrálva 25/26 (96%); kétfelé osztva, 200 felosztás átlaga 90% (77–100%) |
| Ugyanez a STEP angolos átírásából | 14/26 (54%) leave-one-out; ékezet nélkül 21/26 (81%) — **a STEP nem jelöl hosszúságot, ezért nem alkalmas** |
| Független, régi kézi minta (46 alak, köztük ragozott és többszavas) | 44/46 (96%) pontos, nem erre kalibrálva |
| Ragozott alakok a valódi szövegben (299 TAHOT-token, ISTENTISZT-001 versei) | nincs arany; a STEP-pel összevetett mássalhangzó–magánhangzó vázban kézzel igazolt gépi hiba 5 token (**~1,7%**), ha a szókezdő begadkefat a pontozás szerint dől el; a D34 „szókezdő → kemény” szabályával 12 token (~4%). A hosszúság (ékezet) itt nincs mérve. |

**A fő tanulság:** a 26 jóváhagyott alak *könnyű* eset. Egyikben sincs kámec kátán, nem szókezdő hangzó sevá, furtív patah vagy ketiv/qere. A 92% tehát a lemmákra érvényes. A ragozott alakok nehéz eseteit csak a proxy méri, és ott a hiba a kámec kátánban, a hosszú magánhangzó utáni sevában és a ketiv/qere-ben jelenik meg.

## 2. Előzmények, amelyek a mérést befolyásolják

1. **Nem 30, hanem 26 héber arany alak.** Az `adat/kiejtes_kivetelek.tsv` 29 adatsorából 3 görög, 26 héber (2 KIEJT-migráció: `qa.ra`, `shem`; 24 TBESH-lemma-kulcsos sor). A mérés a 26 héberen fut.
2. **Körkörösség.** A 26 alak a meglévő gépi jelöltgyártó (`eszkozok/heber_kiejtes_jeloltek.py`, OSHL-átírás + `adat/kiejtes_heber_jeloltszabalyok.tsv`, S1.7) kimenetéből került kézi jóváhagyásra (D34–D37, 2026.09.29). Ezen a halmazon az a gépezet 26/26-ot ad (a H2555 kézi kivétellel együtt), de ez **nem mérés**. Ezért két, ettől független utat mértem: a pontozott héber szöveget (NIQQUD) és a STEP-átírást.
3. **Az OSHL-gépezet csak lemmára működik.** Az OSHL `atiras` mező a lexikon címszavaié; ragozott alakra (amely a lapon a „szótári alak: …” jelölést kapja) nincs OSHL-átírás. A ragozott alakok gépi kiejtésének egyetlen helyi bemenete a TAHOT pontozott alakja (és a STEP `Kiejtés`).
4. **Volt már egy pesszimista próba** (S0.7, `naplok/SZOTAR_S0_heber_jeloltek.tsv`): nyers niqqudból 20/36 (56%). Ott a hibák fő oka a szóvégi néma hé és a vav mint magánhangzó-hordozó volt, és 3 szkripthiba. A mostani átíró mindkettőt szabályként kezeli.

## 3. Módszer

### 3.1 Arany-halmazok

| Halmaz | Mi | n | Konvenció | Szerep |
|---|---|---|---|---|
| **A** | `adat/kiejtes_kivetelek.tsv` héber sorai; a bemenet a TBESH-lemma (a két migrációs sornál az OSHL-lemma) | 26 | D34–D37 (ח → ch, rafés כ → ch) | kalibrálás + keresztellenőrzés |
| **B** | a régi, kézzel írt ISTENTISZT-001 lap héber párjai (`naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv`, `arany` + `valodi`), egyedi szó+kiejtés párok; kihagyva 13 pontozatlan vagy mássalhangzó-átírás (`שׁמה` → „smh”) és 6 kommentáros/rövidítéses pár | 46 | **D34/D35 előtti**: ח → h, rafés כ → k | független ellenőrzés: a négy konvenció-paraméter átállítva, kalibrálás nélkül |
| **C** | 20 ragozott TAHOT-alak az ISTENTISZT-001 helyeiről | 20 | — | **nincs arany**, kézi átnézésre |
| **proxy** | az ISTENTISZT-001 versek minden TAHOT-tokenje (H9xxx előtagok és STEP-csonkok nélkül) | 299 | — | a nehéz esetek nagyságrendje; a STEP maga is hibázik, ezért az eltéréseket kézzel soroltam be |

### 3.2 A két átíró út (`naplok/HEBER_KIEJTES_meres.py`)

**NIQQUD (pontozott héber → magyaros).** NFD-bontás, a kantilláció (U+0591–U+05AF) és az írásjelek törlése; a meteg megmarad, mert a sevá- és a kámec-döntéshez kell. A makkef szóhatár (`-`). Szabályok:

- **Matres lectionis.** A szóvégi néma hé és álef elmarad (mappik → h). A vav dágessel, magánhangzó nélkül, magánhangzótlan betű után surek (ú). A vav holammal vagy holam utáni néma vav holam male (ó). A jod hirek után í, cere után é, szegol után é (paraméter), kámec után a szóvégi `-ָיו` „-áv”; különben j.
- **Dáges.** Ha az előző betűnek ejtett magánhangzója van: forte, kettőzés (`ss`, `cc`, `ssz`). Szókezdő helyzetben vagy néma sevá után: lene.
- **Begadkefat.** Dágessel kemény (b, k, p). Dáges nélkül lágy (v, ch, f); a szókezdő dáges nélküli betű a D34 szerint kemény (paraméter: `pont_szerint` = a pontozás dönt).
- **Sevá.** Kiejtett (e): szókezdő helyzetben (az egybetűs előtagnál is), kettőzött betű alatt és két sevá közül a másodiknál. Néma: szóvégen és rövid magánhangzó után. Hosszú magánhangzó után a paraméter dönt (`meteg` / `hangzo` / `nema`).
- **Kámec.** Kátán (o), ha meteg nélküli, és a következő ejtett mássalhangzó néma sevás, vagy hátef-kámec követi (paraméter). Különben gádol (á).
- **Furtív patah.** Szóvégi ח/ע/הּ patahja nem a-jellegű magánhangzó után: az a a mássalhangzó elé kerül (paraméter).
- **Mássalhangzók.** Álef és ajin néma; שׁ s; שׂ sz (paraméter); ס sz (paraméter); צ c; ק k; ט/ת t; ו v; י j; ח ch (paraméter); a tetragramma JHVH (paraméter).
- **Magánhangzók.** Kámec á; patah és hátef patah a; cere é; szegol és hátef szegol e; hirek i; holam ó; kubbuc u; surek ú; hátef kámec o.

**STEP (angolos átírás → magyaros).** A szótagpont és a hangsúlyt jelölő nagybetű elhagyva, az aposztróf (álef/ajin) elesik. Cserék: sh → s, ts/tz → c, ch → ch, kh → ch, ph → f, q → k, y → j, w → v, ei → é; a szóvégi néma h elmarad. A hosszúságot a STEP nem jelöli, ezért heurisztika pótolja: nyílt szótagban a → á, zárt szótagban a → a, o → ó, u → ú, i és a zárt szótagbeli e paraméter.

### 3.3 Kalibrálás és keresztellenőrzés

Mindkét útnak véges paramétertere van: a NIQQUD-é 12 paraméter, 3 072 kombináció, a STEP-é 9 paraméter, 512 kombináció. Minden paraméter első értéke az **a priori** választás, amelyet a mérés előtt rögzítettem. A kalibrálás a legtöbb pontos egyezést adó kombinációt választja; holtversenynél azt, amelyik a legkevésbé tér el az a priori értéktől.

- *a priori:* kalibrálás nélkül;
- *kalibrált:* mind a 26-on hangolva, majd ugyanott mérve (optimista);
- *leave-one-out:* minden alakot a többi 25-ön hangolt paraméterekkel mérek;
- *kétfelé osztás:* 13 alakon hangolva, a másik 13-on mérve, 200 véletlen felosztás (seed 20261030) átlaga, minimuma és maximuma.

**Őszinteségi megjegyzés.** A paraméterek a tudatos döntéseket fedik le, a szabályok szerkezetét viszont én írtam, és közben láttam az A és a B halmazt. Ez a keresztellenőrzésben nem jelenik meg, ezért a lemma-számok felső becslésnek tekintendők. Két implementációs hibát a B első futása után javítottam: (a) az egybetűs `בְּ` sevája szóvégi helyzetként néma lett, holott szókezdő; (b) a csak sin-ponttal pontozott alak („שׁמה” → „smh”) bekerült, pedig mássalhangzó-átírás, nem kiejtés. A STEP-oldalon a kettőzött sz (`szsz` → `ssz`) és a szóvégi `-ai` → `-aj` javítás is az első futás után került be. A B tehát nem teljesen vak próba.

### 3.4 Egyezési szintek

- **pontos:** karakterre azonos;
- **ékezet nélkül:** az ékezetek (a magyar átírásban ezek a hosszúságjelek) elhagyva;
- **hossz nélkül:** az ékezetek elhagyva és a kettőzés összevonva (gemináció).

### 3.5 Hibaok-besorolás

Eltérésnél a szkript egyenként átfordítja a döntés-paramétereket. Az az ok, amelynek átfordítása egyezést ad, a hibaok (pl. „ḥ (ח) ch/h”). Ha egyik sem ad egyezést, a besorolás: „hosszúság” (ha hossz nélkül egyezik), különben „egyéb”. A proxy eltéréseit kézzel soroltam be (4.4).

## 4. Eredmények

### 4.1 Összesítés

| Halmaz / út / paraméterek | pontos | ékezet nélkül | hossz nélkül |
|---|---|---|---|
| A / NIQQUD / a priori | 24/26 (92%) | 24/26 (92%) | 24/26 (92%) |
| A / NIQQUD / kalibrált (mind a 26-on) | 25/26 (96%) | 25/26 (96%) | 25/26 (96%) |
| **A / NIQQUD / leave-one-out** | **24/26 (92%)** | | |
| A / NIQQUD / kétfelé osztás, 200× | átlag 90% (min 77%, max 100%) | | |
| A / STEP / a priori | 12/26 (46%) | 21/26 (81%) | 21/26 (81%) |
| A / STEP / kalibrált | 15/26 (58%) | 21/26 (81%) | 21/26 (81%) |
| **A / STEP / leave-one-out** | **14/26 (54%)** | | |
| A / STEP / kétfelé osztás, 200× | átlag 49% (min 15%, max 77%) | | |
| A / OSHL-gépezet (S1.7) — *körkörös, nem mérés* | 26/26 | | |
| B / NIQQUD / régi konvenció, B-n nem kalibrálva | 44/46 (96%) | 45/46 (98%) | 45/46 (98%) |
| B / STEP / régi konvenció (csak TBESH-lemmás egyszavasak) | 20/35 (57%) | 31/35 (89%) | 31/35 (89%) |
| B / OSHL-gépezet (S1.7) / régi konvenció (ahol a pontozott alak OSHL-lemma) | 32/36 (89%) | 32/36 (89%) | 32/36 (89%) |

A kalibrálás egyetlen NIQQUD-paramétert mozdított el az a priori értéktől: `szamech=s`. A STEP-nél is egyet: `e_zart=é`. A NIQQUD-út eredménye tehát lényegében az a priori szabálykészleté, a hangolás alig javít rajta.

### 4.2 A halmaz soronként

A gépi (niqqud) oszlop a 26-on kalibrált paraméterekkel készült, a LOO-kimenet az adott sor nélkül kalibrált paraméterekkel; a ✔/✘ hármas: pontos / ékezet nélkül / hossz nélkül.

| Strong | lemma | jóváhagyott | gépi (niqqud) | pontos / ékezet n. / hossz n. | hibaok | LOO-kimenet | gépi (STEP) | STEP-forrás | pontos / ékezet n. / hossz n. | hibaok (STEP) |
|---|---|---|---|---|---|---|---|---|---|---|
| H7121 | קָרָא | kárá | kárá | ✔ ✔ ✔ |  | kárá | kárá | `qa.ra` | ✔ ✔ ✔ |  |
| H8034 | שֵׁם | sém | sém | ✔ ✔ ✔ |  | sém | sém | `shem` | ✔ ✔ ✔ |  |
| H0127 | אֲדָמָה | adámá | adámá | ✔ ✔ ✔ |  | adámá | ádáma | `a.da.mah` | ✘ ✔ ✔ | hosszúság (a STEP nem jelöli) |
| H0430 | אֱלֹהִים | elóhím | elóhím | ✔ ✔ ✔ |  | elóhím | elóhim | `e.lo.him` | ✘ ✔ ✔ | hosszúság-heurisztika: i |
| H0779 | אָרַר | árar | árar | ✔ ✔ ✔ |  | árar | árar | `a.rar` | ✔ ✔ ✔ |  |
| H0922 | בֹּהוּ | bóhú | bóhú | ✔ ✔ ✔ |  | bóhú | bóhú | `bo.hu` | ✔ ✔ ✔ |  |
| H1121 | בֵּן | bén | bén | ✔ ✔ ✔ |  | bén | bén | `ben` | ✔ ✔ ✔ |  |
| H2403 | חַטָּאָה | chattáá | chattáá | ✔ ✔ ✔ |  | chattáá | chattáa | `chat.ta.ah` | ✘ ✔ ✔ | hosszúság (a STEP nem jelöli) |
| H2416 | חַי | chaj | chaj | ✔ ✔ ✔ |  | chaj | chaj | `chay` | ✔ ✔ ✔ |  |
| H2555 | חָמָס | hámás | chámás | ✘ ✘ ✘ | ḥ (ח) ch/h — kézi kivétel (D36) | chámás | chámasz | `cha.mas` | ✘ ✘ ✘ | ח + számech |
| H3548 | כֹּהֵן | kóhén | kóhén | ✔ ✔ ✔ |  | kóhén | kóhén | `ko.hen` | ✔ ✔ ✔ |  |
| H3678 | כִּסֵּא | kissé | kissé | ✔ ✔ ✔ |  | **kisszé** | kissze | `kis.se` | ✘ ✘ ✘ | számech + hosszúság |
| H4467 | מַמְלָכָה | mamláchá | mamláchá | ✔ ✔ ✔ |  | mamláchá | mamlácha | `mam.la.khah` | ✘ ✔ ✔ | hosszúság (a STEP nem jelöli) |
| H5303 | נְפִלִים | nefilím | nefilím | ✔ ✔ ✔ |  | nefilím | nefil | `ne.phil` | ✘ ✘ ✘ | forrás-eltérés (a TBESH egyes számú alakot ír) |
| H5315 | נֶ֫פֶשׁ | nefes | nefes | ✔ ✔ ✔ |  | nefes | nefés | `ne.phesh` | ✘ ✔ ✔ | hosszúság-heurisztika: e_zart |
| H6093 | עִצָּבוֹן | iccávón | iccávón | ✔ ✔ ✔ |  | iccávón | iccávón | `its.tsa.von` | ✔ ✔ ✔ |  |
| H6975 | קוֹץ | kóc | kóc | ✔ ✔ ✔ |  | kóc | kóc | `qots` | ✔ ✔ ✔ |  |
| H7043 | קָלַל | kálal | kálal | ✔ ✔ ✔ |  | kálal | kálal | `qa.lal` | ✔ ✔ ✔ |  |
| H7451 | רַע | ra | ra | ✔ ✔ ✔ |  | ra | rá | `ra` | ✘ ✔ ✔ | hosszúság-heurisztika: a_nyilt |
| H7496 | רְפָאִים | refáím | refáím | ✔ ✔ ✔ |  | refáím | rápa | `ra.pah` | ✘ ✘ ✘ | forrás-eltérés (a TBESH a H7497 átírását adja) |
| H7497 | רָפָה | ráfá | ráfá | ✔ ✔ ✔ |  | ráfá | rápa | `ra.pah` | ✘ ✘ ✘ | forrás-eltérés (a STEP itt p-t ír ph helyett) |
| H7585 | שְׁאוֹל | seól | seól | ✔ ✔ ✔ |  | seól | seól | `she.ol` | ✔ ✔ ✔ |  |
| H7843 | שָׁחַת | sáchat | sáchat | ✔ ✔ ✔ |  | sáchat | sáchat | `sha.chat` | ✔ ✔ ✔ |  |
| H8004 | שָׁלֵם | sálém | sálém | ✔ ✔ ✔ |  | sálém | sálém | `sha.lem` | ✔ ✔ ✔ |  |
| H8414 | תֹּ֫הוּ | tóhú | tóhú | ✔ ✔ ✔ |  | tóhú | tóhú | `to.hu` | ✔ ✔ ✔ |  |
| H8415 | תְּהוֹם | tehóm | tehóm | ✔ ✔ ✔ |  | tehóm | tehóm | `te.hom` | ✔ ✔ ✔ |  |

**A két LOO-hiba:** a H2555 („hámás”) a D36 szerinti kézi kivétel, ezt szabály nem adhatja ki, csak a kivételtábla. A H3678 („kissé”) pedig a számech konvenciója: ha ez a sor kimarad, a maradék 25-ben a ס egyedül a H2555-ben fordul elő (amely úgyis hibás), így a hangolás nem tanulhatja meg, és az a priori `sz` marad. Mindkettő **konvenció- vagy kivétel-kérdés, nem nyelvi átírási hiba**: a 26 alak közül egyiknél sem téved a niqqud-út a sevában, a dágesben, a begadkefatban vagy a matres lectionisban.

### 4.3 B halmaz (régi kézi lap, független)

44/46 egyezik pontosan. A két eltérés:

| héber | arany (régi lap) | gépi | ok |
|---|---|---|---|
| הַקְּרִיאָה | hakkeriá | hakkeríá | mater jod: a kézi alak a jod előtti hireket röviden írja; a szabály hosszú í-t ad |
| כֹּהֲנִים מַמְלֶכֶת | mamlekhet kóhaním | mamleket kóhaním | konvenció: a kézi lap itt „kh”-t ír, máshol (zákar, sákan) k-t; a régi lap maga sem egységes |

A többszavas párokban a héber szórend a forrásban fordított (RTL-kinyerés, l. N-F131x); a szkript a több egyező szót adó sorrendet veszi.

**A meglévő OSHL-gépezet (S1.7) a B-n 32/36.** Mind a 4 hiba szabályhiány a `adat/kiejtes_heber_jeloltszabalyok.tsv`-ben, amelyet a 26 alak nem hozott elő:

- **ś (שׂ) nincs a táblában:** עָשָׂה → „áśá”, שׂוּם → „śúm”, נָשָׂא → „náśá”;
- **w (mássalhangzó vav) nincs a táblában:** צָוַח → „cáwah”.

Ha a lemmák gépi kiejtése az OSHL-úton menne tovább, ez a két sor hiányzik.

### 4.4 Ragozott alakok: STEP-proxy (299 token)

A TAHOT ISTENTISZT-001 verseinek tokenjeit kétféleképpen írtam át: a niqqud-úton és a STEP-ből. A kettőt **vázszinten** vetettem össze: ékezet és kettőzés nélkül, a ch/h és az sz/s összevonva. A STEP morféma-csonkjai (`sh.M`, `naf.Sh`) kimaradtak, a vajjiqtol „i.” előtagja levágva.

| Beállítás | váz-egyezés |
|---|---|
| a priori (D34: a szókezdő begadkefat kemény) | 276/299 (92%) |
| `szokezdo_begadkefat = pont_szerint` | 281/299 (94%) |

A második beállítás 18 eltérése kézzel besorolva:

| Kié a hiba | db | esetek |
|---|---|---|
| STEP (kihagyott sevá, csonkolás, duplikált magánhangzó) | 13 | קְרֹא „k.Ro'” (2×), נְבִיאֵי „n.vi.'Ei”, צְרֹף „tz.Rof”, בְחֹן „v.Chon”, בְאֵר „v.'Er”, יְפַסְּחוּ „y.fa.se.Chu”, אֱלֹהָי „'e.lo.Ha”, עֲלִילֹתָי „'a.li.lo.Ta” (3×), יַעֲקֹב „ya.'a.Ko”, אֱנוֹשׁ „'e.No.osh” |
| **gépi: kámec kátán, hiányzó** | 2 | כָּל → „kál” (helyesen „kol”; a makkef a TAHOT-vágásban elveszett, a szótag zártsága nem látszik) |
| **gépi: kámec kátán, téves** | 1 | אָכְלוּ → „ochlú” (helyesen „áchelú”: kámec gádol + hangzó sevá, de a szövegben nincs meteg) |
| **gépi: sevá hosszú magánhangzó után** | 1 | יֹּאמְרוּ → „jómrú” (a STEP „yo.me.Ru”, hangzó sevá) |
| **gépi: ketiv/qere** | 1 | ירוּשָׁלִַם → „jrúsálim” (qere perpetuum: Jerúsálajim; a STEP is hibás) |

A D34-es beállításban ezeken felül 7 begadkefat-hiba van, például בְרוּרָה → „berúrá” (helyesen „verúrá”), כֻלָּ → „kullá” (helyesen „chullá”), פְלֵיטָה → „pelétá” (helyesen „felétá”). **A D34 „szókezdő → kemény” szabálya lemmán helyes** (a TBESH-lemmák szókezdő begadkefatja dágest visel). A TAHOT-token viszont előtag nélkül áll, és ilyenkor a dáges hiánya maga mutatja a lágy ejtést.

**Becslés:** ragozott alakon a vázszintű gépi hiba legalább 5/299 ≈ 1,7%. Ez alsó korlát, mert ahol a STEP és a gép ugyanúgy téved, az nem látszik. A hosszúság (á/a, é/e, í/i) hibáit a proxy nem méri. Ezekre a lemma-mérés ad támpontot: a 26-ból egy sem hibás hosszúság miatt.

### 4.5 A döntéstípusok lefedettsége — miért optimista a lemma-szám

Hány alakban fordul elő az adott döntés (a priori futás nyoma):

| Döntéstípus | A (26 lemma) | B (46) | TAHOT, ISTENTISZT-001 (333 token) |
|---|---|---|---|
| sevá (bármely) | 5 — **mind szókezdő, triviális** | 8 | 84 |
| sevá hosszú magánhangzó után | 0 | 0 | 2 |
| kámec kátán | **0** | **0** | 4 |
| dáges forte | 3 | 2 | 24 |
| begadkefat (lágy) | 6 | 6 | 36 |
| mater jod | 3 | 2 | 41 |
| furtív patah | **0** | 1 | 4 |
| ח | 4 | 4 | 23 |
| ס / שׂ | 2 / 0 | 0 / 3 | 5 / 9 |
| tetragramma | 0 | 3 | 23 |

A két arany halmaz a hibalehetőségek legnehezebb részét (kámec kátán, nem szókezdő sevá) **egyáltalán nem teszteli**. Ezekre csak a proxy ad (alsó) becslést.

### 4.6 C halmaz: 20 ragozott alak kézi átnézésre — *nincs arany*

Ezekhez nincs jóváhagyott kiejtés, így a gépi kimenet itt **nem mért, csak bemutatott**. A minta: 8 alak az ISTENTISZT-001 saját Strongjaiból (H7121, H8034), 12 a versek más szavaiból.

| # | igehely | Strong | ragozott alak (TAHOT) | STEP | gépi (niqqud) | gépi (STEP) |
|---|---|---|---|---|---|---|
| 1 | 1Móz 4:26 | H7121 | יִּקְרָא | `i.yik.Ra'` | jikrá | ijikrá |
| 2 | 1Móz 4:26 | H8034 | שְׁמ | `she.M` | sem | sem |
| 3 | 1Móz 4:26 | H7121 | קְרֹא | `k.Ro'` | keró | kró |
| 4 | 1Móz 4:26 | H8034 | שֵׁם | `Shem` | sém | sém |
| 5 | 2Móz 33:19 | H7121 | קָרָאתִֽי | `ka.Ra.ti` | kárátí | káráti |
| 6 | 1Kir 18:24 | H7121 | קְרָאתֶם | `ke.ra.Tem` | kerátem | kerátém |
| 7 | 1Kir 18:24 | H7121 | אֶקְרָא | `'ek.Ra'` | ekrá | ékrá |
| 8 | 1Kir 18:25 | H7121 | קִרְאוּ | `kir.'U` | kirú | kirú |
| 9 | 1Móz 4:26 | H8352 | שֵׁת | `Shet` | sét | sét |
| 10 | 1Móz 4:26 | H1571 | גַּם | `gam-` | gam | gam |
| 11 | 1Móz 4:26 | H1931 | הוּא | `hu'` | hú | hú |
| 12 | 1Móz 4:26 | H3205 | יֻלַּד | `yu.lad-` | jullad | júlad |
| 13 | 1Móz 4:26 | H1121 | בֵּן | `Ben` | bén | bén |
| 14 | 1Móz 4:26 | H0853 | אֶת | `'et-` | et | ét |
| 15 | 1Móz 4:26 | H0583 | אֱנוֹשׁ | `'e.No.osh` | enós | enóós |
| 16 | 1Móz 4:26 | H0227 | אָז | `'az` | áz | az |
| 17 | 1Móz 4:26 | H2490 | הוּחַל | `hu.Chal` | húchal | húchal |
| 18 | 1Móz 4:26 | H3068 | יְהוָֽה | `Yah.weh` | JHVH | JHVH |
| 19 | 1Móz 12:8 | H6275 | יַּעְתֵּק | `i.ya'.Tek` | jaték | ijáték |
| 20 | 1Móz 12:8 | H8033 | שָּׁם | `Sham` | sám | sam |

Két, a C-ből látható korlát, amely nem az átíró hibája, hanem a TAHOT-tokené:

- **(1) Előtag nélkül.** A TAHOT a vav-előtagot külön sorba vágja, ezért az 1. sor „jikrá”, nem „vajjikrá”, és a kettőzött jod nem látszik.
- **(2) Toldalék nélkül.** A birtokos toldalék is külön sorba kerül, ezért a 2. sor csonk („sem”, a teljes szó: „semó”). A lapon a ragozott alak kiejtéséhez a teljes szót kell összerakni a TAHOT-sorokból, különben a kiejtés csonka.

## 5. A hibák kategóriái összefoglalva

| Kategória | Mért hatás | Kezelhető-e szabállyal? |
|---|---|---|
| **Konvenció: ס (számech)** | A: 1 LOO-hiba (kissé). A jóváhagyott lista a ס-t „s”-nek írja (kissé, hámás). Ez az OSHL-táblából öröklődött, mert abban nincs `s → sz` szabály. A magyar olvasó így [ʃ]-nek ejti, azaz a ס és a שׁ a lapon nem különül el. | igen, de **előbb dönteni kell** (s vagy sz) |
| **Konvenció: ח** | A: 1 (hámás, kézi kivétel D36); B: a régi lap h-t ír | kivételtáblával |
| **Begadkefat szókezdő, dáges nélkül** | lemmán 0; ragozott tokenen 7/299 a D34-es szabállyal | igen: ragozott alaknál a pontozás dönt |
| **Kámec kátán** | arany halmazban nincs; proxy: 3/299 (2 hiányzó, 1 téves) | részben: a makkef és a meteg hiánya miatt a pontozott token nem mindig dönti el; lexikai kivétel (כָּל → kol) |
| **Sevá hosszú magánhangzó után** | arany halmazban nincs; proxy: 1/299 | részben (meteg-függő) |
| **Ketiv/qere** | proxy: 1/299 (Jeruzsálem); a tetragramma külön kezelve | csak kivétellistával |
| **Mater jod (hirek)** | B: 1 (hakkeriá vs. hakkeríá) | konvenció |
| **Dáges forte (kettőzés)** | 0 hiba (A: 3, B: 2, proxy: 24 eset) | igen |
| **Furtív patah, makkef, kantilláció** | 0 hiba | igen |
| **Hosszúság a STEP-útban** | A: 5 hiba (a STEP-hibák fele) | **nem**: a STEP nem hordozza |
| **Forrás-eltérés a STEP-ben** | A: 4 (H5303, H7496, H7497, H3678) | nem |
| **TAHOT-token csonk (előtag, toldalék)** | C: látható | igen, a szó összerakásával a TAHOT-sorokból |

## 6. Javaslat (nem döntés — ⛔ a felhasználóé)

**Érdemes-e átállni?** Feltételekkel igen, a ragozott alakokra is. A mért kockázat kicsi és jól körülhatárolt:

- lemmán a nyelvi átírási hiba a mért halmazokon 0; az egyetlen „hiba” konvenció vagy kézi kivétel;
- ragozott alakon a vázszintű hiba ≈ 2% (alsó becslés), és a nehéz esetek három kategóriájára (kámec kátán, sevá hosszú után, ketiv/qere) koncentrálódik.

**Feltételek, ha átállás lesz:**

1. **Bemenet: a pontozott héber (niqqud), nem a STEP-átírás.** A STEP hosszúságot nem jelöl, és forrás-eltérései vannak: 54% LOO, a megbízhatatlan tartományban. Az OSHL-út csak lemmára létezik, és a jelenlegi táblájából két szabály hiányzik (ś, w).
2. **Látható „gépi” jelölés.** Például a kiejtés után kisbetűs „(gépi)” vagy dőlt stílus, hogy a jóváhagyott (kivételtáblás) és a gépi alak megkülönböztethető legyen. A jóváhagyott tábla (`adat/kiejtes_kivetelek.tsv`) mindig elsőbbséget kap; a hámás típusú kivételek és a JHVH is innen jönnek.
3. **Két konvenciódöntés a bekötés előtt:**
   - a ס és a שׂ magyar betűje (`s` vagy `sz`). A jóváhagyott lista ma `s`-t ír a ס-re, a régi kézi lap `sz`-t a שׂ-re;
   - a szókezdő, dáges nélküli begadkefat ragozott alakban a pontozás szerint dőljön el (a D34 lemmára szóló szabálya mellett).
4. **A TAHOT-token összerakása.** A ragozott alak kiejtése a teljes szóra készüljön (előtag + tő + toldalék), ne a TAHOT morféma-sorára; különben „sem” áll „semó” helyett.
5. **Kis kivétellista a tipikus hibákra** (כָּל → kol, יְרוּשָׁלִַם → Jerúsálajim, a kámec-kátán-gyakori szavak). Ezek ugyanabba a kivételtáblába mennek, kézi jóváhagyással.
6. **Bővebb arany minta a nehéz esetekre** a bekötés előtt, például 30–50 ragozott alak kámec kátánnal és nem szókezdő sevával, kézzel jóváhagyva. A mostani 26 + 46 alak ezeket nem tartalmazza, ezért a ragozott alakokra a fenti 2% csak proxy-becslés.

Ha az átállás nem szükséges, a jelenlegi szabály (csak jóváhagyott alak + „szótári alak: …” jelölés) változatlanul helyes. Ekkor a mérés haszna, hogy a jóváhagyásra váró alakokhoz (N-F131w: ISTENTISZT-001 38, HAMART-001 47 stb.) a niqqud-út **jelöltet** adhat kézi jóváhagyásra, ugyanúgy, ahogy az S1.7 tette a lemmákkal.
