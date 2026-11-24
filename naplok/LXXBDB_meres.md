# F240 (LXXBDB) — mérésnapló

*proveniencia: scope=F240 L1–L6 | forras=konkordancia/Macula_heber_*.tsv, konkordancia/LXX_OS/, konkordancia/Strong_szotar.tsv, adat/kulso/lxx_bridge.tsv, konkordancia/BDB_teljes_unabridged.tsv, adat/forditasok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv, pardes.db (a main tükre, csak olvasva) | ts=2026-11-23/24*

A brief: `F240_LXX_BDB_ADATJAVITAS_BRIEF.md`; a döntések: `naplok/F240_dontesek.md`. A mérőeszközök a repóban:
`eszkozok/lxx_strong_javitas.py` (L1, L2, L6), `eszkozok/bdb_konyvketto_javit.py` (L3), `eszkozok/olvaso_szerver/bdb_vers_jelentes.py` (L5).

## 1. osztály (L1) — hamis görög Strong a Macula LXX-párjaiban

**Hol keletkezik.** A Macula forrás `greekstrong` attribútuma (`konkordancia/Macula_heber_*.tsv` `gorog_strong`, változatlan
import), és ennek összesítése, a bcv-commons `lxx_bridge.tsv` (H1242 → G5459: 88 = a token-szám).

**Mérés.** Macula–LXX_OS tokenillesztés (ugyanaz a Károli-vers, ugyanaz az ékezet nélküli alak). Jelölt: a Macula-Strong
az LXX_OS-ben sehol nem fordul elő, és az LXX_OS ugyanazon a tokenen más Strongot ad, vagy nem ad, és az LXX-lemma nem a
Macula-Strong szótöve. 141 jelölt pár, mind ítélve (`naplok/LXXBDB_lxx_jeloltek.tsv`):

| Ítélet | Pár | Mit jelent |
|---|---|---|
| `macula_hiba` | 11 → a javítás után 0 | a címke más lemmára mutat; javítva (`adat/lxx_strong_javitas.tsv`, 29 alaksor) |
| `konvencio` | 100 | a Strong-szótár alakszáma vagy szuppletív töve (μου G3450 ↔ ἐγώ; εἶπον ↔ λέγω; ἔσται ↔ εἰμί; átírt név) |
| `lxx_os_hiba` | 23 | az LXX_OS homográf-hibája, a Macula címkéje helyes (N-F240a) |
| `illesztesi_zaj` | 7 | az ékezet nélküli illesztés a vers más szavára esett (ἓν / ἐν, ᾖ / ἤ) |

A javított hibák (token): πρωὶ → G4404 πρωΐ a G5459 φωσφόρος helyett (89; a H1242 „reggel” 87); az ἄγω 17 alakja → G0071 a
G0033 ἄγε („rajta!”) helyett (40); μόσχους → G3448 a G2353 θρέμμα helyett (42); βόες → G1016 βοῦς a G1003 Βοόζ helyett (26);
ζητήσεις → G2212 (4); ἀνοίξει → G0455 (4); φόρου → G5411 (4); ἀπολλύων → G0622 (1); „megfelelő nélkül”, mert a helyes
lemmának nincs Strong-száma (DT-F240b): ἀποστάτης (4), σμῆγμα (1), αἰτιᾶται (1). Összesen 217 javított token.
A `lxx_bridge` (javított): H1242 → G4404 135, G2250 4, G3722 4 (előtte G5459 88, G4404 47).

**Kapu:** `ellenoriz.py` 44 (a javítás előtti állapoton 11 sértés).

## 2. osztály (L2) — nyelvtani szó az LXX-megfelelők közt

**Hol keletkezik.** Az `adat/grammatikai_strongok.tsv` görög oldala a lemmák számait ismeri (G1473, G4771, G3778, G0846);
a Macula az alakok külön Strong-számát viszi (μου G3450, σου G4675 …). A szűrő (`olvaso_szerver/blokkok._szk_lxx`,
`bdb_adatblokk`) ezért nem ismerte fel őket.

**Mérés (előtte).** 34 alakszám nem volt a listán; a „Görög megfelelő (Septuaginta)” blokkban 31 héber szó mellett, a
BDB-kártya jelentésenkénti LXX-sorában 173 héber szónál (2 642 token) állt ilyen alak (pl. H0430: μου, σοι, ὑμᾶς).
**Utána:** 0 (a 34 alakszám a `GOROG_ALAK` listán). Nem került a listára: εἷς G1520, μία G3391 (számnév; csak az LXX_OS
homográf-hibája miatt esik egybe az εἰς-szel).

**Kapu:** `ellenoriz.py` 45 (a javítás előtti listán 32 sértés).

## 1b és L6 — az LXX_OS homográf- és tulajdonnév-címkéi (N-F240a, külön PR)

**Hol keletkezik.** `eszkozok/lxx_os_import.py`: a lemmát ékezet és kisbetű nélkül keresi a GreekWordList-ben.
**Mérés:** 35 lemma–Strong pár, 3 370 token: `masik_strong` 3 169 (τίς → G5100 1 506; εἷς → G1519 1 027; καρπός → G2591
128; ποῦ 102; ὦ 92; οὗ 59; ἦ 54; στέφανος 51; φοῖνιξ 42; πότε 40; ἕκτος 38 …), `tulajdonnev` 201 (τύραννος → G5181 63;
χριστός → G5547 49; χλόη 14; δορκάς 13; βλαστός 12 …; **πόντος → G4195 Πόντος 2**, a TEREMT-001 2Móz 15:5 „Pontusz”-a).
A Macula-párokban kisbetűs szó tulajdonnévi Strongot ítélet nélkül nem visel (a jelöltlistán a βόες → Βοόζ javítva).

**Kapu:** `ellenoriz.py` 46, plafon 35 pár / 3 370 token (csak csökkenhet; az N-F240a PR-ja nullázza).

## 3. osztály (L3) — kettőzött könyvnév és csonka fejléc

**Hol keletkezik.** A BDB könyvjele szóként maradt a forrásban a hivatkozás előtt („angels Psalm Psa 97:7”, „Job Job 8:10”,
„Gen Genesis 32:33”, „Ez Ezek 16:47”); az F34 a ψ-hibát javította, a „Psalm” szót nem (`naplok/F34_M0_felmeres.md`, M1-es
opció). A fordítás ezt viszi („angyalok Zsolt Zsolt 97:7”), és a fordító az angol „Psalm 40:18”-at is „Zsoltár Zsolt”-ra
tette (6 hely). A csonka fejléc („c. angyalok Zsolt”) a kettőzés első tagjánál vágott fejléc.

**Mérés és javítás.** Angolul 64 jelölt: 33 javítva (26 szócikk), 31 marad (személynév: „friend of Job”, Ezsdrás társai;
tartalmi szó: „in late Psalms”) — `naplok/LXXBDB_konyvketto_csere.tsv`. Magyarul 38 kettőzés 29 fordítássorban javítva,
30 `forras_hash` frissítve, fizetős újrafordítás nélkül (az elavult fordítássor előtte és utána is 158). A
`bdb_szakasz_hu.tsv` 32 szócikknél újragenerálva. Könyvszóra végződő jelentés-fejléc: 31 → 14; a H0430 „c.” fejléce
„angyalok”.

**A maradék 14 fejléc más hiba:** rossz könyvfeloldás („Jóel 1Sám 4:13” → helyesen Jóel 4:13; „Ézs 1Krón 16:4”;
„Ezsd Dán 7:14”). Angolul 21 szócikkben áll könyvszó + más könyv hivatkozása, ennek kb. a fele valódi név (Dán törzse, Jónás).
A döntés az integrátornál (L7 ebben a PR-ban vagy N-tétel).

**Kapu:** `ellenoriz.py` 47 (a javítás előtti állapoton 71 sértés).

## L5 — hamis versenkénti jelentés (tehóm „örvény · 5”)

**Hol keletkezik.** Nem a „see 5 infra” utalás jelentéskezdetként: a `bdb_vers_jelentes.py` `TablaPont.keres` a hivatkozást
a jelentés-tábla szövegében (a nyers JSON) csak előre keresi. A H8415 fejében a nyers szöveg „Isa 106:9”, „Isa 71:20”-at ír
(a ψ rosszul feloldva; az angol forrásban „Psa”), ezért a kurzor a 2., majd az 5. jelentés azonos hivatkozására ugrott, és
onnan minden további hely nem illesztve, a beragadt pontot örökölte (38 sor „-/5”).

**Javítás.** Több előfordulás közül a várt pozícióhoz (az angol pozíció arányos képe) legközelebbi, ha a kurzor utáni első
messze esik (200 karakter); a nem talált hivatkozás a várt pozíciót kapja. **Hatás** (`naplok/LXXBDB_vers_jelentes_diff.tsv`):
1 186 sor / 79 szó változik, 928 nem illesztett sor biztos illesztést kap; a nem illesztett sorok 2 062 → 622; beragadt futam
(≥ 5 egymást követő nem illesztett sor egy számozott ponton) 45 / 1 188 sor → 2 / 10 (H2320, H6677: hosszú felsorolás, a
szomszédos sorok ugyanott biztosan illesztve). H8415: 1Móz 49:25, 5Móz 33:13, 1Móz 7:11 … → 1., Ez 26:19, Hab 3:10 … → 2.,
a Zsolt 71:20 → 5. (ezt mondja a BDB).

**Kiadott lapok.** A 79 szóból lexikonlapon: H8415 (ALVIL-001 csak forrássorban; TEREMT-001 próbalap), H7043, H7843
(HAMART-001: a változott Ézs 36:10 csak a BDB-idézetben), H0430 (ISTENTISZT-001, MENNY-001: a változott Zsolt 97:7 nincs a
lapon). A kiadott és a jóváhagyott lapok 1. táblája nem érintett.

**Kapu:** `ellenoriz.py` 48 (plafon 2 futam / 10 sor; a javítás előtt 45 / 1 188 → bukik), teszt `BeragadtKurzor`.
