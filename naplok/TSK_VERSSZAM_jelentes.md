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

**Javítás (F114.10, a független ellenőri jelentés alapján, `naplok/ELLENOR_TSK_VERSSZAM.md`):** az előző változat hamisan állította, hogy a nincs-pár kulcsok (pl. 1Sám 17:12–31) olyan KJV-versek, amelyeknek a Károliban nincs azonos tartalmú párja. A valós ok más: a `Karoli_versmegfeleltetes.tsv` ezekben a sorokban az `igehely_kjv` mezőt **üresen** hagyja (LXX-hiány, `MT|szamlalas`; 161 üres KJV-sor: MT|szamlalas 86, MT|lxx_os_etalon_f91 66, KEZI|kezi_identitas_javitas 8, KJV|lxx_os_etalon_f91 1), a KJV-vers és a Károli-vers viszont létezik és azonos. A modul ezt „nincs pár”-nak vette, ami regresszió a main-hez képest. A 0/0 mérés (E3) a megfeleltetésből számolja a „helyes” halmazt, tehát körkörös: ezt a hibát nem foghatta meg. A nem körkörös mérés a felmérő F. része és `naplok/F114_elveszett_sorok.tsv`; a döntés DT-F114d.

A nincs-pár kulcsok tételes listája: `python eszkozok/tsk_versszam_felmeres.py` E. rész (stdout-on 80 tételig), valamint `naplok/F114_elveszett_sorok.tsv` (a régi logika által elért kulcsok).

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

## F114.5 — DT-F114c (a): `tsk_kulcs_javitas` (Felhasználó, 2026-10-18)

Az `ISMERT_HIBA_TSK_VERSSZAM` / `ismert_hiba_tsk_versszam` helyett `TSK_KULCS_JAVITAS_SOROK` / `tsk_kulcs_javitas`: 43 név szerinti törölt sor (2 az N-F09g-ből + 41 régi TSK-sor). Negatív teszt: a listán kívüli TSK-sor (és a lista sora más motívumban) `ismeretlen` marad. `teszt_render_diff_osztalyoz.py`: 74 teszt, OK.
Újrafuttatott próba-osztályozás (`--proba`, kilépési kód 0): `tsk_kulcs_javitas=43`, `ismeretlen=0`. Napló: `naplok/F114_proba_diff.tsv`, `naplok/F114_proba_ismeretlen.tsv` (az utóbbi most csak a korábban elfogadott `felhasznalo_elfogadva` sorokat tartalmazza).
`proveniencia: scope=%TEMP%/f114p vs lexikon | forras=eszkozok/render_diff_osztalyoz.py --proba | ts=2026-10-18`

## F114.14 — DT-F114d (b): MT-tartalék csak az `MT|szamlalas` sorokra (Felhasználó, 2026-10-18)

A `tsk_kulcs` az `osztaly=MT`, `forras=szamlalas`, üres `igehely_kjv` sorokra (86 sor) az `igehely_mt`-t veszi KJV-kulcsnak. Más üres-KJV sor és a táblában sor nélküli Károli-vers (`nincs_sor`) „nincs pár” marad (indok: a Károli 1908-ban a Hós 13 15, a Hós 14 10, az Én 6 10 versből áll, a KJV-ben 16, 9, 13; a számegyezés hibás párt adna). Teszt: `teszt_tsk_kulcs.py` 12 teszt, OK (pozitív: 1Sám 17:12, Jer 33:15; negatív: Hós 14:2, Zsolt 18:1, Jób 39:34, Préd 9:21, Zsolt 13:1).
Frissített mérés (felmérő E. és F. rész):
- E: fogyasztói kulcs 21 309, KJV-forrás eltérés 0; B-rész (224 vers) rossz 0 / elmarad 0 (minden Votes és ≥ 15); nincs-pár forrás 272 kulcs / 4 211 sor, cél 282 vers / 3 446 előfordulás.
- F (nem körkörös, a main régi logikájához képest, ÓSZ): régen elért pár 232 697, most 227 736; elveszett pár 30 027, újonnan elért 25 066. Elveszett forrássor 3 851 sor / 247 kulcs: `nincs_sor` 3 653 / 235, `KEZI|kezi` 169 / 10, `KEZI|kezi_tobbforrasu_osszevonas` 26 / 1, `KJV|lxx_os_etalon_f91` 3 / 1 (az utóbbi három valódi eltolódás). Elveszett célelőfordulás 2 548 / 256 vers: `nincs_sor` 2 360 / 243, `KEZI|kezi` 147 / 11, `KEZI|kezi_tobbforrasu_osszevonas` 33 / 1, `KJV|lxx_os_etalon_f91` 8 / 1. Tételes: `naplok/F114_elveszett_sorok.tsv` (506 sor); a `nincs_sor` fejezetek az N-F54a bővítésében.
- `lekerdez.py tsk "1Sám 17:12"`: 16 sor; `tsk "Jer 23:5"`: eléri a Jer 33,14 és 33,16 célokat.
`proveniencia: scope=TSK ÓSZ-sorai | forras=TSK_kereszthivatkozasok.tsv+Karoli_1908.tsv+Karoli_versmegfeleltetes.tsv (tsk_kulcs) | n=232697 | ts=2026-10-18`
