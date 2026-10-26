ELTÉRÉS: 9 tétel

# ELLENOR_F38_adag7 — független ellenőrzés

- Brief: `F38_BDB_FORDITAS_BRIEF.md` (modell: sonnet)
- Tartomány: `61714f36c5d65219b021199d40721fcc23ed6cb5..08f4c80` (26ec7bd, 9358d5b, 9ccbd84, 5931be1, 6244e1c, 48a4f5e, 08f4c80), ág: `ccr-ecfe0c66-bujfae`
- Ellenőr: `fuggetlen-ellenor` subagent (`claude-opus-5-5`, a kért `opus`). A jelentést az ellenőr írási eszköz híján visszaadta; a fájlt az orkesztrátor mentette változtatás nélkül, a végén a saját kiegészítő futtatásaival (külön szakaszban jelölve).

## Az ellenőr jelentése

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | Az ellenőr modellje `claude-opus-5-5`, a kért `opus`. Az új sorok `modell` mezője `claude-sonnet-5-5`, egyezik a végrehajtó commitjainak trailerével (26ec7bd, 9358d5b, 9ccbd84, 5931be1, 6244e1c, 08f4c80 „Co-Authored-By: Claude Sonnet 5.5”). A 48a4f5e (DT323) Opus-sessionből jött, adatsort nem írt. |
| K1 törölt sorok | OK | `adat/forditasok.tsv:740–3000` | `git diff --numstat base..head`: forditasok +2261/−0, a meglévő sorok változatlanok, `elavult` jelölés nincs; helyes, mert a 316 Strongnak nem volt régi sora (szúrópróba: H1101, H7243, H4725, H8065, H6571, H4581 → 28 = 9+7+1+1+3+7, csak új sorok). `EMELES_munka.tsv` +2262/−1: a −1 a fejléc-komment cseréje. `hibas.tsv`: H4725 sora be (9358d5b), majd ki (9ccbd84), nettó 0; H4912 sora be. |
| K2 lefedettség | OK | `naplok/BDB_FORDITAS_sorrend.tsv:651–967` | 317 sor a 7. adagban (649–965). Új sorok: 314 `sz1` + 2 `teljes` (H4725, H8065) = 316 Strong; 7a 650–733 (84) + H4725, 7b 734–825 (92), 7c 826–928 (102, a H4912 nélkül), 7d 929–965 (37). **Hiány: csak a H4912.** **Többlet: nincs.** Sorrendben, ismétlődő `sz1` nincs. |
| K3 nulla-diff | OK | – | Más `adat/` és `konkordancia/` fájl nem változott; `terminologia.tsv`, prompt, `bdb_szakaszok.tsv` érintetlen. |
| K4 E17/DT3 | ELTÉRÉS | `adat/forditasok.tsv` | Δ = +2261 sor (fejléc nélkül 737 → 2998); bontási napló nincs. Commitonkénti numstat: 663 + 1 + 695 + 682 + 220; kategóriák (2259 `sz`, 2 `teljes`) sehol nem rögzítve. |
| K5 ⛔ pontok | OK | brief 80, 95, 117 | M1, Mz, Mj nem érintett; a kapumódosítás megállási ponton, jóváhagyással (DT322). |
| Kérés 1: csak hozzáfűzés, allapot/modell | OK | `forditasok.tsv:740–3000` | Első hunk `@@ -739,0 +740,2261 @@`; a 740–3000. sor mind `sonnet` / `claude-sonnet-5-5`. |
| Kérés 1: forras_hash (13. szabály) | NEM ELLENŐRIZHETŐ (az ellenőr szerepkörében) | – | Az `sz` sorok hash-e SHA-1 formátumú, a munkatábla és a forditasok.tsv hash-e azonos (H6571 sz1). |
| Kérés 3: tesztek | NEM ELLENŐRIZHETŐ (az ellenőr szerepkörében) | – | – |
| Kérés 4 / DT322: a kapumódosítás tartalma | OK | `eszkozok/forditas_kapuk.py:72–74` | Csak a forrásoldali számláló kapott `+ count('«')`-t, ez csak szigorít. `«`/`»` a `BDB_teljes_unabridged.tsv`-ben 1 találat (H4725); `bdb_szakaszok.tsv`, `Thayer_teljes.tsv`: 0. |
| Kérés 4: a döntés azonosítója a kódban | ELTÉRÉS | `forditas_kapuk.py:73`, `teszt_forditas_kapuk.py:507` | A komment és a teszt-docstring a **DT-F38i**-re hivatkozik, a döntés **DT322**; a DT-F38i létező, más tárgyú döntés (`DONTESEK.md:66`). |
| Kérés 2/H4912 | OK | `naplok/BDB_FORDITAS_hibas.tsv:4` | Nincs rögzítve, a hibalistán áll (`11_konyvek`); a forrás „the Praise of Wisdom 1:8-9 is prefixed…” (`BDB_teljes_unabridged.tsv:4594`); `Wisdom`→`Bölcs` (`normalizal.py:164`); kapu-felülbíráló kapcsoló nincs (`emeles.py:1072–1089`). |
| H4912 dokumentációja | ELTÉRÉS | `hibas.tsv:4`; `DONTESEK.md` DT323 | A hibalista sora a DT323 (1)(a) után is „döntésre vár” szöveggel áll; a DT323 nem rögzíti, hogy a 7d nem tudta végrehajtani. |
| D-sorok: DT289 (i), a 98 N-F107b Strong sorrendje | ELTÉRÉS | brief:58; `NYITOTT_FELADATOK.md:172`; `DONTESEK.md:362` | A DT289 🟢 sorrend (i): „külön újrafordító adag(ok) **a 7. adag előtt**”. A diffben egyik új Strong sem a 98 közül való; az új `kovetkezo` a 98-at a 7. adag utánra teszi. Felülíró döntés nincs rögzítve; a 150 000 karakteres szeletelésre sincs rögzített döntés. |
| D1–D11, D-gyok | OK / nem érintett | brief 192–204 | Sonnet-út betartva; a D10 (5) szerint a H1101 sz5 helyes. |
| Szabályok (brief 160–172) | OK | – | Prompt és terminológia változatlan; kapuhibák a hibalistán; `kezi` sorhoz nem nyúlt; rövidítések szúrópróbával rendben. |
| Megállási pont 3: commitüzenet | ELTÉRÉS | 6244e1c, 08f4c80 | A 7c és 7d üzenetéből hiányzik a „<karakter> karakter” rész. |
| `ir:` lista | ELTÉRÉS | `naplok/EMELES_munka.tsv` | Nincs a brief `ir` listáján, mégis +2261 sorral commitolva (azonos a forditasok.tsv új soraival). |
| Fejléc | ELTÉRÉS | brief:9 | `ag: claude/f38-mj-dontes`, nem a munkaág (`ccr-ecfe0c66-bujfae`). |
| A1 | ELTÉRÉS | `DONTESEK.md` DT322 | Mért állítás („csak a H4725 forrásában van `«`”) proveniencia-sor és `manual` jelölés nélkül; az állítás igaz. |
| A2 | OK | `NYITOTT_FELADATOK.md:172` | Az N-F107b valóban nyitott. |
| A3, A4, A5 | nem érintett | – | – |
| A6 | OK | – | `futtat.py`: E12–E15 0 találat. |
| 3 CI-jelentés | NEM ELLENŐRIZHETŐ (összevetés) | – | Saját futtatás (`futtat.py --valtozott … --diff-alap 61714f36… --diff-fej 08f4c80`): E2–E16, E19, E20, E26, E28, E29, E31: 0. E25: 4 régi (CLAUDE.md, MUNKAMENET.md). E27: HIBA 2, JELENTES 105, mind a `FELADATOK.md`-ben (a diff nem érinti). E30: 2 FIGYELMEZTETÉS (9ccbd84 üzenete: „forras”/„forditas” ékezet nélkül). |
| Kérés 5: szúrópróba (15 szócikk) | OK, 1 kivétellel | – | Szakaszszám-egyezés: H2809 2/2, H1101 9/9, H7243 7/7, H8416 11/11, H2232 25/25, H4581 7/7, H0565 2/2, H0635 2/2, H1439 2/2, H2977 5/5, H0223 6/6, H0274 3/3, H8123 2/2, H8283 2/2, H5511 2/2, H6239 2/2; H4725, H8065 `teljes` (SEMA 2.14 táblán kívüli lista). EN↔HU tartalom: héber betűhű, kihagyás/betoldás nincs, kivéve H8123. H5511 „Judges 13:27” → „Józs 13:27”: a bemenet javítása (`bdb_forras_javitas.tsv:6992`). |
| Kérés 5: H8123 | ELTÉRÉS | `forditasok.tsv:2785` | Forrás „Judg 13:24; 14:1, 335t. Judges 14”, fordítás „Bír 13:24; 14:1, 3 összesen 35-ször”: javítótábla nélküli forráskorrekció (a `bdb_forras_javitas.tsv`-ben H8123: 0 sor). |
| Kérés 5: H2809 „→` (DT323 (2)) | OK | `forditasok.tsv:2718` | Forrás „Modern „usbân”, fordítás „Mai `usbân”. |
| Kérés 6: H1101 `\x99` | OK | `forditasok.tsv:1909, 1911` | Két jel a forrásban (sz3, sz5), kettő a fordításban, azonos környezetben. |
| Megfigyelés: verzifikáció | (nem eltérés) | `forditasok.tsv:2718, 1909` | A BDB héber versszámozása átmegy („Én 7:5”, a Károliban Én 7:4; ugyanígy „Zsolt 92:11”, „Hós 2:1”); forráshű, a brief átszámozást nem ír elő (`lekerdez.py karoli`, ts=2026-10-25T10:49Z). |

**Az eltérések súlyossági sorrendben:**
1. (közepes) A DT289 (i) sorrendje nem teljesült: a 98 N-F107b Strong újrafordító adagja a 7. adag *előtt* kellett volna; felülíró döntés nincs rögzítve.
2. (alacsony–közepes) `forditas_kapuk.py:73`, `teszt_forditas_kapuk.py:507`: DT-F38i a DT322 helyett.
3. (alacsony) H8123 sz2: „335t.” → „3 összesen 35-ször”, javítótábla nélküli forráskorrekció.
4. (alacsony) E17/DT3: +2261 sor bontási napló nélkül.
5. (alacsony) A H4912 állapotának rögzítése ellentmondásos (hibalista „döntésre vár”; DT323 végrehajtás-oszlopa).
6. (alacsony) A DT322 mért állítása proveniencia nélkül.
7. (alacsony) A 7c és 7d commitüzenetéből hiányzik a karakterszám.
8. (alacsony) `ir` listán kívül írt fájl: `naplok/EMELES_munka.tsv`.
9. (alacsony) A brief `ag` mezője nem frissült.

## Az orkesztrátor kiegészítő futtatásai (az ellenőr „NEM ELLENŐRIZHETŐ” pontjaira)

`scope=ág ccr-ecfe0c66-bujfae @ 08f4c80 | forras=helyi-futtatas (orkesztrátor-session, claude-opus-5-5) | ts=2026-10-25`

- `python eszkozok/ellenoriz.py`: `RENDBEN: 14 | SÉRTÉS: 0 | KÉZI: 2 | JELENTÉS: 3`; a 13. szabály („Fordítási gyorsítótár (kulcs egyediség, forras_hash)”): RENDBEN.
- `python eszkozok/teszt_forditas_kapuk.py`: OK.
- `python eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py`: OK.
- Az 1. eltérés forrása igazolva: `DONTESEK.md` DT289 Döntés oszlopa: „sors (2), sorrend (i) — … külön újrafordító adag(ok) a 7. adag előtt”.

ELTÉRÉS: 9 tétel
