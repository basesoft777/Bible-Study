# ELLENŐR — F98_TERVEZO_MOD_BRIEF.md · `origin/main...HEAD` (236000d4)

*Készítette: `fuggetlen-ellenor` (claude-opus-5-5; a kért: `opus`, egyezik). A subagentnek nem volt fájlíró eszköze, ezért a jelentést az orkesztrátor mentette el a hand-back szövegéből, tömörítve; a sorok tartalma nem változott. Az ellenőr nem futtatta a teszteket (WSL/`pardes.db` nem érhető el a szerepéből).*

*A commit-hivatkozások az `origin/main`-re való, ütközés nélküli rebase után az új hash-ekre frissítve (F98.27; az ellenőrzött fa tartalma azonos): az ellenőrzéskori HEAD `94162dc9` → `236000d4`, az F98.3 `77022490` → `5e888c89`. A merge-base (`147ada81`, a main commitja) az ellenőrzéskori állapotot írja le, változatlan.*

A merge-base `147ada81`; az ág 3 committal le van maradva az `origin/main` mögött (F99.0 befogadás stb.), ezért az ellenőrzés a háromárú diffre (`origin/main...HEAD`, 28 fájl, +5666/−158) épül. A brief-ben nincs G/D jelölés; helyette a 3. (biztonság), 4. (lépések), 5. (elfogadás) pont és a DT153–f.

**ELTÉRÉS: 5 tétel**

| pont | eredmény | hely | indok |
|---|---|---|---|
| modell | ELTÉRÉS (kisebb) | commit 5e888c89 | 21 commit „Claude Opus 5.5”, az F98.3 (DT153–e rögzítése) „Claude Sonnet 5.5” (az orkesztrátor-session modellje), a brief `modell: opus`. A naplókban a modell mindenhol `claude-opus-5-5`; adattábla-`modell` mező nincs a diffben. |
| DT153–f | OK | DONTESEK.md:228–233 | mind 🟢, a felhasználó chatbeli döntésével; végleges DT-szám nincs |
| csak `belso` kiadás | OK | alkalmazas.py, oldalak.py:162–165, alap.html | `teszt_tervezo.py:390–402`: más kiadásban minden `/tervezo/*` 404, a HTML-ben nincs „tervezo” |
| loopback + proxy-fejlécek + helyi Host | **ELTÉRÉS (közepes)** | tervezo.py:351–369; README; zaras.md:332 | A kód a `remote_addr`-t, a tiltott fejlécek hiányát, a `Host`-ot és az `Origin`/`Sec-Fetch-Site`-ot vizsgálja. Az nginx alapbeállítása (`proxy_pass http://127.0.0.1:8000`) nem ad XFF-et, és a Host-ot `127.0.0.1:8000`-re írja: egy távoli `curl` (Origin/Sec-Fetch-Site nélkül) átmegy, a `GET /tervezo/kod` kódot ad, a `POST /tervezo/mentes` ír. A README és a napló „fordított proxy mögött a mentés nem működik” állítása csak a továbbító fejlécet adó/külső Hostot megtartó proxyra igaz (Caddy). A proxy-választás nyitott (N-F76d). Teszt nem fedi. Javaslat: kifejezett kapcsoló (pl. `PARDES_TERVEZO=1`) vagy a bind-cím ellenőrzése. |
| POST + egyszeri kód | OK | tervezo.py:414–433, 540–578 | a kód a `GET /tervezo/kod`-ról jön (M0-ban jóváhagyott eltérés a „kód a lapban”-tól: a lap gyorsítótárazott); `hmac.compare_digest`, egyszer használható |
| csak regiszteres token, értékszűrés, nincs szabad szöveg | OK | tervezo.py:281–345, 446–457 | tesztek 244–290, 540–550, 589–598 |
| CSP | OK | alkalmazas.py (a `CSP` változatlan) | az előnézet `style.setProperty`, a `tervezo.js`-ben nincs `innerHTML`/`eval` |
| atomi írás, előző állapot, újratöltés, ETag | OK | tervezo.py:372–385, 436–469; gyorsitotar.py | az `arculat.hash` a kulcsban és az ETag-ben |
| robusztusság | ELTÉRÉS (kisebb) | tervezo.py:449–457, 557–564 | a token létezését a memóriabeli adat alapján ellenőrzi, de a lemezes fájlra ír: hiányzó kulcsnál `KeyError` → 500 (nem 400); érvénytelen lemezes JSON → félrevezető 400 „a törzs nem érvényes JSON” |
| regiszter (83 elem, 46 kizárt) | OK | elemek.toml | megszámolva |
| regiszter-őr lefedettsége | ELTÉRÉS (kisebb) | regiszter_or.py:34, 226–259; olvaso.js:58 | (a) az `olvaso.js:58` `classList.toggle('nincs-jeloles')` által adott osztály sem a regiszterben, sem a kizárt listán nincs; a README „a felület minden CSS-osztálya” túlzó. (b) néma kihagyás: `class='…'` (egyszeres idézőjel), összefűzött `'class="a ' + x + '"'`, Jinja `{{ x or 'y' }}` esetén az `x`. Ma ilyen nincs a sablonokban. |
| tartalék | OK (jelölve) | zaras.md:347, 376 | a kliensoldali fele kézi próba, nem automatikus teszt |
| megjelenés-azonosság (M1) | NEM ELLENŐRIZHETŐ | zaras.md:68–111 | böngészős mérés; belső ellentmondás nincs; az M2 nem nyúlt a stíluslaphoz |
| stíluslap: egyetlen forrás | OK | olvaso.css | nincs literál szín/méret/`--token:` definíció |
| tesztek valódi futtatása | NEM ELLENŐRIZHETŐ | zaras.md:364–380 | a darabszámok statikusan egyeznek (45; 68+3=71); proveniencia-sor megvan |
| proveniencia a naplókban | OK | M0.md:11; zaras.md:111, 268, 295, 380 | a scratch-szkriptek nincsenek a repóban (a napló jelzi) |
| **BDB-commitok keveredése** | **ELTÉRÉS (közepes)** | blokkok.py (+216/−10), bdb_jelek.tsv (+65), teszt_olvaso_szerver.py (+75), olvaso.css (+33/−3), arculat.json, teszt_szintek.py | F98.9, F98.11–13 (a felhasználó BDB-jelentésszerkezet munkája) F98.x előtaggal az ágon van, miközben a brief hatókörből kizárja a blokk-tartalom módosítását; a regiszter 74–83. sora és a szelektor-teszt rájuk épül, ezért nem választhatók le. |
| szinkron-szkript | OK | arculat_szinkron.py:177–188 | `--kimenet` kötelező, nem ír a repóba, feltöltés nincs |
| A1, A2, A6 | OK | | A3–A5 nem értelmezett |
| CI-jelentés | OK a saját futásra | | `futtat.py`: E2–E16, E19, E20, E26: 0; E25/E27: ágon kívüli fájlokra |
| adattábla Δ (E17) | OK | | `adat/` és `konkordancia/` Δ = 0 |
| ⛔ pontok | OK | | M0 megállás + döntés, M3 megállás; a pilot nem változott |

**Súlyossági sorrend:** (1) közepes: a helyi kérés feltétele nginx-alapbeállítású proxy mögött megkerülhető, a dokumentáció túlzó; (2) közepes: a BDB-commitok az F98-előtaggal belekeverednek; (3) kisebb: a regiszter-őr nem látja a JS-ből adott osztályt, van néma kihagyási minta; (4) kisebb: lemez/memória eltérésnél 500, rossz lemezes JSON-nál félrevezető 400; (5) kisebb: az F98.3 commit Sonnet-sessionből.

*Megjegyzések:* az ág a main mögött van, merge előtt rebase kell. `belso` kiadásban a Tervező gomb és a `/tervezo/terkep.json` távoli látogatónak is látszik, a mentés nála 403.
