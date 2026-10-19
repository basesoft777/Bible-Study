# ELLENOR_F76_M3_2 — F76_OLVASOI_KONKORDANCIA_BRIEF.md, javítókör 4f117ffd..4039f4e0 (F76.50–F76.53); a teljes M3: 89b30c2e..4039f4e0

*A `fuggetlen-ellenor` subagent jelentése (2026-10-18). Az ellenőrnek nincs fájlíró eszköze, ezért a jelentést az orkesztrátor mentette el; a táblázat a jelentés tartalmát adja.*

**Ítélet: ELTÉRÉS (1 tétel, alacsony, új).** Az előző jelentés (`naplok/ELLENOR_F76_M3.md`) 4 tétele megszűnt.

Modell-ellenőrzés: a kért modell `opus` (a subagent-fájl szerint), a tényleges `claude-opus-5-5`; egyezik. A napló 3. sora és a 4 commit `Co-Authored-By: Claude Opus 5.5` trailere összhangban van.

**Korlát.** A `pardes.db`-n nem futott független SQL, és a `teszt_futtat.py` sem (a szerep parancskörén kívül esnek). A DB-ből vett darabszámok és a tesztfutás eredménye NEM ELLENŐRIZHETŐ; helyettük a DB építési forrás-TSV-jét (`adat/karoli_strong/szavak_Pred.tsv`), a TAHOT-kivonatot és a kódot olvasta.

| pont | eredmény | fájl:sor | indok |
|---|---|---|---|
| 1. ELTÉRÉS: a héber keresés képessége és korlátja | OK | `README.md:56`; `sablonok/kereses.html:26`; `kereses.py:11-17, 266-268, 277-280` | A három hely ugyanazt mondja. Talál: egy token, vagy legfeljebb 3 előtag-betű + egy token. Nem talál: a szuffixumos egybeírt alakra (זרעו, למינו). Bontás: זרע ו, ל מינ ו, szóvégi alak nélkül. Ez a felhasználó (b) döntése. A tényalap: `TAHOT_kivonat.tsv` `^1Móz 1:11\t`, 188–193. sor: ל / מִינ / וֹ és זַרְע / וֹ. |
| 1. — a keresési logika változatlan | OK | `kereses.py` | `git diff -U0 4f117ffd..HEAD -- …/kereses.py`: 3 hunk, mind docstring. |
| 1. — az új tesztek a leírást mérik | OK (tartalom); a futás NEM ELLENŐRIZHETŐ | `teszt_kereses.py:92-97, 221-247, 368-377` | 3 új teszt (`test_heber_magok_szuffixum_korlat`, `test_heber_elotag_es_szuffixum`, `test_sugo_heber_korlat`); összesen 36 teszt, egyezik a naplóval. |
| 2. ELTÉRÉS: a Préd 2:26 határpárja | OK (a DB építési forrásából; a DB maga NEM ELLENŐRIZHETŐ) | `M3.md:47, 51`; `DONTESEK.md:279` | `f22/versosszevonas.tsv`: a Préd 2:26 az egyetlen sor `er_tol`=1-gyel. `tokenek.py:173-175`: az `extra` a fő vers után számozódik. `szavak_Pred.tsv`: a 38. token `רֽוּחַ`, a 39. `כִּ֣י`, a 39–47. a beolvasztott MT 2:25. A végrehajtó 38\|39 párja helyes; az előző jelentés javaslata (נִּי \| כִּי) a TAHOT kulcs-sorrendjéből jött, és hibás volt. A DT220 és a napló összhangban van. |
| 3. ELTÉRÉS: az N-F76b/c elhalasztása | OK | `NYITOTT_FELADATOK.md:63`; `M3.md:96` | +1 sor helyőrzővel, végleges szám nélkül; a javaslat „nem döntés”-ként jelölve. Megjegyzés: a brief törzse (53., 90. sor) továbbra is a #76 részének írja a két lépést; az elhalasztás forrása a NYITOTT-sor. |
| 4. ELTÉRÉS: a napló elavult sorai | OK | `M3.md:3, 51, 95` | „Commitok: F76.42–F76.53”; a DT220 🟢, F76.48. |
| **Új: a Préd 2:26 sorrend-ténye** | **ELTÉRÉS** (alacsony) | `M3.md:51`; `NYITOTT_FELADATOK.md:61`; `DONTESEK.md:279`; README:56; `kereses.html:26` | A napló helyesen rögzíti, hogy a Préd 2:26-ban a DB-sorrend eltér a szövegsorrendtől (az MT 2:26 után jön a 2:25), de ezt tévesen a sqlite-építőnek és az N-F76k-nak tulajdonítja. A sorrend a #22 tokenfolyamából jön (`tokenek.py:173-175` → `szavak_Pred.tsv`). Az N-F76k csak a vers-címke tárolását írja elő, a sorrendet nem említi. A DT220, a README és a súgó sem mondja ki, hogy itt a találat a szövegben nem szomszédos párra esik. A vers-lap héber sorrendjéről egyik nyitott tétel sem szól; ez meglévő adat ténye, nem az M3 okozta. |
| Írási kör | OK | — | `eszkozok/olvaso_szerver/` (4 fájl), a napló, a brief `kovetkezo` sora, `DONTESEK.md` (saját DT220 sor), `NYITOTT_FELADATOK.md` (+1 saját sor). |
| Helyőrzők, nincs végleges szám | OK | — | Új végleges DT/N szám nincs (csak meglévő DT146-hivatkozás). |
| ⛔ M5/M6/M7 | OK | brief:12 | — |
| A1 / A2 | OK | `M3.md:26, 51`; `NYITOTT:61, 63` | Proveniencia-sorok (ts 16:53:56Z, 16:54:53Z); az N-F76k és az N-F76b/c nyitott. |
| A3–A5 | n/a | — | — |
| A6 (E12–E15) | OK | — | `futtat.py`: 0 találat. |
| CI (saját futás) | OK; a CI-jelentéssel NEM ELLENŐRIZHETŐ | — | `futtat.py --valtozott … --diff-alap 4f117ffd --diff-fej HEAD`: E2–E16, E19, E20, E26, E28, E29 0; E25: 3, E27: 40 jelentés (nem a diff fájljai, korábbról); HIBA nincs. |
| Lista 1–5 | OK / n/a | — | 12 törölt sor, mind szövegcsere; az `adat/`, `konkordancia/`, `f22/` alatti TSV-k diffje 0 (Δ = 0); ⛔ rendben. |
| `teszt_bdb_vers_jelentes` `test_bajtra_azonos` | nem az M3 hibája | `M3.md:99` | A main-en is fennáll (a `szamkiosztas` DT-F99n → DT179 cseréje a generált TSV-fejlécben); a diff ezeket a fájlokat nem érinti. |

## ELTÉRÉS

1. **(alacsony, új)** A Préd 2:26 DB-sorrendje eltér a szövegsorrendtől. Ezt csak a napló 51. sora rögzíti, és tévesen a sqlite-építőnek, illetve az N-F76k-nak tulajdonítja; valójában a #22 tokenfolyamából jön. Két lehetőség: az N-F76k (vagy egy új helyőrző) rögzíti a sorrend kérdését, vagy a napló mondata pontosodik.

**Mellékes (nem ELTÉRÉS):** a „csak ott talál, ahol egyetlen token” versszinten igaz. Egy ilyen versen belül a `heber_illeszt` az ugyanott álló bontott előfordulást is kiemelheti (`kereses.py:283-300`); ez kiemelési apróság, DB nélkül nem igazolható.
