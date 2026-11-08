# 10. PaRDeS U3-prompt sablon — a motívum teljes prózája nulláról, egy kézből

**Állapot: v1 (F178.3, 2026-11-08).** A HAMART-001 mint arany (a felhasználó: „a hamart lesz az új arany / fontos hogy most már visszaesés ne legyen innen”) prózai menetének promptja. Minden új cikknél ez a prompt indítja az U3-at (`MUNKAMENET.md` C-w); 2. kiadásnál, ha a próza újraíródik, szintén. A forma szabályai a `sablonok/9_PaRDeS_motivum_forras_sablon.md` 4. pontjában állnak („Az 1/a igehelyenkénti prózája”, „Az új cikk öt szabálya”, „A HAMART-001 mint arany: a lezárás hét szabálya”); ez a fájl a session bemenete, nem szabályforrás — ellentmondásnál a 9-es sablon az irányadó.

*Használat: a `[…]` helyőrzőket a session indítója tölti ki; a prompt többi része szó szerint megy. A session modellje `opus` (értelmező próza, egy kéz: CLAUDE.md, KONTEXTUS K1).*

---

## A prompt

Te a `[ID]` motívum (`[cím]`) teljes prózáját írod meg **nulláról, egy kézből**: a `motivumok/[ID].md` minden kézi szakaszát, egyetlen sessionben. Régi tanulmányból, régi lapból, archívumból mondatot nem viszel át; ha a régi szövegben jó lelet áll, az adatból igazolod, és a saját mondatodban mondod ki.

**Előfeltétel — ellenőrizd, mielőtt egy mondatot írnál:**

1. A határ kész és nem a te döntésed (U2/U3 szétválasztás): a `jeloltek.tsv` motívumsorai döntöttek (`nyitva` 0), a `naplok/HATAR_[ID].md` modelles része friss (`python eszkozok/ellenoriz.py --hatar-ujjlenyomat [ID]` jele egyezik a modelles rész első sorával). Ha nem friss, vagy ebben a sessionben határdöntést hoztál, **állj meg**: a próza a határkör után jön.
2. A modell-ellenőrzés (CLAUDE.md): a saját modellneved a `kiadasok.tsv` / `res_forras.tsv` `proza_modell` mezőjébe kerül, a környezetedből véve.

**Bemenet** (célzottan olvasd, ne egészben):

- `adat/motivumok.tsv` `[ID]` sora: `negativ_kriterium`, `folerendelt_fogalom`, `azonossag_tipusa`;
- `adat/elofordulasok.tsv` `[ID]` sorai: `igehely`, `karoli_szo`, `gerinc_elem`, `funkcio`, `kapcsolodas`, `jelentes_szam`;
- `adat/jeloltek.tsv` `[ID]` elutasított sorai (az okok, nem egyenként);
- az U1 kivonata: `naplok/F123_alapanyag_[ID].md` (vagy a motívum saját U1-fájlja);
- a lap generált része (`lexikon/[ID]_TUDOMANYOS.md`) csak a számokért (Döntési út, 2. és 3. szakasz).

**Amit írsz, sorrendben:**

1. **Kivonat (4 bekezdés).**
   - 1. bekezdés: a lánc vagy a motívum menete a kulcshelyeken, **és a fordulópontja**: hol fordul meg, áll meg vagy vált irányt. A fordulópont adatból igazolt — a beépített sorok `funkcio`-ja, a szó, az igealak —, nem feltevés. Ha két hely között „feszültséget” vagy „ellentmondást” mondanál, nézd meg a két vers szavát: ha más szó vagy más alany áll, a feszültség nem az adaté. *(Tanulság: HAMART-001, 1Móz 8:21 ↔ 9:25.)*
   - 2. bekezdés: a számok a lap adatából (helyek, versek, könyvek, ÓSZ/ÚSZ) és a későbbi helyek csoportjai.
   - 3. bekezdés: a két kötelező határ-elem — a negatív kritérium szó szerint ellenőrizhetően (mely alak tartozik ide, mely nem), az ÚSZ-mérce (a Károli alapszövege, a Textus Receptus), és strukturális/fogalmi hordozónál: a lista keresési módszer eredménye.
   - 4. bekezdés: a fölérendelt fogalom („nem a … általában, hanem …”), a név szerinti tematikus kivételek.
2. **1/a — minden igehely**: a `kapcsolodas` **kerek mondat** (alany, állítmány; idézet csak a fölötte álló Károli-vers szó szerinti része, „…”-ben), alatta a „Funkció:” sor (`címke — magyarázat`, a motívumbeli szerep). Töredék súlyos hiba.
3. **Értelmezés** (PaRDeS-keret, vitatott pontok), **Alkalmazás**, **Módszertan és nyitott kérdések**: a 9-es sablon 4. pontja szerint; a nyitott kérdés tartalmi, a séma-korlát és az adatállapot `【NAPLO】`.
4. **Nave-döntések** (U3b, ha még nincs): az `adat/tematikus_temak.tsv`-be, indokkal; üres Nave-blokkal a lap nem adható ki.

**Olvasói szöveg — mindenütt:**

- a lelettel kezdesz (számok, a szavak kiejtéssel, példahely), és szabály szerinti következtetéssel zársz;
- minden héber, arámi és görög szó mellett a magyaros kiejtés (a lapon egy szónak egy kiejtése van);
- belső szó nem kerül a szövegbe: döntés-azonosító, feladatszám, fájlnév, „gerinc”, „szerep”, „orkesztrátor”, „felhasználó”; a döntés olvasói neve „szerkesztői döntés”;
- a beépítés indoka szerkezeti jegy (lánc, visszautalás, szókapcsolat), nem a szó puszta egyezése;
- hiányt nem töltesz ki asszociatív anyaggal: ha nincs adat, kimondod (CLAUDE.md 3. szabály).

**Önellenőrzés a commit előtt** (mind fusson le, a kimenet a menetnaplóba):

```
python eszkozok/general.py --cel lexikon --id [ID] --ir
python eszkozok/proza_1a.py [ID] --reszletes
python eszkozok/olvasoi_kapu.py [ID] --reszletes
python eszkozok/ellenoriz.py
```

A mérce: 25. szabály RENDBEN (minden 1/a kerek + „Funkció:”), olvasói kapu 0 BUKÁS, 37–39. szabály a motívumra tiszta, a lap regressziós kapui (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`, „A HAMART-001 regressziós kapui”) zöldek. Ha egy kapu bukik, a forrást javítod (a lapot soha), és újragenerálsz.

**Kimenet:** a `motivumok/[ID].md` (forrásréteg) és a menetnapló; tételenkénti commit, UTF-8 fájlból. A lap a generátor kimenete, kézzel nem szerkeszted.
