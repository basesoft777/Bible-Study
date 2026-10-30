# Gépi héber kiejtés — a bekötés (DT-F131y, N-F131w; 2026-10-30)

- **Modell:** `claude-opus-5-5`
- **Döntés:** DT-F131y. A szabályok (R1–R8, R5b, a lexikai R7) a felhasználó kalibrációjából jöttek. A bekötést a felhasználó jóváhagyta, szó szerint: „Mehet”.
- **Proveniencia (mért számok):** `scope=lexikon/ISTENTISZT-001_TUDOMANYOS.md, lexikon/ALVIL-001_TUDOMANYOS.md (HEAD ↔ munkafa) | forras=naplok/HEBER_KIEJTES_bekotes_meres.py | ts=2026-10-30`

## 1. Mi változott

| réteg | fájl | változás |
|---|---|---|
| adat | `adat/kiejtes_kivetelek.tsv` | **2 módosított, 3 új sor** (l. 3. szakasz), proveniencia-sorral; a fejkomment az új szabályt írja le |
| adat-séma | `adat/SEMA.md` 2.17 | héberül a tábla a jóváhagyott forrás, elsőbbséggel; ennek híján gépi, „(…, gépi)” jelöléssel; a régi S3-szabály („a render nem generál”) megszűnt |
| eszköz | `eszkozok/heber_kiejtes.py` (új) | a gépi átíró (R1–R8, R5b, lexikai R7, tetragramma előtaggal), `kiejt()`, `teljes_szo()` |
| eszköz | `eszkozok/lexikon_general.py` | a ragozott héber alak a **teljes szó** (előtag + tő + toldalék a TAHOT vers-soraiból) a saját gépi kiejtésével; a lemma jóváhagyott kiejtése, ennek híján gépi; a SECE-sor kiírt alakja a saját kiejtését kapja, ha nem a lemma; a Jelmagyarázatba egy bekezdés a „gépi” jelölésről |
| eszköz | `eszkozok/kiejtes_szoveg.py` | a szövegszintű pótlás héberül is gépi kiejtést ad (jelölve), az önálló előtag (בְּ) is |
| teszt | `eszkozok/teszt_heber_kiejtes.py` (új) + `teszt_heber_kiejtes_esetek.tsv` (generált: `naplok/HEBER_KIEJTES_tesztesetek.py`) | a két kalibráló minta 100 esete (91 elfogadott, 9 ismert eltérés okkal) és szabályonkénti tesztek |
| teszt | `teszt_kiejtes_szoveg.py`, `teszt_szotari_gerinc.py`, `teszt_szerepmatrix.py` | a régi elvárás („nincs gépi héber kiejtés”, „szótári alak:”, 26 héber sor) a DT-F131y szerint frissítve |
| lap | `lexikon/ISTENTISZT-001_TUDOMANYOS.md`, `lexikon/ALVIL-001_TUDOMANYOS.md` | újragenerálva (`PARDES_DATUM=2026-10-29`, a lapok első GENERÁLT ts-e) |
| napló | `DONTESEK.md` DT-F131y, `NYITOTT_FELADATOK.md` N-F131w | a kiegészítés és a jóváhagyás idézettel; az N-F131w állapota |

## 2. Mérés a két lapon (előtte: a commitolt lap; utána: az újragenerált)

| lap | „gépi” jelölés | különböző héber szó gépi kiejtéssel | „szótári alak:” jelölés | jóváhagyott alak nélküli héber szó a generált részen |
|---|---|---|---|---|
| ISTENTISZT-001 | 0 → **106** | **54** | 69 → 0 | 37 → **3** |
| ALVIL-001 | 0 → **133** | **18** | 128 → 0 | 7 → **3** |

A generált részen maradt 3 alak mindkét lapon a Jelmagyarázat BDB-rövidítése (י׳, ק׳, שׁ׳). Ezek rövidítések, nem szavak. A kiejtés-szabály teljes hiánya (a kézi részekkel):
- ISTENTISZT-001: 41 → 7;
- ALVIL-001: 13 → 9.

A kézi részek hiányai (ISTENTISZT-001: פְּשָׁט, רֶמֶז, דְּרַשׁ, סוֹד; ALVIL-001: שְׁאוֹל, תְּהוֹם és görög szavak) a forrásban javítandók; a generátor a kézi részt nem írja.

**Előtte / utána.**

| hely | előtte | utána |
|---|---|---|
| 1Móz 4:26, Kulcsszó-cella | `segítségül hívni az Úrnak nevét — קְרֹ֖א (szótári alak: kárá); שֵׁ֥ם (szótári alak: sém)` | `segítségül hívni az Úrnak nevét — לִקְרֹ֖א (likró, gépi); בְּשֵׁ֥ם (besém, gépi)` |
| 1Móz 4:26, LXX-tábla | `קְרֹ֖א (szótári alak: kárá)` | `לִקְרֹ֖א (likró, gépi)` |
| SECE-sor (G1941 héber megfelelői) | `\| זָכַר \| — \| H2142 \| emlékezni \|` | `\| זָכַר \| záchar, gépi \| H2142 \| emlékezni \|` |
| SECE-sor, a kiírt alak nem a lemma | (a lemma kiejtése nélkül: —) | `\| זַעַק \| zaak, gépi \| H2201 \| kiáltás \|` |
| SECE-sor, jóváhagyott lemma más pontírással (ALVIL-001) | `\| **שְׁאֹול** … \| seól \|` | változatlan: `seól` (a jóváhagyott marad) |

A ragozott alak most a teljes szó: a „קְרֹ֖א” helyett „לִקְרֹ֖א”, a „שֵׁ֥ם” helyett „בְּשֵׁ֥ם”. Ezt a DT-F131y (5) kéri: a kiejtés a teljes szóra készül.

## 3. A változott adatsorok (`adat/kiejtes_kivetelek.tsv`)

| Strong | alak (TBESH-lemma) | előtte | utána | ok |
|---|---|---|---|---|
| H3678 | כִּסֵּא | kissé | **kisszé** | R1: ס = sz |
| H2555 | חָמָס | hámás | **chámász** | R1 + R8 (a D36 „h” kivétele megszűnik) |
| H3605 | כֹּל | — | **kol** (új) | R2 kivétellista |
| H2451 | חׇכְמָה | — | **chochmá** (új) | R2 kivétellista |
| H3389 | יְרוּשָׁלִַ֫ם, יְרוּשְׁלֵם | — | **jerúsálajim** (új) | R7 |

A módosítást a `naplok/HEBER_KIEJTES_kivetel_frissit.py` végezte: a kulcsot a TBESH-ből veszi, írás előtt összeveti a sorokat az eredetivel, és másodszori futtatásra nem változtat.

## 4. Tudnivalók és nyitott pontok

- **Az R5b következménye.** A tő kezdőbetűje előtag után is kemény, akkor is, ha a pontozás lágyat jelöl. Például a לְבֵית „lebét” lesz, nem „levét”. Ez a döntés szerinti viselkedés; a minta erre egy esetet tartalmazott (וּבֹקֵעַ).
- **Ahol nincs előtag-információ** (szövegszintű pótlás, lemma), ott a szókezdő begadkefat a tő kezdőbetűjeként kemény. A ב-előtag lágy ejtése csak a TAHOT-ból összerakott szóban érvényesül.
- **A törzscikk lefedettségi mátrixa** (`torzscikk_general.py`, héber 10. szerep) továbbra is csak a jóváhagyott kiejtést számítja „adatosítottnak”. A két lexikonlapon ez nem jelenik meg; a törzscikkek újragenerálásakor érdemes eldönteni.
- **A többi hat lexikonlap** (ANTROP, HAMART, HODIT, KIRALY, MENNY, TEREMT) nem lett újragenerálva. Az E28 csak a két migrált lapot nézi; azok a motívumonkénti migrációval (#36) kapják meg az új kiejtést.
- **Az 1. minta 9 tudatos eltérése** (R4 elutasítva, R8, R3 és öt nyitott eset) a tesztben okkal rögzítve (`ismert_elteres`), így egy jövőbeli szabályváltozás látszik.
