ELTÉRÉS: 1 tétel

# ELLENOR_F22_Jozs.md

*Brief: `F22_KAROLI_STRONG_BRIEF.md` (v2.6, D12) · tartomány: `24f39d4..93f5e17` (F22.25–F22.27, 9 commit, 11 fájl) · worktree `wt-f22-jozs`, ág `claude/f22-jozs`. A `fuggetlen-ellenor` jelentése, csak olvasó szerepben készült. Bash-sel csak `git diff`, `git log`, `lekerdez.py` és `futtat.py` futott. A számokat a Grep eszköz számláló módjával (ripgrep, soronként, a `csv` modul nélkül) igazolta. Saját szkriptet nem futtatott. A fájlt az orkesztrátor mentette, a „Kezelés” oszlop az orkesztrátoré.*

**Minősítés: ELTÉRÉS: 1 tétel (közepes 1).** Ezeken a pontokon nincs eltérés: K1/K2 lefedettség és szúrópróba, csak-Sonnet jelölés, kapuhiba, régi arany, az 1–5Móz és az `f21p/` változatlansága, versbeosztás és jóváhagyási napló, kulcs-grep, zárt adat, datasetek, a brief `ir:` mezője, a jelentés számai és a CI. Az eltérés a SEMA 2.20 jóváhagyott-könyv felsorolása.

## Rendben (OK)
- **K1 versek és kötegek:** a Karoli_1908 `^Józs \d+:\d+\t` sorainak száma 658. A `minta_Jozs.tsv` 658 adatsort tartalmaz. A `szavak_Jozs.tsv`-ben `hu 1` és `er 1` sorszámmal 658–658 sor van. A jsonl `"koteg"` értékei 1–66. Az utolsó köteg (66. sor) a Józs 24:26–24:33, azaz 8 vers (65×10+8 = 658).
- **K1 tokenek:** a `szavak_Jozs` 30 405 sor, mind `\t(hu|er)\t`.
  - hu oldal: 14 668 sor, ebből 12 155 `parositva` és 2 513 `betoldas`. Más állapot nincs (12 155+2 513 = 14 668).
  - er oldal: 15 737 sor, ebből 13 822 `parositva` és 1 915 `forditatlan`. Ez megegyezik a TAHOT `^Józs` sorainak számával (15 737).
  - Üres `strong` az er oldalon: 0. `+1000`-es ál-kulcs (`:\d{4}\t`): 0.
  - Versenkénti szúrópróba (hu = minta `karoli_szo`, er = minta `eredeti_szo` = TAHOT): 1:1 18/18 és 18/18; 15:63 23/23 és 27/27/27; 24:33 21/21 és 21/21.
- **K2 Strong:** a Józs 1:1 mind a 18 er-tokenje (TAHOT 118689–118706) és a 24:33 mind a 21 er-tokenje (TAHOT 134405–134425) sorrendben és Stronggal egyezik. A parokban nem `H`-val kezdődő strong: 0.
- **Csak-Sonnet:** a parok 15 023/15 023 sora és a szavak 30 405/30 405 sora `\talacsony\tS$`. `magas`/`kezi`/`fuggoben` mezőérték mindkét táblában 0. C-jsonl nincs: az `f22/valaszok/c/` alatt csak 1Moz, 2Moz és 2Moz_javito van. Mindkét tábla proveniencia-sora `scope=manual | … | ts=manual`, „javaslat: nem lekérdezés-eredmény” megjegyzéssel. A `versosszevonas.tsv` helyesen nem szerepel benne.
- **Kapuhiba:** a vers szintű `"probalkozas": 2` 6 versnél fordul elő: 3:14, 4:18, 6:9, 7:1, 8:24 és 20:9 (jsonl 6., 8., 11., 13., 18. és 53. sor). 6/658 = 0,9%. Nem-`ok` vers-állapot: 0, tehát végleg 0%. A `F22_Jozs_atnezes.tsv` csak fejlécből áll.
- **Régi arany:** a `Karoli_Strong_kivonat` `^Jos` soraiból 5 van (12.4, 13.12, 15.8, 17.15, 18.16, mind H7497). Mind az 5 megvan a `parok_Jozs`-ban H7497-tel (7374., 7866., 8894., 10073. és 10615. sor). Az `f21p/regi_arany_hibas.tsv`-ben Józs-sor nincs.
- **Változatlanság:** a `git diff --stat 24f39d4..93f5e17 -- f21p/ parok_/szavak_1–5Moz f22/valaszok/c f22/versosszevonas.tsv f22/versmegfeleltetes.tsv konkordancia/` parancs kimenete üres.
- **Versbeosztás:**
  - Detektor (`naplok/F22_versbeosztas.md:18`): Józs 658/658 vers, 24 fejezet, 0/0/0/0. A 299–322. sor szerint mind a 24 fejezetben eltolt, K-hiány és E-hiány egyaránt 0.
  - A `versmegfeleltetes.tsv`, a `versosszevonas.tsv` és a `F22_nincs_parja_versek.tsv` egyikében sincs Józs-sor.
  - A `tokenek.py:55` értéke `('2Móz','3Móz','4Móz','5Móz','Józs')`. A jóváhagyási napló új Józs-sora egyezik a detektorral (658/658, 24 fejezet, 0/0).
  - A Józs 21:36–37 ismert MT-problémája itt nem jelentkezik: a TAHOT-ban 33 tokenje van, köztük H1221 Bezer és H3096 Jahaz (21:36), H6932 Kedemoth és H4158 Mephaath (21:37). A `lekerdez.py karoli "Józs 21:36"` és `"Józs 21:37"` tartalomra ugyanezt adja.
- **Kulcs-grep és zárt adat:** a `git log -G "sk-or-v1|sk-ant-|AIza…|ghp_…|api_?key" 24f39d4..93f5e17` és a `git log -G "Karoli_Strong_zart|zart_forras|<S>[0-9]"` egyaránt 0 commitot ad. Új fájl csak a name-status 7 `A` sora.
- **datasetek:** 8 `Karoli_Strong_(parok|szavak)` sor van, és mind a 8 illeszkedik a `5Móz és Józs … Józs csak Sonnettel` mintára. A parok-sorok a `F22_Jozs_jelentes.md`-re is hivatkoznak.
- **SEMA 2.20 csak-Sonnet felsorolás:** a felsorolás bővült a Józs-sal és a két táblával. (A jóváhagyott lista nem bővült, l. 1. tétel.)
- **A brief fejléce:** az `ir:` mező mind a 10 írt fájlt tartalmazza, és a `naplok/ELLENOR_F22_Jozs.md`-t is. Az `allapot: fut`, az `ag: claude/f22-jozs`, a `kovetkezo` mező és a D12, v2.6 sor is jelen van.
- **A jelentés számai** egyeznek a táblákkal: 658 / 66 / 8 / 6/658 / 15 023 / 30 405 / 14 668 (12 155 + 2 513) / 15 737 (13 822 + 1 915) / 5/5 / `magas` 0. A „PR #160 merge-e után” is stimmel: a `24f39d4^` = `e82e7ca` (Merge PR #160).
- **CI:** saját futtatás, `futtat.py --valtozott <11 fájl> --diff-alap 24f39d4 --diff-fej 93f5e17`. Az E2–E16 és az E19 egyaránt 0 találat.

## Táblázat

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| K1 versek/kötegek | OK | `f22/minta_Jozs.tsv`, `f22/valaszok/sonnet/Jozs.jsonl` | Grep count `^Józs \d+:\d+\t` Karoli_1908: 658; minta: 658; jsonl `"koteg": N` 1–66; 66. sor: 24:26–24:33 (8 vers) |
| K1 tokenek | OK (er, szúrópróba) · NEM ELLENŐRIZHETŐ (hu teljes összevetés, „pontosan egyszer”) | `adat/karoli_strong/szavak_Jozs.tsv` | er 15 737 = TAHOT `^Józs` 15 737; hu 14 668. Versenként (1:1, 15:63, 24:33) egyezik a mintával. A teljes hu-összevetés és az egyszeri szereplés az `egyesit.py --ellenoriz` futtatása nélkül nem igazolható |
| K2 Strong | OK (szúrópróba) | `szavak_Jozs.tsv:21–38`, `:30387–30407` | 1:1 18 és 24:33 21 er-token = TAHOT 118689–706 és 134405–425; üres er-strong 0; nem-H strong 0 |
| K3 hash | NEM ELLENŐRIZHETŐ | `naplok/F22_Jozs_jelentes.md:9` | a `git diff f21p/` üres; a kötegenkénti hash-ellenőrzésnek nincs ellenőrizhető nyoma |
| K4 jelentés tartalma | OK | `naplok/F22_Jozs_jelentes.md:7–27` | kapuhiba, arányok, régi arany és `get_usage` szerepel; C-költség n.é. |
| K5 C-költség | n.é. | — | nem volt C-futás |
| K6 zárt adat | OK | — | `git log -G` → 0; új fájl csak a 7 `A` (name-status) |
| K7 újraépítés | NEM ELLENŐRIZHETŐ | jelentés 22. sor | az `egyesit.py --ellenoriz --konyv Józs` a szerepkör megengedett parancsain kívül esik |
| K8 ELLENOR TISZTA + CI | ELTÉRÉS (következmény) | — | a CI saját futtatásra 0 találat, de ez a jelentés nem TISZTA (l. 1. tétel) |
| K9 SEMA/datasetek | ELTÉRÉS (SEMA) · OK (datasetek) | `adat/SEMA.md:937` | l. 1. tétel; datasetek 8/8 |
| csak-Sonnet jelölés | OK | parok/szavak | `\talacsony\tS$` 15 023 és 30 405; `\t(magas\|kezi\|fuggoben)\t` 0 |
| kapuhiba | OK | jsonl 6., 8., 11., 13., 18., 53. sor | vers szintű `probalkozas: 2` 6 db; nem-ok állapot 0 |
| régi arany | OK | `parok_Jozs.tsv:7374,7866,8894,10073,10615` | Grep `^Jos` Karoli_Strong_kivonat: 5 → 5 találat H7497-tel |
| változatlanság | OK | — | `git diff --stat` üres |
| jóváhagyott lista + napló vs. detektor | OK | `tokenek.py:55`, `F22_versbeosztas_jovahagyas.md`, `F22_versbeosztas.md:18, 299–322` | 658/658, 24 fejezet, 0/0/0/0 |
| kulcs-grep | OK | — | `git log -G …` → üres |
| zárt licencű adat hiánya | OK | — | `git log -G …` → üres |
| datasetek 8 sor | OK | `adat/datasetek.tsv` | count 8 |
| brief `ir:` | OK | brief fejléc | mind a 10 írt fájl és a `ELLENOR_F22_Jozs.md` benne van (a jóváhagyási napló kétszer, kozmetikai) |
| jelentés számai | OK | `F22_Jozs_jelentes.md:16–27` | a fenti Grep-számok |
| D1, D6, D7, D12 | OK | brief:163 | könyvenként, zárt adat nincs, `f21p/` változatlan, csak Sonnet |
| D12 / D4 keret 9%→13%, 5 órás ablak 0→27% | NEM ELLENŐRIZHETŐ | jelentés 10. sor | a `get_usage` kimenete nincs a repóban |
| D12 felhasználói jóváhagyás („mehet a Józsué”) | NEM ELLENŐRIZHETŐ | brief:163, napló | chat-döntés; a DT-F22c ✅ megvan (`DONTESEK.md:38`) |
| D2, D3, D5, D8 | n.é. | — | csak Sonnet |
| A1 | OK | parok/szavak 1. sor | `scope=manual`, `ts=manual` |
| A2 | OK | jelentés 33–34. sor, brief `kovetkezo` | a nyitott tételek valóban nyitottak |
| A3–A5 | n.é. | — | nincs tanulmány-, Remez/Sod- és tanítótartalom |
| A6 | OK | — | E12–E15: 0 találat |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | — | CI-jelentést nem kapott; saját futtatás: E2–E16 és E19 0 |
| ⛔ 1. / 2. | OK (a végrehajtás eddig) | brief 67., 122. sor | kapuhiba végleg 0%, C nincs; merge nem történt |
| Keret: „a modell nem ír Strongot” | OK | `f22/_munka/_fix_k053.py` | a subagent szkriptje csak a 20:9 válasz-objektumát írja (Strong nélkül); tartalma azonos a jsonl 53. sorával |
| Ellenőrzőlista 1–5 | OK | numstat | adatsor-törlés 0, kiszűrt TAHOT-token 0; a táblák Δ-ja a jelentés 2. szakaszában bontva |

## Eltérések és Kezelés
| # | Eltérés | Kezelés |
|---|---|---|
| 1 | (közepes) **SEMA 2.20 ↔ kód:** az `adat/SEMA.md:937` szerint `tokenek.VERSBEOSZTAS_JOVAHAGYOTT`: „2Móz, 3Móz, 4Móz, 5Móz; a 3Mózesnek és az 5Mózesnek a listában nincs sora”. A `tokenek.py:55` és a jóváhagyási napló viszont már tartalmazza a Józs-t. | Javítva (F22.28): „2Móz, 3Móz, 4Móz, 5Móz, Józs; a 3Mózesnek, az 5Mózesnek és a Józsuénak a listában nincs sora”. |

**Megfigyelés (nem eltérés):** az `f22/_munka/` munkafájljai nem szerepelnek a `.gitignore`-ban. *Orkesztrátori megjegyzés:* a könyvtár a `.git/info/exclude` 19. sorában ki van zárva (`git check-ignore` megerősíti), így `git add -A` sem viszi be; ugyanígy volt az 1–5Mózesnél (`naplok/F22_1Moz_jelentes.md`, 7. pont).

**A jelentés pontosítása (F22.28):** a keret-mondat („felső becslés”) átírva: a 9% a Józs-jóváhagyás után, az előkészítés előtt mért érték.

**Nem ellenőrizhető (az ellenőr számára):** az `egyesit.py --ellenoriz --konyv Józs` és a K7 újraépítés; a hu-tokenek „pontosan egyszer” szereplése; a K3 kötegenkénti hash-ellenőrzése; a `get_usage`-értékek; a „mehet a Józsué” jóváhagyás; a CI-jelentés egyezése. *Orkesztrátori megjegyzés:* az `egyesit.py --ellenoriz --konyv Józs` az orkesztrátor futtatásában „rendben” (0-s kód), és az újraépítés SHA-256 szerint bájtra azonos — ez nem független igazolás, a jelentés 2. szakasza rögzíti.
