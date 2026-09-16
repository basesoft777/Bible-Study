# SDBH / SDGNT — szemantikai domén-szótárak (héber / görög)

## Forrás

- **Repó:** `ubsicap/ubs-open-license` (https://github.com/ubsicap/ubs-open-license)
- **Commit:** `3a6edd8212df2e1189037ad39687726990c80d56`
- **Verziók:** SDBH v0.9.2 (héber), SDGNT v1.1 (görög)
- **Fájlok és SHA-256:**

| Fájl | SHA-256 |
|---|---|
| `dictionaries/hebrew/JSON/UBSHebrewDic-v0.9.2-en.JSON` | `1686a25dd31dc9afb7b932927e160070667c73caedad11aa7e4482c21f800e8e` |
| `dictionaries/hebrew/JSON/UBSHebrewDicLexicalDomains-v0.9.2-en.JSON` | `fbc862b2c46966cf7f3bf19c2f3e79a7391c34f8c737e1979fa5178ac603d0df` |
| `dictionaries/greek/JSON/UBSGreekNTDic-v1.1-en.JSON` | `d84bb9077a43fa4a4f7e571fe2ffa460fa655d7b78439b366281ce527fd56893` |
| `dictionaries/greek/JSON/UBSGreekNTDicLexicalDomains-v1.1-en.JSON` | `a816a6bb2bdbdd7df6f46f771b5ddb1b9c019d73c3f0147e5a5cead5cfef8b4b` |

**Reprodukáló parancs:**

```bash
python eszkozok/sdbh_sdgnt_import.py --letolt
```

## Licenc és forrásmegjelölés

**CC BY-SA 4.0.** A licenc a forrásmegjelölést kötelezővé teszi, és a származékos
munkára is ugyanezt a licencet írja elő (ShareAlike). A két szótár saját
README-jének zárójeles ©-mondata, szó szerint másolva — ez a licenc által
megkövetelt forrásmegjelölés:

> (UBS Dictionary of Biblical Hebrew © United Bible Societies, 2023.  Adapted from Semantic Dictionary of Biblical Hebrew © 2000-2023 United Bible Societies.)

> (UBS Dictionary of New Testament Greek, © United Bible Societies, 2023. Adapted from Semantic Dictionary of Biblical Greek: © United Bible Societies 2018-2023, which is adapted from Greek-English Lexicon of the New Testa­ment: Based on Semantic Domains, Eds. J P Louw, Eugene Albert Nida © United Bible Societies 1988, 1989.)

Ebből következik: a származékos adat, **beleértve a motívumlexikon
domén-hivatkozásait**, ugyanilyen CC BY-SA 4.0 licenc alá esik. A publikálási
döntés (hogyan és hol tesszük ezt közzé) nyitott — l. `ATALAKITASI_TERV.md.md`
N11.

## Fájlok és oszlopok

| Fájl | Sor (fejléc nélkül) |
|---|---|
| `SDBH_domenek.tsv` | 22 280 |
| `SDGNT_domenek.tsv` | 9 075 |
| `SDBH_SDGNT_domenfa.tsv` | 1 149 |
| `SDBH_SDGNT_anomaliak.tsv` | 185 |

### `SDBH_domenek.tsv` / `SDGNT_domenek.tsv`

Fejléc: `strong strong_kod osszetett nyelv szotar entry_id lemma lexid entry_kod domen_kod domen glossza hivatkozas_n`

**A sor egysége `Strong × jelentés × domén`, nem `Strong × domén`.** A domén a
szótár jelentés-egységén (`LEXMeaning`) ül, nem a Strong-kódon: a `kalal`
(H7043) 11 különböző doménben szerepel, mert mind a 11 jelentése máshová esik
(Agile, Shape, Shame, Curse…). Egy Strong-szintű join a mező-tágításnál minden
jelentés doméntársait egybeöntené egyetlen szó alá — ezt a jelentés-szintű sor
kerüli el.

- `strong` — a Strong-kód levágott alakja (`H0001`, `G0001`); az arámi
  (`A####`) kódok is `H`-előtaggal szerepelnek itt, a `nyelv` oszlop tartja a
  megkülönböztetést.
- `strong_kod` — a Strong-kód eredeti alakja, betű-utótaggal (`H2256b`).
- `osszetett` — a teljes, `+`-jellel összevont StrongCodes-elem, ha a kód
  kifejezéshez (nem önálló szóhoz) tartozik; egyébként `—`.
- `entry_id` / `lemma` — a bejegyzés (`MainId`/`Lemma`) szintjén, nem a
  jelentés szintjén.
- `domen_kod` / `domen` — SDBH-nál a `LEXDomains`, SDGNT-nál elsősorban a
  `LEXSubDomains` (Louw–Nida alcsoport), csak ha az üres, a `LEXDomains`
  (főcsoport). Domén nélküli jelentésnél `domen_kod = domen = —`.
- `hivatkozas_n` — a jelentéshez tartozó `LEXReferences` száma (nem a
  hivatkozott igehelyek listája — az importálásra l. "Ismert korlátok").

### `SDBH_SDGNT_domenfa.tsv`

Fejléc: `szotar kod szint szulo_kod cimke leiras`. A két `LexicalDomains` JSON
teljes hierarchiája: `szulo_kod` a kód utolsó három jegye nélkül (a
legfelső szintnél `—`), `cimke`/`leiras` az `en` lokalizáció.

### `SDBH_SDGNT_anomaliak.tsv`

Fejléc: `szotar entry_id lemma tipus nyers_ertek allapot`. A forrás hibás
(`ervenytelen_kod`) vagy hiányzó (`strong_nelkul`) Strong-kódú bejegyzései,
javítás vagy kitalált előtag nélkül (`CLAUDE.md` 3. szabálya). Az `allapot`
minden sorban `AZONOSITVA, NEM JAVITVA`.

## Mért értékek

| Tétel | SDBH | SDGNT |
|---|---|---|
| adatsor (fejléc nélkül) | 22 280 | 9 075 |
| különböző `strong` | 8 557 | 5 312 |
| különböző `strong_kod` | 8 935 | 5 397 |
| különböző `entry_id` | 7 862 | 5 397 |
| különböző `lexid` | 16 219 | 9 067 |
| különböző `domen_kod` (`—` nélkül) | 380 | 668 |
| `domen_kod = —` sor | 344 | 21 |
| `osszetett ≠ —` sor | 12 | 0 |
| `nyelv = arameus` sor / különböző `strong_kod` | 2 086 / 647 | — |
| doménfa-sor | 411 | 738 |
| anomália-sor | 75 (35 `strong_nelkul` + 5 `ervenytelen_kod` + 35 `jelentes_nelkul`) | 110 `strong_nelkul` |

**Forrás-leltár** (minden forrásbejegyzés pontosan egy helyen áll):

| | forrás | a kivonatban (`entry_id`) | `strong_nelkul` | `jelentes_nelkul` |
|---|---|---|---|---|
| SDBH | 7 932 | 7 862 | 35 | 35 |
| SDGNT | 5 507 | 5 397 | 110 | 0 |

**Lefedettség** (a kivonat `strong` oszlopa a kivonatok lexikai Strong-kódjaihoz
mérve; a héber oldalon a `H9xxx` nélkül):

| | Strong-kód | Token |
|---|---|---|
| `TAHOT_kivonat.tsv` | 8 421 / 8 502 (99,0%) | 259 162 / 299 370 (86,6%) |
| `TAGNT_kivonat.tsv` | 5 252 / 5 410 (97,1%) | 130 159 / 141 489 (92,0%) |

## Ismert korlátok

- **A lefedettség kb. 90%.** Az SDBH még nem teljes szótár (a forrás README-je
  szerint az ÓSZ szókincsének kb. 90%-a áll benne), és **gyakori szavak is
  hiányoznak**, köztük `H1961` (lenni), `H5414` (adni), `H6440` (arc),
  `H5921`, `H0413`, `H3605`, `H3588`. **Az üres `domen`-eredmény ezért nem
  negatív lelet.**
- **Strong-homográfok.** Öt Strong-szám (`H1529`, `H2269`, `H5613`, `H6211`,
  `H8412`) egyszerre héber és arámi szóra is ki van osztva a `TAHOT_kivonat.tsv`
  szerint — ez a forrás Strong-rendszerének sajátossága, nem leképezési hiba.
- **Az anomália-fájl** (`SDBH_SDGNT_anomaliak.tsv`) 185 sora két fajta tételt tart.
  **150 sor javítatlan forráshiba** (`AZONOSITVA, NEM JAVITVA`): szerzőnév a
  Strong-mezőben, előtag nélküli szám, Strong-kód nélküli bejegyzés. **35 sor
  elemzetlen bejegyzés** (`jelentes_nelkul`, `FORRASBAN_BEFEJEZETLEN`): a
  szótár felvette a szót, de jelentés-egységet és domént még nem rendelt
  hozzá — köztük gyakori szavak, pl. `A0116` (*'edajin*, „akkor"), `H0518`
  (*'im*, „ha"), `H1931` (*hú'*, „ő"). A `domen` ezeket külön jelzi. L. a
  döntésnaplót a `SDBH_IMPORT_BRIEF.md`-ben.
- **Az arámi ellenőrzés egysége.** 372 forrásbejegyzés visel csak `A`-kódot;
  ebből 367 van a kivonatban (5 elemzetlen), a 372 mögött pedig 367 különböző
  normalizált kód. A két 367 véletlenül egyezik; az `sdbh_sdgnt_ellenoriz.py`
  mindkét egységet külön ellenőrzi.
- **A `LEXReferences` (héber versszámozás) nincs importálva** — csak a darabszám
  (`hivatkozas_n`). A tényleges igehely-szintű hivatkozás-tábla (szakasz-profil)
  ennek a menetnek szándékosan nem része (`SDBH_IMPORT_BRIEF.md` N1).
- **A domén támasz, nem a mező-hipotézis helyettesítője** (terv D18): a
  szemantikai mező kiválasztása emberi döntés marad. Példa: az `itzávón`
  (H6093, "gyötrelem/kín") doménje *Spasm*, nem *Curse* — a `domen H6093 H0779`
  lekérdezés üres metszetet ad, ez nem cáfolja az `itzávón`↔`arar` tematikus
  kapcsolatot, csak azt mutatja, hogy a domén-szótár másik szemponton osztályoz.
