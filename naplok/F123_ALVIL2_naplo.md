# F123 — az ALVIL-001 új cikkének menetnaplója (U1–U4)

*#123 MIGRACIO2 v2 · ág: `claude/alvil-uj-cikk-b72389` (a `89badc65` main-ről) · 2026-11-02*

## 0. Modell-ellenőrzés

A kért modell (a brief `modell` mezője): `opus`; a session tényleges modellje: `claude-opus-5-5`. **Egyezik**, a munka indulhat (F123.ALVIL2.0).

## U1. Gépi lépések és teljesség-mérés

Napló: `naplok/F123_teljesseg_ALVIL-001.md` (F123.ALVIL2.1). Röviden: a Strong-háló 0 eltérés; a Károli-háló 298 és a szótár-háló 18 eltérése mind olyan vers, amelyben a seól/hádész a Károli alapszövegében nem áll; 8 LXX-többlet; E-vers, amelyet egyik háló sem ad: 0. A korábbi X.A-hoz képest eltérés nincs.

## U2. Döntések átvétele (F123.ALVIL2.2)

**Érvényes, nem kerül újra a felhasználó elé:** a `jeloltek.tsv` ALVIL-001-sorainak döntései; DT-F123d, DT414–DT422, DT498; a Kiadó 28 lektori kérdése alapanyag (`naplok/LEKTOR_ALVIL-001.tsv`), a lektori kártyák lezárása a Kiadó javítása után, külön lépésben (a Kiadóhoz ez a menet nem nyúl).

**A két határdöntés** (a felhasználó, 2026-11-02, ~20:40; DT562):
- `hatar:ALVIL-001:mK1` — Mt 16:18: „Bekerul (Javasolt)”. A jelöltsor `elutasítva` → `beépítve`; az előfordulás-sor az U3-ban, más funkcióval.
- `hatar:ALVIL-001:mK2` — 1Kor 15:55: „Károli (TR) + jelölés (Javasolt)”. A jelöltsor `elutasítva` → `beépítve`; a lap jelöli a kritikai eltérést (θάνατε).
- Az általános szabály (DT563): minden ÚSZ-helyen a Károli alapszövege (TR) a mérce, a kritikai eltérést jelölni kell.

**Új jelöltek a teljesség-mérésből:** 28 `nyitva` sor (18 szótár, 3 Károli-szó, 7 LXX-többlet; a Jób 38:17 a szótár- és az LXX-hálóban is). Kérdés az orkesztrátornak egy üzenetben (2026-11-02), változatokkal és javaslattal; a döntés helye: e napló „U2 — a válasz” pontja.

### U2 — a válasz (2026-11-02, DT564)

Az orkesztrátor döntése a felhasználó 2026-11-02-i felhatalmazásával (»… a döntéseket fogadja, és hozza is meg«), szó szerint: „(a) — mind a 28 elutasítva a negatív kritérium szerint (a seól/hádész nincs a versben a Károli alapszövegében), indoklás-típusonként” · a 295 más szavas eltérés: „lexémánként EGY blokk-sor a `jeloltek.tsv`-ben …, az 1/b-ben pedig lexémánként egy összesítő sor. Rögzítsd DT-F helyőrzővel.” · „ha a kapcsolódó motívumoknál a tartaroó (2Pét 2:4) a MENNY-001/HODIT-001 felé mutat, azt egy mondatban jelezd.”

Végrehajtás (F123.ALVIL2.6): a 28 sor `elutasítva` (szótári összevető hely 18, a Károli más szót fordít 3, a Septuaginta többlete 7); öt blokk-sor (tehóm 33, verem 18, temetkezési sír 68, sírás 130, egyéb 46 vers; a besorolás a vers Strongjai szerint, gépi; lista: `naplok/F123_teljesseg_ALVIL-001_blokkok.tsv`); a 2Pét 2:4 a MENNY-001 felé (Júd 1:6, a vétkes angyalok) egy mondatban a „Miért fontos” résben.

## A negatív kritérium pontosítása (2026-11-02, DT565)

A felhasználó jóváhagyása („mehet”, az orkesztrátor közvetítésével): a `motivumok.tsv` ALVIL-001 `negativ_kriterium` mezője a jóváhagyott szövegre (a közvetített idézetben az ἄβυσσος egy betűje elírt volt; a forrásbeli helyes alak áll); a Kivonat határ-bekezdése ugyanazt mondja: TR-mérce, a kritikai eltérés jelölése (1Kor 15:55), a tehóm mellett az abüsszosz is kizárva. Végrehajtás: F123.ALVIL2.8.
