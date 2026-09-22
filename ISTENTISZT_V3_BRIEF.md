# ISTENTISZT_V3_BRIEF.md — v1

Az ISTENTISZT-001 lexikon-oldal rendbetétele egy menetben: v2 → v3. Kiindulás: `main` = `65d581b`.

## 0. Kiindulás (mérve, 2026.09.22)

- A 2. szakasz G1941 Thayer-blokkja „Fordítás függőben".
- A Minősítés a pilot 21 igehelyére készült; a 4. szakasz 31 igehelyre fut. Minősítetlen, találatot adó igehely: Zak 13:9, ApCsel 2:21, ApCsel 9:14, ApCsel 9:21, ApCsel 22:16, Róm 10:13, Róm 10:14, 1Kor 1:2, 2Tim 2:22, 1Pét 1:17.
- A Kivonat helyőrző.
- A kézi szövegben a régi szakaszszámozásra mutató hivatkozások maradtak.
- A Róm 10:12 (G1941 ἐπικαλουμένους) formula-előfordulás, de nincs az `elofordulasok.tsv`-ben.

## 1. Szabályok

- A kézi szöveget csak a 3. pontban megadott helyeken és módon változtasd; minden más kézi szöveg bájtra azonos marad. A változtatásokat a jelentésben régi → új párként listázd.
- A NAPLO-bejegyzésekben a *study*-ra (nem erre az oldalra) mutató hivatkozások („study 2/b", „study saját 3. pontja") NEM változnak.
- Minden lépés után `ellenoriz.py` kód 0.

## 2. G-döntések

- **G1** A Róm 10:12 bekerül (I1), a 2Tim 2:22 precedense szerint (név nélküli τόν κύριον / αὐτόν, Thayer 5. jelentés együtt sorolja őket).
- **G2** Az oldal státusza: `statusz_verzio=v3`, `statusz_datum=2026.09.22`, `statusz=publikálható` marad.
- **G3** Rokon szavak generált blokkja, TSK+minősítés egysoros táblája, kapcsolat-indoklás adatoszlopa, bibliográfia: nem hatókör (LEXV2_3).

## 3. Tételek

### I1 — Róm 10:12 beépítése
A szabályos jelölt-úton (`jeloltek.tsv` → `betolt.py beepit`), mezők:
- `igehely`: `Róm 10:12`
- `kapcsolodas`: `"…ugyanaz az Ura mindeneknek, a ki kegyelemben gazdag mindenekhez, a kik őt segítségül hívják" — a 10:13-as Jóel-idézet közvetlen bevezetése: a segítségül hívók körét zsidóra és görögre egyaránt kiterjeszti.`
- `pardes_szint`: `Remez`
- `funkcio`: `🎯 előkép/beteljesedés (bevezetés) — a 10:13 idézetét előkészítő egyetemes kiterjesztés`
- `gerinc_elem`, `strong`: `G1941`
- `lexikon_szotar`/`lexikon_entry_id`/`jelentes_szam`/`jelentes_hu`: mint a Róm 10:13 sorában (`TBESG` / `G1941` / `2` / `segítségül hívni, invokálni`)
- `karoli_szo`: `segítségül hívják`
- `azonositas_modja`: `tartalom-alapú`; `megbizhatosag`: `magas`
- `proveniencia`: `scope=manual | forras=TSK (Zak 13:9→Róm 10:12 Votes 18; ApCsel 2:21→Róm 10:12 Votes 29) + TAGNT G1941 + Thayer G1941 5. jelentés | ts=2026-09-22`
- `igazolas`: `nincs`
A jelölt sor döntése `beépítve`. ⛔ Ha a `betolt.py` bármely mezőt elutasít, állj meg.

### I2 — Thayer G1941 fordítás
A `lexikon_hivatkozasok.tsv` `szotar=Thayer`, `strong=G1941` sorának `forditas_hu` mezője, egy sorban, szó szerint:

```
G1941 — ἐπικαλέω ἐπικαλῶ: 1. aorisztosz ἐπεκαλεσα; (szenvedő és közép alak, jelen idő ἐπικαλοῦμαι); perfektum szenvedő ἐπικέκλημαι; pluskvamperfektum egyes szám 3. személy ἐπεκέκλητο, és az augmentum elhagyásával (vö. Winer, Grammatika, 12. §, 5; Buttmann, 33 (29)) ἐπικεκλητο (ApCsel 26:32, Lachmann); 1. aorisztosz szenvedő ἐπεκλήθην; jövő idő közép ἐπικαλέσομαι; 1. aorisztosz közép ἐπεκαλεσάμην; a Septuagintában igen gyakran a קָרָא fordítása; 1. nevet tenni valakire, melléknéven nevezni: τινα (Xenophón, Platón és mások), Mt 10:25 G T Tr WH (a Rec.-ben ἐκάλεσαν); szenvedő alakban ὁ ἐπικαλούμενος: akit melléknéven neveznek, Lk 22:3 R G L; ApCsel 10:18; 11:13; 12:12; 15:22 R G; továbbá ὅς ἐπικαλεῖται, ApCsel 10:5; 10:32; ὁ ἐπικληθείς, Mt 10:3 (R G); ApCsel 4:36; 12:25; egyenértékű a ὅς ἐπεκλήθη kifejezéssel, ApCsel 1:23. Közép jelentésű szenvedő alak (vö. Winer, Grammatika, 38. §, 3): megengedni, hogy valakit melléknéven nevezzenek: Zsid 11:16; közép alak τινα-val: 1Pét 1:17 εἰ πατέρα ἐπικαλεῖσθε τόν stb., azaz ha (magatoknak) Atyaként hívjátok őt, azaz ha Atyátoknak nevezitek. 2. ἐπικαλεῖται τό ὄνομα τίνος ἐπί τινα, a héber פ עַל פ... שֵׁם נִקְרָא... mintájára: „valakinek a nevét nevezik valaki fölött, azaz az ő nevéről nevezik, vagy neki szenteltnek nyilvánítják" (vö. Gesenius, Thesaurus iii., 1232a. o.): ApCsel 15:17, az Ám 9:12-ből (a szóban forgó név Isten népéé); Jak 2:7 (a név: οἱ τοῦ Χριστοῦ). 3. τίνι, a tárgy tárgyesetével; tulajdonképpen: valamit rákiáltani valakire (vö. angol to cry out upon (or against) one); „valamit bűnként vagy szemrehányásként valakinek a terhére róni; valakit valamilyen vádpont alapján perbe idézni, bűncselekményért perbe fogni; hibáztatni valakit valamiért, vádolni valakit valamivel" (Arisztophanész, Béke 663; Thuküdidész 2, 27; 3, 36; Platón, Törvények 6, 761 e.; 7, 809 e.; Dio Cassius 36, 28; 40, 41, és gyakran a szónokoknál (vö. a κατηγορέω címszót)): εἰ τῷ οἰκοδεσπότῃ Βηλζεβουλ ἐπεκάλεσαν (azaz a Belzebúllal való kapcsolattal, az ő segítségének elfogadásával vádolták, vö. Mt 9:34; 12:24; Mk 3:22; Lk 11:15), πόσῳ μᾶλλον τοῖς ὀικιακοις αὐτοῦ, Mt 10:25, L WH széljegyzeti olvasata a Vaticanus nyomán (lásd fent az 1. pontot); ezt az olvasatot Rettig védte a Studien und Kritiken 1838-as évfolyamában, 477. skk. o., valamint Alexander Buttmann (1873) ugyanebben a folyóiratban, 1860, 343. o., és újszövetségi grammatikájában is, 151 (132); (továbbá Weiss a Meyer-kommentár 7. kiadásában, az adott helynél). Ez a kifejezés azonban (Belzebúl a Belzebúl segítsége helyett) túl nehézkes ahhoz, hogy ne valamely tudatlan írnok javítását sejtesse, aki azon botránkozott meg, hogy (e hely kivételével) az evangéliumokban sehol sem mondják Jézus ellenségeiről, hogy Belzebúlnak nevezték volna őt. 4. segítségül hívni (mint a német anrufen), invokálni; közép alakban: segítségül hívni magának, a maga javára: valakit segítőként, ApCsel 7:59, ahol τόν κύριον Ἰησοῦν értendő (βοηθόν, Platón, Euthüdémosz 297 c.; Diodórosz 5, 79); τινα μάρτυρα: tanúmul, 2Kor 1:23 (Platón, Törvények 2, 664 c.); bíróként, azaz hozzá fellebbezni, hozzá folyamodni: Καίσαρα, ApCsel 25:11; 26:32; 28:19; (τόν Σεβαστόν, ApCsel 25:25); szenvedő főnévi igenévvel, ApCsel 25:21 (hogy megtartassék). 5. héber mintára (mint a יְהוָה בְּשֵׁם קָרָא: segítségül hívni a JHVH név kimondásával, 1Móz 4:26; 12:8; 2Kir 5:11 stb.; vö. Gesenius, Thesaurus, 1231b. o. (vagy héber szótára a קָרָא címszónál); a kifejezés magyarázata az, hogy az Istenhez intézett imádságok rendszerint az isteni név segítségül hívásával kezdődtek: Zsolt 3:2; 6:2; 7:2 stb.) ἐπικαλοῦμαι τό ὄνομα τοῦ κυρίου: segítségül hívom (a magam javára) az Úr nevét, azaz segítségül hívom, imádom, tisztelem az Urat, azaz Krisztust: ApCsel 2:21 (a Jóel 2:32-ből); ApCsel 9:14, 21; 22:16; Róm 10:13; 1Kor 1:2; τόν κύριον, Róm 10:12; 2Tim 2:22; (a görög íróknál gyakran ἐπικαλεῖσθαι τούς Θεούς, mint Xenophón, Cyril [értsd: Kürupaideia] 7, 1, 35; Platón, Tímaiosz 27 c.; Polübiosz 15, 1, 13).
```

### I3 — Minősítés
(a) A 739. sor „⚠ ELTÉRÉS: …" mondata helyett: `a pilot 2026.09.06-i, 21 igehelyes állapotára vonatkozik; a 2026.09.09-i bővítés 10 igehelyének és a Róm 10:12-nek a minősítése lent (2026.09.22).`
(b) A 747. sor „⚠ ELTÉRÉS: …" mondata helyett: `a pilot 21 igehelyére; a kiegészítés lent.`
(c) A „**A 2Móz 33:19/34:5 → Ézs 12:4 …**" bekezdés ELÉ, szó szerint:

```
**Kiegészítés (2026.09.22) — a 2026.09.09-i bővítés 10 igehelye és a Róm 10:12 (TSK Votes ≥ 15 és Károli-KH), azonos kritériummal: tartalmazza-e a cél-igehely a H7121+H8034 / ἐπικαλέομαι (epikaleomai) formulát:**

- Zak 13:9 → 46 TSK-találat + Károli-KH 1Pét 1:6-7: a formulát a már dokumentált Jóel 2:32, ApCsel 2:21 és Róm 10:14 — **független megerősítés** — mellett egyedül a Róm 10:12 tartalmazza (Votes 18) — **ÚJ, VALÓDI TALÁLAT** (l. lent). Név nélküli segítségül hívást (H7121, שֵׁם – sém nélkül) tartalmaz a Zsolt 50:15, Zsolt 91:15, Jer 29:12, Ézs 58:9 és Ézs 65:24: rokon igei használat, nem a formula, NEM a motívum része. A többi 37 találat (tisztítás, próbatétel, szövetségi formula) a formula szempontjából NEM releváns.
- ApCsel 2:21 → Róm 10:13 (Votes 29), Jóel 2:32 (Votes 26) — **független megerősítés**; Róm 10:12 (Votes 29) — **ÚJ, VALÓDI TALÁLAT**, azonos a fentivel; Zsolt 86:5 (H7121, név nélkül) — rokon, NEM a formula; Károli-KH 1Móz 25:21-26 — a 25:25-26-ban a H7121+H8034 névadás („nevezék nevét Ézsaunak"), nem segítségül hívás — NEM releváns.
- Róm 10:13 → ApCsel 2:21 (Votes 106), Jóel 2:32 (Votes 103), és a Károli-KH ugyanezt a két helyet adja — **független megerősítés**.
- 2Tim 2:22 → Károli-KH 1Kor 1:2 — **független megerősítés**; a 7 TSK-találat (1Pét 2:11; 3:11; 1Kor 6:18; Zsolt 119:9; 1Tim 6:11; Zsid 12:14; 1Tim 4:12) az erkölcsi intelmet köti össze — NEM releváns.
- ApCsel 9:14 → 1Sám 13:13-14, Zsolt 89:21-22; ApCsel 9:21 → Gal 1:23; ApCsel 22:16 → ApCsel 2:38, Jón 1:5; Róm 10:14 → Mk 16:15-16, 1Móz 3:15; 1Kor 1:2 → 1Kor 6:11; 1Pét 1:17 → ApCsel 10:34-35, Gal 4:6, Róm 2:6-11, Zsid 12:28 — mind ellenőrizve, egyik sem tartalmazza a formulát, NEM relevánsak.
- Róm 10:12 (saját hivatkozásai) → Jel 17:14 (Votes 15), Fil 4:19 (Votes 18), Róm 3:22 (Votes 15), Károli-KH ApCsel 10:34-35 — egyik sem tartalmazza a formulát, NEM relevánsak.

**ÚJ IGEHELY: Róm 10:12** — *„Mert nincs különbség zsidó meg görög között; mert ugyanaz az Ura mindeneknek, a ki kegyelemben gazdag mindenekhez, a kik őt segítségül hívják."*
— **ἐπικαλουμένους** (*epikalúmenúsz*, G1941), ugyanaz az ige, mint a 10:13-nál és a 10:14-nél; a Thayer az 5. jelentésnél a 2Tim 2:22-vel együtt sorolja fel (τόν κύριον – ton kürion, név nélkül).
Funkció: ELŐKÉP/BETELJESEDÉS klaszter kiegészítése — a 10:13-as Jóel-idézet közvetlen bevezetése, amely a segítségül hívók körét zsidóra és görögre egyaránt kiterjeszti.
```

### I4 — Elavult hivatkozások
(a) A kézi szakaszokban minden erre az oldalra mutató régi szakaszhivatkozás átírása: `1/b. szakasz` → `6. szakasz — PaRDeS keretrendszer`; `6. szakasz — Módszertani napló` (és önálló `6. szakasz`, ha a Módszertani naplóra utal) → `7. szakasz — Módszertani napló`; `8. szakasz — Nyitott kérdések` → `7. szakasz — Nyitott kérdések és séma-korlátok`; `9. szakasz` / `10. szakasz` → `Kolofon`; `7. szakasz` (ÚJ FELISMERÉS) → jelentsd, ne írd át. A `2.`–`5.` és a `2/b` hivatkozások helyesek, maradnak. A mért helyek (a `65d581b` szerint): 433., 963., 980., 1026. sor; keress további előfordulást is.
(b) A 540. sor helyett: `*(Megjegyzés: a G0994 nem a motívum saját tokenje, ezért a 2. szakasz generált része nem ad hozzá szócikket; LXX-beli szerepét a 3. szakasz mutatja: Ézs 12:4.)*`
(c) A Nyitott kérdések 3. pontjában a „**A fájl repóba emelése még külön döntést igényel.**" helyett: `~~A fájl repóba emelése még külön döntést igényel.~~ — 2026.09.20-án lezárva (F7.1): közkincs, \`konkordancia/Thayer_teljes.tsv\`; a teljes G1941-szócikk és magyar fordítása a 2. szakasz generált részében áll.`
(d) A Nyitott kérdések listájának végére, a következő sorszámmal, szó szerint:

```
N. **UBS-besorolás (2026.09.22)** — az UBS Greek New Testament Dictionary az ApCsel 9:14 ἐπικαλουμένους (epikalúmenúsz) alakját nem a 33.176-os „segítségül hívni" jelentéshez sorolja, hanem a 11.28-hoz („Isten népéhez tartozni", szó szerint: „akire valakinek a nevét hívják"), és a 11.28 megjegyzése ezt a verset a hagyományos értelmezéstől eltérőként kifejezetten megnevezi; az 1Pét 1:17 hozzárendelése kettős (33.131 és 33.176). Mindkettő a 6. Értelmezés feldolgozandó kérdése; a lexikon-adat (1. szakasz, UBS-oszlop) a forrás besorolását mutatja.
```
(az `N.` helyére a tényleges következő sorszám)

### I5 — Kivonat
A `## Kivonat *(kézi)*` alatti helyőrző helyett, szó szerint:

```
A motívum az ószövetségi קָרָא בְּשֵׁם יְהוָה (kárá besém JHVH), „segítségül hívni az Úr nevét" formulát és újszövetségi folytatását követi: formulaikus azonosság, 32 igehelyen (22 ószövetségi, 10 újszövetségi). A formula az 1Móz 4:26-ban jelenik meg először, a pátriárkák oltárépítéséhez kötődik, majd a zsoltárokban és a prófétáknál liturgikus és eszkatológiai formává válik (Jóel 2:32). A Septuaginta a 22 ószövetségi helyből 18-at az ἐπικαλέω (epikaleó) igével ad vissza; eltér a két isteni önkihirdetésnél (2Móz 33:19; 34:5: καλέω, kaleó) és az Ézs 12:4-ben (βοάω, boaó), a Zsolt 116:17-ben pedig a tagmondat hiányzik a görögből. Az Újszövetség a Jóel 2:32-t szó szerint idézi (ApCsel 2:21; Róm 10:13), és a formulát Krisztusra alkalmazza: a „segítségül hívók" a korai gyülekezet önmegnevezésévé válnak (ApCsel 9:14, 21; 1Kor 1:2).
```

### I6 — Státusz
`motivumok.tsv`: ISTENTISZT-001 `statusz_verzio=v3`, `statusz_datum=2026.09.22`.

### I7 — Generálás és ellenőrzés
`general.py --cel mind --ir`, majd `--ellenoriz` fixpont. Ellenőrizd és jelentsd: (1) az Előfordulások 32 sor (22 ÓSZ / 10 ÚSZ), a Róm 10:12 UBS-jelentéssel; (2) a 4. szakasz 32 igehelyre fut; (3) a G1941 Thayer-blokkban nincs „Fordítás függőben"; (4) a kézi szövegben nincs `1/b. szakasz`, `8. szakasz`, `9. szakasz`, `10. szakasz` hivatkozás (a study-ra mutatók kivételével); (5) a Kivonat nem helyőrző; (6) a kolofonban v3; (7) a többi 7 oldal változatlan; (8) `ellenoriz.py` kód 0, az összesítő értékével. Commit tételenként, push, zárójelentés a régi → új szövegpárokkal (I3a–b, I4a–c).

## Döntésnapló

| Verzió | Dátum | Döntés |
|---|---|---|
| v1 | 2026.09.22 | Az ISTENTISZT-001 egy menetben v3-ra. Róm 10:12 felvéve (TSK ×2, TAGNT, Thayer 5. jelentés; a 2Tim 2:22 precedense). A Thayer G1941 fordítása, a 10+1 igehely minősítése, a kivonat és az UBS-kérdés szövege chatben készült. Rokon szavak generált blokkja, TSK+minősítés egysoros tábla, kapcsolat-indoklás adatként, bibliográfia: LEXV2_3. |
| v2 | 2026.09.22 | P1: I2 kiejtéssel — a Thayer G1941 `forditas_hu` mezője az `ISTENTISZT_V3_POTLAS.md` szerinti, kiejtéssel ellátott szövegre cserélve. |
| v3 | 2026.09.22 | P2–P3: kiejtés a kézi szövegben — 54+46 csere a 2/b „🇭🇺 Magyarul" bekezdésekben és a többi kézi szövegben, a `65d581b` eredeti tartalomhoz illesztett célsorokkal (a 980. sor esetén git diff-térképpel). |
| v4 | 2026.09.22 | P4: UBS-cellák jelölése — `eszkozok/lexikon_general.py` `ubs_jelentes_cella()`: ÓSZ-sor, G-token nélküli sor és hozzárendelés nélküli Strong-token mind jelölve, összetett token tokenenként; mind a 8 lexikon-oldalon élesítve. |
| v5 | 2026.09.22 | Z1–Z2: utolsó kiejtés-pótlás (kézi + lexikon_hivatkozasok) — a P5-ben jelzett 6 kivétel a kézi szövegben (`ISTENTISZT_V3_ZARO.md` Z1), 25 csere a `lexikon_hivatkozasok.tsv` BDB H7121/H3548 és TBESG G1941 `forditas_hu` mezőiben (Z2, a KIRALY-001 oldalt is érintve). A teljes szövegű (blockquote-on kívüli, generált résszel együtti) záró ellenőrzés 5 további, adatmezőből (elofordulasok.tsv `funkcio`, motivumok.tsv `negativ_kriterium`/`folerendelt_fogalom`, kapcsolatok.tsv leírás) származó kiejtés-hiányt talált — nincsenek csere-táblával lefedve, nem javítva, l. a Z3-zárójelentés. |
