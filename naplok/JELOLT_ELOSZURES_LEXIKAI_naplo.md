# JELOLT_ELOSZURES_LEXIKAI_naplo.md — N-F150a M0 mérés (a lexikai kiterjesztés)

*Modell: claude-sonnet-5-5 · 2026-11-02 · ág: `claude/f150-lexikai-eloszures-b19e01` · folytatja: `naplok/JELOLT_ELOSZURES_naplo.md` (#150 M0, DT432 (d)).*

*(proveniencia: scope=adat/jeloltek.tsv (`jelolt_tipus=elofordulas`, `dontes` = beépítve vagy elutasítva; a lexikai hordozójú motívumok: n=198, 173 beépítve + 25 elutasítva) + adat/elofordulasok.tsv (gerinc-kombinációk) + adat/motivumok.tsv (`azonossag_tipusa`) + konkordancia/Strong_szotar.tsv (rokonság: „Gyök/Származtatás”) | forras=naplok/JELOLT_ELOSZURES_LEXIKAI_meres.py (jelolt_eloszures.vizsgal_lexikai; szerep_karoli.vers_strongok: TAHOT+TAGNT, Károli-kulcs) | ts=2026-11-02)*

Újrafuttatás: `python naplok/JELOLT_ELOSZURES_LEXIKAI_meres.py` (csak olvas).

## 1. A javított szabály

Három, egymástól független javítás a `vizsgal_lexikai`-ban (a formulaikus ág változatlan, a mért 0/36 hamis kizárás és 120 felismert elutasítás ugyanaz):

- **sz — szomszédos versek.** A jelölt versei és a mindkét oldali szomszédos vers (±1) összesített Strong-halmaza az ablak; a gerinc-kombináció akkor „megvan”, ha minden tagja az ablakban van. (A Luk 1:46 ψυχή és a Luk 1:47 πνεῦμα így együtt adja a G5590+G4151 párt.)
- **r — rokon alak.** A kombináció egy tagja akkor is kielégül, ha az ablakban van egy belőle **származtatott** szó. A rokonságot a `Strong_szotar.tsv` „Gyök/Származtatás” oszlopa adja (a Strong-számok kiolvasva; pl. G5591 ψυχικός ← G5590; G4152 πνευματικός ← G4151; H5303 ← H5307), memóriából nem. Egy lépés, csak a származtatott irány.
- **n — nyelv.** Csak a jelölt nyelvű (G/H) kombinációk számítanak; a jelölt nyelve a vers Strong-halmazából jön. Ha a motívumnak nincs ilyen nyelvű kombinációja, a gép nem dönt (`vizsgalando`, „a motívumnak nincs G-nyelvű gerinc-kombinációja”).

A kiterjesztés **alapból ki van kapcsolva**: a `LEXIKAI_BEKAPCSOLT` üres, ezért a kimenet (`naplok/ELOSZURES_*.tsv`) változatlan. A bevezetés motívumonként ⛔ döntés.

## 2. Eredmény: a nyolc változat a lexikai motívumokon

| változat | hamis kizárás (173 beépítve) | felismert elutasítás (25) |
|---|---|---|
| alap (#150 szabálya) | **7** | 14 |
| n | 4 | 14 |
| r | 6 | 14 |
| rn | 3 | 14 |
| sz | 5 | 11 |
| szn | 2 | 11 |
| szr | 3 | 11 |
| **szrn** | **0** | **11** |

**Csak mind a három javítás együtt adja a 0 hamis kizárást** (szrn). A felismert elutasítás 14-ről 11-re csökken (−3, mind HODIT-001: a szomszédos vers a kombinációt kielégíti).

## 3. Motívumonként (szrn)

| motívum | beépítve | elutasítva | hamis kizárás (alap → szrn) | felismert (alap → szrn) | megjegyzés |
|---|---|---|---|---|---|
| ALVIL-001 | 72 | 5 | 0 → 0 | 4 → 4 | |
| ANTROP-001 | 8 | **0** | 4 → 0 | – | nincs elutasított sor: a 0 hamis kizárás igaz, de **felismerést nem lehet mérni** |
| HODIT-001 | 33 | 4 | 0 → 0 | 3 → **0** | a szomszéd-ablak minden felismerést elvesz (alap szabály is 0 hamis) |
| KIRALY-001 | 9 | 13 | 0 → 0 | 4 → 4 | |
| MENNY-001 | 9 | 1 | 3 → 0 | 1 → 1 | a 3 NT-hely a nyelvszűrés (n) miatt nem dönt, l. 4. |
| TEREMT-001 | 42 | 2 | 0 → 0 | 2 → 2 | |

A 7 ismert eset soronként (szrn): Luk 1:46, Luk 1:47 (sz: a pár a szomszéd versben); 1Kor 2:14 (r: ψυχικός ← G5590); 1Kor 2:15 (sz+r: a 14. vers G4151-e és az 15. vers πνευματικός-a); Júd 1:6, Júd 1:14-15, 2Pét 2:4-5 (n: a MENNY-001 kombinációi mind héberek, G-helyen a gép nem dönt).

## 4. MENNY-001 — tartalmi kérdés (⛔)

A MENNY-001 `gerinc` kombinációi (`elofordulasok.tsv` `strong`): `H1121+H0430`, `H5303` — mind héber. Az NT-helyek (Júd 1:6, Júd 1:14-15, 2Pét 2:4-5) az `elofordulasok.tsv`-ben `referencia:` / `idézet:` / `formula:` típusú kapcsolattal állnak (nincs Strong), tehát **szerkezetileg nem lexikai kapcsolatúak**, a `motivumok.tsv` `azonossag_tipusa` mezője mégis `lexikai`. A két nyitott NT-jelölt (Mt 24:38, Luk 17:27) ugyanide esik.

- **(A) nyelvszűrés (megvalósítva, a `motivumok.tsv` nem változik).** A gép az NT-helyeken nem dönt, az ÓSZ-helyeken dönt. 0 hamis kizárás; a mintán a MENNY-001 egyetlen elutasítása (ÓSZ) felismert. Hátrány: az NT-hely mindig `vizsgalando` (a gép a MENNY-001 NT-jelöltjeiről nem mond semmit).
- **(B) átsorolás `referenciális`-ra** (a `motivumok.tsv`-ben). Tartalmi döntés: a MENNY-001 meghatározása („a בְּנֵי (הָ)אֱלֹהִים szórendi mintát VAGY a נְפִלִים szót kell tartalmaznia”) szerint az NT-helyek a *referencia* miatt tartoznak ide, nem a lexémából — de a negatív kritérium (lexikai) ezt kizárja; az átsorolás a lexikon-oldalt is érinti.
- **(C) a MENNY-001 teljesen kimarad** (a gép sehol nem dönt). Túlzottan óvatos: az ÓSZ-hely szabálya működik.

**Javaslat: (A).** Okok: nem érinti a `motivumok.tsv`-t; általános szabály (nem MENNY-specifikus kivétellista); 0 hamis kizárás.

## 5. A bevezetés (⛔)

A kiterjesztett szabály a mintán 0 hamis kizárást ad minden lexikai motívumon. Kis minta és torzítás (a #150 naplója szerinti szó szerinti torzítás itt is érvényes), ezért motívumonként:

- **ANTROP-001:** 0 elutasítás a mintában → a bekapcsolás a hamis-kizárás oldalon igazolt (0/8), de a haszon nem mérhető. A kisebb kockázat miatt bekapcsolható; a következő elutasítás a szabályt ellenőrzi.
- **HODIT-001:** a szomszéd-ablak miatt 3/4 → 0/4 felismerés: **bekapcsolva nem ad hasznot** (nincs hibás eredmény, csak üres).
- **ALVIL-001, KIRALY-001, TEREMT-001, MENNY-001:** 0 hamis kizárás, felismerés 4/5, 4/13, 2/2, 1/1.

Javaslat: bekapcsolni mind a hat lexikai motívumon (a küszöb 0 hamis kizárás mindenhol teljesül); a HODIT-001 üres haszna nem kárt jelent. A döntés ⛔ a felhasználó/orkesztrátor (a `LEXIKAI_BEKAPCSOLT` halmaz egy sora).

## 6. Korlátok

1. A lexikai elutasítások száma kicsi (25), a felismerési arány (11/25) nem általánosítható; a 0 hamis kizárás egy 173 soros mintán igaz.
2. A szabály az ablakban ±1 vers egyesített halmazát nézi: ez nagyobb ablak, tehát *kevesebb* kizárást ad (a hibás kizárás ritkább, a haszon kisebb). A HODIT-001 mutatja a kompromisszum árát.
3. A rokonság egy lépés, csak a származtatott irány (szülő → származék); a testvér- és többlépéses rokonságot nem vesszük, ami óvatosan javít (kevesebb felismerés, nem több hamis kizárás).
4. A nyelvszűrés a vers nyelvét a Strong-halmaz első betűjéből (G/H) veszi; kevert (arám/LXX) helyekre nem külön szabály.
