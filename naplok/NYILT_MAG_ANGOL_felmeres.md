# A nyílt mag angol rétege — felmérés (F170, 1. lépés)

*FELADATOK #170 · 2026-11-05 · modell: claude-opus-5-5 · a számok forrása: `python naplok/F170_felmeres.py` (csak olvas; a `nyilt_mag/` main-állapotán, aa61de89)*

## 1. Oszlopok besorolása

**Zárt** = a kapu `ZART` listájában álló vagy a generátor rögzített szótárából képzett oszlop (értékei felsorolhatók,
a kódkönyv soronként leírja). **Szabad** = projektben írt magyar próza vagy címke. **Adat** = azonosító, igehely,
szám, dátum, eredeti nyelvű vagy forrásszöveg (nem fordítandó).

| Fájl / oszlop | Besorolás | Egyedi érték | Karakter (egyedi) | Megjegyzés |
|---|---|---:|---:|---|
| `elofordulasok.funkcio` | szabad (rövid címke) | 55 | 1 128 | a brief 3. pontja |
| `kizarasok.indoklas` | szabad | 175 | 36 142 | a brief 3. pontja |
| `kizarasok.korabbi_minosites` | szabad | 15 | 4 077 | az indoklás folytatása (a ` \| ` utáni rész) |
| `beepitesi_dontesek.indoklas` | szabad | 236 | 25 208 | a brief 3. pontja (felvételi indoklás) |
| `dontesnaplo.kerdes` + `.dontes` | szabad | 16 | 4 185 | a nyilvános döntésnapló; a kapu (c) ezt is szabad szövegnek méri |
| `motivumok.cim` | szabad | 9 | 429 | a brief 4. pontja |
| `motivumok.rovid_cimke` | szabad | 9 | 144 | |
| `motivumok.tema` | szabad | 8 | 125 | |
| `motivumok.negativ_kriterium` | szabad | 9 | 4 193 | a brief 4. pontja |
| `motivumok.folerendelt_fogalom` | szabad | 9 | 898 | a brief 4. pontja |
| **szabad összesen** | | **532** | **≈ 76 500** | |
| `kizarasok.kizaras_oka` | zárt (az `adat/elutasitasi_okok.tsv` `cimke`-je + „(összesítő sor)” + „a besorolás nincs rögzítve”) | 55 | 2 267 | ma **nem** áll a kapu `ZART` listájában, nincs kódkönyv-sora |
| `forrasok_es_licencek.ok` | zárt (a generátor rögzített mondatai) | 8 | 460 | ma nem `ZART` |
| `elofordulasok/kapcsolatok/motivum_kapcsolatok.forras_megnevezes` | zárt, `; `-vel összetett (a generátor `FORRAS_OSZTALY`-a + dataset-név) | 8 | 318 | ma nem `ZART` |
| `kapcsolatok.lekerdezes_tipusa` | zárt | 1 | 30 | a másik két táblában `ZART`, itt nem |
| a többi `ZART` oszlop (16 oszlop, 8 tábla) | zárt | 102 | — | mind van kódkönyv-sora magyar + angol leírással (`leiras_en`) |
| `karoli_szo` (két tábla) | adat | 200 | 3 115 | a Károli-fordítás szava: a forrásszöveg maga, **nem fordítandó** |
| `horgony` | adat | 38 | 318 | Strong-szám, átírt szópár, igehely, görög formula |
| `jelentes_en` | adat (angol) | 42 | 1 838 | l. 3. pont |

**Költségbecslés (szabad szöveg).** ≈ 76 500 karakter magyar forrás ≈ 25–30 ezer bemeneti token, ≈ 20–25 ezer kimeneti
token, plusz a kötegenkénti utasítás. Sonnettel API-n ez **1 USD alatt** marad (≈ 30 ezer × 3 USD/M + 25 ezer × 15 USD/M
≈ 0,5 USD, kötegelési többlettel ≈ 0,7 USD); előfizetéses Sonnet-subagentben külön költség nincs. A zárt címkék
(≈ 3 000 karakter) ugyanebben a menetben fordíthatók, a kódkönyvbe kerülnek.

## 2. Igehely-oszlopok és könyvnevek

Igehelyet hordozó oszlop: `igehely`, `cel_igehely`, `forras_igehely`, `igehely_a`, `igehely_b`, `csoport_sor_igehely`
(6 tábla). **7 233 igehely-cella, 65 különböző könyvnév.**

- **Leképezhetetlen könyvnév: 1 (`Sir`, 24 cella, mind a `kizaras_csoportok.tsv` `igehely` oszlopában).** Eredete: az
  F123 teljességi blokk-listák (`naplok/F123_teljesseg_*_blokkok.tsv`) a TAHOT könyvnevét viszik tovább, a TAHOT pedig
  a Jeremiás siralmait `Sir`-nek írja. A projekt ezt az aliast már kezeli (`eszkozok/bdb_konyv_javit.py`
  `TAHOT_KONYV = {'Sir': 'JSir'}`, `eszkozok/bdb_adatblokk.py` `PAROK_KONYV_ALIAS`). A versszámok a JSir-rel
  egyeznek (pl. `Sir 3:58`: a JSir 3. fejezete 66 vers). **Javaslat:** ugyanez az alias a generátorban, és a csomag
  magyar `igehely` oszlopa is `JSir`-t írjon (a csomag egyetlen helyén áll `Sir`); minden más ismeretlen könyvnévre a
  generátor megáll.
- **Szabálytalan alak: 1 cella** — `beepitesi_dontesek.tsv` `cel_igehely` = `ApCsel 2:27; ApCsel 2:31` (két igehely
  egy cellában). OSIS-ban a lista szóközzel válik (`Acts.2.27 Acts.2.31`); a generátor így képzi.
- **Tartomány:** `1Móz 4:10-11` alakú cellák vannak → OSIS `Gen.4.10-Gen.4.11`.
- **Versszámozás.** A magyar `igehely` a Károli-versszámozást követi (CLAUDE.md, TAHOT-kulcs: F85). Az OSIS-kulcs
  könyvkódja szabványos, **a fejezet- és versszám a Károli-számozás** — a kódkönyv ezt kimondja. A KJV-/NRSV-
  versszámozásra átkulcsolt kulcs a `konkordancia/Karoli_versmegfeleltetes.tsv`-re épülne, amelynek licenc-címkéje
  részben „minden jog fenntartva” (a saját eltolási réteg); a nyílt magba így nem kerülhet a licencszűrés megváltoztatása
  nélkül. Ez nem e feladat része; nyitott tételnek javasolt (N-F170b).
- **Leképezési lánc:** magyar rövidítés → STEPBible-rövidítés (`konkordancia/Konyv_normalizalo_tabla.tsv`, 66 sor) →
  OSIS-könyvkód (a 66 kanonikus könyv OSIS 2.1.1 kódja, rögzített táblában a generátorban; a STEPBible-rövidítés nem
  OSIS: `Exo`/`Exod`, `1Ki`/`1Kgs`, `Ezk`/`Ezek`, …).

## 3. A `jelentes_en` mai forrása

`elofordulasok.tsv`: 255 sor, ebből **55-ben van `jelentes_en`, 200-ban üres.** A kitöltött érték a sor `szotar`
oszlopa szerinti szótár angol szövegrészlete (BDB 131 / Thayer 20 / TBESG 6 sor a `szotar` oszlopban; a `jelentes_en`
a BDB- vagy Thayer-szócikk kivonata, pl. `1Móz 3:17` H0127: „ground (as tilled, yielding sustenance)”). A
STEPBible-glosszával (TBESH/TBESG `Gloss` oszlop) **3 egyezik, 52 eltér**: a `jelentes_en` tehát **nem a
STEPBible-glossza**, hanem közkincs-szótárkivonat (BDB, Thayer; licenc: közkincs, a #162 szűrésén átment).

**Javaslat (a brief 5. pontja):** a meglévő `jelentes_en` marad (szótári jelentés, a `szotar` oszlop nevezi meg a
forrását); mellé új oszlop, `strong_glossza_en`: a sor Strong-számának STEPBible-glosszája (TBESH/TBESG `Gloss`
oszlop, CC BY 4.0, attribúcióval: „Data created by www.STEPBible.org based on work at Tyndale House Cambridge”).
Ez a 200 üres sor angol olvasójának is ad szófogódzót (Strong-számmal: 247 sor). A glossza a TBESH-ban a Brief
lexicon „Meaning” oszlopától külön álló rövid címke; a DT-F33f a TBESH egészét CC BY 4.0-nak sorolta. Több
Strong-számos (`H7121 + H8034`) sornál a glosszák ` + `-szal fűződnek.

## 4. Amit a felmérés a kapuról mutat

- A `kizaras_oka`, a `forrasok_es_licencek.ok`, a `forras_megnevezes` és a `kapcsolatok.lekerdezes_tipusa` ma nem
  áll a `ZART` listában, tehát értékeinek nincs kódkönyv-sora — a kapu (b) ezekre is kiterjesztendő.
- A `datum` oszlop vegyes alakú (`2026.09.05` és `2026-09-05`); ez nem e feladat tárgya, de a nemzetközi olvasónak
  zavaró: nyitott tételnek javasolt (N-F170c).
