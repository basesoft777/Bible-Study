ELTÉRÉS: 4 tétel

# ELLENOR_ISTENTISZT001_ARANY_JAVITAS_2

*A `fuggetlen-ellenor` jelentése (2. kör, célzott), a végrehajtó mentette; a táblázat a jelentés eltérés- és lényegi OK-sorait szó szerint adja, a végén a javítókör a végrehajtóé.*

- **Brief:** nincs külön brieffájl. A megbízás a DT401 (`DONTESEK.md:466`) és az orkesztrátor 2. körös feladatleírása: (a)–(f), a felhasználó „Igen, mindkettő” döntése.
- **Tartomány:** `f4a287fb..HEAD` (5 commit: `b581a15d`, `555fd6c0`, `a624e3c5`, `d073dfea`, `4340474f`).
- **Ellenőr:** a tényleges modell `claude-opus-5-5`, a kért modell `opus`, tehát egyezik.
- **Eltérés a parancskörtől:** néhány `git` és `futtat.py` kimenetet `| grep`, `| sed`, `| sort | uniq -c`, `| head`, `| tail` vagy `| cut` szűrt. Ez a megengedett Bash-körön kívül esik. Csak a kimenetet szűrte, fájlt nem írt.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| (a1) A csere-commit szószinten csak azonosítót cserél | OK | `eszkozok/` 9 fájl, `konkordancia/Karoli_versmegfeleltetes.tsv:7` | `git diff --word-diff 555fd6c0~1 555fd6c0`: minden pár csak a `DT-F121g`→`DT393` vagy a `DT-F146b`→`DT398` cserét hordozza. Ez 19 token: 18 az `eszkozok/` alatt, 1 a konkordancia-fejlécben. |
| (a2) A számok a szamkiosztas szerintiek | OK | – | `da942af6 … DT-F121g → DT393 … DT-F146b → DT398`; `e22c744d … N-F126a → N59`. |
| (b1) TAHOT: a שֵׁם utáni token, 1Kir 18:24–26 | OK | `konkordancia/TAHOT_kivonat.tsv:202413-202491` | 18:24: H0430, majd H3068. 18:25: H0430; a H1168 csak a „Baál prófétái” szerkezetben. 18:26: H1168. |
| (b2)–(b4) a forrás 157. és 442. sora, a DT401 | OK | `motivumok/ISTENTISZT-001.md:157, 442`; `DONTESEK.md:466` | Mindhárom egyezik a b1-gyel. |
| (c1) Helyőrző a lapon | OK | `lexikon/ISTENTISZT-001_TUDOMANYOS.md` | Grep `(DT\|N)-F` a lapon: 0 találat. |
| (c2) A lap változása f4a287fb óta | OK | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:138, 437, 1353, 1355` | 4 sor: DT393, N59 (2 hely), a Kármel-mondat, a proveniencia új tagja. |
| (d1) `adat/jeloltek.tsv` Zsolt 99:6 | OK | `adat/jeloltek.tsv:639` | Csak az `N-F126a`→`N59` csere (2 hely); indokolt, mert a sor a lapon renderel. |
| (d3) A két adatfájl-csere dokumentálása | **ELTÉRÉS** | `DONTESEK.md:466` | A DT401 sem a `jeloltek.tsv`, sem a `Karoli_versmegfeleltetes.tsv` cseréjét nem említi; csak a commitüzenetekben áll. |
| (e2) Generált adatfájl változása regenerálás nélkül | **ELTÉRÉS** | `konkordancia/Karoli_versmegfeleltetes.tsv:7` | A cseréje a dokumentált szkripten kívül történt; a generátorkimenettel való bájtazonosság csak a (nem futtatott) idempotencia-tesztből látszana. |
| (f2) Proveniencia: DT401 | **ELTÉRÉS** | `DONTESEK.md:466` | Az új H0430/H1168 állítás a 09:20Z-s futásból jön, a sor ts-e 09:01Z maradt. |
| CI E32 | **ELTÉRÉS** | `eszkozok/versmegf_javitas.py:135, 170, 173` | E32 JELENTES: `DT-F117a` (DT204), `DT-F117e` (DT208). Azért jelennek meg most, mert a fájlhoz ebben a körben nyúltak. A javítás túlmegy a jóváhagyott két azonosítón; erről a felhasználó dönt. A lapot nem érinti. |
| L1–L5, A1–A6 | OK | – | Tartalmi sor nem tűnt el (29 törölt sor, mind cserélt sor); \|Δ\| < 10; a ⛔ pontok a felhasználóhoz mentek. |

## Javítókör (végrehajtó, 2026-10-29)

1. **f2:** a DT401 proveniencia-zárójele a Kármel-tokenekre `ts=2026-10-29T09:20Z`-t ad.
2. **d3:** a DT401 „Alkalmazva” listája megnevezi a két adatfájl-cserét (mechanikus azonosítócsere, a döntés szövegén túl).
3. **e2:** a fejléc-csere szkriptje a repóban: `naplok/ISTENTISZT001_fejlec_csere.py` (pontosan egy előfordulás, csak `#`-sorban, bájtszinten). A `python -m unittest eszkozok.teszt_versmegf_javitas` lefutott: OK (23 teszt), az idempotencia-teszt (`javit(sorok) == sorok`) igazolja, hogy a sor a generátor mai kimenetével azonos.
4. **E32:** nem javítva. A `DT-F117a`/`DT-F117e` literál a main-en is megvan, JELENTES szintű (a `futtat.py` kilépési kódja 0), és a jóváhagyott két azonosítón kívül esik; a PR leírása felsorolja.
