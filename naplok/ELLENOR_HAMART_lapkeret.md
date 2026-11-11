ELTÉRÉS: 7 tétel

# Független ellenőrzés: HAMART-001 lapkeret (F182.67)

*Brief: `F182_HAMART_JAVITO_BRIEF.md` (a brief fejléce `allapot: lezarva`; a tétel a #182 keretében készült). Tartomány: `3565fe5f..4bed9629` (`git merge-base origin/main HEAD` = 3565fe5f; egy commit). Ág: `claude/hamart-lapkeret`. Ellenőr: claude-opus-5-5, 2026-11-11. A jelentést a fő szál (claude-opus-5-5) írta ki az ellenőr válaszából, mert az ellenőrnek nincs fájlíró eszköze. Az ellenőrzés közben az ág további commitokat kapott (F182.68–70: az idézés adatai, a HELYORZO-kapu, a DOI-beállítás); ezeket a tartomány nem fedi.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | A session claude-opus-5-5, a kért modell opus; a commit Co-Authored-By sora egyezik. Hogy valóban ez a modell futott-e, nem igazolható. |
| Hatókör: csak az `uj_szerkezet` | OK | `eszkozok/lexikon_general.py:5342, 5544, 5658, 5687, 8995` | Minden új kódág `uj_szerkezet` / `uj` alatt fut; `UJ_LAPSZERKEZET = {'HAMART-001'}`; a `lexikon/` alatt csak a HAMART-001 lapja változott. |
| A lap eleje az adatból | OK | `lexikon/HAMART-001_TUDOMANYOS.md:5-11`; `adat/motivumok.tsv:10` | A cím, a negatív kritérium és a fölérendelt fogalom szó szerint egyezik; a mutató a `#kolofon` horgonyra visz. |
| „Régi forma” = Kolofon-tábla, próza nem volt | **ELTÉRÉS (2)** | `dontesek/uj/hamart-lapkeret.md:1`; `naplok/HAMART_lapkeret_jelentes.md:9` | Hogy prózai változat nem volt: igaz. Hogy a három mező „a Kolofon táblájában állt”: hamis. A régi törzscikkben (`archivum/HAMART-001/HAMART-001_torzscikk_regi.md:6-19`) az azonosító tábla a lap **elején** áll, a Kivonat előtt (… Negatív kritérium, Fölérendelt fogalom); az első lexikonlapot a „## 0. Metaadatok” tábla nyitotta (`git log -1 -L1,22:lexikon/HAMART-001_TUDOMANYOS.md 197bdfc0`); a `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md:14-18` ugyanígy. |
| Licenc: `NYILT_MAG_ADAT` ↔ a `nyilt_mag_export.py` beolvasása | OK | `eszkozok/nyilt_mag_export.py:1077-1083` | A hat beolvasott adattábla pontosan a `NYILT_MAG_ADAT`; a HAMART-sorok a magban: előfordulás 47 = 47, kizárások 288 + beépítések 47 = jelöltek 335, kapcsolatok 56 = 56. |
| Licenc: a nyílt mag CC BY 4.0 | OK | `nyilt_mag/README.md:7, 64, 76` | „**Licence:** CC BY 4.0 (the open core's own data and text)”. |
| Licenc: a nyílt mag terjedelme az előfordulás-tábla sorában | **ELTÉRÉS (1)** | lap `:3550, 3642` | A lap szerint az előfordulás-tábla egészében CC BY 4.0, a mag azonban csak az adatoszlopokat adja ki: a funkció magyarázata kimarad (`nyilt_mag_export.py:740-752`), a `kapcsolodas` nincs a kimenetben (1123-1127); `README.md:80`: „Not included: … passage-by-passage exposition”. A lap 2. szakasza éppen ezeket használja. |
| Licenc: DT623 és `Karoli_Strong_parok` | OK | `DONTESEK.md:658`; `adat/licencek.tsv:53` | CC BY 4.0. |
| Licenc: a fordítástábla sora | **ELTÉRÉS (1)** | `eszkozok/lexikon_general.py:5612-5613`; lap `:3551, 3638` | A kód minden más licencet eldob, „a forrásszöveg közkincs” pedig nem igaz a lapon megjelenő UBS DNTG-glosszákra (CC BY-SA 4.0; a `forditasok.tsv` UBS_DNTG sorai, a lapon a „UBS-domének (Louw–Nida)” sorai). |
| Licenc: a „minden jog fenntartva” sorok nincsenek a magban | OK | lap `:3630-3660` | A maradó sorok egyike sem forrása a nyílt mag exportjának. |
| Módszertani elvek ↔ `HAYS_LEKEPEZES.md` | OK | `kozlemeny/HAYS_LEKEPEZES.md:15-21`; lap `:3592` | Mind a hét pont egyezik. Megjegyzés: a közlemény linkje megszűnt, a cím csak idézőjelben áll; az MI- és a közel-keleti közlemény linkje megmaradt. |
| Belső sorok kimaradnak | OK | lap `:3596-3611` | A „Kézi forrás” és a „Kereszthivatkozás-napló” törölve; a 9 azonosító mező a Kolofonban. |
| A helyőrzők változatlanok (3. kérés) | OK (HEAD) | lap `:3599`, `:3519-3525` | A tartományban a helyőrzők maradtak; a munkakönyvtárban commitolatlan módosítás töltötte ki őket (tartományon kívül; azóta F182.68). |
| Tesztek: elkapják-e a hibát | **ELTÉRÉS (6)** | `eszkozok/teszt_kesz_lap_hamart.py:146-147, 45` | Generátorszintű, rontott bemenetű teszt az `olvasoi_licencek`-re és az `egyszerusitett_kolofon`-ra nincs; a fordítástábla-ellenőrzés csak negatív; a jelöltek és a Károli–Strong sorát nem nézi; az A02-teszt a `motivumok.tsv`-vel való egyezést nem. |
| Sablon 6 ↔ kód | OK | `sablonok/6_PaRDeS_lexikon_oldal_sablon.md:557` | Egyezik; a forrás- és a magyarázórész kettéválasztását (1.) a sablon sem mondja. |
| K21 | OK | `sablonok/KESZ_LAP_KOVETELMENY.md:55` | |
| A02 | **ELTÉRÉS (4)** | `sablonok/KESZ_LAP_KOVETELMENY.md:214` | A státusz frissült, a leírás maradt („Az azonosító tábla a lap elején…”). |
| DT-F182s, helyőrző | OK | `dontesek/uj/hamart-lapkeret.md:1` | Helyőrzős, végleges szám nincs az ágon. A felhasználó idézett szavai NEM ELLENŐRIZHETŐK. |
| Halott kód, elavult megjegyzések | **ELTÉRÉS (5)** | `eszkozok/lexikon_general.py:6613-6618, 6594-6597, 5659-5660` | Az `azonosito_tabla()`-t semmi nem hívja; a megjegyzések szerint még a tábla „nyitja a lapot”. |
| Kettős zárójel | **ELTÉRÉS (7)** | lap `:3550, 3553, 3554, 3558` | „(CC BY 4.0 (a nyílt adatmagban))”: a `'- %s (%s)'` formátum és a `NYILT_MAG_LICENC` zárójele egymásba ágyazódik. |
| A1 | OK | — | A „régi forma” állítás lekérdezés-hiányos (2.). |
| A2–A5 | OK (nem érintett) | — | |
| A6 (E12–E15) | NEM ELLENŐRIZHETŐ (részben) | — | E12 497, E13 49 JELENTES, E14/E15 0. |
| CI-jelentés ↔ saját futás | NEM ELLENŐRIZHETŐ | — | A saját futás E28 HIBA 1-et adott a munkakönyvtár commitolatlan módosításából (nem a HEAD-ből); az újrafuttatás egy másik worktree zárja miatt nem fejeződött be. |
| `ellenoriz.py`, tesztfutás | NEM ELLENŐRIZHETŐ | — | A szerep nem engedi. |
| Lista 1–5 | OK | — | 35 törölt sor bontva (az azonosító tábla átkerült, 2 belső sor törölve, 12 licencsor átírva, 1 mondat cserélve); `.tsv` nem változott; a brief nem tartalmaz ⛔ pontot. |

**Az ELTÉRÉS-ek súlyossági sorrendben:**

1. **(tartalmi)** A fordítástábla licencsora hamis („a forrásszöveg közkincs” nem igaz az UBS-glosszákra, CC BY-SA 4.0); az előfordulás-tábla CC BY sora az igehelyenkénti magyarázatra is kiterjed, holott az a nyílt magból kimarad.
2. **(tartalmi, döntést kíván)** A DT-F182s és a jelentés történeti premisszája hamis: a „régi” formában a tábla a lap **elején** állt, kulcs–érték alakban; a prózai alak a végrehajtó értelmezése. A forma kérdése a felhasználóé.
3. **(mechanikus)** A tesztek nem fogják el az 1. tételt (6.).
4. **(mechanikus)** Az A02 leírása elavult (4.); halott kód és elavult megjegyzések (5.); kettős zárójel (7.).
