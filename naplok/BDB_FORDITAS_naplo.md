# F38 BDB_FORDITAS — futásnapló

*Brief: `F38_BDB_FORDITAS_BRIEF.md` v1 · ág: `claude/admiring-bohr-texair` · indult: 2026.10.01*

## M0 — Felmérés (F38.1)

Parancs: `python naplok/BDB_FORDITAS_M0.py` (csak olvas; egyetlen kimenete a
`naplok/BDB_FORDITAS_sorrend.tsv`). Minden szám ebből a futásból.

### 1. Előfeltétel (F34)

- Az F34 merge-commitja (`fa501c9`) az `origin/main`, a `main` és a `HEAD` őse: **igen**.
- BDB-forrás: 8 090 szócikk, 6 325 071 karakter (a brief 6,40 milliót írt; a különbség a
  brief becslése, a mérés ez).
- **A 13. kapu (fejezetszám) a forráson nem 0 jelzést ad: 91 szócikk jelez.** Mérés: a forrás
  könyvnévvel jelölt igehelyeit a 11. kapu leképezésével (`forditas_kapuk._konyv_mintak`)
  Károli-alakra fordítva, szócikkenként `ellenoriz_fejezetszam`. Ebből 83 szócikk az F34
  maradék-listáján van (`naplok/F34_M2_maradek.tsv`, N-F34: a ψ-hiba B/R maradéka, amelyet az
  F34 a felhasználó döntésével — DT-F34b/c — szándékosan hagyott meg); 8 szócikk nincs rajta
  (nem ψ eredetű könyvfeloldási hibák, az N-F34c köre):

  | Szócikk | Jelzés (Károli-alakban) |
  |---|---|
  | H0854 | Ján 30, Ján 54, Jón 11 |
  | H3117 | Dán 40 |
  | H5750 | 2Krón 43, 2Krón 45 |
  | H6684 | Jón 20 |
  | H6881 | Dán 19 |
  | H8034 | Dán 22 (a brief „Dán 22:14” példája) |
  | H8478 | Dán 18, Dán 21, Dán 24 |
  | H9004 | Dán 23 |

  Az M1 adag négy szócikke érintett: H9009 (1Kir 45, 59, 61, 66), H9005 (Hab 41, Jóel 9),
  H0413 (5Móz 37), H0834 (Ruth 8, 9) — mind az F34 maradék-listáján.

  **Kezelés:** a brief M0.1 szó szerint megállást írna elő („Ha nem, megáll és jelez”); a
  brief „Szabályok” szakasza viszont pontosan erre az esetre ad eljárást („Forráshiba … a
  fordítás hűen átveszi, a 13. kapu jelzése a naplóba kerül; a forrást ez a menet nem
  javítja”), és a maradékot az F34 jóváhagyottan hagyta nyitva. A menet az utóbbi szerint
  haladt tovább az M1-gyel; a kérdés a `DONTESEK.md` DT-F38 (b) pontjában a felhasználóé. A
  13. kapu nem gátoló (JELZES), a forrásbeli hibás igehely a fordításban változatlanul
  (Károli-rövidítéssel) szerepel.

### 2. Gyakoriság — forrásválasztás

A brief „Károli Ószövetségben mért” Strong-gyakoriságot kér. **Strong-címkés teljes Károli-ÓSZ
nincs a `konkordancia/` alatt:** a `Karoli_Strong_kivonat.tsv` 383 adatsor (tanulmányokból
kézzel kigyűjtött kivonat). A brief szerint „közkincs vagy nyílt licencű” Strong-címkés
ószövetségi szövegből kell számolni; a menet a **`konkordancia/TAHOT_kivonat.tsv`**-t
használta (STEPBible TAHOT, CC BY 4.0; a héber/arámi szöveg szavanként Strong-címkével; a
gyakoriság = a Strong-szám sorainak száma). Ok: a héber szavak tényleges előfordulását
számolja, nem egy fordítás címkézését; a versszámozása a Károliéval egyező (magyar kulcs).
Ismert korlát: a `CLAUDE.md` szerint nem teljes (az F34 mérése szerint csak a Jób 41
hiányzik, N-F34b) — a sorrendet ez legfeljebb egy-két helyen mozdítja.

Összevetés: `konkordancia/KJV_Strongs_teljes.tsv` (közkincs, angol szavak Strong-címkéje).

| | Címkézett szó | Különböző H-szám | ebből BDB-szócikk |
|---|---|---|---|
| TAHOT | 468 968 | 8 546 | 8 003 |
| KJV | 227 196 | 8 584 | 8 025 |

A top-N halmazok átfedése (TAHOT ~ KJV): top-50: 31, top-100: 69, top-500: 444. Az eltérés
oka főként, hogy a KJV a fordításban nem megjelenő héber szavakat (névelő, `אֵת`, kötőszó,
prefixumok) nem vagy másként címkézi; a TAHOT ezeket számolja.

**Megjegyzés:** a TAHOT a prefixumokat (névelő `H9009`, `ו` kötőszó `H9005`, `ב` elöljáró
`H9003`) külön STEPBible-számmal címkézi, és a BDB-forrásnak is van ilyen kulcsú szócikke. Ezért
a sorrend élén ezek állnak. 87 BDB-szócikk TAHOT-gyakorisága 0; ezek a lista végén, Strong-szám
szerint.

### 3. Sorrend

`naplok/BDB_FORDITAS_sorrend.tsv` (`sorszam`, `strong`, `gyakorisag`, `karakter`, `adag`):
TAHOT-gyakoriság szerint csökkenő, egyenlőnél Strong-szám. Kimaradt a 26 kész szócikk (az
`adat/forditasok.tsv` BDB `teljes` sorai).

| | Szócikk | Karakter |
|---|---|---|
| Fordítandó | 8 064 | 6 198 682 |
| ebből 2 000 karakter fölött | 606 | – |
| ebből 20 000 karakter fölött | 11 | max. 45 414 (H9005) |

### 4. Szegmenshatárok (20 000 karakter fölött)

Javaslat: a vágás strukturális helyzetű (előtte `— `, `. ` vagy `; `) tagolásjelölő vagy
igetörzs-címke előtt, mohón, legfeljebb kb. 10 000 karakteres szegmensekre. A szegmens a
fordítás vázlatrésze; a kapukra és a táblába a szócikk egyben kerül (a #28 G4151/H1121
gyakorlata). Pozíció = karakter-eltolás a forrásban.

| Strong | Sorszám | Karakter | Határok (pozíció «jelölő») | Szegmenshosszak |
|---|---|---|---|---|
| H9005 | 2 | 45 414 | 8651 «b», 18603 «(β)», 28584 «(γ)», 38449 «b» | 8651/9952/9981/9865/6965 |
| H0834 | 7 | 22 469 | 8742 «c», 16954 «3» | 8742/8212/5515 |
| H3588 | 11 | 23 687 | 9357 «b», 18177 «a» | 9357/8820/5510 |
| H1961 | 12 | 24 992 | 9780 «a», 19560 «b» | 9780/9780/5432 |
| H3117 | 19 | 20 257 | 9162 «b», 16155 «h» | 9162/6993/4102 |
| H6440 | 20 | 21 162 | 9559 «b», 18093 «a» | 9559/8534/3069 |
| H5414 | 22 | 23 371 | 6520 «i», 15098 «b» | 6520/8578/8273 |
| H1980 | 27 | 43 729 | 6260 «(3)», 15367 «3», 25328 «d», 34211 «4» | 6260/9107/9961/8883/9518 |
| H4480 | 32 | 35 799 | 8886 «b», 16784 «b», 25436 «(3)», 35389 «II» | 8886/7898/8652/9953/410 |
| H7725 | 41 | 21 596 | 9957 «i», 19770 «7» | 9957/9813/1826 |
| H5920 | 3785 | 37 656 | 8153 «f», 16712 «c», 24866 «c», 34323 «b» | 8153/8559/8154/9457/3333 |

### 5. Adagok

M1 kb. 150 000 karakter, utána kb. 500 000. Szabály: a szócikk a folyó adagba kerül, ha vele
az adag nem lépi túl a célt (különben új adag nyílik); a sorrend nem változik.

| Adag | Szócikk | Karakter | Sorszám |
|---|---|---|---|
| 1 (M1) | 9 | 148 984 | 1–9 |
| 2 | 37 | 495 907 | 10–46 |
| 3 | 81 | 497 174 | 47–127 |
| 4 | 116 | 498 339 | 128–243 |
| 5 | 163 | 499 783 | 244–406 |
| 6 | 242 | 498 550 | 407–648 |
| 7 | 321 | 499 983 | 649–969 |
| 8 | 423 | 499 276 | 970–1392 |
| 9 | 591 | 499 137 | 1393–1983 |
| 10 | 847 | 499 809 | 1984–2830 |
| 11 | 1 173 | 499 684 | 2831–4003 |
| 12 | 1 693 | 499 602 | 4004–5696 |
| 13 | 2 252 | 499 559 | 5697–7948 |
| 14 | 116 | 62 895 | 7949–8064 |

Az M1 kilenc szócikke (TAHOT-gyakoriság / karakter): H9009 (23 943 / 15 815), H9005
(20 806 / 45 414), H9003 (15 766 / 18 043), H0853 (10 945 / 6 621), H3068 (6 528 / 10 103),
H0413 (5 515 / 10 139), H0834 (5 500 / 22 469), H3605 (5 412 / 12 770), H0559 (5 309 / 7 610).

**Eltérés a brief `ir` listájától:** a `naplok/BDB_FORDITAS_M0.py` mérőszkript nincs a listán
(a #34 `naplok/F34_M0_felmeres.py` mintájára készült, csak olvas).
