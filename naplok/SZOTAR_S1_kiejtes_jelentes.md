# SZOTAR_S1_kiejtes_jelentes.md — S1.3 (`eszkozok/kiejtes.py`) jelentése

*2026.09.28 · a `SZOTAR_BRIEF.md` v1.5 S1.3 tételének záró jelentése.*

## 1. Amit ez a tétel ad

`eszkozok/kiejtes.py` — a görög SBL-stílusú (Unicode makronos) akadémiai
átirat → magyaros kiejtés konvertere, `adat/kiejtes_szabalyok.tsv` (22
sorrendfüggő, literális csereszabály) és `adat/kiejtes_kivetelek.tsv`
(egész-alak kivételek, `nyelv=gorog`) alapján. CLI: `--atir SZOVEG`,
`--ellenoriz` (aranykészlet-próba, nem ír), `--onteszt`.

## 2. D32 — javítás a szabálytábla első (S1.2) változatához képest

Az S1.2-ben felvett `kiejtes_szabalyok.tsv` **ellenőrzés nélkül** azt
feltételezte, hogy az upsilon (υ) SBL-átirata mindig `y` (pl. `kyrios`) —
ez a feltételezés **kézi visszafejtésből** (a célszövegből visszafelé
következtetve) született, nem a tényleges forrásadatból. Az S1.3
ellenőrzés (`konkordancia/TBESG.txt`/`TAGNT_kivonat.tsv` közvetlen
lekérdezése) kimutatta: **a tényleges SBL-forrás sima `u`-t használ**
(`κύριος` → `kurios`, nem `kyrios`; `κηρύσσω` → `kērussō`, nem `kēryssō`).

**Javítva:** a `Y`/`y` szabály törölve, `U`/`u` szabály bekerült (az `ou`
diftongus-szabály UTÁN, hogy egy `ou`-ban lévő `u` ne váljon tévesen
`ü`-vé); a makron-ū szabály célja `ú`-ról `ű`-re módosult (a hosszú
ü-hang megkülönböztetésére a sima `u`-tól).

**Második hiba, ugyanebben a körben:** az `u`→`ü` szabály először az
**αυ/ευ diftongusok** `u`-ját is tévesen átalakította (`καύχημα` →
`kauchēma` → hibásan `kaükhéma` `kaukhéma` helyett) — az αυ/ευ-ban az
`u` nem álló upsilon-hang. Javítva: `eszkozok/kiejtes.py` `atir()`-ja az
`au`/`Au`/`eu`/`Eu` szekvenciákat a szabálytábla lefutása előtt
maszkolja (azonos technikával, mint a σσ-geminációt, l. alább).

**Harmadik hiba, ugyanebben a körben:** a σσ (dupla szigma) → `ssz`
átírás (magyar geminációs helyesírás) **nem tehető be a szekvenciális
szabálytáblába**, mert az általános `s`→`sz` szabály a `ssz`-ben BENNE
MARADÓ két bare `s` betűt újra feldolgozná. Megoldás: a `σσ`-t az
`atir()` a szabálytábla előtt maszkolja, a séma-táblában (`adat/SEMA.md`
2.16) és a `kiejtes_szabalyok.tsv` fejlécében is dokumentálva, hogy ez a
sor **szándékosan hiányzik** a táblából.

Mindhárom hibát a `--onteszt` és a `--ellenoriz` aranykészlet-próba
fogta ki, nem kézi átolvasás.

## 3. `--ellenoriz` — teljes kimenet

```
=== S1.3 kiejtes.py --ellenoriz ===
Aranykeszlet (naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv, gorog, arany): 30 egyedi par, ebbol 26 "tiszta" (szo-/kifejezes-szintu, toldas nelkuli) par tesztelheto itt automatikusan; 4 kontextus-fuggo (nevelo-/rovidites-toldassal) par nem, l. a C:\Users\bases\Desktop\Bible-Study\naplok\SZOTAR_S1_kiejtes_arany_sbl.tsv fejleceben es a jelentes vegen.
Ebben a futasban vizsgalt parok szama: 26

Fo proba: 26/26 par egyezik pontosan.

Szabalyonkenti lefedettseg (hany par forrasa tartalmazza a mintat):
  #1 'Ch' -> 'Kh': 0 par
  #2 'ch' -> 'kh': 1 par <-- 1 part fed le, KIVETEL-JELOLT, nem mozgatva
  #3 'Ph' -> 'F': 0 par
  #4 'ph' -> 'f': 1 par <-- 1 part fed le, KIVETEL-JELOLT, nem mozgatva
  #5 'OU' -> 'Ú': 0 par
  #6 'ou' -> 'ú': 1 par <-- 1 part fed le, KIVETEL-JELOLT, nem mozgatva
  #7 'U' -> 'Ü': 0 par
  #8 'u' -> 'ü': 4 par
  #9 'Z' -> 'Dz': 0 par
  #10 'z' -> 'dz': 3 par
  #11 'S' -> 'Sz': 1 par <-- 1 part fed le, KIVETEL-JELOLT, nem mozgatva
  #12 's' -> 'sz': 8 par
  #13 'Ē' -> 'É': 0 par
  #14 'ē' -> 'é': 3 par
  #15 'Ō' -> 'Ó': 0 par
  #16 'ō' -> 'ó': 15 par
  #17 'Ā' -> 'Á': 0 par
  #18 'ā' -> 'á': 0 par
  #19 'Ī' -> 'Í': 0 par
  #20 'ī' -> 'í': 0 par
  #21 'Ū' -> 'Ű': 0 par
  #22 'ū' -> 'ű': 0 par

1 part lefedo szabalyok (kivetel-jeloltek, 4 db):
  #2 'ch' -> 'kh' -- egyedul a(z) 'καύχημα' par hasznalja (forras: 'kauchēma')
  #4 'ph' -> 'f' -- egyedul a(z) 'φωνέω' par hasznalja (forras: 'phōneō')
  #6 'ou' -> 'ú' -- egyedul a(z) 'ἐπικαλουμένους' par hasznalja (forras: 'epikaloumenous')
  #11 'S' -> 'Sz' -- egyedul a(z) 'Σήμ' par hasznalja (forras: 'Sēm')

Kihagyasos (leave-one-out) proba: minden 1-part-lefedo szabalyt egyenkent eltavolitva ujrafuttatjuk a TELJES 26 paros keszletet -- elvart eredmeny: PONTOSAN a sajat parja bukik el, semmi mas nem valtozik. (Ez nem klasszikus per-pelda leave-one-out, mert a szabalyok nem par-specifikusan "tanultak", hanem kezzel, a teljes aranykeszletre egyszerre levezetett altalanos fonetikai szabalyok -- igy az egyetlen mechanikusan ismetelheto valtozat az, hogy egy szabaly KIVETELET elhagyva izolaltan bukik-e csak a sajat parja.)
  #2 'ch' kihagyva: RENDBEN -- kizarolag a sajat parja ('καύχημα') bukik, semmi mas
  #4 'ph' kihagyva: RENDBEN -- kizarolag a sajat parja ('φωνέω') bukik, semmi mas
  #6 'ou' kihagyva: RENDBEN -- kizarolag a sajat parja ('ἐπικαλουμένους') bukik, semmi mas
  #11 'S' kihagyva: RENDBEN -- kizarolag a sajat parja ('Σήμ') bukik, semmi mas

MEGJEGYZES: a fenti 100%%-os (vagy annal alacsonyabb) egyezes ONMAGABAN NEM elfogadasi erv -- a lefedettsegi es kihagyasos reszlet egyutt ertekelendo (SZOTAR_BRIEF.md D31 mintajara).
```

## 4. A 4 kihagyott ("kontextus-függő") arany pár

A `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv` gorog "arany" 30 egyedi
párjából 4-et **nem** tesztelt a `--ellenoriz`, mert a célszöveg olyan
szót/rövidítést told hozzá, amit a puszta forrás-szó karakterenkénti
átírása nem tud reprodukálni (nem `kiejtes.py`-hiba, hanem az adat
jellege):

| Forrás (görög) | Cél | Miért nem tesztelhető |
|---|---|---|
| `καλούμενος` | `ho kalúmenosz` | a `ho` névelő nincs a forrásban (a study szövegkörnyezetéből jön) |
| `ὃν Βριάρεων καλέουσι θεοί` | `hon Briareón kaleúszi theoi` | teljes idézett mondat, a rekesztő lehelet (ὃν) SBL-visszafejtése bizonytalan |
| `ὄνομα ἐπί τινι` | `k. onoma epi tini` | a `k.` rövidítés-előtag nincs a forrásban |
| `τινὰ ἐπὶ τῷ ὀνόματι τοῦ πατρός` | `k. tina epi tó onomati tú patrosz` | a `k.` előtag, és a `τῷ` datívusz-alak SBL-je nem egyértelmű |

Ezek a párok a jövőben — ha valaki a kézi ISTENTISZT-001-szöveg egy-egy
kifejezését is gépi próbába akarja vonni — külön, a `k.`/`ho`
kontextus-szó eltávolításával tesztelhetők; ez nem ennek a tételnek a
tárgya.

## 5. Adatminőségi lelet a gold-készletben (nem blokkoló)

A `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv` "szo" oszlopában **12
görög "arany" pár csonkolt** — az első (ékezetes/lehelet-jeles) betű
hiányzik (pl. `γκαλέω` `ἐγκαλέω` helyett, `νομάζω` `ὀνομάζω` helyett).
Ez egy korábbi (S0-előtti) másolási/kódolási hiba a tesztkészletben, nem
ennek a tételnek a bevezetése. A `naplok/SZOTAR_S1_kiejtes_arany_sbl.tsv`
minden ilyen sorban a `megjegyzes` oszlopban jelzi a csonkolást, és a
teljes (helyreállított) görög alakot használja a nyomon követhetőséghez
— a tényleges SBL-forrás és a célkiejtés érintetlen, tehát a próbát nem
érinti. **Javaslat, nem döntés:** a `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv`
saját maga is javítható lenne, de ez a tábla más menetek (K10, RENDER)
saját mérési alapja is, ezért ezt a jelentést csak jelzésnek szánom, nem
javítási kérésnek.

## 6. Redundáns kivétel-jelöltek

A `adat/kiejtes_kivetelek.tsv` (S1.2-migráció) 3 görög sora —
`epikaleō`, `kaleō`, `boaō` — **a mostani szabálytáblával önmagában is
helyesen adódna** (mindhárom pusztán az `ō`→`ó` szabályt igényli). Az
`atir()` ennek ellenére a kivétel-útvonalon oldja fel őket (egész-alak
egyezés elsőbbséget élvez), ami helyes eredményt ad, de a 3 sor jelenleg
**felesleges**. Nem távolítottam el — ez az S2.1 tétele (a kódbeli
`KIEJT` tábla kivezetésével együtt, D30/D31 nulla-diff elve szerint), és
a döntés (megtartani dokumentációs célból vagy törölni) emberi mérlegelést
igényel.

## 7. Összegzés

- `eszkozok/kiejtes.py` elkészült, `--atir`/`--ellenoriz`/`--onteszt`.
- A 26 tesztelhető arany pár mindegyike egyezik (26/26).
- 4 szabály fed le pontosan 1 párt; mindegyiket a kihagyásos próba
  igazolta (a szabály nélkül KIZÁRÓLAG a saját párja bukik el).
- 4 arany pár kontextus-függő, nem tesztelhető ezzel az eszközzel — l. 4. szakasz.
- Adatminőségi lelet (12 csonkolt "szo"-sor) és egy redundancia-lelet
  (3 felesleges kivétel) dokumentálva, egyik sem blokkoló.
- **A 100%-os egyezés önmagában nem elfogadási érv** — a fenti
  lefedettségi és kihagyásos részlet együtt adja a tényleges bizonyítékot.

A menet végi ⛔-nél ennek a jelentésnek a 3. szakaszában felsorolt „1 párt
lefedő szabályok” (4 db) a 26 héber kiejtés-jelölttel és a kézi
BDB-etimológia-határokkal együtt kerülnek jóváhagyásra.
