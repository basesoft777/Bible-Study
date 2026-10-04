ELTÉRÉS: 5 tétel

# ELLENOR_F22_5Moz.md

*Brief: `F22_KAROLI_STRONG_BRIEF.md` (v2.5, D11) · tartomány: `85d4ac0..48b4c24` (F22.20–F22.21, 9 commit) · worktree `wt-f22-5moz-ellenor`. A `fuggetlen-ellenor` jelentése, csak olvasó szerepben. Saját szkriptet nem futtatott: a számokat a Grep eszköz számláló módjával (ripgrep) igazolta. A fájlt az orkesztrátor mentette. A „Kezelés” oszlop az orkesztrátoré.*

**Minősítés: ELTÉRÉS: 5 tétel (közepes 2, alacsony 3).** A K1/K2, a csak-Sonnet jelölés, a kapuhiba, a régi arany, a változatlanság, a versbeosztás, a kulcs-grep és a zárt adat pontján nincs eltérés.

## Rendben (OK)
- K1/K2: 959 vers (Karoli_1908 `^5Móz`: 959; minta: 959 adatsor; szavak `hu 1` és `er 1` sorszámmal: 959–959); 96 köteg (jsonl `"koteg"` 1–96; az utolsó a 34:4–34:12, 9 vers). Szavak: összesen 45 447. Ebből hu 22 582 (18 516 `parositva`, 4 066 `betoldas`, más állapot 0), er 22 865 = a TAHOT `^5Móz` sorainak száma (22 865), ebből 2 206 `forditatlan`. Üres `strong` az er oldalon 0. Strong-szúrópróba: az 5Móz 12:32 mind a 23 er-tokenje sorrendben egyezik a TAHOT-tal; az 1:1-é is (31 token).
- Csak-Sonnet: parok 23 392/23 392 és szavak 45 447/45 447 sor `alacsony`/`S`. `magas`/`kezi`/`fuggoben` 0 (a 3 „magas” találat a magyar szó: 3:5, 12:2, 28:52). C-jsonl nincs (Glob `**/*5Moz*`: 6 fájl, egyik sem `c/`). A proveniencia-sor `scope=manual … ts=manual`, a `versosszevonas.tsv` helyesen nem szerepel benne.
- Kapuhiba: a jsonl-ben 13 vers `probalkozas: 2` → 13/959 = 1,4%. Minden vers `allapot: ok`, a nem-ok állapotok száma 0 → végleg 0%. Az átnézési fájl csak fejlécből áll.
- Régi arany: a `Karoli_Strong_kivonat` `^Deu.` soraiból 7 van; mind a 7 megtalálható a `parok_5Moz`-ban a várt Stronggal (2:11, 2:20, 3:11, 3:13 H7497; 8:7, 33:13 H8415; 32:22 H7585). A `regi_arany_hibas.tsv`-ben 5Móz-sor nincs.
- Változatlanság: `git diff --stat 85d4ac0..48b4c24 -- f21p/ parok_/szavak_1–4Moz f22/valaszok/c f22/versosszevonas.tsv f22/versmegfeleltetes.tsv` üres. A `48b4c24..HEAD` szakaszban is csak a SEMA és a datasetek változott (F33/F46).
- Versbeosztás: a `F22_versbeosztas.md` szerint az 5Móz 959/959 vers, 34 fejezet, minden fejezetben 0/0/0. A `versmegfeleltetes.tsv`-ben és a `versosszevonas.tsv`-ben 5Móz-sor nincs. A `VERSBEOSZTAS_JOVAHAGYOTT = ('2Móz','3Móz','4Móz','5Móz')`, a jóváhagyási naplóban van 5Móz-sor. Ismert versbeosztási határok (12:32/13:1, 22:30/23:1, 29:1/28:69): a Károli is és a TAHOT-kivonat is angol számozású. `lekerdez.py karoli "5Móz 12:32"`, `"5Móz 22:30"`, `"5Móz 29:1"` szövege tartalomra egyezik a TAHOT-sorokkal. Eredeti nélküli Károli-vers: a mintában 0, a `F22_nincs_parja_versek.tsv`-ben 5Móz 0.
- Kulcs-grep és zárt adat: `git log -G "sk-or-v1|sk-ant-|AIza…|ghp_…|api_?key" 85d4ac0..48b4c24` → 0 commit. `git log -G "Karoli_Strong_zart|zart_forras|<S>[0-9]"` → 0. Új fájl csak a 11 felsorolt (numstat).
- datasetek: mind a 8 sor (4 study-típus × parok/szavak) bővült az 5Mózzel és a jelentés hivatkozásával.
- A jelentés számai egyeznek a táblákkal: 23 392 / 45 447 / 959 / 96 / 13 / 7/7.
- CI (`futtat.py --valtozott <11 fájl> --diff-alap 85d4ac0 --diff-fej 48b4c24`): E2–E16 és E19 egyaránt 0 találat.

## Táblázat

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| K1 versek/kötegek | OK | `f22/minta_5Moz.tsv`, `f22/valaszok/sonnet/5Moz.jsonl` | Grep count `^5Móz \d+:\d+\t` Karoli_1908: 959; minta: 959; jsonl `"koteg": N`: 1–96 |
| K1 tokenek | OK (er) · NEM ELLENŐRIZHETŐ (hu, egyszeri szereplés) | `adat/karoli_strong/szavak_5Moz.tsv` | er 22 865 = TAHOT `^5Móz` 22 865. A hu 22 582-t a `tokenek.py` nélkül nem lehet a Károlival összevetni; a „pontosan egyszer” az `egyesit.py --ellenoriz` futtatása nélkül nem igazolható |
| K2 Strong | OK (szúrópróba) | `szavak_5Moz.tsv:18649–18671` | Az 5Móz 12:32 23 er-tokenje = TAHOT 440116–440138. Üres er-strong 0. A parokban nem `H`-val kezdődő strong 0 |
| K3 hash | NEM ELLENŐRIZHETŐ | — | `git diff f21p/` üres; a kötegenkénti ellenőrzésnek nincs nyoma, amit ellenőrizni lehetne |
| K4 jelentés tartalma | OK | `naplok/F22_5Moz_jelentes.md:14-24` | kapuhiba, arány, régi arany, `/usage` benne van; C-költség n.é. (nincs C) |
| K5 C-költség | n.é. | — | nincs C-futás |
| K6 zárt adat | OK | — | `git log -G` → 0; új fájl csak a 11 felsorolt |
| K7 újraépítés | NEM ELLENŐRIZHETŐ | — | az `egyesit.py` futtatása a szerepkörön kívül esik |
| K8 ELLENOR TISZTA + CI | ELTÉRÉS | — | l. 1. tétel |
| K9 SEMA/datasetek | ELTÉRÉS (SEMA) · OK (datasetek) | `adat/SEMA.md:937` | l. 2. tétel |
| csak-Sonnet jelölés | OK | parok/szavak | 23 392 és 45 447 sor `\talacsony\tS$`; `kezi`/`magas` 0 |
| kapuhiba | OK | jsonl 7,9,30,31,35,40,44×2,47,52,62,74,81. sor | `"probalkozas": [2-9]` → 13; nem-ok állapot 0 |
| régi arany | OK | `parok_5Moz.tsv:1314,1488,2138,2216,6120,22008,22861` | 7 `Deu.`-sor → 7 találat |
| D1, D6, D7, D11 | OK | brief D11 | a fentiek szerint |
| D4 / /usage 76→84% | NEM ELLENŐRIZHETŐ | jelentés 10. sor | `get_usage`-kimenet nincs a repóban |
| D2, D3, D5, D8 | n.é. | — | csak Sonnet, nincs eltérés-típus, a próbaszakasz és a C csak az 1–2Mózre vonatkozott |
| A1 | OK | proveniencia-sorok | `scope=manual`, `ts=manual`, „javaslat, nem lekérdezés” |
| A2 | ELTÉRÉS | `naplok/F22_5Moz_jelentes.md:32` | l. 4. tétel |
| A3–A5 | n.é. | — | nincs tanulmány-, Remez/Sod- és tanítótartalom |
| A6 | OK | — | E12–E15: 0 találat, nincs megítélendő figyelmeztetés |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | — | CI-jelentést nem kaptam. A saját futtatásom: E2–E16 és E19 0 találat; E17 és E18 nem szerepel a kimenetben |
| ⛔ pontok | ELTÉRÉS | brief 122., 126. sor | l. 1. tétel |
| Ellenőrzőlista 1. kiszűrt/törölt sorok | OK | numstat | A törölt sorok mind cserék: brief 3, SEMA 1, datasetek 8, tokenek.py 1. Adatsor-törlés 0, kiszűrt TAHOT-token 0 (er = TAHOT). A hu oldali szűrés (írásjel) NEM ELLENŐRIZHETŐ |
| Ellenőrzőlista 2. kulcstartomány | OK | — | 34 fejezet, 959 vers mind jelen; minden er-tokennek van Strongja |
| Ellenőrzőlista 3. nulla-diff hatóköre | OK | — | Üres a diff: `f21p/`, az 1–4Móz táblái, `f22/valaszok/c`, `versosszevonas.tsv` és `versmegfeleltetes.tsv`, mindkettő a tartományban. Nem vonatkozik: a SEMA és a datasetek `48b4c24..HEAD` közötti változására (F33/F46) |
| Ellenőrzőlista 4. táblák Δ-ja (fejléc nélkül) | OK | numstat | `parok_5Moz.tsv` +23 392 (új; +2 sor proveniencia+fejléc), `szavak_5Moz.tsv` +45 447 (új), `datasetek.tsv` Δ 0 (8 csere), `konkordancia/*.tsv` Δ 0. Bontás: a jelentés 2. szakasza (mind `alacsony`/`S`). A hu/er és állapot szerinti bontás csak itt szerepel: hu 18 516 + 4 066, er 20 659 + 2 206 |
| Ellenőrzőlista 5. ⛔ | ELTÉRÉS | — | 1. tétel |

## Eltérések és Kezelés
| # | Eltérés | Kezelés |
|---|---|---|
| 1 | (közepes) ⛔ 2. megállás / 22.7 / K8: merge előtt nem futott független ellenőri kör. A `48b4c24` a PR #139-cel (`ef1e545`) került a main-be, a `ELLENOR_F22_5Moz.md` nélkül, és a jelentés sem említi az ellenőri kört. Ezt a kört utólag pótolja. | Utólag pótolva ezzel a jelentéssel (`claude/f22-5moz-ellenor`, F22.22–F22.23). |
| 2 | (közepes) SEMA 2.20 (`adat/SEMA.md:937`, a HEAD-en is): a „Csak-Sonnet könyv” felsorolás még „3Móz és 4Móz”, a `parok_5Moz.tsv`/`szavak_5Moz.tsv` sehol sincs megnevezve. A diff csak a jóváhagyott listát bővítette. | Javítva (F22.24): a 2.20 bekezdés „első öt könyv”, a csak-Sonnet felsorolásban az 5Móz és a két tábla, hivatkozással a jelentésre. |
| 3 | (alacsony) A `48b4c24`-en a brief ellentmondott magának: a `kovetkezo` és a jelentés szerint „DT-F22c: lezárva”, a D9 szerint „nyitva”, és a DONTESEK.md-ben nem volt DT-F22c ✅ sor (a `281388d` nem őse a `48b4c24`-nek). | A main-en rendezve (DONTESEK DT-F22c ✅, a D9 a HEAD-en „lezárva”); csak rögzítendő. |
| 4 | (alacsony) A2: a jelentés 4. szakasza („Push és PR nem készült”, „a #114 és a #131 merge-e után”) már nem nyitott. A `#139` merge-ölve, a `#114` is; a `#131`-nek a main-en nincs merge-commitja. | Javítva (F22.24): a PR-pont áthúzva, „Lezárva” megjegyzéssel (PR #139, PR #160). |
| 5 | (alacsony) A brief `ir:` listájában nincs `naplok/ELLENOR_F22_5Moz.md` (a 4Móz-menet a sajátját felvette); a HEAD-en is hiányzik. | Javítva ebben a menetben (F22.23). |

**Nem ellenőrizhető:** `egyesit.py --ellenoriz` és K7, a hu-tokenek egyszeri szereplése, a K3 kötegenkénti hash-ellenőrzése, a `/usage` 76→84% (és az 5 órás ablak 9→74%), a 70%-os indítási szabály felhasználói jóváhagyása („1”), a CI-jelentés egyezése (CI-jelentést nem kaptam).
