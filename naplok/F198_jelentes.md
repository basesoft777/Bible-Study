# F198 — A nyílt mag és a hatástörténet: jelentés

*Modell: claude-sonnet-5-5 · 2026-11-11 · ág: `claude/brave-allen-7b2eb6`*

## Mi készült

A nyílt mag (`nyilt_mag/`) négy új táblát kapott a #690-nel bekerült visszhang-adatból, forrásonként licenccel:

| Tábla | Sor | Forrás (licenc) | Mi kerül be |
|---|---|---|---|
| `visszhang_megfelelok.tsv` | 101 | Targum (közkincs), Vulgata (közkincs), LXX (CC BY 4.0, LXX_OS) | a láncszavak megfelelője a versben: alak, lemma, kiejtés, jelentés, betoldás, megjegyzés |
| `visszhang_tanuk.tsv` | 6 | HCF-metaadat (közkincs-dedikáció), Sefaria (CC BY), Glossa Ordinaria (közkincs) | tanú, mű, kor, egy saját szavas mondat; idézet nincs |
| `vitatott_forrasok.tsv` | 3 | a lektorált kiadvány bibliográfiai adata | szerző, cím, megjelenés, DOI; összefoglaló nincs; a 2 hiány-sor üres szerzővel |
| `sblgnt_apparatus.tsv` | 61 | SBLGNT-apparátus (CC BY 4.0) | az apparátus-jegyzetek a motívumok újszövetségi igehelyeire |

Minden tábla: kódkönyv-sor (79 új sor az `adat/nyilt_kodkonyv.tsv`-ben), OSIS-pár az igehelyhez, `…_en` címke a zárt oszlopokhoz, gépi angol pár a szabad szöveghez (91 egyedi szöveg, `adat/nyilt_angol.tsv`), OLVASSEL/README-szakasz a forrásmegjelölésekkel, ellenőrző összeg. A `forrasok_es_licencek.tsv`-ben a hét használt forrás „forrás” szerepű lett.

## Mi nem került be, és miért

- **Chain Lineage-tanú** (nincs licenc; a felhasználó: „ez most így marad”): az exportáló nem veszi át (4 sor), a kapu új `VISSZHANG` ellenőrzése bukik, ha bármely cellában a neve, a végpontja vagy a BiblIndex szerepel.
- **`bdb` megfelelő-sor** (31 sor: 19 ellenőrzött, 12 ellenőrizetlen): nincs a jóváhagyott listán (DT778, N157).
- **Ellenőrizetlen sor** (1 `lxx`; a 12 `bdb` fent): a lapon sem renderel.
- **A vitatott források összefoglaló-szövege** (DT779): az absztrakt licence forrásonként eltér.
- **HCF GitHub-URL** (1 sor): a csomagban a GitHub-hivatkozás tiltott (KANONIKUS); a sor `forras_url`-je üres, a forrás megnevezése áll.
- A `megjegyzes`-ből a munkaközi ellenőri jelölések (`[ellenőri …]`, `[lemma megerősítve …]`) kimaradnak; hat LXX-sor „fordításra vár” jelentése üres marad (hiány, nem kitöltve).

## Licenc: két figyelmeztetés

1. **LXX-sorok.** A kinyerés a szó kiválasztásához a `LXX_versszintu_parok`-at (a zárt, származtatott réteg) is használta; a csomagba a kiválasztott szó (egy vers egy tényszava) és a CC BY LXX_OS szövegéből való alak megy, `forras_licenc` = CC BY 4.0. Ezt a felhasználónak kell megerősítenie (DT778). Ha nemet mond, az `lxx` kivétele egy sor az exportálóban.
2. **A vitatott források bibliográfiai adata** OpenAlexből és Crossrefből való; a `licencek.tsv`-ben ehhez nincs sor, ezért a táblának nincs `forras_licenc` oszlopa: a szerző, a cím és a DOI tényadat, szöveg nincs benne. A licenc-leltár bővítése külön tétel lehet (N158 javaslat).

## Kapuk

- Nyílt mag kapuja (E35, `nyilt_mag_kapu.py`): **0 BUKÁS**, 60 FIGYELMEZTETÉS (mind a már meglévő; a #198 egyet sem ad: 21 `nincs fordítás` a kizárásoknál, KJV-említések, 1 ARANY-adat hiány).
- Új kapu-ellenőrzés: `VISSZHANG`; a `URL_OSZLOP` kivétel a snake_case-mintára (URL-ekben `by_father`).
- ARANY: a Targum, a Vulgata, a Glossa és az SBLGNT 0 tétellel, 0,00% (az arány-kapu csak az `elofordulasok.tsv`-t számolja; ezek a táblák nem abba írnak).
- A lap (`lexikon/`) és az olvasói kapu nem változott (a diff csak az `ir` fájlokat érinti).

## Ellenőri javítókör (ELTÉRÉS 10 tétel, egy kör)

- Számütközés: a #688 már F197-et foglalt; a feladat F198-ra, a helyőrzők DT778/b-re, N157/b-re számozva.
- SBLGNT: a tartomány-igehelyek (pl. Gal 3:13-14, Zsid 6:7-8) versenként illesztve; a jegyzetek száma ennek megfelelően nőtt.
- „Ellenőrzött”: az LXX-sorok 27-ét gépi ellenőrzés hagyta jóvá (egyetlen lemma a versben), nem második kéz; az OLVASSEL/README ezt kimondja.
- Angol pár: az Efrém-sor és az „átkozta (őt: a földet)” javítva.
- Kódkönyv: az SBLGNT `igehely_osis` a forrás saját számozását mondja; a teljes SBLGNT-megjelölés az OLVASSEL/README-ben áll.
- DT779 🟡-re (a felhasználó dönt); N158 felvéve (OpenAlex/Crossref licenc-sor).
- Nyitva marad, jelezve: a HCF-metaadat jogi átnézése kereskedelmi kiadás előtt (`licencek.tsv`); a kapu `minden jog fenntartva` címkét nem tilt a hatástörténet-táblákban (a `forrasok_es_licencek` kapu azt a kizárásnál fogja).
