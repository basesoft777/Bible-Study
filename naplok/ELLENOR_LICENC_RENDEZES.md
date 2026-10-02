# Független ellenőrzés — F33 (tömör változat; az ellenőri jelentés alapján)

*Ág: `claude/f33-licenc-rendezes` · 2026.10.02 · 1. kör: 8 eltérés; a mechanikusak javítva (F33.5).*

| # | Eltérés | Állapot |
|---|---|---|
| 1 | K6/L5: a DT-F24 🟢 marad | felhasználó döntötte, nem hiba |
| 2 | K1/D1: a mérce a forrásrepók saját README-jére is kiterjesztve (BDB, Strong_szotar, OSHL); ellentmond a `adat/SEMA.md` 889–891. sorának | **felhasználói döntés**, nem javítva |
| 3 | BDB `tisztazott`, de a licenc-/megjegyzés-szöveg szerint a formázási réteg nem igazolt | **felhasználói döntés**, nem javítva |
| 4 | TBESG `kereskedelmi=feltetelesen`, a DT-F33a szerint `igen` | javítva (a TBESH marad `feltetelesen`) |
| 5 | elavult megjegyzések: TAGNT/TAHOT/TIPNR („kereskedelmi ezért tisztazatlan”), Strong_szotar, LXX_versszintu_parok/Karoli_versmegfeleltetes („TAHOT (tisztazatlan)”) | javítva |
| 6 | proveniencia-fejlécsorok (3–4. sor) elavult/hiányos | javítva |
| 7 | zárónapló: hiányzik az L0/1 darabszám, a hét README-alapú sor, az `LXX_kivonat` olvasói soronként | javítva |
| 8 | TBESG idézet: „work at␣␣Tyndale House” (dupla szóköz, TBESG.txt:12) | javítva |

**OK pontok:** K2 (a zárónapló számai a táblából), K3 (MCGED bajtazonos), K4 (DT-F33b), a 39 sor/9 oszlop szerkezet, minden `tisztazott` sor `forras_hely`-e idézet+URL+dátum, a nem érintett sorok változatlanok.

**Korlát:** a 7 új külső idézet (BDB, TAGNT, TAHOT, TIPNR, TSK, Macula_gorog, LXX_OS) a helyi repóból **nem volt ellenőrizhető** (külső forrásból valók, 2026-10-02-i lekéréssel); csak a forrás újralekérésével igazolható.

## Kiegészítés — a 2. és 3. eltérés lezárása (DT-F33c, F33.8)

A felhasználó döntött: README csak a JOGTULAJDONOS szó szerinti, a fájlt megnevező/lefedő nyilatkozataként fogadható el. Soronként: BDB, Karoli_1908, Karoli_KH → `tisztazatlan` (kiadás-készítői besorolás); Strong_szotar, OSHL, LXX_OS → `tisztazott` marad (jogtulajdonos README/LICENSE-DATA). Végállapot: 19 `tisztazott` / 20 `tisztazatlan`. SEMA 2.19 2. szabálya kiegészítve. Nyitott megfigyelés (nem javítva): TBESH megjegyzése és KJV_Strongs_teljes besorolása. Az ellenőrző szabály az N-F33b javaslat.

## Kiegészítés — DT-F33d (F33.9)

SEMA `allapot` + `kozkincs` (feltételek: kor, kiadás-azonosítás, a kiadás készítőjének szó szerinti nyilatkozata). KJV_Strongs_teljes → `kozkincs` (eBible copr.htm szó szerint; a Strong-címkék CrossWire-licence nyitott). TBESH → `tisztazatlan`. BDB marad `tisztazatlan`. **Végső arány (a táblából): 17 `tisztazott` / 1 `kozkincs` / 21 `tisztazatlan`.** A korábbi „nyitott megfigyelések” (TBESH, KJV_Strongs_teljes) ezzel lezártak. Az `eszkozok/ellenorzes/` nem ellenőrzi a `licencek.tsv` értékkészletét (a kozkincs elfogadásához eszközmódosítás nem kell).

