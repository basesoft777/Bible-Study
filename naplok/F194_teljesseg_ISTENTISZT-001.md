<!-- F194.2: a mérés a `naplok/F194_teljesseg_meres.py` futtatója, az F123-as hálókkal és az új ÚSZ-feltétellel (DT-F194a: ἐπικαλέω + ὄνομα + az Úr megnevezése, G2962/G2424). Az alábbi szöveg az F123-as szkript sablonja; a 4. szakasz rögzített mondatai az F123-as mércét írják le. A 2. kiadás mércéjén az E-versek közül a görög feltételt a TAGNT kritikai szövegén az ApCsel 22:16 sem teljesíti (ott αὐτοῦ áll, κυρίου nélkül); a Károli a Textus Receptust követi („az Úrnak nevét”), ezért a vers marad (DT-F194a). A LXX-híd (6. lépés): naplok/F194_lxx_hid_ISTENTISZT-001.tsv, a döntések: naplok/F194_lxx_jeloltek.py. -->
# F123 U1 — az ISTENTISZT-001 teljesség-mérése három hálóval (DT548)

*#123 MIGRACIO2 v2 · U1 (`munka: adat`) · ág: `claude/relaxed-raman-0562d4` · modell: claude-sonnet-5-5 · 2026-11-12*

*Döntés nélküli mérés az arany lap (kiadott, 1. kiadás) kifejezésére. Eszköz: `eszkozok/teljesseg_meres.py` függvényei, a motívum-specifikus futtató `naplok/F123_ISTTELJ_meres.py` (a kifejezés ellenőrzése tokensorrendből). Soronkénti kimenet: `naplok/F123_teljesseg_ISTENTISZT-001.tsv` (695 sor, minden sor mellett a háló proveniencia-sora); a tömeges, kifejezés nélküli osztályok: `naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv`. A `jeloltek.tsv`-be ez a menet nem írt.*

## 0. A mért állapot

- Strongok (az `elofordulasok.tsv` `strong` mezője): **H7121** (קָרָא, qárá) + **H8034** (שֵׁם, sém; a gerinc-elem páros), **G1941** (ἐπικαλέω, epikaleó). A negatív kritérium az ónom-t is megköveteli (G3686, onoma; az ÚSZ-sorok `strong` mezőjében nincs, a páros tagja).
- Előfordulás-versek: 20. Jelölt-versek (`elofordulas`): 131.
- A motívum kifejezése (a mérés „kifejezés a versben” mércéje, `motivumok.tsv` negatív kritérium, DT476/DT478): ÓSZ: H8034 a H9003 (be-) előtaggal, a név után legfeljebb 2 tokenen belül H3068 (JHVH), és a H7121 legfeljebb 9 tokenen belül előtte vagy utána; ÚSZ: G1941 és G3686 legfeljebb 6 tokenre egymástól. A névmási rag („nevét”) vagy más név a héber szövegben nem JHVH, tehát nem teljesít.
- **1. háló (Strong):** a motívum szópárjai: (H7121 ∧ H8034) és (G1941 ∧ G3686) egy versben. Szópár-mód, mert az azonosság hordozója a kifejezés (formulaikus), nem egy szó; a H7121 egyedül 687, a H8034 771 vers, a G3686 215 vers (TAHOT/TAGNT-mérés, 2026-11-04).
- **2. háló (Károli-szó), szótári alakok:** `segítségül` (a formula magyar kifejezése: az E-sorok `karoli_szo` mezőiben 20 sor), továbbá a `hív` ∧ `név` és a `kiált` ∧ `név` együttállás egy versben (a `karoli_szo`-mezők alakjai: név 18, hív 16+, kiált 2). Kimaradnak a környezet szavai (Úr, Isten, ott, az, ti, Ábrám, Baál, örökkévaló) és az egyedi nevek. Indok: a szó önmagában csak a „segítségül” kellően szűk (az Istennek szóló hívás); a „hív” és a „kiált” a Károlinál sok mást fordít (hívni = elnevezni, meghívni), ezért csak a „név” társaságában számít háló-találatnak. A 2Móz 33:19 és 34:5 („kiáltom előtted az Úr nevét”, „nevén kiáltá az Urat”) a „kiált” ∧ „név” szabályon át fogható meg. A szótövező ismert korlátja (SZOTOVEZES_meres.md): a „segítségűl” írásmód külön sor.
- **3. háló (szótár):** BDB (`bdb_vers_jelentes.tsv`) és Thayer (`thayer_vers_jelentes.tsv`) által a **H7121**-nél és a **G1941**-nél idézett Károli-versek. A H8034 és a G3686 szócikke a névről szól, nem a hívásról, ezért a szótár-háló az igék Strongjaira szűkül.

## 1. Összegzés

| Háló | Találat (vers) | E | J | ELTÉRÉS | ebből a versben áll a motívum kifejezése |
|---|---|---|---|---|---|
| 1. Strong (TAHOT + TAGNT, szópár) | 204 | 20 | 28 | **156** | 0 |
| 2. Károli-szó | 96 | 20 | 17 | **59** | 0 |
| 3. Szótár (BDB H7121, Thayer G1941) | 395 | 12 | 45 | **338** | 0 |
| fordított irány: E-vers, amelyet egyik háló sem ad | | | | **0** | |

Az E-vers, amelyet egyik háló sem ad: —.

Proveniencia:
- `scope=TAHOT-teljes+TAGNT-teljes: egy versben (H7121)+(H8034) | (G1941)+(G3686) | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | n=204 | ts=2026-11-12T06:58Z`
- `scope=Karoli_1908-teljes | forras=Karoli_1908.tsv+adat/szoto/karoli_szotari_alak.tsv | szotari_alak=segítségül; hív∧név; kiált∧név | n=96 | ts=2026-11-12T06:58Z`
- `scope=H7121+G1941 | forras=adat/bdb_vers_jelentes.tsv+adat/thayer_vers_jelentes.tsv (karoli_vers) | n=395 | ts=2026-11-12T06:58Z`

## 2. A kifejezés nélküli ELTÉRÉS-találatok osztályai (gépi osztályozás)

A találatok (vers, háló szerint, egy vers több hálóban is szerepelhet) a vers tokensorrendje szerint, elsőbbségi sorrendben osztályozva. A versenkénti lista: `naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv`.

| Osztály | Vers | Tartalom |
|---|---|---|
| besem_JHVH_nelkul | 11 | qárá + be-sém áll, de nem JHVH a név birtokosa (névmási rag, más név, elohim: a DT476/DT478 kizárása) |
| elnevezes_nev | 125 | qárá + sém, de elnevezés („nevét X-nek nevezte”), nem invokáció |
| epikaleo_onoma_nelkul | 0 | G1941 áll, onoma nélkül (név nélküli segítségül hívás, DT476 K2) vagy nem a közelében |
| kulon_kontextus | 20 | qárá és sém a versben, de nem egy szerkezetben |
| qara_nev_nelkul | 245 | qárá áll a versben, név (sém) nélkül: hívás, kiáltás, meghívás |
| mas_lexema | 50 | a vers más lexémája (a hív/kiált/segítségül magyar szó más héber vagy görög szót fordít) |

Az `epikaleo_onoma_nelkul` és `besem_JHVH_nelkul` versek száma és tartalma a 4. szakaszban külön áll, mert ezek a határ közelében esnek.

## 3. A 2. kiadás jelöltjei: a háló talál, az adat nem ismeri, és a versben a motívum kifejezése áll

Ide azok a versek kerülnek, amelyek (a) legalább egy hálóban ELTÉRÉS-ként szerepelnek (az `elofordulasok.tsv`-ben és a `jeloltek.tsv`-ben sincsenek), és (b) a héber/görög szövegben a fenti kifejezés áll. A lista keresési eredmény, nem döntés; a felvétel a 2. kiadás menetében, a negatív kritérium és a `jeloltek.tsv` döntéssel történik. Ez a menet nem ír a `jeloltek.tsv`-be.

**Nincs ilyen vers: a három háló a kifejezéssel mért teljes ÓSZ/ÚSZ-ben nem hozott új helyet.** Az 1. kiadás listája (22 vers) a mérce szerint teljes. A határesetek a 4. szakaszban állnak.

Proveniencia: `scope=ISTENTISZT-001 ELTÉRÉS × TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (tokensorrend) | forras=naplok/F123_ISTTELJ_meres.py | ts=2026-11-12T06:58Z`

## 4. A határ közelében: a döntött jelöltek és a kifejezés

- **J-vers, nem E, a versben a kifejezés áll** (már döntött; csak tájékoztató, a mérés nem érinti): 1 vers: ApCsel 15:17.
- **E-vers, amelyen a kifejezés-mérce nem teljesül: 1Kir 18:25, 18:26** — ezek a kontrasztként megtartott kivételek (a névhez elohéchem, illetve ha-Báal tartozik, nem JHVH; DT476), tehát a mérce és a motívum-meghatározás kivétele egyezik.
- **Szóalak szerinti közeli esetek, amelyeket a mérce kizár:** 1Móz 16:13 („nevezé az Urat”, qárá + sém-JHVH be- nélkül, elnevezés), 2Móz 17:15 (oltár-elnevezés: JHVH Nisszi), Sir 3:55 (Siralmak 3:55, „nevedet” névmási raggal, a megszólított JHVH külön szó; DT476 K4). Ezek az osztályozásban elnevezes_nev, illetve besem_JHVH_nelkul alatt állnak, nem jelöltek.
- A „kifejezés” mérce ÓSZ-ben szigorú: qárá-t követő **besém-JHVH**. Az olyan alakok, amelyekben a JHVH helyén névmási rag vagy más név áll (a negatív kritérium: Zak 13:9, Zsolt 105:1, Jer 10:25, Ézs 43:1, 44:5, 45:3), nem tartoznak ide (DT476/DT478).

## 5. Vakfoltok

- A Károli-háló nem fog meg olyan E-verset, ahol a magyar kifejezés más (pl. „kiáltom előtted az Úr nevét”) — l. a 2. háló szabályát és az E-vers, amelyet egyik háló sem ad: sor. A TAGNT kritikai szöveg (NA28 stb.) és a Károli alapszövege (TR) között szövegváltozat lehet; az ÚSZ-versek a TAGNT szerint mértek.
- Az ÚSZ-ben az epikaleó-t onoma nélkül is használják (Róm 10:12, 14, 2Tim 2:22): ezek a G1941 31 versének részei, a `jeloltek.tsv`-ben `elutasítva` (DT476 K2); az `epikaleo_onoma_nelkul` osztály ezért üres: a G1941 minden verse E vagy döntött J.
