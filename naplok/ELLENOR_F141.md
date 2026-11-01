ELTÉRÉS: 6 tétel

*A jelentést a független ellenőr (`fuggetlen-ellenor`) adta vissza szövegként, mert a saját sessionjében nem volt fájlíró eszköze; az orkesztrátor mentette változatlanul ide. Alap: de52823..ccr-6c9c92aa-tnvazz (HEAD = d8335516).*

# ELLENOR_F141 — F141_LEXIKON_LITERAL_JAVITAS_BRIEF.md

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | Az ellenőr tényleges modellje `claude-opus-5-5`, a kért (subagent-fájl) `opus`: egyezik. A menet nem írt `modell` mezőt adattáblába (`git diff --stat de52823..HEAD -- adat konkordancia`: üres). A commitok `Co-Authored-By: Claude Sonnet 5.5` sora egyezik a brief `modell: sonnet` mezőjével. |
| L1 újrafelmérés | OK | `DONTESEK.md:413` | A bfba346f a felmérést a DT-F141a-ban rögzítette (4 maradék literál, 74 előfordulás 17 fájlban). |
| L2 ⛔ DT343 | ELTÉRÉS (a történetben, utólag javítva) | `DONTESEK.md:413` | A 6cac68d6 („DT343 eldöntve …”) a döntést a felhasználó döntése előtt írta be (az orkesztrátor félreértette a „Javaslat” választ). A c9420101 visszavonta. A visszavonás tiszta: `git diff 6cac68d6^..c9420101 --stat` üres. Ezután jött az ad73da2e (a döntés rögzítése), és csak azután a b69e17e6 (megvalósítás). Hogy a felhasználó a chatben ténylegesen döntött-e: a repóból NEM ELLENŐRIZHETŐ. |
| L3 4 literál javítása | OK | `eszkozok/ellenoriz.py:207,237,264`; `eszkozok/f127_jeloltek_bovit.py:31` | `git diff de52823..HEAD -- …`: 4 sorban DT-F127b → DT277. A `futtat.py --teljes --minta 100` E32-listájában egyik fájl sem szerepel. |
| L3/L5 E32 sorszám | **ELTÉRÉS (súlyos)** | `eszkozok/ellenorzes/szabalyok.py:2442` | `sor = csp.lineno + csp.value.count('\n', …)`: implicit string-összefűzésnél (`'a' 'b'` több soron) a literál egyetlen Constant, amelynek a `lineno`-ja az első sor. A szabály minden találatot az első sorra teszi. Futtatással igazolva: `futtat.py --teljes --minta 100` kimenetében `helyesiras.py:556` 4×, a helyőrzők valójában az 556., 557., 558. sorban állnak; `karoli_modern.py:160` 6×, a helyőrzők a 165–166. sorban; `igealak.py:1174` 4×, a helyőrzők az 1178. sortól. Következmények: (1) rossz fájl:sor; (2) az `e32-kihagy` jelölést a rossz sorban keresi; (3) a D8-szintezés miatt a meglévő összefűzött literál folytatósorába visszaírt helyőrző JELENTÉS lesz, nem HIBA (épp a javított `ellenoriz.py:236–237` mintája). A brief 5. lépésének célja erre az esetre nem teljesül, és teszt sincs rá: a `test_pozitiv_tobbsoros_literal_pontos_sora` csak `"""…"""` literált vizsgál. |
| L3 E32 definíció-szűrés | ELTÉRÉS (latens; kódolvasásból) | `eszkozok/ellenorzes/szabalyok.py:2370–2374` | Az `import szamkiosztas` a `szamkiosztas.py`-t az `eszkozok/` alól tölti be. A `szabalyok.py` (31. sor) és a `futtat.py` (40. sor) csak az `eszkozok/ellenorzes`-t teszi a `sys.path`-ra. Az `eszkozok/` csak akkor kerül oda, ha az E28 előbb meghívja a `_general_modul()`-t (1904. sor). Ha nem, az `ImportError`-t a `except Exception: pass` lenyeli, és a „ma is definiált helyőrző nem kiosztott” szűrés csendben kimarad: újrahasznált helyőrzőn hamis HIBA, és sorrendfüggő teszt (a `test_kiosztasok_a_szamkiosztas_commitokbol` önállóan várhatóan bukik). Nem futtatva. |
| L4 nulla-diff (DT344) | NEM ELLENŐRIZHETŐ (részben OK) | `lexikon/*_TUDOMANYOS.md` | Grep `beépített motívumközi jelölt áll, DT277` a `lexikon/` alatt: 8 találat 8 fájlban. `…áll, DT-F`: 0 találat. A `general.py --ir` újragenerálás diffjét az ellenőr nem futtathatta. A feltétel szűkítése rögzítve: `naplok/F141_zaras.md:5`, `DONTESEK.md:414`. |
| L5 teszt | OK (számolva), a futás NEM ELLENŐRIZHETŐ | `eszkozok/ellenorzes/tesztek/test_szabalyok.py:1537–1633` | 15 tesztmetódus, egyezik a zárónaplóval. A „180 teszt OK” állítást az ellenőr nem futtathatta. |
| D DT343 | OK (tartalom) | `DONTESEK.md:413` | A megvalósítás egyezik az (a) változattal. Az állapot „🟢 eldöntve, alkalmazásra vár”, holott alkalmazva van (megjegyzés). |
| D DT344 | NEM ELLENŐRIZHETŐ | `DONTESEK.md:414` | A felhasználó chates „B” döntése a repóból nem igazolható. |
| számok 74 ↔ 70 | ELTÉRÉS (alacsony) | `DONTESEK.md:413`; `naplok/F141_zaras.md:7` | A DT343 74 előfordulást ír 17 fájlban (benne a `teszt_emeles.py` 15 helye). Az E32 saját futása: 70 találat 13 fájlban; a `teszt_*` fájlokat kizárja, így 74 − 4 − 15 = 55 ≠ 70. A két mérés nincs megfeleltetve. |
| `ir` mező | ELTÉRÉS (alacsony) | `F141_LEXIKON_LITERAL_JAVITAS_BRIEF.md:15` | Írt fájl a `test_szabalyok.py`, a `DONTESEK.md` és a `naplok/F141_zaras.md` is, de egyik sincs az `ir`-ben; a `szamkiosztas.py` benne van, de nem változott. |
| commit-azonosítók | ELTÉRÉS (alacsony) | – | Az F141.1, F141.2, F141.3 tételazonosító kétszer szerepel a `git log`-ban (bfba346f/ad73da2e, 6cac68d6/b69e17e6, c9420101/2e1cbf0b). |
| A1 | OK (nem érintett) | – | |
| A2 | OK (részben NEM ELLENŐRIZHETŐ) | `naplok/F141_zaras.md:12–14` | A 70 literál nyitott: E32 = 70. Az „E2-E30” lépésnév nyitott: `.github/workflows/ellenorzes.yml:68`. A 7 lap elavultsága generátor-futás nélkül nem ellenőrizhető. |
| A3, A4, A5, A6 | OK (nem érintett) | – | |
| CI-jelentés | NEM ELLENŐRIZHETŐ | – | Helyi futás: E16 HIBA 1 (a PR-cím nem „[ELLENŐRZŐ]” előtagú), E25 JELENTÉS 4, E27 JELENTÉS 41, E32 0, a többi 0. `--pr-cim "[ELLENŐRZŐ] F141: E32"`-vel az E16 0. |
| CL1 törölt sorok | OK | – | 6 törölt sor, mindegyiknek van cseresora (brief fejléc 2, literál 4). |
| CL2 kulcstartomány | OK (nem érintett) | – | |
| CL3 nulla-diff hatóköre | NEM ELLENŐRIZHETŐ | – | A DT344 szerint a nulla-diff csak a `DT277` sorra vonatkozik; a 7 lap egyéb tartalma elavult. |
| CL4 TSV-sorszám Δ | OK | – | `git diff --stat de52823..HEAD -- adat konkordancia`: üres. |
| CL5 ⛔ pontok | ELTÉRÉS | – | Ugyanaz, mint az L2 sor. A DT-F141b-nél a megállás nem látszik (NEM ELLENŐRIZHETŐ). A `lexikon/` nincs a diffben. |

ELTÉRÉS-ek súlyossági sorrendben:
1. E32 sorszám implicit összefűzésnél (`szabalyok.py:2442`): futtatással igazolva.
2. `import szamkiosztas` `sys.path`-függés (`szabalyok.py:2370`): kódolvasásból.
3. ⛔ DT343: a döntést a felhasználó előtt rögzítette (6cac68d6), utólag visszavonva.
4. A 74 ↔ 70 szám nincs megfeleltetve.
5. Az `ir` mező nem fedi az írt fájlokat.
6. Ismétlődő commit-tételazonosítók.
