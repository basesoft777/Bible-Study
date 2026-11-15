# F223 — Részleges kapu és „csak szövegek” export

*Modell: claude-sonnet-5-5 · 2026-11-15 · alap: `origin/main` (7ddc0cef, majd a main-behozás után 21390501) · ág: `claude/trusting-carson-7572be`*

## 1. Menet

**(b) Részleges kapu — kész.** `python eszkozok/push_elott.py --reszleges` (az alapértelmezett mód változatlanul a teljes kapu; a CI mindig teljes futás, a workflow-hoz és a `--ci-egyezes` szabályhoz nem nyúltam).

- **Leképezés egy helyen:** `RESZLEGES_LEKEPEZES` (`eszkozok/push_elott.py`). Hat kihagyható lépés (`E1`, `E38-E39`, `teszt-szabaly`, `teszt-kapuk`, `teszt-kinyer`, `E18`); minden változott útvonal mintára illesztve adja az érintett lépéseket. Az E2–E39 (`futtat.py`) és a CI-egyezés mindig fut: az előbbi maga is diff-hatókörű (az E35 csak adat-táblára, az exportgenerátorra és a lexikonlapra, az E28 csak az érintett lapra indul; brieffejlécre, naplóra, `.md`-re nem: `teszt_push_elott.py` 10b.).
- **Biztonsági szabály:** egy változott fájl, amely egyik mintára sem illeszkedik, vagy törölt/átnevezett/típust váltott fájl, vagy nem olvasható zöld jegyzés/diff esetén minden lépés fut. A `naplok/` alatt csak a `.md` ismert (a `.py/.tsv/.txt` fájlt kód tölti be), a `.claude/` alatt csak a `commands/` és az `agents/` `.md` fájljai.
- **Main-behozás:** a lépésenkénti zöld jegyzés (`<git-dir>/push_elott_zold.json`: lépés → a fej, amelyen utoljára rendben futott) miatt a „behozott változás” is bekerül: egy lépés fut, ha az utolsó zöld fej és a mostani közti `git diff --name-status` érint rá illeszkedő fájlt. Jegyzés nélkül (az ág első futása) minden lépés fut. A jegyzés csak tiszta fán, teljes (`--lepes` nélküli) futás után frissül; bukott lépésé törlődik.
- **Szabály:** a `.claude/commands/kovetkezo.md` „PUSH ELŐTT” szakasza egy mondattal kiegészült (a `/kiadas` és a `/lap-javit` ide hivatkozik, azokhoz nem nyúltam).
- **Teszt:** `eszkozok/teszt_push_elott.py` 10. szakasz (a fájl összesen 51 esete zöld): a brieffejléc-változásnál csak az E18 fut (az adat-, csomag-, tesztlépések kimaradnak); ismeretlen fájlnál (`valami.xyz`, `naplok/szkript.py`, `.claude/settings.json`, …) és D/R/T/C státusznál a teljes kapu fut; a zöld jegyzés kör-oda-vissza, hibás/más verziójú jegyzés érvénytelen; az E35 brieffejlécre/naplóra nem indul; `--ci-egyezes` változatlanul zöld.

## 2. Mért futási idő (a gép közben mások gateit is futtatta; az E2–E39 lépés 19–256 mp között ingadozik a terhelés miatt)

| Változás | Teljes kapu | `--reszleges` |
|---|---|---|
| (alapmérés) 1 új brief-fájl, 1 fájl | **615 mp** (10 perc 15 mp falióra; ebből `test_szabalyok.py` 192, E1 63, E39 51, E18+tesztje 133, `brief_lezaras` 54) | — |
| **ugyanaz a változás:** napló-.md + brief-fejléc, 5 fájl, az előző zöld futás után | **680 mp** | **161 mp** (E2–E39 45 + E18 49 + `feladatok.py` tesztek 59; E1, E38/E39, minden teszt kihagyva) — **4,2× gyorsabb** |
| main-behozás (a main hozott `eszkozok/` kódot is) | — | 561 mp: minden lépés futott, mert kódfájl változott (az indok lépésenként kiírva); a leképezés itt helyesen nem spórol |
| az ág első futása | — | teljes (nincs jegyzés) |

Az utolsó jelentett sor mutatja a korlátot: ahol a main-behozás kódot hoz, a részleges mód nem gyorsít, és így is kell. A nyereség a brief-, napló-, döntés- és `.md`-változásoknál, illetve a csak adatot hozó main-behozásnál van (ott az E18/az adatlépések futnak, a kódtesztek nem).

## 3. (a) „Csak szövegek” mód — nem készült, vár

Az ütközés-korlát szerint az exportálókhoz csak a `local_be6e01b0` (nyílt Károli-csomagok) PR-jának mergelése után nyúlok. Az állapot (2026-11-15, `gh pr list`): a PR sem a main-en nincs, sem nyitottként nem látszik (a nyitott PR-ek: #725, #729, #736). A tervet leírtam az orkesztrátor jegyzetmappájában (`F223_a_reszletes_terv_csak_szovegek_mod.md`): a szövegek egy függvénybe emelése, `--csak-szovegek` mód (az ellenőrzőösszeg-fájl csak a szövegsorai és a `KIADAS`/`RELEASE` hash cserélődik), az E35 két osztályra bontása (szöveg/adat); fontos nyitott kérdés, hogy az `nyilt_mag_szovegek.py` jelenleg nem váltója az E35-nek, és hogy a szövegek mért számai adatból jönnek-e. Az (a) külön, utólagos menet.

## 4. Nyitott megjegyzés

- A `push_elott.py` lépéslistája nem futtatja a `proza_allitas.py --kapu`-t (E41), pedig a `STATIKUS_HIVASOK` és a workflow tartalmazza; a `--ci-egyezes` ezt nem jelzi (csak a szkript-útvonal egyezését nézi). Ez régebbi hézag; ezt a menet nem érintette, külön tétel.
