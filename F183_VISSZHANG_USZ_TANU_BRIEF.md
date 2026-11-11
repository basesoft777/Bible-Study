---
feladat: 183
cim: Visszhang 2. fázis — újszövetségi ág és tanúréteg a HAMART-001-en
kod: VISSZHANG_USZ_TANU
tipus: feladat
fazis: folyamat
modell: opus
allapot: fut
ag: claude/visszhang-usz-tanu
ad: a HAMART-001 visszhang-rétegének ÚSZ-ága (Vulgata, szövegváltozat, LXX-előkép) és tanúrétege (egyházatyai index, rabbinikus, Glossa Ordinaria) kinyerő táblából, két kézzel; akadémiai forrás a vitatott pontoknál; N-F176b/c; makett jóváhagyása után a generátor és a HAMART-lap újragenerálása
kovetkezo: "F183 fut: hatástörténeti főszakasz, ÚSZ-ág, tanúréteg (ebben a sessionben, subagent nélkül)"
munka: folyamat
olvas: [F176_VISSZHANG_ADAT_BRIEF.md, "tematikus_lezart/HAMART-001*", "tematikus_lezart/naplok/HAMART-001*", F178_LEXIKON_AG_LEZARAS_BRIEF.md, konkordancia/VISSZHANG_README.md, konkordancia/Vulgata_Clementina.tsv, konkordancia/SBLGNT_apparatus.tsv, konkordancia/TAGNT_valtozatok.tsv, adat/visszhang_megfelelok.tsv, adat/SEMA.md, motivumok/HAMART-001.md, lexikon/HAMART-001_TUDOMANYOS.md, naplok/HATAR_HAMART-001.md]
ir: [eszkozok/lexikon_general.py, eszkozok/visszhang/, adat/visszhang_megfelelok.tsv, adat/visszhang_tanuk.tsv, adat/SEMA.md, adat/datasetek.tsv, konkordancia/VISSZHANG_README.md, lexikon/HAMART-001_TUDOMANYOS.md, naplok/F183_jelentes.md, .github/workflows/ellenorzes.yml]
fugg: [176, 182]
nem_fugg: [123, 151, 178, 179]
---

# Brief-tervezet — Visszhang 2. fázis: újszövetségi ág és tanúréteg

*Orkesztrátori tervezet, 2026-11-08. Befogadásra (`/befogad`, külön sessionben). A felhasználó: „A visszhang 2 ne kerüljön ennyire hátra” (2026-11-08) → közvetlenül a #178 merge-e után indul, a közlési ággal (#174/#175) párhuzamosan (nincs közös `ir`).*

**Javasolt fejléc:** `tipus: feladat`, `fazis: folyamat`, `modell: opus` (az értelmező ítélet; a webes/licenc-lépés Sonnet-subagentben), `fugg: [178]`, `munka: folyamat` [javaslat].
`olvas`: `F176_VISSZHANG_ADAT_BRIEF.md`, `F178_LEXIKON_AG_LEZARAS_BRIEF.md`, `konkordancia/VISSZHANG_README.md`, `konkordancia/Vulgata_Clementina.tsv`, `konkordancia/SBLGNT_apparatus.tsv`, `konkordancia/TAGNT_valtozatok.tsv`, `adat/visszhang_megfelelok.tsv`, `adat/SEMA.md`, `lexikon/HAMART-001_TUDOMANYOS.md`, `naplok/HATAR_HAMART-001.md`.
`ir`: `eszkozok/lexikon_general.py`, `eszkozok/visszhang/` [javaslat], `adat/visszhang_megfelelok.tsv`, `adat/visszhang_tanuk.tsv` (új) [javaslat], `adat/SEMA.md`, `adat/datasetek.tsv`, `konkordancia/VISSZHANG_README.md`, `lexikon/HAMART-001_TUDOMANYOS.md`, `naplok/F<nn>_jelentes.md`, `.github/workflows/ellenorzes.yml` (N-F176c).

**Orkesztrátori kiegészítés (2026-11-09):** (1) a #178 a main-ben van (PR #655), a brief fejléce nem `lezarva` → nem függés, hanem `olvas` + egyeztetett eltérés; (2) **sorrend:** a HAMART javító menete (külön brief, `HAMART_JAVITO`) után fut — `fugg` arra a feladatra; (3) a rokon nyelvi tábla a 4.8 „Nyelvi háttér” pontban áll (a javító menet F13 döntése) — ez a brief a 4.11-hez és a 4.8-hoz nem nyúl, csak az ÚSZ-ágot és a tanúréteget adja hozzá; (4) menetrend (a felhasználó jóváhagyásával, 2026-11-08): a forma (makett) a menet előtt, futás közben nincs bővítés, a gépi részek párhuzamosan, lépésenkénti időmérés, a teljes tesztkör a menet végén; (5) a lap előfeltétel-térképe: a megosztott mappa `HAMART_ELOFELTETEL_TERKEP_2026-11-09.md`.

**A HAMART-001 az új, teljes arany (a felhasználó, 2026-11-08: „Hamart legyen teljes, új arany.”):** a HAMART-001 1. kiadása (`/kiadas`) a 2. fázis után történik, a teljes visszhang-réteggel (ÓSZ-ág, ÚSZ-ág, tanúréteg, akadémiai forrás); a többi lap ehhez mér.

**Átvihetőség (a felhasználó, 2026-11-08: „Legyen biztosítva, hogy ezt át tudjuk vinni, ne legyen visszaesés.” · „A többi lapra. Aztán az új lapok így készüljenek.”):** minden új szabály három helyen él — sablon (6/9, U3-prompt, MUNKAMENET-lépés), HIBA-szintű kapu minden lapra (teszttel: HAMART 0 HIBA, rontott másolat jelez), döntés (helyőrzővel). A HAMART után a többi lap nem tömeges újragenerálással, hanem motívumonként a teljes folyamaton megy át (a felhasználó: „Ne a régi hibákkal írjuk újra a többi lapot. Minden menjen át a teljes folyamaton”), ugyanazzal a generátorral és kapukkal, kivétellista nélkül; ez a brief csak a HAMART-001-et írja; az új cikkek a MUNKAMENET C-lépéseiből magától ezt a formát kapják.

## Előzmény
- A #176 behozta az adatréteget (Targum PD, Vulgata Clementina, SBLGNT-apparátus, TAGNT-változatok, BDB rokon írások), a #178 a lapra tette az ÓSZ-ágat (4.11: lánc-szavanként n/N, alapvonal-szabály, BDB-háttér; DT-F178a és kiegészítése).
- Kimaradt (2. fázis): az **ÚSZ-ág** és a **tanúréteg**; nyitva N-F176a (Vulgata-kiadás, Glossa Ordinaria), N-F176b (BDB-hézag H6093, H1863), N-F176c (teszt_visszhang a CI-ben).
- Licenc (2026-11-08, `forraskutatas_osszegzes` + jogi kör): mérce „kimenetbe tehető”; NC kizárt; Sefaria links CC BY (`manual` proveniencia); sermonindex/early-church-fathers: igazítás CC BY 4.0, csak index (a quote mező nem); NuBerea: hozzáférés kérve, a szerzők jóváhagyására vár; Peshitta: nincs szabad forrás; IxTheo/WiBiLex/Biblindex: eszközből nem elérhető.

## Tételek
**V0 — Modell-ellenőrzés, előfeltétel:** a #178 a main-ben.

**V1 — ÚSZ-ág (a HAMART ÚSZ-helyein: Róm 8:21, Gal 3:13-14, Zsid 6:8, Jel 11:18, 19:2 — a lap aktuális listája szerint).** Lánc-szavanként, az ÓSZ-ág formájában: Vulgata (Clementina ÚSZ) n/N; szövegváltozat (SBLGNT-apparátus, TAGNT) csak ha a lánc szavát érinti; az ÓSZ-előkép a meglévő LXX-hídból (a görög láncszó a LXX-ben). Peshitta: „nem azonosítható: szabad forrás nincs” — nem hiány-kitöltés.

**V2 — Tanúréteg (csak Remez/Sod helyeken, hagyományonként legfeljebb 1, csak ha ugyanazt a kapcsolatot látja):**
- egyházatyai index (sermonindex/early-church-fathers: hely + szerző + mű, idézet nélkül; a szöveget szabad kiadásból — CCEL/PD — a modell olvassa és egy mondatban összefoglalja, linkkel);
- rabbinikus (Sefaria links, csak az ÓSZ-helyen át; PD/CC0/CC BY szöveg);
- Glossa Ordinaria (N-F176a; Migne 1880, közkincs) értékelése forrásként.
Kinyerő tábla (`adat/visszhang_tanuk.tsv`, séma a SEMA-ba): ki mondja, melyik hely, milyen kapcsolatot lát (egy mondat), forrás-URL + lekérdezési dátum, `kinyeres`/`modell`/`ellenorzes`/`proveniencia`; két kéz (aki kinyer, nem ellenőriz); ellenőrizetlen sor nem renderel; arány-kapu (1% FIGY / 5% HIBA) érvényes.

**V3 — Akadémiai hang csak a vitatott pontoknál (7. szakasz):** OpenAlex/Crossref/DOAB lekérdezéssel, lektorált forrás, lehetőleg több hagyományból; emlékezetből semmi.

**V4 — Hézagok:** N-F176b (a H6093, H1863 BDB-szócikke más úton: Sefaria `rid` vagy szkenből célzott átírás; addig „nem azonosítható”); N-F176c (teszt_visszhang a CI-be).

**V5 — Makett előbb (tanulság: a #176 gépi makettje „nem jó semmire”):** a V1–V2 leletéből HAMART-makett (artifact), ⛔ a felhasználó jóváhagyása a formára; utána generátor (`lexikon_general.py`), HAMART-lap újragenerálása, saját átnézés; ⛔ a többi lap csak a HAMART jóváhagyása után, egy körben.

**V6 — Jelentés, független ellenőr, draft PR.**

## Nem része
- Új adatkészlet licenc-ellenőrzés nélkül (playbook 2. pont, `adat/datasetek.tsv`); NC forrás; a bible-mcp kimenete (DT32); Strack–Billerbeck; igehirdető/gyülekezeti tanító.
- NuBerea-adatkészlet, amíg a hozzáférés nincs meg (és letöltés előtt külön kérdés, 549 MB).
