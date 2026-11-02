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

## 7. Döntések (2026-11-02; DT-F160a, DT-F160b)

Az orkesztrátor döntése a felhasználó 2026-11-02-i felhatalmazásával: »… a döntéseket fogadja, és hozza is meg«.

- **DT-F160a:** MENNY-001 → (A) nyelvszűrés; a `motivumok.tsv` nem változik. A (B) átsorolás a #123 MENNY-001 migrációjában dől el (N-F160a; Mt 24:38, Luk 17:27).
- **DT-F160b:** `LEXIKAI_BEKAPCSOLT` = ALVIL-001, KIRALY-001, TEREMT-001, MENNY-001. Az ANTROP-001 (0 elutasítás) és a HODIT-001 (nincs haszon) kimarad; újramérésük a #123 migrációi után (N-F160b).

## 8. A HAMART-001 hordozója

A `motivumok.tsv` szerint a HAMART-001 `azonossag_tipusa` = **strukturális** (nem lexikai, nem formulaikus). A #150 formulaikus szabálya sem a #160 lexikai szabálya nem vonatkozik rá: a hordozó-szabály szerint minden sora `vizsgalando` („a hordozó nem formulaikus: a gépi szabály nem dönt”; ma 8 nyitott sor). Mért ok: hordozó-szűrés nélkül a szabály 83/163 elutasítást ismerne fel, de 5 hamis kizárást adna (Ézs 24:5-6, Hós 4:1-3, Mt 15:19, Mk 7:21-23, 2Pét 3:6-7; `naplok/JELOLT_ELOSZURES_naplo.md` 3.1). Tehát a #123 HAMART-001 menetében a gépi sorrend nem segít: az átnézés sorrendje kézi. Ez nem a lexikai tétel feladata, a hordozót nem módosítottuk.

## 9. A kimenet változása lokálisan (a `jelolt_eloszures.py` futása a bekapcsolt halmazzal)

A `naplok/ELOSZURES_*.tsv` fájlok közül két sor-halmaz változik; a többi (ALVIL-001, TEREMT-001, ANTROP-001, HODIT-001, HAMART-001, ISTENTISZT-001, TEREMT-002) bájtra azonos.

| motívum | sor | előtte | utána |
|---|---|---|---|
| MENNY-001 | Mt 24:38 | vizsgalando (a hordozó nem formulaikus) | vizsgalando (nincs G-nyelvű gerinc-kombináció) |
| MENNY-001 | Luk 17:27 | vizsgalando (a hordozó nem formulaikus) | vizsgalando (nincs G-nyelvű gerinc-kombináció) |
| KIRALY-001 | 1Pét 2:9 | vizsgalando (a hordozó nem formulaikus) | **valoszinu_ki** (G0282+G0540+G5010, G5010 hiányzik; az ablakban a gerincből: semmi) |

**⚠ Figyelmeztetés a KIRALY-001 1Pét 2:9 soráról.** A `jeloltek.tsv` indoklása szerint a hely a régi napló szerint beépítve (2026.09.09, retroaktív pótlás, „szó szerinti LXX-idézés, G0934+G2406”), csak a `jeloltek.tsv`-ben és az `elofordulasok.tsv`-ben nincs sor (elbírálás: N-F63a). A gép `valoszinu_ki`-t ad, mert a KIRALY-001 jelenlegi kombinációi közt a G0934+G2406 (βασίλειον ἱεράτευμα) nincs benne. Ez **ismert ellenpélda**: a kombináció-halmaz hiányos, tehát ez egy hamis kizárás-jelölt egy nyitott soron — a mérés (0/173) a *döntött* sorokra igaz, ezt nem fogta meg. A kimenet csak átnézési sorrend (a döntés a felhasználóé, a `jeloltek.tsv` nem változik), de a küszöb szellemében a KIRALY-001 bekapcsolása az N-F63a eldöntéséig kérdéses: a `LEXIKAI_BEKAPCSOLT`-ból egy sor törlése elegendő. A döntés az orkesztrátoré.
