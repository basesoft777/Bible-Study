# Olvasói kapu — a gépi hibaosztályok javítása (OLVJ, 2026-11-02)

*Végrehajtó: `claude-sonnet-5-5` (kért: sonnet; egyezik). Tételek: OLVJ.1–5. Bemenet: `naplok/OLVASOI_KAPU_jelentes.md`, `naplok/OLVASOI_KAPU_meres.md`.*

## 1. Eredmény

A kapu 675 BUKÁS-t mért a 9 lapon. A próza nélküli, gépi osztályok javítása után **598**; a három, a mai generátorral
egyforrású lapon (ISTENTISZT-001, ALVIL-001, TEREMT-002) újragenerálva, a hat régi sablonú lap érintetlen (l. 3.).

| Osztály | előtte | utána | Mi történt |
|---|---|---|---|
| BELSO | 131 | 102 | 1/b. tábla, „Negatív kritérium”, hiányjelzések olvasói alakra (OLVJ.1); a maradék kézi próza és régi lapok |
| ANGOL | 57 | 49 | `(was called)`, `scan`, `study`, `LXX_OS` az indoklásban és a generált mondatokban (OLVJ.1) |
| IDEZOJEL | 52 | 38 | egyenes `"` → „…” a kész lapon (OLVJ.2); a maradék a hat régi lapon |
| KONYV | 38 | 28 | könyvrövidítés a normalizáló tábla alakjára (OLVJ.2); a maradék 27 a régi lapokon (HAMART 29), 1 ALVIL („De”) |
| KOLOFON | 27 | 19 | „nincs kiadva — feldolgozás alatt” a Kiadás / Próza modellje / Változásjegyzék helyén (OLVJ.3); a maradék a régi lapokon |
| BDB_JEL | 9 | 2 | `^`, `,,`, rafe (OLVJ.4); a maradék a nyers forrás torz átírása |
| ATIRAS | 18 | 17 | a JHVH/Jahve egységesítés (OLVJ.4); a többi választást kíván |
| ZAROJEL | 3 | 3 | szakaszhatáron csonkult BDB-mondat: nem javítható találgatás nélkül |
| PROZA_1A, IDEZET, PONT, FUNKCIO_URES | 340 | 340 | nem ennek a menetnek a feladata (az új cikkek prózájával jönnek) |
| **összes** | **675** | **598** | |

| Lap | előtte | utána | újragenerálva |
|---|---|---|---|
| ISTENTISZT-001 | 61 | 24 | igen (1. kiadás: a 2. kiadás függő változása, l. 4.) |
| ALVIL-001 | 145 | 120 | igen |
| TEREMT-002 | 32 | 17 | igen |
| ANTROP-001 | 37 | 37 | nem |
| HAMART-001 | 118 | 118 | nem |
| HODIT-001 | 78 | 78 | nem |
| KIRALY-001 | 50 | 50 | nem |
| MENNY-001 | 45 | 45 | nem |
| TEREMT-001 | 109 | 109 | nem |

## 2. Hibaok-lánc osztályonként

| Osztály | Nyers forrás | Konverzió / generátor | Megjelenítés (javítva itt) |
|---|---|---|---|
| BELSO/ANGOL (1/b.) | `adat/jeloltek.tsv` `indoklas`: a munkafolyamat naplója (DT-szám, orkesztrátor, angol címke) | `szerep_kizart.blokk_torzs` az `indoklas`-t szó szerint a cellába tette | `szerep_kizart.olvasoi_indok`: az olvasói ok marad, a nyers szöveg a lábjegyzetben; adat nem változik (DT28) |
| IDEZOJEL | vegyes: kézi rések, `jeloltek.tsv`, szótári fordítás | — | `olvasoi_utofeldolg.idezojel` a kész lapon (egy helyen, idempotens) |
| KONYV | a források saját rövidítései (Csel, Ésa, Ezék, Mát, Zef …) | — | `olvasoi_utofeldolg.konyv`; szó szerinti angol sor és a „BDB-ben: „…”” hely nem változik |
| KOLOFON | `adat/kiadasok.tsv`: kiadott lapnak van sora, a többinek nincs | `kolofon_kiadas_sorok` üres listát adott | „nincs kiadva — feldolgozás alatt” (nem kitalált adat) |
| BDB_JEL | `DictBDB.json`: `<sup>…</sup>` | `konkordancia/_convert_bdb.py:11`: `<sup>` → `^` | `olvasoi_utofeldolg.bdb`: `^` → szóköz, `,,` → `,`, rafe elhagyva |
| ATIRAS (JHVH) | — | `heber_kiejtes` R6 (Jahve) a Jelmagyarázatban | a Jelmagyarázat és a héber rövidítések címe JHVH |

**KONYV, a szótári idézet:** a BDB/Thayer szó szerinti angol sora (≥ 3 angol funkciószó) és a „BDB-ben: „Gen 3:14”” alak
nem változik. A lap saját magyar fordításában álló rövidítés (pl. HAMART szótári sorai) változik. A mért maradék 28
KONYV-tétel döntő része (HAMART 29 előfordulás-tétel) a hat régi lapon áll, amelyeket nem generáltam újra.

## 3. Mi nem készült el, és miért (⛔ az orkesztrátornak)

1. **A hat régi sablonú lap (ANTROP, HAMART, HODIT, KIRALY, MENNY, TEREMT-001) nincs újragenerálva.** A lapjuk a régi
   generátorral készült; a mai generátor helyben-frissítése (`--ir`) 760–3 190 sornyi szerkezeti változást hoz (új „Mit
   mutat ez a rész?” bevezetők, új szakaszok, a Jelmagyarázat bővülése), nem csak formahibát javít. Próbában (nem
   commitolva) a hat lap BUKÁS-a 437 → 363, a FIGYELMEZTETÉS nő. A javításuk az új cikkekkel együtt értelmes; a
   kérdés: kéri-e a felhasználó mégis a helyben-frissítést a régi lapokra? A kapu mérése addig a régi állapotot mutatja.
2. **ATIRAS: tohu/tóhú (TEREMT-002), hádész/hadész (ALVIL-001).** A kézi forrás *tohu*, *bohu*, *hádész*; a gépi
   kiejtés (zárójelben) tóhú, bóhú, hadész. Az egység választás kérdése (a kézi próza átírása, vagy a gépi szabály):
   a forrás szavait nem írtam át.
3. **Torz átírás a nyers forrásban:** `She®°ôl` (ALVIL), `†or°¹n` (ISTENTISZT) a `DictBDB.json`-ban is így áll; a
   helyes alak csak találgatható, ezért nem javítottam. Csonkult zárójel a BDB-szakasz határán (ISTENTISZT 2 db,
   TEREMT-002 1 db): a mondat a következő szakaszban folytatódik.
4. **Kézi forrásban álló BELSO/ANGOL tételek** (6., 6/b., 7. szakasz, Kivonat, `elofordulasok.tsv` kapcsolódás-szöveg
   egy sora): a motívum prózájának része, az új cikkel együtt íródik át (a három újragenerált lapon a mért maradék: `olvasoi_kapu.py ID --reszletes`).

## 4. Az ISTENTISZT-001 (1. kiadás) változása

A lap a 2. kiadás függő változása (N85): `naplok/OLVJ_ISTENTISZT_lapdiff.md` (szó szerinti diff, 196 cserélt sor:
73 idézőjel, 31 könyvrövidítés, 26 belső jelölés az 1/b.-ben, 66 egyéb forma). Tartalmi állítás nem változott.

## 5. Ellenőrzés

- `python eszkozok/olvasoi_kapu.py --osszes`: 598 BUKÁS (előtte 675).
- `ellenoriz.py`: 0 SÉRTÉS. A 11. szabály (rés-forrás egyezés) az egységesítés előtti és utáni lapot is elfogadja
  (`ellenoriz.res_egyezik`), ezért a hat nem újragenerált lap nem sérti.
- Feed 3. kapu (nulla-diff) a három újragenerált lapon: l. a PR leírását.
- Új tesztek: `teszt_olvasoi_utofeldolg.py` (15), `teszt_szerep_kizart.py` `TestOlvasoiIndok` (8).
- Bukó tesztek, amelyeket nem ez a menet okozott (a hibaüzenet az ISTENTISZT-001 mai adatszámát várja másnak: 22 ≠ 33 sor, 13 ≠ 14 mondat): `teszt_szotari_gerinc` (5), `teszt_szerepmatrix` (3). A teljes futás eredménye a PR leírásában.
