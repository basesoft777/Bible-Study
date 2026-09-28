# FP2 — kiegészítő elemzések a 7. lépés előtt (2026.09.28, felhasználói kérésre)

## 1. `finish_reason` és `reasoning_tokens` a nyers usage-ból

`fp2/usage_elemzes.py`. A `fordit.py` **nem tárolja** a nyers `finish_reason`-t a
sikeres válaszban (`cache_ir` csak a `usage`-et és a validált `eredmeny`-t menti) —
de a kód logikája miatt ez közvetve mégis megállapítható: az `openrouter_hivas` minden
`finish_reason ∈ {length, max_tokens, error}` választ **elutasít és újrapróbál**; ha 3
kísérlet után sem sikerül, `OpenRouterHiba`-t dob, ami `naplok/…/FORDITAS_P_hibak`-ba
(itt: `fp2/_run/hibak/`) íródna. **Ez a könyvtár üres/nem is jött létre** — tehát a teljes
FP2-futás egyetlen hívása sem futott ki `length`-re úgy, hogy az a végleges,
mentett fordításban is `length` maradt volna.

`reasoning_tokens`: **mindhárom modellnél és minden hívásnál 0** (a `fordit.py`
`reasoning: {enabled: false}`-t küld, ez működik).

A DeepSeek csonkolt kimeneteinek `completion_tokens` értékei (pl. `G1311`: 52,
`G5010`: 113, `G5356`: 126, `G2672`: 131, `G4151` darabjai: 71–292) **nem kerek/plafon-
szerű számok** (nem 512/1024/2048/4096 közelében állnak meg) — ez **cáfolja** azt a
hipotézist, hogy egy hallgatólagos (a `fordit.py` által be nem állított) `max_tokens`
plafonba ütköztek volna. A csonkolás tehát **nem paraméterhiba** ebben az értelemben.

**Empirikus teszt (a felhasználó kérésére):** a 4 legrövidebben csonkolt, egy-darabos
DeepSeek-kimenetet (`G1311`, `G5010`, `G5356`, `G2672`) újrafuttattam explicit
`max_tokens=8000`-rel (`fp2/ujra_max_tokens.py`, teljes költség: 0,0018 USD).
**Mind a 4 újrafuttatás teljes, hű fordítást adott** (hosszarány 1,05–1,07).

| Szócikk | Eredeti pontszám (0–10) | Új pontszám (max_tokens=8000-rel) |
|---|---:|---:|
| G1311 | 1 (kihagyás, kritikus) | **10** |
| G5010 | 0 (kihagyás, kritikus) | **10** |
| G5356 | 1 (kihagyás, kritikus) | **10** |
| G2672 | 1 (kihagyás, kritikus) | **10** |

**Értelmezés:** mivel a `max_tokens` explicit megadása minden esetben javított, de a
`completion_tokens` eredeti értékei nem utaltak plafon-ütközésre, a legvalószínűbb
magyarázat **nem a paraméter**, hanem a **DeepSeek megbízhatatlansága ugyanazon a
determinisztikus (temperature=0) bemeneten** — ez megegyezik a kor2 saját, korábbi
leletével (`naplok/FORDITAS_P7_g1941_deepseek.md`: a `G1941` egyszeri csonkolása 3
újrafuttatásból egyszer sem ismétlődött). **Gyakorlati következtetés a #7-hez:** a
`FORDITAS_ELES_THAYER_BRIEF.md` G6 önjavító hurka (1× újra ugyanazzal a modellel) a
DeepSeek csonkolásainak nagy részét valószínűleg megoldaná — ez fontos adat a
tartalék-modell döntéshez.

## 2. A 20 közös (kor2) szócikk — kor2 vs. FP2, modellenként

| Modell | kor2-pontszám (P6-jelentés, 0–10) | FP2-pontszám (ugyanaz a 20 szócikk) | Különbség |
|---|---:|---:|---:|
| Gemini 3.1 Flash Lite | 8,70 | **9,60** | **+0,90** |
| DeepSeek V4 Flash | 8,60 | **5,05** | **−3,55** |

**A Gemini javulása — okok szerint bontva:**
- **Prompt v3:** a v2 kiegészítés #4 szabálya ("`from X down` → „X-tól kezdve”, soha
  nem „lefelé”") közvetlenül azt a hibát javítja, amit a kor2 vak bírálat **több
  szócikken is** (`G1311`, `G5351` stb.) "lefelé" tükörfordításként rótt fel — ez az
  FP2-mintában egyszer sem fordult elő.
- **Terminológia v2:** az `aorist`→`aorisztosz`, `marginal reading`→`széljegyzeti
  olvasat`, `Winer's Grammar`→`Winer, Grammatika` stb. 25 új sora pontosan a kor2 vak
  bírálat hibalistájából származik (l. `naplok/FORDITAS_P_terminologia_v2.tsv`
  fejléce) — ezek a kor2-ben ismételten hiányzó/inkonzisztens fordítások az FP2-ben
  következetesen megjelennek.
- **Bírálati szigor:** a kor2-ben és az FP2-ben is én (Claude) bíráltam ugyanazzal a
  rubrikával; a Gemini egyik mintában sem kapott pontossag=0 értéket — nincs jel
  szigor-eltolódásra.
- **Csonkolás:** a Geminit egyik menetben sem érintette.

**A DeepSeek visszaesése — okok szerint bontva:**
- **Prompt/terminológia:** ezek **bővítő** jellegű, hossz-növelő szabályok (nem
  vonnak el semmit) — nem magyarázzák, miért adna a modell **rövidebb** választ.
- **Bírálati szigor:** a kor2-ben a DeepSeek 20 szócikkéből 1 kapott pontossag=0-t
  (a `G1941`, dokumentáltan egyszeri hiba); az FP2-ben **12/20** (60%) kritikus —
  ez nem magyarázható a bíráló szigorának változásával, mert ugyanaz a bíráló,
  ugyanazzal a rubrikával, és a hiba típusa (súlyos hosszcsökkenés) objektíven
  mérhető, nem csak ítélet kérdése.
- **Csonkolás (darabolás):** a 20 közös szócikk közül csak 1 (`G1941`) igényelt
  volna darabolást a v1 kor2-mintában is (3746 kar. < 4000, valójában **nem**
  darabolt) — tehát a regresszió **nem** a darabolási mechanizmus mellékhatása.
- **Legvalószínűbb ok — infrastruktúra-/ár-változás:** a `naplok/FP2_felmeres.md`
  0.4 pontja szerint a `deepseek/deepseek-v4-flash` OpenRouter-ára a kor2 (2026.09.26)
  óta **kb. háromszorosára nőtt** (0,047→0,14 USD/1M bemenet). Az OpenRouter gyakran
  több háttér-szolgáltató között routol egy modellazonosító mögött; egy ilyen mértékű
  áremelkedés tipikusan szolgáltató- vagy kvantálás-váltásra utal. Ez **konzisztens**
  az 1. pontban mért empirikus ténnyel: ugyanaz a prompt, ugyanaz a modellazonosító,
  ugyanaz a hőmérséklet — de az újrafuttatás 4/4 esetben sikeres volt. A regresszió
  tehát **valószínűleg a mögöttes szolgáltatás megbízhatóságának/verziójának
  változása**, nem a módszertan (prompt/terminológia) hatása.

## 3. A G0266-korrekció szabályának gépies alkalmazása mind a 90 kimenetre

**A kulcs felfedése UTÁN** (l. `naplok/FP2_kapu_es_darabolas_elemzes.md`) alkalmaztam
gépiesen: **hosszarány < 0,8 VAGY görög/héber-paritás SÉRTÉS ⇒ kritikus kihagyás.**
Szkript: `fp2/biralat_mechanikus_javitas.py`. Kimenet: `fp2/biralat_vegleges.tsv`
(az eredeti, olvasáson alapuló pontszám és hibabesorolás **külön oszlopban megmaradt**,
nem íródott felül).

**11/90 sor** kapott eltérő minősítést a gépies szabály szerint, mint a kézi olvasás:

- **3 eset, ahol a gép szigorúbb** (`G0004`-C, `G0012`-B, `G5590`-B, mind MiniMax):
  apró görög/héber token-eltérés (pl. egy sérült ékezet vagy egy duplikált
  angol fejléc-töredék) miatt SÉRTÉS, amit a kézi olvasás nem minősített kritikusnak.
- **2 eset, ahol a gép olyat jelez, amit a kézi olvasás átsiklott** (`G4151`-A
  [Gemini], `G1343`-B [Gemini]): mindkettő a leghosszabb, darabolt szócikkek közé
  tartozik, ahol a kézi olvasás (erőforrás-korlát miatt) nem volt karakterpontos
  összevetés — **ezt korlátozásként vállalom**, és a gépi jelzést megbízhatóbbnak
  tekintem ezen a két soron, amíg nincs teljes újraellenőrzés.
- **3 eset, ahol a gép "átenged" egy valódi kritikus hibát** (`G1944`-A [MiniMax],
  `G5013`-B [MiniMax]: teljesen angolul hagyott szócikk; `G1106`-A [Gemini]:
  `Phi`→`Filem` hivatkozási csere): **egyik gépi ellenőrzés sem érzékeny** arra, ha a
  modell a forrást **változatlan hosszal és görög/héber tartalommal, de le nem
  fordítva** adja vissza, vagy ha egy hivatkozás könyvneve téves, de a szám:szám minta
  és a rövidítés önmagában érvényes marad. **Ez egy strukturális rés mind a
  hosszarány-, mind a görög/héber-, mind a Károli-rövidítés-ellenőrzésben** — a
  jelentésbe "javítandó a #7 előtt" jelöléssel kerül, az FP2-ben nem javítom.

## 4. A `Phi`→`Filem` kapurés

Lásd fent (3. pont, utolsó alpont) és `naplok/FP2_kapu_es_darabolas_elemzes.md` 1.
pontja. **Csak a jelentésbe kerül**, "javítandó a #7 (éles Thayer-fordítás) előtt"
jelöléssel — az FP2 gépi kapuját (`fp2/kapuk.py`, ill. az alapja,
`naplok/FORDITAS_P4_ellenoriz.py`) **nem módosítom** ebben a próbában.
