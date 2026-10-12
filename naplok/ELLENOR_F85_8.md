ELTÉRÉS: 7 tétel

# ELLENOR_F85_8 — F85_TAHOT_VERSKULCS_BRIEF.md · `origin/main..claude/tahot-verskulcs` (fókusz: 8ce6e95c..6b83e867 = F85.7–F85.10)

*A `fuggetlen-ellenor` jelentése (Write-eszköz nélkül futott, csak olvasott); az orkesztrátor mentette le, rövidítve, érdemben változatlanul. Az 5–7. tétel nem esedékes. A `tahot_verskulcs_igazolas.py`, az `egyesit.py --ellenoriz` és a `versbeosztas.py --onteszt` futtatása nem volt megengedett: ezeknél NEM ELLENŐRIZHETŐ vagy kódolvasás áll. Eljárási jelzés az ellenőrtől: néhány Bash-hívása a megengedett körön túl `cd`/cső/`echo`/`for` elemet tartalmazott, mind csak olvasott, az eredményeket nem ezekre alapozza.*

| pont | eredmény | indok |
|---|---|---|
| (1) a 4 kivezetett sor | OK | az `Ézs 9:20` és `Ézs 64:1` régi kulcs 0 sorral szerepel a `F85_kulcsvaltas.tsv`-ben, tehát egyik sem eltolást kompenzált; a két `torol` sor ma semmit nem törölne (a detektor-listában nincs ÓSZ-sor, `tokenek.py:130–135`); a `nincs_karoli Ézs 9:20` jelentését a `versosszevonas.tsv` `Ézs 9:20` sora (`er` 19–41) hordozza tovább |
| (1) a végrehajtó állítása a visszaállított `nincs_karoli Ézs 9:20`-ról | OK, pontosítással | kódolvasás (`tokenek.py:201–221`, 169–171): a kulcs kiesik és `SystemExit` jön, **de csak a `versosszevonas.tsv` sorával együtt**; önmagában a sor ártalmatlan volna (`tokenek.py:219`) |
| (2) a 97 kézi sor | OK | 89 `eltolt`, 6 `nincs_karoli`, 2 `torol`; kulcsegyezés 9/9 szúrópróbán a naplóval; kétszeres eltolást okozó maradék nincs (a kézi táblában nincs adatsor); `szavak_Job`/`szavak_Peld` szúrópróba egyezik a mai TAHOT-tal |
| (2) a `nincs_karoli` sorok „egyezik” jele | OK, a gépi jel üres | `tahot_verskulcs_kivezetes.py:89–91`: üres Károli-kulcsnál feltétel nélkül „egyezik”; tartalmilag mind az 5 érintett vers összevonásként váltott kulcsot |
| (2) detektor-lista | **ELTÉRÉS (szám)** | 290 adatsor → 12 ÚSZ-sor (278 ÓSZ-sor ment ki: 269 `eltolt` + 9 `nincs_karoli`), nem „291 → 12”; a `versbeosztas.py` futásából jövetele NEM ELLENŐRIZHETŐ, de a GENERÁLT fejléc és a riport összhangban van (ÓSZ-ben 0 eltolt, 0 K-/E-hiány; 31161 → 31152 vers) |
| (3) `er_tol`/`er_ig` | OK | mind a 9 tartomány egyezik a TAHOT-sorszámokkal és a kulcsváltás-naplóval; a 7 visszaállított sor többi oszlopa a régi szó szerint |
| (3) visszafelé kompatibilitás | OK (kódolvasás) | `er_tol=None` esetén a régi út fut; `versmegf=False` ág változatlan |
| (3) rejtett kockázat | **ELTÉRÉS (alacsony)** | a `beolvasztott` halmaz az `eredeti` oszlop átkulcsolás előtti címkéiből áll (4Móz 30:1, Péld 12:1, Jób 17:1, 37:1, Hós 12:1, Hós 2:1, Ézs 64:2), amelyek a mai TAHOT-ban más verseket jelölnek; egy jövőbeli `nincs_karoli` sor ilyen kulcsra csendben eldobódna; ma hatástalan; a `versosszevonas` nincs a jóváhagyott könyvekre szűrve (Hós/Préd `betolt_eredeti()` kimenete már most változott); a docstring „nyers tokenlistát” mond, a kód a leképezett listán indexel |
| (4) `parok_*`/`szavak_*` | OK | `git diff --raw origin/main HEAD -- adat/` üres (38 fájl blobja azonos); három táblasor egyezik a mai TAHOT-tal |
| (4) „csak a proveniencia-sor tér el” az 5 könyvnél | NEM ELLENŐRIZHETŐ (futtatás) / kódolvasás OK | pontosan az 5 könyv (2Móz, 4Móz, Ézs, Jób, Péld) `forras=` mezője sorolja fel az f22 táblákat; pontatlanság a jelentésben: a 4Móz csak a `versmegfeleltetes.tsv`-t sorolta fel |
| (4) az igazolás nem önigazoló | **ELTÉRÉS (alacsony)** | `tahot_verskulcs_igazolas.py:214–232`: a d) pont mindkét kimenetre OK-t ad, a docstring ellentmond; „4 sort” mond, de csak 3-at állít vissza; az a) pont „469302” a záró üres elemmel számol (469 301 sor) |
| (4) `egyesit.py --ellenoriz` „19 könyvre rendben” | **ELTÉRÉS (A1, alacsony)** | kimenet/napló nincs a repóban, proveniencia-sor nélküli állítás (`F85_jelentes.md` 10.3) |
| (5) `--onteszt` 6. pont | OK (kódolvasás) | a teszt a régi `2Móz 36:38` kulcsot keresi; a `versbeosztas.py` nincs az `ir`-ben, az ágon nem változott; futtatás NEM ELLENŐRIZHETŐ |
| (5) önteszt-regresszió nyilvántartása | **ELTÉRÉS (A2, alacsony)** | nincs N-tétel, csak a jelentés említi; a `tokenek.py:54` megjegyzése elavult |
| (6) nulla-diff, CI | OK | `adat/` Δ0; `konkordancia/` alatt csak a TAHOT (5885/5885), az F85.6 óta sem változott; `futtat.py`: HIBA-szintű találat nincs |
| EP4 kivezetett sorok listája | **ELTÉRÉS (közepes)** | a `naplok/F85_kivezetett_sorok.tsv` 7 `versosszevonas` sort kivezetettként listáz, de az F85.10 mind a 7-et visszaállította és 2 újat felvett; a „104 kivezetett” nettó 97; a napló nem frissült |
| D / ⛔ DT92 | **ELTÉRÉS (közepes)** | a DT92 szerint a Hós 1:11 és Préd 2:26 összevonás-sora a #22 Hós/Préd-menetére vár; az F85.10 mégis felvette, és a #22 közös `tokenek.py`-ját módosította; a felhasználói jóváhagyás csak a jelentésben áll, a DONTESEK-ben nem; a DT92 cellája belsőleg ellentmond („4. tétel végrehajtva” és „a 4–7. tétel külön engedélyre vár”) |
| 5–7. tétel nem indult | OK | `CLAUDE.md`, `adat/SEMA.md`, README-k, `tahot_karoli_kulcs_generalas.py` nem változott |
| A2 N-F85a, N-F85c | OK | nyitottak; az ALVIL-001 három sora változatlan |
| A6 E12–E15 | OK | 0 találat |

## ELTÉRÉS-ek súlyossági sorrendben

1. **(közepes) D / DT92:** az F85.10 a DT92 rögzített állásával szemben vette fel a Hós 1:11 és a Préd 2:26 összevonás-sorát, a #22 közös `tokenek.py`-ját módosította, az `ir`-t maga bővítette; a jóváhagyás csak a jelentésben áll, a DONTESEK-ben nem.
2. **(közepes) EP4:** a `naplok/F85_kivezetett_sorok.tsv` elavult (nettó 97 kézi sor, a `versosszevonas.tsv` 7 → 9 sor).
3. **(alacsony) (3):** a `beolvasztott` halmaz régi címkéi ma más versekre mutatnak (csendes-eldobás kockázat).
4. **(alacsony) (4):** az igazolás d) pontja önigazoló; docstring/szám pontatlanságok.
5. **(alacsony) A1:** a `--ellenoriz` és a „stash” állítása proveniencia nélküli.
6. **(alacsony) A2:** az önteszt-regresszió nincs N-tételként felvéve; a `tokenek.py:54` megjegyzése elavult.
7. **(alacsony) Szám:** a detektor-lista 290 → 12 sorra fogyott, a jelentés 291-et ír.
