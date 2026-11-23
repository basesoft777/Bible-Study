# F239 átadó — U2 (határ és érvvázlat) → U3 (próza, egy Opus-menetben)

*2026-11-23 · író: `claude-opus-5-5` · ág: `claude/nervous-kare-9d2361` (PR #820). Az U3 új Opus-sessionben indul ebből a jegyzetből és a brief U3-szakaszából (`F239_TEREMT001_CIKK_BRIEF.md`).*

## Mi kész, hol áll

| Mi | Hol |
|---|---|
| A határ: a négy ID-kérdés, a kizárások (K1–K6), a nehéz esetek (B1–B5), a mező-hipotézis, a határ-ellenőrre adott válaszok | `naplok/F239_hatar.md` |
| A határ-ellenőr öt kérdése (második vélemény) | `naplok/HATAR_TEREMT-001.md`, Modelles rész |
| Az érvvázlat: A lexikai alap (A1–A7), B láncbeli szerep (B1–B9), C vitatott pontok (V1–V6), D válasz a bírálatra | `naplok/ERVNAPLO_TEREMT-001.md` |
| A bírálat | `naplok/BIRALAT_TEREMT-001.md` |
| A lépésnapló, a döntések indokkal | `naplok/F239_naplo.md`; a döntések: `dontesek/uj/nervous-kare-9d2361.md` |
| Adat | `adat/jeloltek.tsv`: a TEREMT-001 előfordulás-jelöltjei: beépítve 42, elutasítva 32, nyitva 0 (javaslat, a szerkesztő döntésére vár). `adat/elutasitasi_okok.tsv` +2 (TEREMT-001 101, 102). A seól-kapcsolat és a Nave-sorok nincsenek az adatban (az F239.5 felvette, az F239.6 kivette; a szerkesztő szavára várnak). |

## Az U3 bemenete (ezt olvasd)

1. Ez a jegyzet és a brief U3-szakasza.
2. `naplok/ERVNAPLO_TEREMT-001.md` teljesen: a próza ehhez mér (az „eldöntve” pontokat a lap kimondja, a „nyitva” pontok a Vitatott pontok közé kerülnek mindkét olvasattal, a „kimarad” állítás sehol nem áll).
3. `naplok/F239_hatar.md` 1. és 6. pontja (a határ szövege a lapra; a K2-válasz U3-feladata).
4. Az adattáblák TEREMT-001 sorai (`elofordulasok.tsv` 42 sor, a `funkcio` mezőkkel), a bizonyítéklap versenként (`naplok/BIZONYITEK_TEREMT-001.md`).
5. A sablonok: `sablonok/10_PaRDeS_U3_proza_prompt_sablon.md`, `sablonok/9_PaRDeS_motivum_forras_sablon.md`; a HAMART-001 mintalapból csak a Kivonat-bekezdés és 2–3 arany 1/a-tétel.

## Mit NEM kell elolvasni

A régi tanulmány egészét (`tematikus_lezart/Tehom_tematikus.md`: alapanyag, mondat nem költözik belőle; ha kell, csak a 3. szakasz), az U1 nyers kimeneteit (`…_lekerdezesek.txt`, `…_felmeres_kiserok.tsv`, `…_igealak.tsv`), a `…_teljesseg.tsv`-t (224 sor; a döntés megvan), a határ-ellenőr és a bíráló teljes jelentését (a válaszok az érvnaplóban és a határ-fájlban).

## Az U3 kötelező elemei (az U2-ből)

- **A határ olvasói mondata** (a határ-ellenőr K2): a Kivonat vagy a Módszertan kimondja, hogy a Károli „mélység” szava nem jelzi a tehómot (a motívum verseiben „tenger”, „víz”, „örvény” is; 95 más versben a „mélység” más szót fordít), és a két szomszéd pár (Jón 2:4 és 2:6; Jób 41:31 és 41:32) példaként áll.
- **A Septuaginta szerepe**: híd, nem hordozó; az ÚSZ ἄβυσσος-a tágabb a tehómnál (érvnapló A3–A4).
- **A seól-motívum** kapcsolódó motívumként, ha a szerkesztő így dönt (kérdéslista 7. pont; az Ez 31:15 a közös vers); a tohu va-vohu (1Móz 1:2) csak a prózában.
- **Számok a mai adatból**: 35 héber vers, 36 előfordulás; 9 újszövetségi vers; a régi tanulmány számai (35-ször, 34 vers) elavultak (N58: a régi tanulmány archiválásával zárul, a régi szöveget nem javítjuk).
- **Az 1/a minden igehelye** kerek mondat + „Funkció:” sor; belső jel (DT-, N-, F-szám, `.tsv`, „gerinc”) az olvasói rétegben nincs.

## Az U3 technikai teendői (az U1–U2-ből)

- `adat/res_forras.tsv`: a 9 sor a `motivumok/TEREMT-001.md` kézi forrásra kötve (a `kivonat` sor most B47-et ad), az `alkalmazas` sor kivezetve (DT756).
- `adat/jeloltek.tsv`: a Jób 41:32 sor `forras_kereses`-e a régi `scan H8415` alak (a TEREMT-002-n B04-et adott): az új generátor futása előtt az elfogadott alakra.
- A négy kiválasztott Nave-téma (PIT, EARTH, DEW, PSALMS) magyar neve az `adat/nave_tema_hu.tsv`-ben még nincs (`glossza_lexikon_forditas.py nave`).
- A fordítás-lista (U1 7. pont) a befagyasztás miatt nem készült: az új generátor `--kimenet`-es próbafutásakor pótlandó.
- A régi tanulmány, a KH-napló, a régi `motivumok/TEREMT-001.md` és a törzscikk `archivum/TEREMT-001/` alá, ARCHÍV fejléccel; a hivatkozások ugyanabban a commitban (E27).
- Az U1b (visszhang 1–2, Sonnet + másik kéz) a lánc véglegesítése után futhat: a lánc-szavak H8415 és G0012, a láncversek a 42 beépített sor (a Jel 20:1–3 sorsa a DT-F239d szerint).

## Nyitott döntések (a szerkesztőnél: `naplok/F239_szerkeszto_kerdesek.md`)

A határ egésze (`naplok/F239_hatar.md`, a 28 jelölt döntése) javaslat, a szerkesztő döntésére vár; az U3 csak a döntés után indulhat, és ha a szerkesztő eltér, előbb a határ és az adat igazodik. A seól-kapcsolat és a Nave-sorok a szerkesztő szava után a `naplok/F239_U2_dontesek_ir.py`-vel kerülnek be (a fejlécben álló teendővel); a kritérium-szöveg (2. pont) és a Jel 20:1–3 (6. pont) döntése az adatban még nincs alkalmazva.
