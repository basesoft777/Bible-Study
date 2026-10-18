# TSK-versszám javítás — jelentés (F114, a 3.5 elfogadási mérés)

*2026-10-18 · modell: claude-sonnet-5-5 · ág: `claude/tsk-versszam` · alap: `origin/main` be85d5de · mérőszkript: `eszkozok/tsk_versszam_felmeres.py` (E. rész)*

Az öt fogyasztó (`lexikon_general.tsk_index`, `lekerdez.cmd_tsk`, `nem_vizsgalt.tsk_kor`, `sqlite_epit._kereszthivatkozasok`, `olvaso_pilot/adat.py`) a `eszkozok/tsk_kulcs.py` átváltón át olvassa a TSK-t: forrás- és célkulcs Károli-versszámon áll. Az ÚSZ-en az átváltó azonosságot ad (DT-F114b (b), N-F114a).

## E1 — a nyers mező nem olvasható megkerüléssel

`grep` az öt fájlon az `['Igehely']` / `['Kapcsolódó igehely']` mezőre: a TSK-t érintő minden olvasás a `tsk_kulcs.karoli_sorok` / `forras_sorok` / `karoli_index` kimenetén történik (`lexikon_general.py:1916–1923` `tsk_index`; `lekerdez.py` `cmd_tsk`; `nem_vizsgalt.py:454`; `sqlite_epit.py:684–689`; `olvaso_pilot/adat.py:168–176`). A többi találat más táblát olvas (TAHOT, TAGNT, Károli-KH, TIPNR, BSB, KJV), nem a TSK-t.

## E2 — a dataset bájtra változatlan

`konkordancia/TSK_kereszthivatkozasok.tsv`: sha256 `168c44158d94363af6292c0d15a550afe04e46f97d9a1c52e84b1ad9cd421c16`, git blob `a1b6a607ea2c71e4b60daccfaa0519e0d6bbee93`, azonos az `origin/main`-nel.

## E3 — felmérőszkript a javított átváltón át (ÓSZ)

| Mérés | Érték |
|---|---|
| A. fogyasztói úton olvasott ÓSZ Károli-kulcs | 21 234; KJV-forrása nem a megfeleltetés szerinti: **0** |
| B. `elofordulasok.tsv` ÓSZ-versei (megfeleltetéssel) | 224 vers |
| B. minden Votes | rossz versről **0**, elmarad **0** |
| B. Votes ≥ 15 | rossz versről **0**, elmarad **0** |
| nincs-pár forrás-KJV-kulcs (ÓSZ, a sor kimarad) | 345 kulcs, 4 976 sor |
| nincs-pár cél-KJV-vers (ÓSZ, a sor kimarad) | 359 vers, 4 378 előfordulás |

A nincs-pár kulcsok tételes listája: `python eszkozok/tsk_versszam_felmeres.py` E. rész (a kulcs- és darabszám-lista teljes kimenete, a stdout-on 80 tételig). A nincs-pár kulcsok a KJV-nek olyan versei, amelyeknek a Károliban nincs azonos tartalmú párja (pl. 1Sám 17:12–31, 2Móz 35–36, 1Kir 6:12–14 számozás-eltérései, `Karoli_versmegfeleltetes.tsv`: üres KJV-oszlop / hiányzó KJV-pár). Ezeket az átváltó explicit „nincs pár”-ként kezeli; a sor kimarad (nem csendes azonosság).

A felmérő mérése közben két mérőhibát javítottam (a szkript a javítás után 0/0-t mér): az ÚSZ-célok a „helyes” halmazban azonosságot kapnak, a Votes-küszöb 0 esetén a negatív Votes-sorok (pl. `-14`) is bent vannak.

`proveniencia: scope=TSK-teljes ÓSZ + elofordulasok.tsv ÓSZ-versei | forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv (tsk_kulcs) | n=432949 | ts=2026-10-18`

## E4 — próbagenerálás (a repón kívülre: `%TEMP%/f114p`)

`python eszkozok/general.py --cel lexikon --kimenet <TEMP>` + `--cel torzscikk`:
- ALVIL-001 `#### Préd 9:12` alatt a 12 TSK-sor: Kol 3:23 (Votes 71) az első, majd Ef 5:16, Róm 12:11, **Zsolt 6:6** (24), 1Kor 9:24, Préd 11:6, 2Krón 31:20, 31:21, Jer 29:13, Mt 6:33, Ézs 38:18, Ézs 38:19. A N-F09g-listában a „Zsolt 6:5” a TSK **KJV**-célja volt; Károli-kulccsal Zsolt 6:6 (a Károli 6:6 = KJV 6:5). Ez a céloldali javítás helyes, de a lista egy sora emiatt nem azonos (l. alább, DT-F114c).
- ALVIL-001 `#### Zsolt 18:6` alatt nincs Zsolt 50:15 (`grep -c "Zsolt 50:15"` = 0).
- TEREMT-001 `#### Zsolt 36:7` alatt nincs Ruth 2:12 (`grep -c "Ruth 2:12"` = 0).

## Lekérdezések (F114.2)

`python eszkozok/lekerdez.py tsk "Préd 9:12"` → első sor `Kol 3,23	Votes=71`; `tsk "Zsolt 18:6"` → nem tartalmaz `Zsolt 50,15`-öt; `tsk "Zsolt 16:10"` → `Zsolt 49,16 Votes=23` (nem 49,15); `tsk "Zsolt 18:1"` → 0 sor, „nincs KJV-pár” jelzéssel.
`proveniencia: scope=range:Préd 9:12 | forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv (tsk_kulcs, KJV->Károli) | n=49 | ts=2026-10-18` (a CLI kimenetéből).

## Tesztek

- `python eszkozok/teszt_tsk_kulcs.py`: 10 teszt, OK.
- `python eszkozok/teszt_futtat.py --gyors` a WSL-natív `~/pardes/pardes.db`-vel (építve 2026-10-14, a régi KJV-kulcsú `tsk` táblával): `teszt_olvaso_szerver.py` 2 hiba (`TestD2PilotEgyezes.test_1moz_1_25`, `test_zsolt_22`: `vers:tsk_top6` / `vers:tsk_darab` eltérés), mert a pilot (új, Károli-kulcsú) és a régi DB `tsk` táblája nem egyezik. Ez a #101 (a `pardes.db` újraépítése) hatóköre.
- Igazolás: a javított `sqlite_epit.py --mod teljes`-szel a repón kívülre épített ideiglenes adatbázison (919 MB, 135,8 s, 75 tábla) a `teszt_olvaso_szerver.py` **73 teszt, OK** (a D2-egyezés zöld). Az ideiglenes adatbázis törölve.
- `teszt_bdb_vers_jelentes.py` 1 hiba (`Ujrageneralas.test_bajtra_azonos`): a fejlécben `DT-F99n` ↔ `DT179` számozás-különbség, nem TSK-hatás; ennek az ágnak a változtatásai nem érintik.
- `teszt_arculat`, `teszt_indito`, `teszt_pilot_aranymintaval`, `teszt_tervezo`: zöld.

## Az N-F09g kivezetés (3.6) — megállás

A `render_diff_osztalyoz.py --proba` a friss próbán (`%TEMP%/f114p`): `ismert_hiba_tsk_versszam` = 2 sor még törölt: a tudományos oldal `- TSK: Zsolt 6:5 (Votes: 24)` és a törzscikk összevont sora (ugyanezen jelölttel). Ok: az éles lexikon a KJV-célt (Zsolt 6:5) hordozza, az átváltóval a helyes Károli-cél Zsolt 6:6. A brief szerint ilyenkor megállás (DT-F114c).
Ugyanezen a próbán az `ismeretlen` kategória 41 sorú, mind TSK-sor, az éles lexikon régi (KJV-kulcsú / KJV-célú) TSK-sora, amelyet az átváltás kiegészít vagy kivesz (pl. ALVIL-001 Zsolt 18:6 alatt Zsolt 50:15, 49:15 → 49:16; ANTROP/HAMART/ISTENTISZT/TEREMT/MENNY TSK-sorai). Ezek a #36/#10 éles újragenerálásakor a diff-osztályozóban `ismeretlen`-ként állnának meg.
