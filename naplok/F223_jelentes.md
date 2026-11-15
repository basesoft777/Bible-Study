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

## 3. (a) „Csak szövegek” mód — a nyílt magra kész (a #737 mergelése után, 2026-11-15)

- **A mérés korrekciója.** A feladatleírás szerint az exportáló „a teljes adatot (Károli–Strong kb. 600 000 sor) újragenerálja”. Mért futási idő: nyílt mag 15 mp, Károli – Strong 20 mp, modernizált Károli – Strong 21 mp; a három csomag a commitolt állapotával bájtra azonos. A nyereség ezért a nyílt magnál volt értelmes (15 → 0,6 mp), és ott az igazi hozadék az E35 fájlonkénti összevetése és a szöveg-/adatréteg tiszta szétválasztása.
- **Nyílt mag (`eszkozok/nyilt_mag_export.py`).** A szöveg-rész külön függvényekbe került (`szovegek_epit`, `szovegek_lezaras`, `osszeg_epit`); a teljes export ezeket hívja, a `--csak-szovegek` mód (`export_csak_szovegek`) ugyanezeket, de az adatfájlokat a commitolt csomagból olvassa és nem írja. Újraépül: ISMERT_HIBAK, KNOWN_ISSUES, kodkonyv.tsv, KODKONYV, OLVASSEL, README, MODSZER, METHODS, ATTRIBUCIO, LICENSE, CITATION.cff, .gitattributes, a közlemény-tervezet és az ellenőrzőösszeg-fájlok (ELLENORZO_OSSZEG, KIADAS, RELEASE): 17 fájl. A számok (sor-darabszámok, lezárt motívumok, kizárt források) a commitolt táblákból jönnek; a nyitott jelöltek száma az `adat/jeloltek.tsv`-ből. **A teljes exporttal egyezés mérve:** a refaktorált teljes export a commitolt csomaggal bájtra azonos (a refaktor nem változtatott semmit), és a `--csak-szovegek` ugyanazt a 17 fájlt adja, mint a teljes export (`teszt_nyilt_mag.py` `CsakSzovegek`, 3 teszt: azonosság, az adat-sorok az összegben változatlanok, hiányzó csomagnál megáll).
- **E35 fájlonként.** Az `eszkozok/nyilt_mag_szovegek.py` (a szövegsablon) eddig nem váltotta ki az E35-öt. Mostantól kiváltja, és ha csak ez változott (adat-tábla, exportgenerátor, lexikonlap nem), az összevetés fájlonkénti: csak a 17 szöveg-/összeg-fájlt hasonlítja (0,4 mp a 9 mp helyett), az adatfájlt nem; a hibaüzenet a `--csak-szovegek` parancsot javasolja. Adat-tábla vagy az exportgenerátor módosításánál a teljes összevetés marad (`test_szabalyok.py` `E35Teszt`, 4 új teszt).
- **A két Károli-csomag: nem készült el (N-F223b).** A szövegeik számai a forrásokból és a mérésből jönnek, a visszaépítés külön és kockázatos munka ~20 mp-es export mellett.

## 4. N-F175e — a „bizonyosság” szövegeinek igazítása (DT-F175e: a bizonyosság a mért pontosság)

- A modell-egyezésen alapuló belső szűrő neve és leírása („csak magas bizonyosságú pár igazolhat sort”) kikerült a nyílt mag nyilvános szövegéből (hu és en): `ISMERT_HIBAK.md`, `KNOWN_ISSUES.md` (`nyilt_mag_export.py`), `MODSZER.md`, `METHODS.md` (`nyilt_mag_szovegek.py`), a `szó-szintű-gépi` kódkönyv-sora (`adat/nyilt_kodkonyv.tsv`, `ts` 2026-11-15; `KODKONYV.md`, `kodkonyv.tsv`). A csomag újragenerálása a `--csak-szovegek` móddal történt (9 fájl változott: 6 szöveg + 3 összeg-fájl; az adatfájlokhoz nem nyúlt; a teljes exporttal kontrollálva azonos). A mag KIADAS-hash-e változott.
- **Kapu.** `nyilt_mag_kapu.py` `NYILVANOS_TILTOTT`: a „magas/alacsony bizonyosság”, „high/low confidence” alak tiltott a próza-fájlokban (teszt: négy tiltott és egy megengedett eset a `teszt_nyilt_mag.py`-ban: a „bizonyosság a mért pontosság” megengedett). A két Károli-kapu (`karoli_strong_kapu.py` `MODELL_EGYEZES`, ezt a modern is használja) a teljes „bizonyoss” tilalom helyett ugyanerre az alakra szűkült (a `532d8c34` visszavétele; a mért pontosságra a szó használható).
- **Nem érintett, a felhasználó dönt (N-F223a):** a `bizonyossag` oszlop a kapcsolat-táblákban és a `megbizhatosag` oszlop szövege.

## 5. Mérés és nyitott kérdések

- `teszt_nyilt_mag.py`: 97 teszt, 1 bukik (`test_teljes_mag_0_bukas`); a bukás **ennek a PR-nak előzménye**: a `nyilt_mag_kapu.py` a main-en (`1b4493e0`) is 150 BUKÁS-t ad (elavult fordítás), l. N-F223c. A két Károli-csomag tesztje zöld (24, 15).
- A két Károli-kapu `VALTOZATLAN` pontja a `nyilt_mag/` szándékos változtatása miatt pirosat mutat (N-F223d); a CI nem futtatja.
- Új N-tételek: `nyitott/uj/trusting-carson-7572be.md` (N-F223a–d).

## 6. Nyitott megjegyzés

- A `push_elott.py` lépéslistája nem futtatja a `proza_allitas.py --kapu`-t (E41), pedig a `STATIKUS_HIVASOK` és a workflow tartalmazza; a `--ci-egyezes` ezt nem jelzi (csak a szkript-útvonal egyezését nézi). Ez régebbi hézag; ezt a menet nem érintette, külön tétel.
