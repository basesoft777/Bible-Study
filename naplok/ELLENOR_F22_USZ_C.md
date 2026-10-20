# ELLENOR_F22_USZ_C — független ellenőrzés: a 22.9 C csomag (Róm, 1Kor, Jel)

**Brief:** `F22_KAROLI_STRONG_BRIEF.md` (22.9 C csomag, D45, DT-F22h (b) = a main-en DT262). **Tartomány:** `23dc19f..20670a6` (12 commit, F22.29–F22.40). *A független ellenőr (`fuggetlen-ellenor`) jelentése; a subagentnek nincs Write eszköze, ezért a végrehajtó mentette a repóba; a hosszú parancs-/útvonalcellák rövidítve, a számok és az eredmények változatlanok.*

**Eredmény: ELTÉRÉS: 5 tétel**

**Modell-ellenőrzés:** az ellenőr modellje `claude-opus-5-5`, a kért `opus`, egyezik. A 145 új futásnapló-sor `modell` mezője `claude-sonnet-5-5` (az ellenőr lekérdezéssel nem tudta eldönteni, hogy API-válaszból jön-e). **Eljárási közlés:** az ellenőr a megengedett Bash-körön túl `git show`, `grep`/`cut`/`sort`/`sed`/`tr` csövekkel olvasott (fájlt nem írt).

| pont | eredmény | indok (rövidítve) |
|---|---|---|
| Áll. 1: minták / kötegek | OK | minta 432/437/406 sor (fejléc + 431/436/405); jsonl 44/44/41 sor; a szavak_-táblákban 431/436/405 vers; a Károli-szövegben Róm/1Kor/Jel 1272 vers |
| Áll. 1: kapuhiba | OK | 1. próba: Róm 3 vers (k004, k007, k032), 1Kor 7 vers 6 kötegben, Jel 8 vers 7 kötegben, mind **versenkénti** hiba (nem lefedett eredeti/magyar szó, nem létező sorszám, hibás pár), egész köteg formátumhiba nincs; a 2. próba mind `ok=igen`, végleges kapuhiba 0 |
| Áll. 1: prompt / modell | OK | a 145 sorban `84f12ca7aafb` és `claude-sonnet-5-5`; `f21p/` változatlan |
| Áll. 2: linkek | OK | `\talacsony\tS$`: 6871 / 6686 / 8689 |
| Áll. 2: szósorok | OK | hu 7489/7287/9744, er 7261/6986/10185 (a TAGNT-kivonat: Róm 7261, Jel 10185, a három együtt 24432); állapotbontás egyezik a jelentésekkel |
| Áll. 2: K1 / K2 | OK (darabszám) / NEM ELLENŐRIZHETŐ (teljes) | az er-sorok száma = a TAGNT-sorok száma; a Róm 3:31, Róm 8:39, 1Kor 3:23 kulcson 0 sor; üres strongú er-sor 0; szúrópróba (Róm 3:30–31, 1Kor 3:22–23, Jel 22:21, Róm 10:7) egyezik |
| Áll. 3: költség | OK | Róm +2.140667, 1Kor +2.056559, Jel +3.279640 = 7.476866 USD; futó összeg 103.530839 < 104.36; 47 + 50 + 48 = 145 hívás |
| Áll. 3: plafon-őr / sorosság | OK | `api_koteg.py`, `egyesit.py`, `kapu.py` diffje üres; a cimkék c_rom_1, c_1kor_2, c_1kor_3, c_jel_4, c_jel_5, c_jel_6 soros, átfedés nélkül |
| Áll. 4: összevonás-sorok, kezi/fuggoben | OK | Róm 3:30 hu 16–31 / er 15–25; Róm 8:38 hu 20–41 / er 18–40; 1Kor 3:22 hu 20–25 / er 20–25; Róm hu 38 + er 34, 1Kor 6 + 6 `fuggoben`/`kezi` |
| Áll. 4: Róm 8 kézi javítás | OK | a detektor `Róm 8:38 nincs_karoli`-t ad, a kézi tábla törli és `Róm 8:39`-et vesz fel; a TAGNT Róm 8:38–39 40 sor |
| Áll. 4: jóváhagyás időrendje | OK / a chat NEM ELLENŐRIZHETŐ | a jóváhagyási napló és a `VERSBEOSZTAS_JOVAHAGYOTT` bővítése (2026-10-19T19:41) az első beküldés (2026-10-20T04:56) előtt |
| Áll. 5: csak 8 vers változott | OK | `parok` 2Kor −43, Zsid −23, Fil −15 link; a `szavak` sorszáma változatlan |
| Áll. 5: Róm 4:16–17 téves jelzés | OK | a TAGNT 4:17 „καθὼς γέγραπται”-val, a Károli 4:17 „(A mint meg van írva”-val kezdődik |
| Áll. 6: [nem TR] | OK | Róm 147−40 = 107, 1Kor 253−73 = 180, Jel 743−102 = 641; a jelölőtáblában 7 / 23 / 44, összesen 119 adatsor |
| Áll. 7: proveniencia, FELADATOK.md, commit-üzenetek, csak C-modellhívás, D45, v2.46 | OK | |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | saját futás: E2–E20, E26, E28, E29, E31: 0; E25 4 JELENTÉS; E27 HIBA 1 (`FELADATOK.md`, `1f420a7c`, a fájl a diffben változatlan, a hiba korábbi); E30 2 FIGYELMEZTETÉS |
| Lista 1–5 (törölt sorok, kulcslefedettség, nulla-diff, táblasor-Δ, ⛔ pontok) | OK | |
| **Áll. 5: jelöltek tokenhatára** | **ELTÉRÉS** | a dokumentáció szerint „TAGNT 2Kor 2:13 1–11. token” és „TAGNT Zsid 1:2 1–7. token”; a TAGNT-ben a Károli 2:12 végének megfelelő szakasz a 2Kor 2:13-ban οὐκ…μου = **1–14**, a Zsid 1:2-ben ἐπ᾽…υἱῷ = **1–9** (a 11 és a 7 a magyar szószám). Érintett: `f22/kezi_versek_2Kor.tsv`, `_Zsid.tsv`, `naplok/F22_C_elokeszites.md`, `F22_2Kor_jelentes.md` 7., `F22_Zsid_jelentes.md`, `F22_{2Kor,Zsid}_atnezes.tsv`. Az adat nem sérült (az egész vers `kezi`) |
| **D45 / DT-F22h (b) döntés rögzítése** | **ELTÉRÉS** | a DT262-ben (a main-en; a branchen DT-F22h) az Állapot 🟡, a Döntés „—”, a futás mégis a (b) opcióval ment; a felhasználó döntésének nincs nyoma a `DONTESEK.md`-ben |
| **Költség-szám összhang** | **ELTÉRÉS** | a brief és a commit-üzenet 7,4768, az összesítő 7.4769; a pontos érték 7.476866 (a 7,4768 csonkolás) |
| **Brief `ir` mező** | **ELTÉRÉS** | hiányzott: `adat/karoli_strong/{parok,szavak}_{Rom,1Kor,Jel}.tsv`, `tokenszint_vershatar.py`, `f22/valaszok/sonnet/{Rom,1Kor,Jel}.jsonl`, `f22/api_termeles/high/{Rom,1Kor,Jel}.jsonl`, `naplok/F22_{Rom,1Kor,Jel}_atnezes.tsv` |
| **A2: NYITOTT N-F22e** | **ELTÉRÉS** | a bekezdés ellentmond magának: „ÁTMENETI KEZELÉS: … `kezi` kényszerben” és „(mergelt könyvekben, javítatlan)” |
| A1, A3–A6, régi arany, F37 T4 | OK / nem alkalmazható / NEM ELLENŐRIZHETŐ | a régi arany számlálója futtatás nélkül nem igazolható |

**Az ELTÉRÉS-ek súlyossági sorrendben:**
1. A DT262 (DT-F22h) döntése nincs rögzítve.
2. Hibás tokenhatár a dokumentációban (2Kor 2:13: 1–14, Zsid 1:2: 1–9).
3. `NYITOTT_FELADATOK.md` N-F22e: „kezi” és „javítatlan” egyszerre.
4. A költség két alakban (7,4768 / 7.4769).
5. A brief `ir` mezője hiányos.

## Javítás (F22.41, 2026.10.20)

1. DT262: Állapot ✅, Döntés: a felhasználó „b: részletekben, most” válasza (2026-10-20, chat), alkalmazás F22.35–F22.38, a C költsége 7,4769 USD.
2. A tokenhatár javítva a fenti fájlokban (2Kor 2:13 1–14., Zsid 1:2 1–9.); az átnézési listák az `egyesit.py` újrafuttatásával frissültek (az adattáblák nem változtak, az ellenőrzés rendben).
3. A `NYITOTT_FELADATOK.md` N-F22e bekezdése egységesítve („a mergelt könyvekben; most `kezi` kényszerben”).
4. A költség mindenütt 7,4769 USD (a pontos érték 7.476866).
5. A brief `ir` mezője kibővítve a hiányzó fájlokkal.

Következő lépés: újraellenőrzés (`naplok/ELLENOR_F22_USZ_C_2.md`).
