# ELLENOR_F28 — F28_EMELES_BRIEF.md · e39f145..cade303

*A `fuggetlen-ellenor` jelentésének mentése az orkesztrátor által (az ellenőrnek nem volt fájlíró eszköze). Az ellenőr nem futtatta a `teszt_*.py` / `test_szabalyok.py` teszteket és az `ellenoriz.py`-t: ezek NEM ELLENŐRIZHETŐ-t kaptak.*

**Eredmény: ELTÉRÉS, 8 tétel.** Az `origin/main` közben `5cb63a2` (4 committal előrébb, F22.1); merge előtt a main-t be kell hozni.

## ELTÉRÉSEK súlyossági sorrendben

1. **`lekerdez.py` „Sir” álnév (DT25 d) — súlyos.** Az álnév a `parse_igehely`-ben van (`lekerdez.py:104,130`), nem csak a scope-olvasásban. Ezt hívja a `load_tahot`/`load_tagnt`, `to_step`, `cmd_lxx_hid`, `lexikon_general.py:123,898`, `n14_hamart_betoltes.py:527`. A `parse_range` nem kapta meg, a `_lxx_filename` kulcsa `"Sir"` maradt. Mért regressziók: `lxx-hid "Sir 2:8"` és `"JSir 2:8"` is „Nincs LXX-kivonat ehhez a könyvhöz: JSir”; `gerinc "Sir 2" …` n=0 (`"JSir 2"` n=20); `scan H1323 --szakasz "Sir 2"` n=0 (`"JSir 2"` n=10); `tsk "JSir 2:8"` n=0; `karoli "JSir 2:8"` „Nincs Károli-szöveg”. Az `auditok.tsv:169` proveniencia (n=24) nem futtatható újra. A `teszt_lekerdez_sir.py` ezeket az utakat nem fedi.
2. **E19 `--teljes` módban el sem indul** (`szabalyok.py:869`, `futtat.py:68-76`, `kozos.py:189-206`): a `fajlok != ['__TELJES__']` feltétel mindig igaz, „## E19 (0 talalat)” hamis tisztát mutat. Az `ellenorzes.yml:63` lépésneve („E2-E16”) nem frissült.
3. **Kapuk menet közbeni lazítása** (`forditas_kapuk.py`: 5eca96a, fe84076, 82e00ed, a412e9e): az E4 önújrapróbát, utána `bukottak.tsv`-t ír elő; 6 kalibrálás történt. A `HU_TOVALTOZAT {'lélek': ('lelk',)}` minta a „lelkiismeret”, „lelkész” szóra is illeszkedik.
4. **A1:** a kódkomment „A lekérdezés kimenete a JSir alakot írja” cáfolható (`scan H1323 --szakasz "JSir 2"` kimenete `Sir 2:1 …`; a `tsk "Sir 2:8"` proveniencia `scope=range:Sir 2:8`); az `EMELES_naplo.md:223-225` TAHOT-illeszkedési állítása csak a JSir-tartományra igaz.
5. **K5:** a brief fejléce `allapot: lezarva` lett, mielőtt a független ellenőrzés tiszta volt és draft PR készült.
6. **`ir`-lista:** a `eszkozok/ellenorzes/szabalyok.py` és `tesztek/test_szabalyok.py` nincs a brief `ir` listáján.
7. **Szentlélek-lista:** 12 találatból 9 szerepel; a 3 kimaradt (`lexikon/ANTROP-001_TUDOMANYOS.md:71,108`, `TEREMT-001_TUDOMANYOS.md:159`) GENERÁLT-blokkban van; a kizárás nincs jelezve.
8. **CI-jelentés:** a napló E9-et „HIBA”-nak írja, a mérés JELENTÉS (`SEMA.md:235,236`), kilépési kód 0 (PR-cím nélkül E16 HIBA).

## OK (kódolvasás / mintavétel)

13. szabály kódja (`ellenoriz.py:615-650`); SEMA 2.14 `opus`; E19 logika; E17/E18 számfoglalás (az E19 szabad szám); E0 lista (39 + G1941 kimarad); prompt v4 (csak hozzáadás); 39 új sor (29 `opus`, 10 `kezi`; +G1941 = 11 `kezi`), helyőrző-maradvány 0; szúrópróba H6093/G0813/G5010; H7121 2.c/3 csere; H1121 szóköz; terminológia v2 (3 sor); MUNKAMENET C0 sor; E8 nem kötelező; render nem változott; Lam → JSir tábla-sor; A6 (E12–E15) 0; törölt sorok 12, adatsor nem tűnt el.

## NEM ELLENŐRIZHETŐ az ellenőr által

A tesztek és az `ellenoriz.py` futtatása; a `forras_hash` SHA-1 számolása; az `emeles.py minta --seed 28` reprodukálása; a felhasználói jóváhagyás nyoma a végrehajtó DONTESEK-soránál több nincs; az E17 küszöbe (DT3 🟡); a `lexikon_general.py` hatása a Lam→JSir váltásra.

## Megjegyzés

A G5010-ben „Septuaginta Zsolt 109:5” LXX-számozású hely Károli-rövidítéssel áll (Károli szerint Zsolt 110:4). A „Dán 22:14” a BDB-forrás saját hibája (`BDB_teljes_unabridged.tsv:7501`), nem a ψ-feloldásé.
