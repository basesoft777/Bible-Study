# F123 U1 — az ANTROP-001 teljesség-mérése három hálóval (DT548)

*#123 MIGRACIO2 v2 · U1 (`munka: adat`) · ág: `claude/confident-brahmagupta-93518c` · modell: claude-opus-5-5 · 2026-11-03 · sablon: `9_` v1 (DT-F123c)*

*Döntés nélküli mérés. Eszköz: `eszkozok/teljesseg_meres.py`, ennél a motívumnál bővítve a **szópár-móddal** (`--kollokacio --rokon G4151=G4152,G5590=G5591`; teszt: `eszkozok/teszt_teljesseg_meres.py`, 11 OK), mert a motívum azonossága nem egy szó, hanem két szó együttállása: az 1. háló így a pár (vagy a tagok melléknévi alakjának) közös versei, nem a négy Strong egyenkénti ~1 600 verse. Soronkénti kimenet: `naplok/F123_teljesseg_ANTROP-001.tsv` (2 500 sor, minden sor mellett a háló proveniencia-sora). Az eltérések gépi lexéma-osztálya: `naplok/F123_teljesseg_ANTROP-001_blokkok.tsv` (`naplok/F123_ANTROP2_osztaly.py`); a TR/kritikai szövegállás: `naplok/F123_ANTROP2_tr_kritikai.tsv`. A hét lépés determinisztikus részének mai futása: `naplok/F123_ANTROP2_u1_kimenet.txt` (`naplok/F123_ANTROP2_u1_futtat.sh`, 20 sor az `adat/auditok.tsv`-ben, B4).*

## 0. A mért állapot

- Gerinc-elem (`elofordulasok.tsv` `gerinc_elem`): **G4151+G5590** (πνεῦμα + ψυχή; 7 sor) és **H5315+H2416** (nefes + chajjá; 1 sor: 1Móz 2:7). Rokon alak (a negatív kritérium „vagy melléknévi alakjuk” kitétele): G4152 πνευματικός, G5591 ψυχικός.
- Előfordulás-versek: 8. Jelölt-versek (`elofordulas`): 25 (a 20 jelöltsor tartomány-sorai versenként).
- A Károli-háló szótári alakjai (`--karoli-szavak`): **lélek, lelki, szellem, szellemi**. Kiválasztás: a `karoli_szo` mezők szavai közül azok, amelyek a két szó (és melléknevük) fordításai; a környezet szavai (élő, megelevenítő, Isten, ember, a névelők) és a Zsid 4:12 „szívnek” alakja kimarad — a Károli ott a ψυχή-t fordítja szívnek, de a „szív” más szavak (καρδία, lév) állandó fordítása, a háló vele használhatatlan lenne. A „valótok” (1Thessz 5:23, a πνεῦμα fordítása) ugyanezért kimarad.

## 1. Összegzés

| Háló | Találat (vers) | E | J | ELTÉRÉS | ebből a versben áll a pár |
|---|---|---|---|---|---|
| 1. szópár (TAHOT + TAGNT, egy versben) | 71 | 5 | 6 | **60** | 60 (mind a héber pár) |
| 2. Károli-szó | 1 072 | 8 | 16 | **1 048** | 41 (mind a héber pár) |
| 3. szótár (BDB H5315, H2416; Thayer G4151, G4152, G5590, G5591) | 1 357 | 7 | 15 | **1 335** | 60 (mind a héber pár) |
| fordított irány: E-vers, amelyet egyik háló sem ad | | | | **0** | |

**Eredmény.** A görög szópár minden közös verse (egy versben 10: 6 főnévpár, 4 rokon alakkal) az adatban van, előfordulásként (5) vagy jelöltként (6; 1Pét 1:22, Mt 12:18, Fil 1:27, 1Kor 15:44, 15:46, Júd 1:19 — a Fil 1:27 a régi döntési fájlból, a többi a #108-ból és az X.A-ból). Az 1. háló 60 eltérése a héber pár (nefes + chajjá) 60 verse, amelyet a DT503 blokkban zár ki (közülük kettő, a Jób 12:10 és a Jón 4:8, külön sor). A 2. és a 3. háló eltéréseiből egy sem hordozza a görög párt: a versben csak az egyik szó áll, vagy más szó. Ez mért tény; a jelöltek minősítése az U2 döntése.

Három E-vers (Luk 1:46, 1:47, 1Kor 2:15) nem a szópár-hálóból jön, mert a pár két versen át, egy mondatban áll (Luk 1:46–47), illetve két vers ellentétében (1Kor 2:14–15); a Károli- és a szótár-háló megfogja őket. A versablakos mérés (±1 vers) az X.A-ban futott (`naplok/F123_adat_ANTROP-001.md` 1b.), a mai újrafuttatás: 3.

Proveniencia:
- `scope=TAHOT-teljes+TAGNT-teljes: egy versben (G4151|G4152)+(G5590|G5591) | (H5315)+(H2416) | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | n=71 | ts=2026-11-03T08:50Z`
- `scope=Karoli_1908-teljes | forras=Karoli_1908.tsv+adat/szoto/karoli_szotari_alak.tsv | szotari_alak=lelki+lélek+szellem+szellemi | n=1072 | ts=2026-11-03T08:50Z`
- `scope=G4151+G4152+G5590+G5591+H2416+H5315 | forras=adat/bdb_vers_jelentes.tsv+adat/thayer_vers_jelentes.tsv (karoli_vers) | n=1357 | ts=2026-11-03T08:50Z`

## 2. Az eltérések lexémánként (gépi osztályozás, 1 715 vers)

Egy vers egy osztályba kerül, az első egyező szerint (a sorrend az elsőbbség). A három háló eltérései együtt:

| Osztály | Vers | Hálók (Károli / szótár / szópár) | Mi áll a versben |
|---|---|---|---|
| héber pár | 60 | 41 / 60 / 60 | nefes + chajjá egy versben, a görög pár nélkül (DT503) |
| rúah + nefes | 5 | 4 / 4 / — | Jób 7:11, Ézs 26:9, Ézs 42:1, Jer 2:24, Préd 6:9: héber szópár; a negatív kritérium a görög szópárt kéri |
| csak πνεῦμα | 335 | 313 / 330 / — | a ψυχή nem áll a versben (legtöbbször a Szent Lélek) |
| csak ψυχή | 81 | 49 / 78 / — | a πνεῦμα nem áll a versben (legtöbbször: élet, személy) |
| csak πνευματικός | 16 | 16 / 14 / — | a ψυχή és a ψυχικός nem áll a versben |
| csak ψυχικός | 1 | — / 1 / — | Jak 3:15 („földi, testi és ördögi”) |
| csak nefes | 551 | 385 / 400 / — | ÓSZ |
| csak rúah | 200 | 192 / 30 / — | ÓSZ |
| csak chaj/chajjá | 359 | — / 359 / — | ÓSZ (a BDB H2416 idézett helyei) |
| más héber szó | 66 | 27 / 39 / — | a Károli „lélek”-je más szót fordít (nesámá, lév stb.), vagy a szótár összevető helye |
| más görög szó | 41 | 21 / 20 / — | ugyanez az Újszövetségben |

Proveniencia: `scope=naplok/F123_teljesseg_ANTROP-001.tsv ELTÉRÉS-sorai × TAHOT/TAGNT (G4151, G4152, G5590, G5591, H5315, H2416, H7307) | forras=naplok/F123_ANTROP2_osztaly.py, split('\t') | n=1715 | ts=2026-11-03T08:51Z`

**A Károli szóhasználata.** A Károli a két görög szót nem választja szét: a ψυχή-t és a πνεῦμα-t is többnyire „lélek”-nek fordítja (Luk 1:46–47: mindkettő „az én lelkem”), a πνεῦμα-t az 1Thessz 5:23-ban „valótok”, a ψυχή-t a Zsid 4:12-ben „szívnek” adja vissza, „szellem” csak az 1Kor 15:45-ben áll („megelevenítő szellemmé”). A melléknevek: ψυχικός „érzéki” (1Kor 2:14; 15:44, 46; Júd 1:19) vagy „testi” (Jak 3:15), πνευματικός „lelki”. A Károli-háló ezért nem a párt, hanem a „lélek” szó ezer versét adja; a megkülönböztetés a magyar szövegben nem látszik, csak az eredetiben.

## 3. Szövegállás: Textus Receptus és kritikai kiadás (`9_` v1, 3. szabály; DT563)

Mind a 21 újszövetségi E- és J-versben megnézve, a két szó és melléknevük minden alakján (37 szó; a TAGNT „Kritikai kiadás” mezője):

- **E-helyeken eltérés nincs:** az 1Thessz 5:23, Zsid 4:12, Luk 1:46, 1:47, 1Kor 2:14, 2:15 és 15:45 minden érintett szava a TR-ben és az NA28-ban is áll.
- **J-helyeken három szó csak a TR-ben áll:** 1Pét 1:22 πνεύματος („a Lélek által”), Luk 9:55 πνεύματός („minémű lélek van ti bennetek”) és Luk 9:56 ψυχάς („az emberek lelkét”). A kritikai szövegből mindhárom hiányzik.
- A többi J-hely (1Kor 15:44, 15:46, Júd 1:19, Fil 1:27, Mt 12:18, 1Pét 3:19–20, 2Kor 1:22–23, ApCsel 4:31–32, 20:23–24, Júd 1:20) mindkét szövegben azonos.

## 4. A Septuaginta-híd a héber pár helyein

A 61 nefes + chajjá vers Septuaginta-megfelelőjében a görög pár két helyen áll: **Jób 12:10** (ψυχή + πνεῦμα) és **Jón 4:8** (ψυχή + πνεῦμα, ahol a πνεῦμα a keleti szél). 58 helyen csak a ψυχή, egy versnek (1Sám 17:55) nincs Septuaginta-megfelelője; az 1Móz 2:7-ben a Septuaginta πνοή-t (lehelet) ír, nem πνεῦμα-t. A `9_` v1 4. szabálya szerint a Septuaginta-többlet nem előfordulás (a motívum a héber, illetve a görög eredeti szövegre épül); a próza tényként említheti.

Proveniencia: `naplok/F123_ANTROP2_u1_lxx_hid.tsv` (a mai újrafuttatás, 61 sor, soronként a saját `lxx-hid` proveniencia-sorával; ts=2026-11-03T08:44Z).

## 5. A hét lépés mai futása (1., 3–6.) és a változás az X.A-hoz képest

| Lépés | Eredmény | Proveniencia |
|---|---|---|
| 1. gerinc-metszet | 1Thessz 5:23 × Zsid 4:12: 3 (G4151, G5590, G2316 θεός); Luk 1:46–47 × 1Kor 15:45: 2 (G4151, G5590); 1Móz 2:7 × 1Kor 15:45: 0 (héber és görög nem metszhető; a híd az LXX) | `scope=range:1Thessz 5:23+Zsid 4:12 … n=3 | ts=2026-11-03T08:46Z` stb., `naplok/F123_ANTROP2_u1_kimenet.txt` |
| 3. scan | G4151: 351 vers; G5590: 96; G4152: 21; G5591: 5; H5315: 683; H2416: 449 | ts=2026-11-03T08:46–47Z |
| 4. kollokáció | G4151+G5590: 6; G4151+G5591: 2 (1Kor 2:14, Júd 1:19); G4152+G5590: 0; G4152+G5591: 2 (1Kor 15:44, 15:46); H5315+H2416: 61; H7307+H5315: 8 (mért, nem gerinc-elem) | ts=2026-11-03T08:47Z |
| 5. igealak | G5591: 6 alak; G4152: 26 alak | ts=2026-11-03T08:47Z |
| 6. LXX-híd | 1Móz 2:7 (πνοή + ψυχή), Jób 12:10, Jón 4:8; a teljes 61 hely: 4. | ts=2026-11-03T08:47Z |

**A változás az X.A-hoz** (`naplok/F123_adat_ANTROP-001.md`, 2026-11-02) képest — a három munkaszkript (`f108`, `rokon`, `lxx`) mai újrafuttatása, a kimenet `naplok/F123_ANTROP2_u1_*.tsv`: **új hely 0, eltűnt hely 0, gerinc-elemet érintő eltérés nincs.** Az egyetlen különbség a 9 X.A-hely állapota: „ÚJ” → „jelölt (nyitva)”, mert a DT501 óta a `jeloltek.tsv`-ben vannak (a #108-összevetés jelölt-sora ezért 11 → 20).

## 6. Az eltérések elbírálása (U2)

A 12 egyenkénti jelölt: 3 `beépítve` (1Kor 15:44, 15:46, Júd 1:19), 9 `elutasítva` (nem egy mondat 4, nem megkülönböztető szerepben 4, a Júd 1:19–20 tartomány-sora 1); a héber pár Septuaginta-hídjának két helye (Jób 12:10, Jón 4:8) külön sorban `elutasítva`; a 2. szakasz 1 715 eltérő verse 11 lexémánkénti blokk-sorban (a héber pár blokkja 58 vers: a 60-ból a két külön sor nélkül). Az elutasítási okok: `adat/elutasitasi_okok.tsv`, 5 ANTROP-001-sor. A döntés és forrása: `naplok/F123_ANTROP2_naplo.md` U2.
