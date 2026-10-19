# ELLENOR_F76_M3 — F76_OLVASOI_KONKORDANCIA_BRIEF.md, 89b30c2e..183e456f (F76.42–F76.48)

*A `fuggetlen-ellenor` subagent jelentése (2026-10-18). Az ellenőrnek nincs fájlíró eszköze, ezért a jelentést az orkesztrátor mentette el szó szerint.*

**Ítélet: ELTÉRÉS** (4 tétel: 2 közepes, 2 alacsony).

Modell-ellenőrzés: a kért modell `opus` (a subagent-fájl szerint), a tényleges `claude-opus-5-5`; egyezik. A menet modelljelölése (`naplok/OLVASOI_KONKORDANCIA_M3.md:102`: `claude-opus-5-5`) összhangban van a 7 commit `Co-Authored-By: Claude Opus 5.5` trailerével. Adattábla `modell` mezőjét a diff nem írja.

**Korlát.** A `pardes.db`-n nem futott független SQL, és a `teszt_futtat.py` sem: mindkettő kívül esik a szerep megengedett parancskörén. Ahol ezek kellettek volna, ott NEM ELLENŐRIZHETŐ áll; helyettük TSV-alapú `lekerdez.py`, `Grep` és kódolvasás.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| Írási kör (`ir` + DONTESEK/NYITOTT saját sor + brief-fejléc) | OK | — | `git diff --numstat 89b30c2e..HEAD`: 16 fájl, mind az `eszkozok/olvaso_szerver/` alatt van, vagy `naplok/OLVASOI_KONKORDANCIA_M3.md`, `DONTESEK.md` +1, `NYITOTT_FELADATOK.md` +1, brief-fejléc. `adat/`, `konkordancia/`, `f22/`, `sqlite_epit.py` érintetlen. |
| Helyőrzők (DT-F76j, N-F76k), nincs végleges DT/N szám az ágon | OK | `DONTESEK.md:279`, `NYITOTT_FELADATOK.md:61` | `git diff -U0` |
| ⛔ M5/M6/M7 | OK | brief:12 | A diffben nincs telepítés, VPS vagy közzététel. |
| Strong-ág, ismert kérdés | OK (TSV-n); DB-n NEM ELLENŐRIZHETŐ | `M3.md:170-174` | `lekerdez.py scan H0216` → n=110 (napló: 110 vers); `scan H0430` → 2248 (2248); `scan G3056` → 318 (318); `kollokacio H1254 H0430` → 12 vers (12). |
| Magyar szó (pontos / szótári alak / (c)) és frázis, ismert kérdés | NEM ELLENŐRIZHETŐ (darabszám) | `M3.md:154-169` | DB nélkül nem mérhető. Szövegszinten: `karoli "1Móz 1:3"` → „Legyen világosság: és lőn világosság.” (2 előfordulás, a teszt ezt várja); `karoli "1Móz 1:2"` → „kietlen és” benne van. |
| Héber frázis: előtag-tolerancia | **ELTÉRÉS** | `kereses.py:259-266, 296-317` | A README és a docstring szerint „a beírt szó 1–4 egymást követő token összefűzése”. A jelölt verseket viszont csak a `heber_magok` szűri (a szó maga + az előtag-betűk utáni maradék), és ennek egy tokennel kell egyeznie. A TAHOT a névmási szuffixumot is külön tokenként tartja (`1Móz 1:11`: `לְ`/`מִינ`/`וֹ`, `זַרְע`/`וֹ`; `4Móz 29:39`: `כֶם`). Ezért a szuffixumos szó egybeírva hamis „Nincs találat”-ot ad: (1) *זרעו* a gyors útra megy (pontos token), 0; (2) *למינו* jelöltjei [למינו, מינו, ינו], egyik sem token, 0. Néma nem-találat; a teszt (`teszt_kereses.py:84-90, 203-212`) csak az előtagos esetet fedi. |
| Héber frázis a `token_karoli`-ból (egyeztetett eltérés) | OK | `M3.md:117`; brief:51 | M0 3.6 és E4/E5 szerint; a `frazis_pozicio` nincs használva. |
| Vershatár (Károli-vers) | OK (kódolvasásból) | `lekerdezesek.py:216-224`; `kereses.py:269-293` | Az önillesztés `igehely`-egyezést követel; a `heber_illeszt` versenként fut. |
| DT-F76j: a 9 hely = `f22/versosszevonas.tsv` | OK | `DONTESEK.md:279`, README, `kereses.html`, `NYITOTT:61` | A 9 adatsor mind a négy helyen pontosan egyezik; a döntés alkalmazása (README + súgó + N-F76k) megvan. |
| DT-F76j mérőtábla: határpárok | **ELTÉRÉS** (Préd 2:26) | `M3.md:144`; `DONTESEK.md:279` | 8 helyen a határon álló párt adja a tábla. A Préd 2:26-ban az er 1–9 a beolvasztott 2:25; a 9. token `נִּי`, a 10. `כִּ֤י`. A `נָתַן חָכְמָה` a 18.\|19. token, az MT 2:26 belsejében, tehát nem határpár. A „mind a 9 helyen mérve” a Préd 2:26-ra nem igazolt (a korlát logikailag ott is fennáll). A DB sorszámrendje NEM ELLENŐRIZHETŐ. |
| Paraméterezett SQL (N-F76c logika) | OK | `lekerdezesek.py:118-250` | Minden bemenet `?` paraméter; a `_frazis_sql` szövege csak n∈{2,3,4}-től függ; a `kereses.py`-ban nincs `execute`. |
| Escape (XSS) | OK (kódolvasásból) | `kereses.py:354-367`; `blokkok.py:83-89`; `kereses.html` | Jinja autoescape, `Markup %`, `urlencode`. Futtatással NEM ELLENŐRIZHETŐ. |
| Üres eredmény jelzése | OK | `kereses.html` | „Nincs találat”, 0 vers (a szuffixumos héber esetben hamis üres eredmény, l. fent). |
| Forrás- és licencsor, jelleg | OK | `blokkok.py:64-89`; `oldalak.py:279` | Indulási ellenőrzés a `KERESES` blokkokra; hiányuk `BlokkHiba`. |
| Kiadási kapcsoló / hozzáférési szint | OK (kód); a teszt NEM ELLENŐRIZHETŐ | `oldalak.py:306-311`; `kereses.py:181,228-237` | A KERESES tábláiban nincs `kjv`/`mcged`; a `kereses.*` szintezhető. |
| N-F76b (Playwright) / N-F76c (Semgrep CI-lépés) | **ELTÉRÉS** (alacsony) | brief:89-90; M0:208, 351, 356 | `.github`-ban 0 találat. Az N-F76c szerint „amint van nyilvános keresőfüggvény … a #76 kódjával együtt kerül be”; az M3 jelentése nem írja, hogy elmarad, és hová kerül. Unittest-pótlék van. |
| K5 mért idők, proveniencia | OK (formailag); számok NEM ELLENŐRIZHETŐ | `M3.md:150` | Proveniencia-sor megvan; az *és* alapmódban 134/169 ms (100 ms fölött), a napló jelzi és az M4-re hárítja. |
| Napló belső összhangja | **ELTÉRÉS** (alacsony) | `M3.md:102, 146` | A 102. sor „Commitok: F76.42–F76.46”, a tartomány F76.48-ig tart; a 146. sor „DT-F76j (nyitott)”, ellentmond a 190. sornak és a 🟢 állapotnak. |
| `test_bajtra_azonos` piros a main-en is | OK (statikusan); futtatással NEM ELLENŐRIZHETŐ | `bdb_vers_jelentes.py:268-270` | A generátor „DT-F99n”-t ír, az `adat/bdb_vers_jelentes.tsv` 2. sora DT179-et (a `szamkiosztas` cseréje). `git diff 89b30c2e main -- adat/bdb_vers_jelentes.tsv eszkozok/olvaso_szerver/` üres: a main ugyanaz. Nem az M3 hibája. |
| A1 memória vs. lekérdezés | OK | `M3.md:146, 150` | A mért állításoknál van proveniencia-sor. |
| A2 nyitott tételek | OK | `NYITOTT:61, 71, 76` | N-F94f, N-F94d nyitott, a súgó jelzi; N-F76k új, nyitott. |
| A3, A4, A5 | n/a | — | Nincs tanulmány, párhuzam, nevesített tanító. |
| A6 (E12–E15) | OK | — | `futtat.py` E12–E15: 0 találat. |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | — | Saját futás (`futtat.py --valtozott … --diff-alap 89b30c2e --diff-fej HEAD`): E2–E16, E19, E20, E26, E28, E29 0 találat; E25: 3, E27: 40 JELENTES (nem a diff fájljai, korábbról). HIBA nincs. |
| Lista 1: kiszűrt/törölt sorok | OK | — | 16 törölt sor, mind szöveg- vagy kódcsere; adatsor nincs törölve. |
| Lista 2: kulcstartomány-lefedettség | NEM ELLENŐRIZHETŐ | — | A 9 párosítatlan ÚSZ-könyvben a magyar keresés nem talál (dokumentált). |
| Lista 3: „nulla-diff” hatóköre | OK | — | `adat/`, `konkordancia/`, `f22/`, `.tsv` diff 0 (a `pardes.db` verziózatlan). |
| Lista 4: táblasor-Δ (E17, DT3) | OK | — | Minden `adat/` és `konkordancia/` `.tsv` Δ=0. |
| Lista 5: brief ⛔ | OK | — | L. fent. |
| Tesztek (276 OK / 1 FAIL) | NEM ELLENŐRIZHETŐ | `M3.md:127` | A végrehajtó állítása; az ellenőr nem futtatta. |

## ELTÉRÉS-ek súlyossági sorrendben

1. **(közepes)** A héber keresés a szuffixumos vagy nem előtaggal kezdődő, több tokenből álló szót egybeírva nem találja meg (*זרעו*, *למינו*): hamis üres eredmény, ellentétben a README és a docstring ígéretével. Javítás: a jelölt a szó bármely 1–4 tokenes bontásának egy darabjából, vagy a súgó ígéretének szűkítése; teszt is kell rá.
2. **(közepes-alacsony)** A DT-F76j mérőtáblájában és a DONTESEK példájában a Préd 2:26 párja (נָתַן חָכְמָה) nem a határon áll; a határpár (TAHOT-sorrendben) נִּי \| כִּי. Újramérés, és a napló 3. szakaszának és a DT-F76j szövegének javítása.
3. **(alacsony)** Az N-F76b/N-F76c CI-lépés (Playwright/Semgrep) hiányzik, és az elhalasztása nincs dokumentálva.
4. **(alacsony)** A napló elavult sorai: 102 („F76.42–F76.46”) és 146 („DT-F76j (nyitott)”).

**Mellékes (nem ELTÉRÉS):** kötőjeles bemenetnél `szoto` módban az előfordulás-szám tokenszámnak tűnik (`kereses.py:212-217, 240`; DB nélkül nem igazolható). A gyorsítótár kulcsában nincs benne az `ut` (`alkalmazas.py:43-46`), ezért egy extra paraméteres kérés `vissza`-linkje más URL-hez is kiszolgálható; ártalmatlan.
